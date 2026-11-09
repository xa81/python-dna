"""Error and performance telemetry (Sentry store endpoint).

Port of the telemetry half of php-dna ``SharedApiConfigAndUtilsTrait``:

* On by default; ``set_error_reporting_enabled(False)`` turns it off and
  ``set_telemetry_minimal(True)`` sends the minimal payload.
* Failed calls send an error event, a sample of successful calls (4 %, and
  every call slower than one second) sends a performance transaction.
* Only credentials are masked (API key, passwords, auth/EPP codes, tokens).
* Events are posted from a daemon thread: never blocks, never raises into
  the caller.
"""

import getpass
import json
import os
import platform
import random
import re
import ssl
import threading
import time
import traceback
import urllib.request
import uuid
from urllib.parse import urlsplit

from . import _php as php
from .shared import APPLICATION, DEFAULT_CACHE_TTL, DEFAULT_IGNORED_ERRORS, PERFORMANCE_SAMPLE_RATE
from ._version import VERSION

# Filled in once the Sentry project for python-dna exists; empty = telemetry is a no-op.
DEFAULT_SENTRY_DSN = ""

_MASK_RE = re.compile(r"auth|epp|password|passwd|secret|token|api[_-]?key", re.IGNORECASE)

_ip_cache = {"ip": None, "at": 0.0}
_ip_lock = threading.Lock()


def parse_dsn(dsn):
    """``https://<public>[:<secret>]@<host>/<project>`` -> parts, or ``None``."""
    if not dsn or not isinstance(dsn, str):
        return None
    try:
        parts = urlsplit(dsn.strip())
    except ValueError:
        return None
    host = parts.hostname
    project = (parts.path or "").lstrip("/")
    public_key = parts.username
    if not host or not project or not public_key:
        return None
    return {
        "host": host,
        "project_id": project,
        "public_key": public_key,
        "secret_key": parts.password or None,
        "store_url": "https://%s/api/%s/store/" % (host, project),
    }


def telemetry_mask(data, depth=0):
    """Replace credential values (by key name) with ``***``; keep everything else."""
    if depth > 8:
        return "[…]"
    if isinstance(data, dict):
        out = {}
        for key, value in data.items():
            if _MASK_RE.search(php.strval(key)):
                out[key] = value if (value == "" or value is None) else "***"
            else:
                out[key] = telemetry_mask(value, depth + 1)
        return out
    if isinstance(data, (list, tuple)):
        out = []
        for value in data:
            out.append(telemetry_mask(value, depth + 1))
        return out
    return data


def map_trace_status(success, api_code):
    """OTel-compatible span status from the outcome and ``API_<n>`` code."""
    if success:
        return "ok"
    if api_code is None:
        return "unknown"
    m = re.search(r"-?\d+", php.strval(api_code))
    if not m:
        return "unknown"
    code = int(m.group(0))
    if code in (401, 2202):
        return "unauthenticated"
    if code == 403:
        return "permission_denied"
    if code in (404, 510):
        return "not_found"
    if code in (408, 504):
        return "deadline_exceeded"
    if code == -1:
        return "unavailable"
    if 500 <= code < 600:
        return "internal_error"
    if 400 <= code < 500:
        return "invalid_argument"
    return "unknown"


def _iso_utc(ts):
    millis = int(round((ts % 1) * 1000))
    if millis >= 1000:
        millis = 999
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(ts)) + ".%03dZ" % millis


def _server_ip():
    """Public IP of this host (cached for DEFAULT_CACHE_TTL seconds)."""
    with _ip_lock:
        if _ip_cache["ip"] and time.time() - _ip_cache["at"] < DEFAULT_CACHE_TTL:
            return _ip_cache["ip"]
    try:
        req = urllib.request.Request("https://api.ipify.org", headers={"User-Agent": APPLICATION + "/" + VERSION})
        with urllib.request.urlopen(req, timeout=2) as resp:
            ip = resp.read(64).decode("ascii", "replace").strip()
        if re.match(r"^[0-9a-fA-F:.]+$", ip):
            with _ip_lock:
                _ip_cache["ip"] = ip
                _ip_cache["at"] = time.time()
            return ip
    except Exception:  # noqa: BLE001 - telemetry never fails the caller
        pass
    return "unknown"


