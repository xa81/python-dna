"""Shared test helpers: import path, fake transport, comparison."""

import os
import sys
from urllib.parse import parse_qsl, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from domainnameapi.transport import HttpResponse, TransportError  # noqa: E402

FIXTURE_DIR = os.path.join(ROOT, "tests", "testdata", "conformance")

RESELLER = "00000000-0000-4000-8000-000000000001"
API_KEY = "conformance-api-key"


class FakeTransport(object):
    """Serves queued responses in order and records every request."""

    def __init__(self, responses=None):
        self.queue = list(responses or [])
        self.requests = []

    def push(self, status, body="", headers=None):
        self.queue.append({"status": status, "body": body, "headers": headers or {}})
        return self

    def push_error(self, errno, message):
        self.queue.append(TransportError(errno, message))
        return self

    def send(self, request):
        self.requests.append(request)
        if not self.queue:
            raise AssertionError("fake transport: no queued response for %s %s" % (request.method, request.url))
        nxt = self.queue.pop(0)
        if isinstance(nxt, Exception):
            raise nxt
        return HttpResponse(nxt["status"], nxt.get("body", ""), nxt.get("headers") or {})


def parse_php_query(query):
    """Decode a query string like PHP parse_str (flat keys and key[sub] nesting)."""
    out = {}
    for key, value in parse_qsl(query, keep_blank_values=True):
        if "[" in key and key.endswith("]"):
            base, rest = key.split("[", 1)
            parts = [base] + rest[:-1].split("][")
            node = out
            for p in parts[:-1]:
                node = node.setdefault(p, {})
            node[parts[-1]] = value
        else:
            out[key] = value
    return out


def split_url(url, base_path="/api/v1/"):
    parts = urlsplit(url)
    path = parts.path
    if path.startswith(base_path):
        path = path[len(base_path):]
    return path, parse_php_query(parts.query)


def is_empty_container(v):
    return isinstance(v, (list, dict)) and len(v) == 0


def diff(expected, actual, path="", ignore=()):
    """Return a list of human-readable differences (empty when equal).

    Rules from conformance/README.md: an empty list equals an empty object,
    numbers compare by value (but booleans are not numbers), key order is
    irrelevant, paths in ``ignore`` only need to be non-negative integers.
    """
    if path in ignore:
        if isinstance(actual, bool) or not isinstance(actual, int) or actual < 0:
            return ["%s: expected a non-negative integer, got %r" % (path or "<root>", actual)]
        return []
    if is_empty_container(expected) and is_empty_container(actual):
        return []
    if isinstance(expected, bool) or isinstance(actual, bool):
        if type(expected) is not type(actual) or expected != actual:
            return ["%s: expected %r, got %r" % (path or "<root>", expected, actual)]
        return []
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return [] if expected == actual else ["%s: expected %r, got %r" % (path or "<root>", expected, actual)]
    if isinstance(expected, dict) and isinstance(actual, dict):
        out = []
        for k in sorted(set(expected) | set(actual), key=str):
            p = "%s.%s" % (path, k) if path else str(k)
            if k not in expected:
                out.append("%s: unexpected key (value %r)" % (p, actual[k]))
            elif k not in actual:
                out.append("%s: missing key (expected %r)" % (p, expected[k]))
            else:
                out.extend(diff(expected[k], actual[k], p, ignore))
        return out
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            return ["%s: expected %d items, got %d (%r)" % (path or "<root>", len(expected), len(actual), actual)]
        out = []
        for i, (e, a) in enumerate(zip(expected, actual)):
            out.extend(diff(e, a, "%s.%d" % (path, i) if path else str(i), ignore))
        return out
    if type(expected) is not type(actual) or expected != actual:
        return ["%s: expected %r, got %r" % (path or "<root>", expected, actual)]
    return []