def _current_user():
    try:
        return getpass.getuser()
    except Exception:  # noqa: BLE001
        return ""


def _post(url, payload, auth_header):
    """Blocking POST used inside the background thread (short timeouts)."""
    req = urllib.request.Request(
        url,
        data=payload.encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Sentry-Auth": auth_header,
            "User-Agent": APPLICATION + "/" + VERSION,
        },
    )
    with urllib.request.urlopen(req, timeout=2) as resp:
        resp.read(1024)


def _encode(event):
    try:
        return json.dumps(event, default=php.strval, ensure_ascii=False)
    except (TypeError, ValueError):
        return ""


class Telemetry(object):
    """Telemetry for one client instance.

    ``client`` is the :class:`~domainnameapi.rest.DNARest` instance whose
    ``last_request``/``last_response``/... state describes the failing call.
    """

    def __init__(self, client, dsn=None):
        self.client = client
        self.enabled = True
        self.minimal = False
        self.dsn = DEFAULT_SENTRY_DSN if dsn is None else dsn
        self._session_trace_id = None
        # Replaceable for tests: called with (url, json_payload, auth_header).
        self.poster = _post
        # Run synchronously instead of in a thread (tests).
        self.synchronous = False

    # -- shared tag helpers -------------------------------------------------

    def session_trace_id(self):
        if self._session_trace_id is None:
            self._session_trace_id = uuid.uuid4().hex
        return self._session_trace_id

    def environment(self):
        url = self.client.get_service_url()
        if isinstance(url, str) and "ote." in url.lower():
            return "ote"
        return "production"

    def common_tags(self, error=None):
        c = self.client
        tags = {}
        if not php.empty(c.reseller_id):
            tags["reseller"] = php.strval(c.reseller_id)
        domain = php.get(c.last_request, "payload", "domainName")
        if not php.empty(domain) and isinstance(domain, str) and not self.minimal:
            tags["domain"] = domain
        if not php.empty(c.last_function):
            tags["operation"] = php.strval(c.last_function)
        tags["api_type"] = "REST"
        if error is not None:
            msg = php.strval(getattr(error, "message", str(error)))
            code = getattr(error, "code", 0)
            m = re.search(r"API_(-?\d+)_ERROR", msg)
            if m:
                tags["api_code"] = "API_" + m.group(1)
            elif php.is_numeric(code) and php.intval(code) != 0:
                tags["api_code"] = "API_%d" % php.intval(code)
            if php.is_numeric(code) and php.intval(code) != 0:
                tags["status_code"] = str(php.intval(code))
        tags["library_version"] = VERSION
        return tags

    def classification(self, error):
        msg = php.strval(getattr(error, "message", str(error)))
        tags = self.common_tags(error)
        m = re.search(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", msg)
        if m:
            tags["ip_value"] = m.group(1)
        api_code = tags.get("api_code")
        n = msg
        n = re.sub(r"^\[API_ERROR\]:\s*", "", n, flags=re.IGNORECASE)
        n = re.sub(r"API_-?\d+_ERROR\s*-\s*Failed\s*-\s*", "", n, count=1, flags=re.IGNORECASE)
        n = re.sub(r"\s*\(Reseller Id[^)]*\)\s*", "", n, flags=re.IGNORECASE)
        n = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "{ip}", n)
        n = re.sub(r"'[^']{0,80}'|\"[^\"]{0,80}\"", "{v}", n)
        n = re.sub(r"\b\d{2,}\b", "{n}", n)
        n = re.sub(r"\s+", " ", n).strip()
        if n == "":
            n = api_code if api_code else error.__class__.__name__
        elif api_code and not n.startswith(api_code):
            n = api_code + ": " + n
        if len(n) > 160:
            n = n[:157] + "..."
        return {
            "value": n,
            "tags": tags,
            "fingerprint": ["dna", APPLICATION, tags.get("operation", "unknown"), n],
        }

    # -- dispatch -------------------------------------------------------------

    def _dispatch(self, event):
        """Post an event off the caller's thread. Never raises.

        The event is built synchronously from the client state of the failing
        call; only the public-IP lookup and the POST run in the thread.
        """

        def run():
            try:
                parsed = parse_dsn(self.dsn)
                if parsed is None:
                    return
                if not self.minimal and event["tags"].get("ip_address") is None:
                    event["tags"]["ip_address"] = _server_ip()
                payload = _encode(event)
                if payload == "":
                    return
                auth = [
                    "sentry_version=7",
                    "sentry_client=%s/%s" % (APPLICATION, VERSION),
                    "sentry_key=" + parsed["public_key"],
                ]
                if parsed["secret_key"]:
                    auth.append("sentry_secret=" + parsed["secret_key"])
                self.poster(parsed["store_url"], payload, "Sentry " + ", ".join(auth))
            except Exception:  # noqa: BLE001 - telemetry must never surface
                pass

        try:
            if self.synchronous:
                run()
            else:
                t = threading.Thread(target=run, name="domainnameapi-telemetry")
                t.daemon = True
                t.start()
        except Exception:  # noqa: BLE001
            pass

    def send_error(self, error):
        """Report a failed call (fire and forget)."""
        try:
            if not self.enabled or parse_dsn(self.dsn) is None:
                return
            message = php.strval(getattr(error, "message", str(error)))
            for ignored in DEFAULT_IGNORED_ERRORS:
                if ignored in message:
                    return
            self._dispatch(self._error_event(error, message, self._snapshot()))
        except Exception:  # noqa: BLE001
            pass

    def send_performance(self, duration_ms, start_ts, end_ts):
        """Report a sampled successful call (fire and forget)."""
        try:
            if not self.enabled or parse_dsn(self.dsn) is None:
                return
            self._dispatch(self._performance_event(duration_ms, start_ts, end_ts, self._snapshot()))
        except Exception:  # noqa: BLE001
            pass

    def should_sample(self, duration_ms):
        return duration_ms > 1000 or random.randint(1, 1000) <= PERFORMANCE_SAMPLE_RATE

    def _snapshot(self):
        """Copy the client state now; the thread runs after the caller moved on."""
        c = self.client
        return {
            "last_request": c.last_request,
            "last_response": c.last_response,
            "last_response_headers": c.last_response_headers,
            "last_parsed_response": c.last_parsed_response,
            "last_function": c.last_function,
            "started_at": c.started_at,
        }

    # -- event builders ------------------------------------------------------

    def _frames(self, error):
        frames = []
        tb = getattr(error, "__traceback__", None)
        stack = traceback.extract_tb(tb) if tb is not None else traceback.extract_stack()[:-3]
        for fr in stack:
            frames.append({
                "filename": os.path.basename(fr.filename),
                "lineno": fr.lineno or 0,
                "function": fr.name or "",
            })
        return frames

    def _error_event(self, error, message, snap):
        c = self.client
        classification = self.classification(error)
        elapsed = time.time() - (snap["started_at"] or time.time())
        tags = {
            "handled": "yes",
            "level": "error",
            "url": "NA",
            "transaction": "NA",
            "trace_id": uuid.uuid4().hex[:16],
            "runtime_name": "Python",
            "runtime_version": platform.python_version(),
            "elapsed_time": php.number_format(elapsed, 4),
            "application": APPLICATION,
            "ip_address": "" if self.minimal else None,  # looked up in the background
            "vhost_user": "" if self.minimal else _current_user(),
        }
        tags.update(classification["tags"])
        event = {
            "event_id": uuid.uuid4().hex,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": "error",
            "logger": "python",
            "platform": "python",
            "culprit": "domainnameapi.DNARest via rest.py",
            "message": {"formatted": classification["value"]},
            "exception": {
                "values": [{
                    "type": APPLICATION + " Exception",
                    "value": classification["value"],
                    "stacktrace": {"frames": self._frames(error)},
                }]
            },
            "tags": tags,
            "extra": {
                "request_data": telemetry_mask(snap["last_request"]),
                "response_data": telemetry_mask(snap["last_response"]),
                "openssl_v": getattr(ssl, "OPENSSL_VERSION", "NA"),
                "openssl_n": getattr(ssl, "OPENSSL_VERSION_NUMBER", "NA"),
                "original_message": message,
            },
            "release": VERSION,
            "environment": self.environment(),
            "fingerprint": classification["fingerprint"],
        }
        if self.minimal:
            for key in ("url", "ip_address", "vhost_user", "ip_value"):
                event["tags"].pop(key, None)
            lr = snap["last_request"] if isinstance(snap["last_request"], dict) else {}
            event["extra"]["request_data"] = {
                "method": php.strval(lr.get("method", "")),
                "endpoint": urlsplit(php.strval(lr.get("url", ""))).path or "",
            }
            event["extra"]["response_data"] = {
                "http_code": php.intval(php.get(snap["last_response_headers"], "http_code")),
            }
        return event

    def _performance_event(self, duration_ms, start_ts, end_ts, snap):
        c = self.client
        trace_id = self.session_trace_id()
        root_span = uuid.uuid4().hex[:16]
        child_span = uuid.uuid4().hex[:16]
        op = "http.client"

        api_code = None
        code = php.get(snap["last_parsed_response"], "Code")
        if isinstance(code, str):
            api_code = code
        else:
            code = php.get(snap["last_response"], "error", "code")
            if isinstance(code, str):
                api_code = code
        status = map_trace_status(True, api_code)

        tags = self.common_tags()
        if api_code is not None and "api_code" not in tags:
            tags["api_code"] = api_code
        http_code = php.intval(php.get(snap["last_response_headers"], "http_code"))
        if http_code != 0:
            tags["status_code"] = str(http_code)

        lr = snap["last_request"] if isinstance(snap["last_request"], dict) else {}
        method = php.strval(lr.get("method")) or "GET"
        call_url = php.strval(lr.get("url"))
        call_host = urlsplit(call_url).hostname if call_url else urlsplit(php.strval(c.get_service_url())).hostname
        call_host = call_host or ""
        span_data = {"http.request.method": method}
        if call_host:
            span_data["server.address"] = call_host
        if call_url and not self.minimal:
            span_data["url.full"] = call_url.split("?", 1)[0]
        if "status_code" in tags:
            span_data["http.response.status_code"] = int(tags["status_code"])
        description = ("%s https://%s" % (method, call_host)) if call_host else php.strval(snap["last_function"])

        base_tags = {
            "application": APPLICATION,
            "ip_address": "" if self.minimal else None,  # looked up in the background
            "vhost_user": "" if self.minimal else _current_user(),
        }
        base_tags.update(tags)
        return {
            "event_id": uuid.uuid4().hex,
            "platform": "python",
            "level": "info",
            "type": "transaction",
            "transaction": "API." + php.strval(snap["last_function"]),
            "transaction_info": {"source": "custom"},
            "release": VERSION,
            "environment": self.environment(),
            "timestamp": _iso_utc(end_ts),
            "start_timestamp": _iso_utc(start_ts),
            "contexts": {
                "trace": {"trace_id": trace_id, "span_id": root_span, "op": op, "status": status},
                "runtime": {"name": "python", "version": platform.python_version()},
            },
            "tags": base_tags,
            "measurements": {
                "duration": {"value": float(duration_ms), "unit": "millisecond"},
            },
            "spans": [{
                "span_id": child_span,
                "parent_span_id": root_span,
                "trace_id": trace_id,
                "op": op,
                "description": description,
                "status": status,
                "data": span_data,
                "start_timestamp": _iso_utc(start_ts),
                "timestamp": _iso_utc(end_ts),
            }],
        }
