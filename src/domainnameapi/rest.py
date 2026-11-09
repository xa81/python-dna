"""REST client for the DomainNameAPI gateway.

Faithful port of php-dna ``DomainNameApi/DNARest.php``: same endpoints, same
request bodies and query strings, same return envelopes. Every public method
catches gateway failures and returns ``{'result': 'ERROR', 'error': {...}}``
instead of raising.
"""

import math
import re
import time
import unicodedata

from . import _php as php
from .shared import (
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_ERRORS,
    DEFAULT_NAMESERVERS,
    DEFAULT_REASON,
    DEFAULT_TIMEOUT,
    RESULT_ERROR,
    RESULT_OK,
    USER_AGENT,
    ApiError,
    format_error_code,
    normalize_host_name,
    normalize_host_name_list,
    set_error,
)
from .telemetry import Telemetry
from .transport import CURLE_OPERATION_TIMEDOUT, HttpRequest, TransportError, UrllibTransport

URL_PROD = "https://api.domainresellerapi.com/api/v1"
URL_OTE = "https://ote.domainresellerapi.com/api/v1"

# Gateway DomainStatus enum -> textual label.
DOMAIN_STATUS_MAP = {
    0: "Active",
    1: "WaitingForRegistration",
    2: "WaitingForDocument",
    3: "WaitingForIncomingTransfer",
    4: "TransferredOut",
    7: "PendingDelete",
    8: "Deleted",
    9: "ConfirmationEmailSend",
    11: "WaitingForOutgoingTransfer",
    12: "PendingHold",
    15: "ModificationPending",
    18: "InCase",
    19: "PendingRestore",
}

# Gateway DomainRenewalMode enum -> textual label.
DOMAIN_RENEWAL_MODE_MAP = {
    1: "AutoRenew",
    2: "AutoExpire",
    3: "AutoDelete",
}

# Zone record types the gateway accepts (probed against the live gateway).
ZONE_RECORD_TYPES = ["A", "AAAA", "ALIAS", "CAA", "CNAME", "DS", "MX", "NAPTR", "PTR", "SRV", "TLSA", "TXT"]

# Redirect types accepted by /domains/forwards.
FORWARD_TYPES = ["Standard", "Frame"]

# Minimum gap between two /domains/zones calls, in seconds.
ZONE_MIN_INTERVAL = 1.0

_HTTP_REASONS = {
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    409: "Conflict",
    422: "Unprocessable Entity",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
}

_BOILERPLATE_RE = re.compile(r"Exception of type '[^']*' was thrown", re.IGNORECASE)
_IPV4_RE = re.compile(r"^(0|[1-9]\d{0,2})\.(0|[1-9]\d{0,2})\.(0|[1-9]\d{0,2})\.(0|[1-9]\d{0,2})$")
_PCRE_SPACE = " \t\n\x0b\f\r"

_COUNTRY_MAP = {
    "turkey": "TR", "türkiye": "TR", "turkiye": "TR",
    "united states": "US", "united states of america": "US", "usa": "US",
    "united kingdom": "GB", "great britain": "GB", "england": "GB",
    "germany": "DE", "deutschland": "DE", "france": "FR", "spain": "ES",
    "italy": "IT", "netherlands": "NL", "india": "IN", "china": "CN",
    "russia": "RU", "canada": "CA", "australia": "AU", "brazil": "BR",
}


def _http_status_reason(status):
    status = php.intval(status)
    if status in _HTTP_REASONS:
        return _HTTP_REASONS[status]
    if status >= 500:
        return "Server Error"
    if status >= 400:
        return "Client Error"
    return "Unexpected Response"


def _format_api_date(value):
    """'Y-m-d\\TH:i:s', or '' when missing or unparseable."""
    if value is None or value == "":
        return ""
    ts = php.strtotime(php.strval(value))
    return "" if ts is None else php.format_timestamp(ts)


def _remaining_days_from_date(value):
    if value is None or value == "":
        return 0
    ts = php.strtotime(php.strval(value))
    if ts is None:
        return 0
    return max(0, int(math.ceil((ts - php.now()) / 86400.0)))


def _is_ipv4(value):
    if not isinstance(value, str):
        value = php.strval(value)
    m = _IPV4_RE.match(value)
    return bool(m) and all(int(g) <= 255 for g in m.groups())


def _normalize_domain_status(value):
    if php.is_numeric(value):
        return DOMAIN_STATUS_MAP.get(php.intval(value), php.strval(value))
    return php.strval(value)


def _sanitize_person_name(name):
    """Keep letters (any alphabet), whitespace, apostrophes and hyphens."""
    kept = []
    for ch in php.strval(name):
        if ch in "'-" or ch.isspace() or unicodedata.category(ch).startswith("L"):
            kept.append(ch)
    clean = "".join(kept)
    clean = re.sub(r"\s+", " ", clean)
    return php.trim(clean)


def _normalize_country_code(country):
    country = php.trim(country)
    if country == "":
        return ""
    if php.strlen(country) == 2:
        return php.strtoupper(country)
    key = php.strtolower(country)
    return _COUNTRY_MAP.get(key, country)


def _normalize_phone(number, country_code):
    """Split a free-form number into (subscriber digits, country code)."""
    number = php.strval(number)
    has_intl_prefix = bool(re.match(r"^[" + _PCRE_SPACE + r"]*(\+|00)", number))
    digits = re.sub(r"[^0-9]", "", number)
    cc = re.sub(r"[^0-9]", "", php.strval(country_code))

    if digits == "":
        return "", cc

    if has_intl_prefix:
        if digits.startswith("00"):
            digits = digits[2:]
        if cc != "" and digits.startswith(cc) and len(digits) > len(cc):
            digits = digits[len(cc):]
    elif cc != "" and digits.startswith(cc) and len(digits) > 10:
        digits = digits[len(cc):]

    if cc == "":
        if len(digits) == 12 and digits.startswith("90"):
            cc = "90"
            digits = digits[2:]
        else:
            cc = "90"

    if len(digits) > 1 and digits[0] == "0":
        digits = digits.lstrip("0")

    return digits, cc


def _flatten_validation_errors(validation_errors):
    parts = []
    for ve in php.values(validation_errors):
        if isinstance(ve, str):
            if php.trim(ve) != "":
                parts.append(php.trim(ve))
            continue
        if not php.is_array(ve):
            continue
        message = php.trim(php.strval(php.get(ve, "message"))) if php.get(ve, "message") is not None else ""
        members = []
        member_list = php.get(ve, "members")
        if php.is_array(member_list):
            for member in php.values(member_list):
                label = _humanize_validation_member(php.strval(member))
                if label != "":
                    members.append(label)
        if members and message != "":
            parts.append(", ".join(members) + " - " + message)
        elif members:
            parts.append(", ".join(members))
        elif message != "":
            parts.append(message)

    unique = []
    for p in parts:
        if p not in unique:
            unique.append(p)
    return " | ".join(unique)


_ROLES = {
    "administrativecontact": "Admin", "administrative": "Admin",
    "technicalcontact": "Tech", "technical": "Tech",
    "registrantcontact": "Registrant", "registrant": "Registrant",
    "billingcontact": "Billing", "billing": "Billing",
}


def _humanize_validation_member(member):
    member = php.trim(member)
    if member == "":
        return ""
    member = member.lstrip("$.")
    member = re.sub(r"\[\d+\]", "", member)
    segments = [s for s in re.split(r"[./]+", member) if s != ""]
    if not segments:
        return ""
    out = []
    for seg in segments:
        out.append(_ROLES.get(php.strtolower(seg), php.ucfirst(seg)))
    return php.trim(" ".join(out))


def _stringify_attributes(attrs):
    out = {}
    for key, value in php.items(attrs):
        if isinstance(value, bool):
            out[key] = "true" if value else "false"
        elif value is None:
            out[key] = ""
        elif isinstance(value, (str, int, float)):
            out[key] = php.strval(value)
        else:
            out[key] = php.json_encode(value)
    return out


_TR_KEY_MAP = {
    "TRABISDOMAINCATEGORY": "TRABISDOMAINCATEGORY",
    "TRABISCITIZENID": "TRABISCITIZENID",
    "TRABISCITIZIENID": "TRABISCITIZENID",  # long-standing typo -> canonical
    "TRABISTAXOFFICE": "TRABISTAXOFFICE",
    "TRABISTAXNUMBER": "TRABISTAXNUMBER",
}


def _normalize_tr_attributes(attrs):
    """Reduce legacy .tr TRABIS attributes to the REST schema."""
    if not php.is_array(attrs) or not attrs:
        return attrs if php.is_array(attrs) else []
    normalized = {}
    for key, value in php.items(attrs):
        if not isinstance(key, str) or key not in _TR_KEY_MAP:
            continue
        if key == "TRABISCITIZIENID" and "TRABISCITIZENID" in normalized:
            continue
        normalized[_TR_KEY_MAP[key]] = value
    if normalized.get("TRABISDOMAINCATEGORY") is not None:
        cat = php.strtolower(php.trim(php.strval(normalized["TRABISDOMAINCATEGORY"])))
        if cat in ("1", "owner", "personal", "individual"):
            normalized["TRABISDOMAINCATEGORY"] = "Owner"
        elif cat in ("0", "corporate", "company"):
            normalized["TRABISDOMAINCATEGORY"] = "Corporate"
    return normalized


def _relativize_record_name(name, domain_name):
    """Bare label the gateway expects; the apex becomes ''."""
    name = php.trim(name)
    domain = php.rtrim(php.strtolower(php.trim(domain_name)), ".")
    if name == "" or name == "@":
        return ""
    bare = php.rtrim(name, ".")
    if php.strcasecmp_equal(bare, domain):
        return ""
    suffix = "." + domain
    if len(bare) > len(suffix) and php.strcasecmp_equal(bare[-len(suffix):], suffix):
        return bare[:-len(suffix)]
    return bare


def _qualify_record_name(name, domain_name):
    """FQDN form the zone listing returns ("www" -> "www.example.com.")."""
    name = php.trim(name)
    domain = php.rtrim(php.strtolower(php.trim(domain_name)), ".")
    apex = domain + "."
    if name == "" or name == "@":
        return apex
    bare = php.rtrim(name, ".")
    suffix = "." + domain
    if php.strcasecmp_equal(bare, domain) or php.strtolower(bare)[-len(suffix):] == suffix:
        return bare + "."
    return bare + "." + apex


def _unsupported_zone_type(type_):
    type_ = php.strtoupper(php.trim(type_))
    if type_ == "":
        return "Record type is required."
    if type_ not in ZONE_RECORD_TYPES:
        return 'Record type "%s" is not supported by the DNS zone API. Supported types: %s.' % (
            type_, ", ".join(ZONE_RECORD_TYPES))
    return None


def _same_record_value(type_, a, b):
    is_txt = php.strtoupper(type_) == "TXT"

    def normalize(v):
        v = php.trim(v)
        if is_txt:
            if len(v) > 1 and v[0] == '"' and v[-1] == '"':
                v = v[1:-1]
            return v
        return php.strtolower(php.rtrim(v, "."))

    return normalize(a) == normalize(b)


def _build_zone_struct(name, type_, content, ttl):
    ttl = php.intval(ttl)
    if ttl < 1:
        ttl = 3600
    if ttl > 86400:
        ttl = 86400
    return {
        "name": php.strval(name),
        "ttl": ttl,
        "type": php.strtoupper(php.strval(type_)),
        "contents": [php.strval(v) for v in php.values(php.array_cast(content))],
    }


def _parse_contact_ids(contacts):
    result = {
        "Billing": {"ID": 0},
        "Technical": {"ID": 0},
        "Administrative": {"ID": 0},
        "Registrant": {"ID": 0},
    }
    if not php.is_array(contacts):
        return result
    type_map = {"Billing": "Billing", "Tech": "Technical", "Admin": "Administrative", "Registrant": "Registrant"}
    for c in php.values(contacts):
        api_type = php.coalesce(php.get(c, "ContactType"), php.get(c, "contactType"), "")
        key = type_map.get(api_type) if isinstance(api_type, str) else None
        if key:
            result[key]["ID"] = php.coalesce(php.get(c, "handle"), php.get(c, "id"), 0)
    return result


def _parse_contact_info(data):
    if php.empty(data):
        return []
    g = lambda *k: php.get(data, *k)  # noqa: E731
    return {
        "ID": php.coalesce(g("handle"), g("id"), ""),
        "Status": php.coalesce(g("status"), "Active"),
        "AuthCode": php.coalesce(g("authCode"), ""),
        "FirstName": php.coalesce(g("firstName"), ""),
        "LastName": php.coalesce(g("lastName"), ""),
        "Company": php.coalesce(g("companyName"), g("organizationName"), g("company"), ""),
        "EMail": php.coalesce(g("eMail"), g("emailAddress"), g("email"), ""),
        "Type": php.coalesce(g("type"), ""),
        "Address": {
            "Line1": php.coalesce(g("address"), g("addressLine1"), ""),
            "Line2": php.coalesce(g("addressLine2"), ""),
            "Line3": php.coalesce(g("addressLine3"), ""),
            "State": php.coalesce(g("state"), g("stateOrProvince"), ""),
            "City": php.coalesce(g("city"), ""),
            "Country": php.coalesce(g("country"), g("countryCode"), ""),
            "ZipCode": php.coalesce(g("postalCode"), g("zipCode"), ""),
        },
        "Phone": {
            "Phone": {
                "Number": php.coalesce(g("phone"), g("phoneNumber"), ""),
                "CountryCode": php.coalesce(g("phoneCountryCode"), ""),
            },
            "Fax": {
                "Number": php.coalesce(g("fax"), g("faxNumber"), ""),
                "CountryCode": php.coalesce(g("faxCountryCode"), ""),
            },
        },
        "Additional": php.coalesce(g("additionalAttributes"), []),
    }


def _map_values(value, fn):
    """PHP ``array_map`` (keys of an associative array are preserved)."""
    if isinstance(value, dict):
        return {k: fn(v) for k, v in value.items()}
    return [fn(v) for v in php.values(value)]


class DNARest(object):
    """Low-level REST client. Use :class:`domainnameapi.DomainNameAPI`."""

    URL_PROD = URL_PROD
    URL_OTE = URL_OTE
    ZONE_RECORD_TYPES = ZONE_RECORD_TYPES
    FORWARD_TYPES = FORWARD_TYPES

    def __init__(self, reseller_id, token, test_mode=False, transport=None, sentry_dsn=None):
        self.service_url = URL_OTE if test_mode else URL_PROD
        self.reseller_id = reseller_id
        self.token = token
        self.transport = transport if transport is not None else UrllibTransport()
        self.ssl_verify = True
        self.timeout = DEFAULT_TIMEOUT
        self.connect_timeout = DEFAULT_CONNECT_TIMEOUT
        self.zone_min_interval = ZONE_MIN_INTERVAL
        self._last_zone_request_at = 0.0

        self.last_request = {}
        self.last_response = {}
        self.last_response_headers = {}
        self.last_parsed_response = {}
        self.last_function = ""
        self.started_at = time.time()

        self.telemetry = Telemetry(self, sentry_dsn)

    # ------------------------------------------------------------------
    # Settings and diagnostics
    # ------------------------------------------------------------------

    def set_ssl_verification(self, enabled):
        self.ssl_verify = bool(enabled)

    def set_error_reporting_enabled(self, enabled):
        self.telemetry.enabled = bool(enabled)

    def set_telemetry_minimal(self, minimal):
        self.telemetry.minimal = bool(minimal)

    def get_request_data(self):
        return self.last_request

    def set_request_data(self, request):
        self.last_request = request
        return self

    def get_response_data(self):
        return self.last_response

    def set_response_data(self, response):
        self.last_response = response
        return self

    def get_response_headers(self):
        return self.last_response_headers

    def set_response_headers(self, headers):
        self.last_response_headers = headers
        return self

    def get_parsed_response_data(self):
        return self.last_parsed_response

    def set_parsed_response_data(self, response):
        self.last_parsed_response = response
        return self

    def get_last_function(self):
        return self.last_function

    def set_last_function(self, function):
        self.last_function = function
        return self

    def get_service_url(self):
        return self.service_url

    def set_service_url(self, url):
        self.service_url = url

    # ------------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------------

    def _pace_zone_request(self, endpoint):
        """Keep consecutive /domains/zones calls ``zone_min_interval`` seconds apart."""
        if not php.ltrim(endpoint, "/").startswith("domains/zones"):
            return
        if self._last_zone_request_at > 0.0 and self.zone_min_interval > 0:
            wait = self.zone_min_interval - (time.time() - self._last_zone_request_at)
            if wait > 0:
                time.sleep(wait)
        self._last_zone_request_at = time.time()

    def _error_details(self, exc, fallback=None):
        """Details for a catch block: parsed Details, else raw body, else the message."""
        details = php.get(self.last_parsed_response, "Details")
        if details is not None:
            return details
        raw = php.get(self.last_response, "raw_response")
        if raw is not None:
            return raw
        return exc.message if fallback is None else fallback

    def _fail(self, exc, default_code):
        code = format_error_code(exc.code) or default_code
        return {
            "result": RESULT_ERROR,
            "error": set_error(code, exc.message, self._error_details(exc)),
        }

    def _request(self, method, endpoint, data=None):
        """Send one gateway call; returns the decoded body or raises ApiError."""
        if data is None:
            data = {}
        self._pace_zone_request(endpoint)
        self.started_at = time.time()

        endpoint = php.strval(endpoint)
        self.last_function = "request:" + method + " " + endpoint.lstrip("?").split("?", 1)[0]
        url = php.strval(self.service_url) + "/" + endpoint.lstrip("/")
        self.last_request = {"url": url, "method": method, "payload": data}

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-KEY": php.strval(self.token),
            "__reseller": php.strval(self.reseller_id),
            "User-Agent": USER_AGENT,
        }
        body = None
        if method in ("GET", "DELETE"):
            if not php.empty(data):
                url += "?" + php.http_build_query(data)
        else:
            body = php.json_encode(data)

        req = HttpRequest(method, url, headers, body, self.timeout, self.connect_timeout, self.ssl_verify)
        try:
            resp = self.transport.send(req)
        except TransportError as err:
            self.last_response_headers = {"url": url, "http_code": 0, "total_time": time.time() - self.started_at}
            self.last_response = {"raw_response": False}
            if err.errno == CURLE_OPERATION_TIMEDOUT:
                message = "Could not reach the DomainNameAPI service: the connection timed out. (" + err.message + ")"
            else:
                message = "Curl error during request: " + err.message
            self.last_parsed_response = set_error("CURL_%d" % err.errno, message, message)
            error = ApiError(message, err.errno)
            self.telemetry.send_error(error)
            raise error

        status = resp.status
        body_text = resp.body
        self.last_response_headers = {
            "url": url,
            "http_code": status,
            "content_type": resp.headers.get("Content-Type", resp.headers.get("content-type")),
            "total_time": time.time() - self.started_at,
            "headers": dict(resp.headers),
        }
        decoded = php.json_decode(body_text)
        self.last_response = decoded if decoded is not None else {"raw_response": body_text}

        if 200 <= status <= 299:
            parsed = decoded
            self.last_parsed_response = parsed
            duration = (time.time() - self.started_at) * 1000
            if self.telemetry.enabled and self.telemetry.should_sample(duration):
                self.telemetry.send_performance(duration, self.started_at, time.time())
            return parsed

        parsed = decoded
        if status in (301, 302):
            parsed = {
                "message": "Invalid API credentials",
                "code": "CREDENTIALS",
                "details": "Authentication failed. Check your API key and reseller ID.",
            }

        error_message = php.coalesce(php.get(parsed, "message"), php.get(parsed, "error", "message"), body_text)
        error_code = php.coalesce(php.get(parsed, "code"), php.get(parsed, "error", "code"), "HTTP_%d" % status)
        error_details = php.coalesce(php.get(parsed, "details"), php.get(parsed, "error", "details"), body_text)

        if php.trim(error_message) == "":
            error_message = "HTTP %d - %s" % (status, _http_status_reason(status))
            if php.trim(error_details) == "":
                error_details = error_message

        is_boilerplate = bool(_BOILERPLATE_RE.search(php.strval(error_message)))
        if is_boilerplate or php.strval(error_message) == php.strval(error_code):
            details_clean = php.trim(re.sub(r"^Dna[" + _PCRE_SPACE + r"]+", "", php.strval(error_details), count=1))
            if (details_clean != ""
                    and details_clean != php.strval(error_message)
                    and details_clean != php.strval(error_code)
                    and not _BOILERPLATE_RE.search(details_clean)):
                error_message = details_clean
            else:
                error_message = ("The operation could not be completed by the registry (error: "
                                 + php.strval(error_code) + "). Please try again or contact support.")

        validation_errors = php.coalesce(php.get(parsed, "error", "validationErrors"), php.get(parsed, "validationErrors"))
        if php.is_array(validation_errors) and validation_errors:
            flattened = _flatten_validation_errors(validation_errors)
            if flattened != "":
                error_details = flattened

        self.last_parsed_response = set_error(error_code, error_message, error_details)
        error = ApiError(php.strval(error_message), status)
        self.telemetry.send_error(error)
        raise error

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    def get_reseller_details(self):
        try:
            response = self._request("GET", "deposit/accounts/me")
            resp = {}
            if php.get(response, "resellerId") is not None:
                usd = php.strval(php.coalesce(php.get(response, "usdBalance"), 0))
                resp["result"] = RESULT_OK
                resp["id"] = php.get(response, "resellerId")
                resp["active"] = True  # the API returns no status
                resp["name"] = php.coalesce(php.get(response, "resellerName"), "")
                resp["balance"] = usd
                resp["currency"] = "USD"
                resp["symbol"] = "$"
                resp["balances"] = [
                    {"balance": usd, "currency": "USD", "symbol": "$"},
                    {
                        "balance": php.strval(php.coalesce(php.get(response, "tryBalance"), 0)),
                        "currency": "TL",
                        "symbol": "TL",
                    },
                ]
            else:
                resp["result"] = RESULT_ERROR
                resp["error"] = set_error("CREDENTIALS", "Invalid response format",
                                          "Response does not contain required fields")
            return resp
        except ApiError as e:
            return self._fail(e, "RESELLER_DETAILS")

    def get_current_balance(self, currency_id="USD"):
        currency_name = php.strtoupper(currency_id)
        currency_map = {
            "USD": {"id": 2, "name": "USD", "symbol": "$"},
            "TRY": {"id": 1, "name": "TL", "symbol": "TL"},
            "EUR": {"id": 3, "name": "EUR", "symbol": "€"},
            "GBP": {"id": 4, "name": "GBP", "symbol": "£"},
        }
        mapped = currency_map.get(currency_name, {"id": 0, "name": currency_name, "symbol": ""})
        try:
            response = self._request("GET", "deposit/accounts/me", {"currency": currency_name})
            balance_key = php.strtolower(currency_id) + "Balance"
            return {
                "ErrorCode": 0,
                "OperationMessage": "Command completed succesfully.",
                "OperationResult": "SUCCESS",
                "Balance": php.number_format(php.floatval(php.coalesce(php.get(response, balance_key), 0)), 2),
                "CurrencyId": mapped["id"],
                "CurrencyInfo": None,
                "CurrencyName": mapped["name"],
                "CurrencySymbol": mapped["symbol"],
            }
        except ApiError as e:
            return {
                "ErrorCode": format_error_code(e.code) or "BALANCE",
                "OperationMessage": e.message,
                "OperationResult": "FAILED",
                "Balance": "0.00",
                "CurrencyId": mapped["id"],
                "CurrencyInfo": None,
                "CurrencyName": mapped["name"],
                "CurrencySymbol": mapped["symbol"],
            }

    # ------------------------------------------------------------------
    # Search and lists
    # ------------------------------------------------------------------

    def check_availability(self, domains, extensions, period, command="create"):
        try:
            queries = []
            for domain in php.values(domains):
                for tld in php.values(extensions):
                    queries.append({"domainName": php.strval(domain) + "." + php.ltrim(tld, ".")})

            if not queries:
                return {
                    "result": RESULT_ERROR,
                    "error": set_error("AVAILABILITY", "Domain names not found.",
                                       "No domain names provided for availability check"),
                }

            response = self._request("POST", "domains/bulk-search", queries)

            availability = []
            items = php.coalesce(php.get(response, "infos"), response)
            if php.is_array(items):
                for item in php.values(items):
                    if not php.is_array(item):
                        continue
                    tld_value = php.get(item, "tld")
                    if tld_value is None:
                        name = php.strval(php.coalesce(php.get(item, "domainName"), ""))
                        pos = name.rfind(".")
                        tld_value = name[pos + 1:] if pos >= 0 else ""
                    tld = php.strtolower(tld_value)
                    domain_raw = php.coalesce(php.get(item, "domainName"), "")
                    domain_name = php.strtolower(domain_raw).replace("." + tld, "")
                    status = php.strtolower(php.coalesce(php.get(item, "status"), ""))
                    is_available = any(php.loose_equals_string(status, s) for s in ("available", "1", "true"))
                    price = php.get(item, "price")
                    availability.append({
                        "TLD": tld,
                        "DomainName": domain_name,
                        "Status": "available" if is_available else "notavailable",
                        "Command": command,
                        "Period": php.coalesce(php.get(item, "period"), period),
                        "IsFee": php.coalesce(php.get(item, "isPremium"), False),
                        "Price": php.number_format(php.floatval(price), 4) if price is not None else None,
                        "Currency": php.get(item, "currency"),
                        "Reason": php.get(item, "reason"),
                    })
            return availability
        except ApiError as e:
            return self._fail(e, "AVAILABILITY")

    def get_list(self, extra_parameters=None):
        try:
            extra = php.to_dict(extra_parameters)
            # Legacy paging keys (PageNumber is 0-based) -> SkipCount / MaxResultCount / Sorting.
            if extra.get("PageSize") is not None:
                extra["MaxResultCount"] = php.intval(extra["PageSize"])
            if extra.get("PageNumber") is not None:
                page_size = php.intval(php.coalesce(extra.get("PageSize"), 200))
                extra["SkipCount"] = php.intval(extra["PageNumber"]) * page_size
            if extra.get("OrderColumn") is not None:
                direction = "DESC" if php.strtoupper(php.strval(php.coalesce(extra.get("OrderDirection"), "ASC"))) == "DESC" else "ASC"
                extra["Sorting"] = php.strval(extra["OrderColumn"]) + " " + direction
            for key in ("PageNumber", "PageSize", "OrderColumn", "OrderDirection"):
                extra.pop(key, None)

            params = {"MaxResultCount": 200, "SkipCount": 0}
            for key, value in extra.items():
                if isinstance(key, int):
                    params[len(params)] = value  # array_merge renumbers integer keys
                else:
                    params[key] = value
            response = self._request("GET", "domains", params)

            def domain_row(item):
                status_code = php.get(item, "statusCode")
                status_text = php.get(item, "statusText")
                if status_code is not None and status_code != "" and not php.is_numeric(status_code):
                    status = php.strval(status_code)
                elif status_text is not None and status_text != "" and not php.is_numeric(status_text):
                    status = php.strval(status_text)
                else:
                    status = _normalize_domain_status(php.coalesce(php.get(item, "status"), ""))
                return {
                    "ID": php.intval(php.coalesce(php.get(item, "id"), 0)),
                    "Status": status,
                    "DomainName": php.coalesce(php.get(item, "domainName"), ""),
                    "AuthCode": php.coalesce(php.get(item, "authCode"), ""),
                    "LockStatus": "true" if not php.empty(php.get(item, "lockStatus")) else "false",
                    "PrivacyProtectionStatus": "true" if not php.empty(php.get(item, "privacyProtectionStatus")) else "false",
                    "IsChildNameServer": "true" if not php.empty(php.get(item, "hosts")) else "false",
                    "Contacts": {
                        "Billing": {"ID": ""},
                        "Technical": {"ID": ""},
                        "Administrative": {"ID": ""},
                        "Registrant": {"ID": ""},
                    },
                    "Dates": {
                        "Start": _format_api_date(php.get(item, "startDate")),
                        "Expiration": _format_api_date(php.get(item, "expirationDate")),
                        "RemainingDays": php.intval(php.coalesce(php.get(item, "remainingDay"), 0)),
                    },
                    "NameServers": php.coalesce(php.get(item, "nameServers"), []),
                    "Additional": [],
                    "ChildNameServers": [],
                }

            items = php.get(response, "items")
            return {
                "data": {
                    "Domains": _map_values(items, domain_row) if items is not None else [],
                },
                "result": RESULT_OK,
                "TotalCount": php.intval(php.coalesce(php.get(response, "totalCount"), 0)),
            }
        except ApiError as e:
            return self._fail(e, "DOMAIN_LIST")

    def get_tld_list(self, count=20):
        try:
            response = self._request("GET", "products/tlds", {"MaxResultCount": count, "SkipCount": 0})

            tld_data = []
            id_counter = 1
            tld_items = php.get(response, "items")
            if php.is_array(tld_items):
                price_types = [
                    ("register", "registration"),
                    ("renew", "renew"),
                    ("transfer", "transfer"),
                    ("restore", "restore"),
                    ("refund", "refund"),
                    ("backorder", "backorder"),
                ]
                for tld in php.values(tld_items):
                    pricing = {}
                    currencies = {}

                    def add_price(out_type, info):
                        period = php.intval(php.coalesce(php.get(info, "period"), 1))
                        if period < 1:
                            period = 1
                        price = php.get(info, "price")
                        pricing.setdefault(out_type, {})[period] = (
                            php.number_format(php.floatval(price), 4) if price is not None else "0.0000")
                        currencies[out_type] = php.coalesce(php.get(info, "currency"), "")

                    first = php.get(tld, "prices", 0)
                    if first is not None and php.is_array(first):
                        for api_type, out_type in price_types:
                            api_value = php.get(first, api_type)
                            if api_value is None:
                                continue
                            if php.is_array(api_value) and php.get(api_value, 0) is not None:
                                for price_info in php.values(api_value):
                                    if php.is_array(price_info):
                                        add_price(out_type, price_info)
                            elif php.is_array(api_value):
                                add_price(out_type, api_value)

                    # Periods in ascending numeric order, as string keys (JSON object keys).
                    pricing_out = {}
                    for out_type, periods in pricing.items():
                        pricing_out[out_type] = {str(k): periods[k] for k in sorted(periods)}

                    tld_data.append({
                        "id": id_counter,
                        "status": php.coalesce(php.get(tld, "status"), "Active"),
                        "maxchar": php.coalesce(php.get(tld, "constraints", "maxLenght"), 63),
                        "maxperiod": php.coalesce(php.get(tld, "maxRegistrationPeriod"), 10),
                        "minchar": php.coalesce(php.get(tld, "constraints", "minLength"), 1),
                        "minperiod": php.coalesce(php.get(tld, "minRegistrationPeriod"), 1),
                        "tld": php.get(tld, "name"),
                        "pricing": pricing_out,
                        "currencies": currencies,
                    })
                    id_counter += 1

            return {"data": tld_data, "result": RESULT_OK}
        except ApiError as e:
            return self._fail(e, "TLD_LIST")

    # ------------------------------------------------------------------
    # Domain
    # ------------------------------------------------------------------

    def get_details(self, domain_name):
        try:
            response = self._request("GET", "domains/info", {"DomainName": domain_name})
            return self._parse_domain_info(response)
        except ApiError as e:
            return self._fail(e, "DOMAIN_DETAILS")

    def sync_from_registry(self, domain_name):
        return self.get_details(domain_name)

    def modify_name_server(self, domain_name, name_servers):
        try:
            payload = {"domainName": domain_name, "nameServers": normalize_host_name_list(name_servers)}
            response = self._request("PUT", "domains/dns/name-server", payload)
            return {
                "result": RESULT_OK,
                "data": {"NameServers": php.coalesce(php.get(response, "nameServers"), name_servers)},
            }
        except ApiError as e:
            return self._fail(e, "MODIFY_NS")

    def enable_theft_protection_lock(self, domain_name):
        try:
            # Locking and unlocking are separate endpoints; the body carries the domain only.
            self._request("POST", "domains/lock", {"domainName": domain_name})
            return {"result": RESULT_OK, "data": {"LockStatus": True}}
        except ApiError as e:
            return self._fail(e, "ENABLE_LOCK")

    def disable_theft_protection_lock(self, domain_name):
        try:
            self._request("POST", "domains/unlock", {"domainName": domain_name})
            return {"result": RESULT_OK, "data": {"LockStatus": False}}
        except ApiError as e:
            return self._fail(e, "DISABLE_LOCK")

    def modify_privacy_protection_status(self, domain_name, status, reason="Owner request"):
        try:
            if php.empty(reason):
                reason = DEFAULT_REASON  # noqa: F841 - kept for parity; the gateway takes no reason
            payload = {"domainName": domain_name, "privacyStatus": status is True}
            self._request("POST", "domains/privacy", payload)
            return {"data": {"PrivacyProtectionStatus": status}, "result": RESULT_OK}
        except ApiError as e:
            return self._fail(e, "MODIFY_PRIVACY")

    def renew(self, domain_name, period):
        try:
            response = self._request("POST", "domains/renew", {"domainName": domain_name, "period": period})
            if php.truthy(php.coalesce(php.get(response, "expirationDate"), False)):
                return {
                    "result": RESULT_OK,
                    "data": {"ExpirationDate": _format_api_date(php.get(response, "expirationDate"))},
                }
            self.telemetry.send_error(ApiError("[DOMAIN_RENEW] " + DEFAULT_ERRORS["DOMAIN_RENEW"]["description"], 0))
            return {"result": RESULT_ERROR, "error": set_error("DOMAIN_RENEW")}
        except ApiError as e:
            return self._fail(e, "RENEW_DOMAIN")

    def register_with_contact_info(self, domain_name, period, contacts, name_servers=None,
                                   epp_lock=True, privacy_lock=False, additional_attributes=None):
        if name_servers is None:
            name_servers = []
        if additional_attributes is None:
            additional_attributes = []
        try:
            payload_contacts = []
            for type_, details in php.items(contacts):
                payload_contacts.append(self._parse_contact(details, php.ucfirst(php.strtolower(type_))))

            # Normalise and drop empties first, then fall back to the defaults.
            name_servers = normalize_host_name_list(name_servers)
            if not name_servers:
                name_servers = list(DEFAULT_NAMESERVERS)

            if php.strtolower(php.strval(domain_name))[-3:] == ".tr":
                additional_attributes = _normalize_tr_attributes(php.array_cast(additional_attributes))

            # The gateway types tldAttributes as a string dictionary.
            additional_attributes = _stringify_attributes(php.array_cast(additional_attributes))

            payload = {
                "domainName": domain_name,
                "period": period,
                "nameServers": name_servers,
                "isLocked": epp_lock,
                "privacyEnabled": privacy_lock,
                "contacts": payload_contacts,
                "tldAttributes": php.JsonObject(additional_attributes),
            }
            response = self._request("POST", "domains/register-with-contacts", payload)
            return self._parse_domain_info(response)
        except ApiError as e:
            return self._fail(e, "REGISTER_DOMAIN")

    # ------------------------------------------------------------------
    # Child nameservers
    # ------------------------------------------------------------------

    def add_child_name_server(self, domain_name, name_server, ip_address):
        try:
            payload = {
                "domainName": domain_name,
                "hostName": normalize_host_name(name_server),
                "ipAddresses": [{
                    "ipAddress": ip_address,
                    "ipVersion": "v4" if _is_ipv4(ip_address) else "v6",
                }],
            }
            self._request("POST", "domains/dns/host", payload)
            return {"result": RESULT_OK, "data": {"NameServer": name_server, "IPAdresses": [ip_address]}}
        except ApiError as e:
            return self._fail(e, "ADD_CHILD_NS")

    def delete_child_name_server(self, domain_name, name_server):
        try:
            payload = {"domainName": domain_name, "hostName": normalize_host_name(name_server)}
            self._request("DELETE", "domains/dns/host", payload)
            return {"result": RESULT_OK, "data": {"NameServer": name_server}}
        except ApiError as e:
            return self._fail(e, "DELETE_CHILD_NS")

    def modify_child_name_server(self, domain_name, name_server, ip_address):
        try:
            name_server = normalize_host_name(name_server)
            payload = {
                "domainName": domain_name,
                "hostName": name_server,
                "newHostName": name_server,
                "ipAddresses": [{
                    "ipAddress": ip_address,
                    "ipVersion": "v4" if _is_ipv4(ip_address) else "v6",
                }],
            }
            response = self._request("PUT", "domains/dns/host", payload)
            return {
                "result": RESULT_OK,
                "data": {
                    "NameServer": php.coalesce(php.get(response, "hostName"), name_server),
                    "IPAdresses": php.coalesce(php.get(response, "ipAddresses"), [ip_address]),
                },
            }
        except ApiError as e:
            return self._fail(e, "MODIFY_CHILD_NS")

    # ------------------------------------------------------------------
    # Contacts
    # ------------------------------------------------------------------

    def get_contacts(self, domain_name):
        try:
            domain_info = self._request("GET", "domains/info", {"DomainName": domain_name})
            type_map = {"Admin": "Administrative", "Billing": "Billing", "Tech": "Technical", "Registrant": "Registrant"}
            contacts = {}
            contact_items = php.get(domain_info, "contacts")
            if php.is_array(contact_items):
                for item in php.values(contact_items):
                    api_type = php.coalesce(php.get(item, "contactType"), "")
                    key = type_map.get(api_type) if isinstance(api_type, str) else None
                    if key is None:
                        key = php.ucfirst(php.strtolower(api_type))
                    merged = dict(php.to_dict(item))
                    merged["type"] = key
                    contacts[key] = _parse_contact_info(merged)

            ordered = {}
            for key in ("Administrative", "Billing", "Registrant", "Technical"):
                if contacts.get(key) is not None:
                    ordered[key] = contacts[key]
            return {"data": {"contacts": ordered}, "result": RESULT_OK}
        except ApiError as e:
            return self._fail(e, "GET_CONTACTS")

    def save_contacts(self, domain_name, contacts):
        try:
            payload_contacts = []
            for type_, details in php.items(contacts):
                payload_contacts.append(self._parse_contact(details, php.ucfirst(php.strtolower(type_))))
            response = self._request("PUT", "domains/contacts/update",
                                     {"domainName": domain_name, "contacts": payload_contacts})
            parsed = {}
            response_contacts = php.get(response, "contacts")
            if php.is_array(response_contacts):
                for contact in php.values(response_contacts):
                    parsed[php.ucfirst(php.strtolower(php.get(contact, "type")))] = _parse_contact_info(contact)
            return {"result": RESULT_OK, "data": {"contacts": parsed}}
        except ApiError as e:
            return self._fail(e, "SAVE_CONTACTS")

    # ------------------------------------------------------------------
    # Transfers
    # ------------------------------------------------------------------

    def transfer(self, domain_name, epp_code, period, contacts=None):
        try:
            payload_contacts = []
            if not php.empty(contacts):
                for type_, details in php.items(contacts):
                    payload_contacts.append(self._parse_contact(details, php.ucfirst(php.strtolower(type_))))
            payload = {
                "domainName": domain_name,
                "authCode": epp_code,
                "period": period,
                "contacts": payload_contacts,
            }
            response = self._request("POST", "domains/transfer", payload)
            return self._parse_domain_info(response)
        except ApiError as e:
            return self._fail(e, "TRANSFER_DOMAIN")

    def _transfer_action(self, domain_name, action, default_status, default_code):
        try:
            response = self._request("POST", "domains/transfers/" + action, {"domainName": domain_name})
            return {
                "result": RESULT_OK,
                "data": {
                    "DomainName": domain_name,
                    "Status": php.coalesce(php.get(response, "status"), default_status),
                },
            }
        except ApiError as e:
            return self._fail(e, default_code)

    def cancel_transfer(self, domain_name):
        return self._transfer_action(domain_name, "cancel", "Cancelled", "CANCEL_TRANSFER")

    def approve_transfer(self, domain_name):
        return self._transfer_action(domain_name, "approve", "Approved", "APPROVE_TRANSFER")

    def reject_transfer(self, domain_name):
        return self._transfer_action(domain_name, "reject", "Rejected", "REJECT_TRANSFER")

    def check_transfer(self, domain_name, auth_code):
        try:
            response = self._request("POST", "domains/transfers/check",
                                     {"domainName": domain_name, "authCode": auth_code})
            g = lambda k: php.get(response, k)  # noqa: E731
            available = not php.empty(g("transferAvailabilityStatus"))
            envelope = {
                "result": RESULT_OK if available else RESULT_ERROR,
                "data": {
                    "TransferAvailabilityStatus": available,
                    "AuthCodeIsRequired": not php.empty(g("authCodeIsRequired")),
                    "AuthCodeIsValid": not php.empty(g("authCodeIsValid")),
                    "UserTransferRequired": not php.empty(g("userTransferRequired")),
                    "TransferLock": not php.empty(g("transferLock")),
                    "Message": php.strval(php.coalesce(g("message"), "")),
                    "MessageKey": php.strval(php.coalesce(g("messageKey"), "")),
                    "Additional": php.array_cast(g("additionalAttributes")) if g("additionalAttributes") is not None else [],
                },
            }
            if not available:
                envelope["error"] = set_error(
                    "TRANSFER_NOT_AVAILABLE",
                    php.coalesce(g("message"), "Domain is not transferable"),
                    php.coalesce(g("messageKey"), g("message"), ""),
                )
            return envelope
        except ApiError as e:
            return self._fail(e, "CHECK_TRANSFER")

    # ------------------------------------------------------------------
    # DNS zone
    # ------------------------------------------------------------------

    def get_resource_records(self, domain_name):
        try:
            response = self._request("GET", "domains/zones", {"domainName": domain_name})
            records = []
            for rset in php.values(php.array_cast(response)):
                if not php.is_array(rset):
                    continue
                name = php.coalesce(php.get(rset, "name"), "")
                type_ = php.coalesce(php.get(rset, "type"), "")
                ttl = php.intval(php.coalesce(php.get(rset, "ttl"), 0))
                rows = php.coalesce(php.get(rset, "records"), [])
                if not php.is_array(rows) or not rows:
                    records.append({"Name": name, "Type": type_, "TTL": ttl, "Content": "", "Disabled": False})
                    continue
                for rec in php.values(rows):
                    records.append({
                        "Name": name,
                        "Type": type_,
                        "TTL": ttl,
                        "Content": php.coalesce(php.get(rec, "content"), ""),
                        "Disabled": not php.empty(php.get(rec, "disabled")),
                    })
            return {"result": RESULT_OK, "data": {"records": records}}
        except ApiError as e:
            return self._fail(e, "GET_ZONE")

    def add_resource_record(self, domain_name, name, type_, content, ttl=3600, apply=True):
        try:
            why = _unsupported_zone_type(type_)
            if why:
                return {"result": RESULT_ERROR, "error": set_error("ADD_ZONE", why, why)}
            name = _relativize_record_name(name, domain_name)
            body = {"zoneStruct": _build_zone_struct(name, type_, content, ttl)}
            endpoint = "domains/zones?" + php.http_build_query({"domainName": domain_name})
            self._request("POST", endpoint, body)
            if php.truthy(apply):
                self.apply_resource_records(domain_name)
            return {
                "result": RESULT_OK,
                "data": {"Name": name, "Type": type_, "TTL": php.intval(ttl), "Content": content},
            }
        except ApiError as e:
            return self._fail(e, "ADD_ZONE")

    def edit_resource_record(self, domain_name, record_name, name, type_, content, ttl=3600, apply=True):
        try:
            why = _unsupported_zone_type(type_)
            if why:
                return {"result": RESULT_ERROR, "error": set_error("EDIT_ZONE", why, why)}
            name = _relativize_record_name(name, domain_name)
            body = {"zoneStruct": _build_zone_struct(name, type_, content, ttl)}
            endpoint = "domains/zones?" + php.http_build_query({"domainName": domain_name, "recordName": record_name})
            self._request("PUT", endpoint, body)
            if php.truthy(apply):
                self.apply_resource_records(domain_name)
            return {
                "result": RESULT_OK,
                "data": {"Name": name, "Type": type_, "TTL": php.intval(ttl), "Content": content},
            }
        except ApiError as e:
            return self._fail(e, "EDIT_ZONE")

    def delete_resource_record(self, domain_name, name, record, record_type, apply=True):
        try:
            self._request("DELETE", "domains/zones", {
                "domainName": domain_name,
                "Name": name,
                "Record": record,
                "RecordType": record_type,
            })
            if php.truthy(apply):
                self.apply_resource_records(domain_name)
            return {"result": RESULT_OK, "data": {"Name": name, "Type": record_type, "Content": record}}
        except ApiError as e:
            return self._fail(e, "DELETE_ZONE")

    def apply_resource_records(self, domain_name):
        try:
            endpoint = "domains/zones/apply?" + php.http_build_query({"domainName": domain_name})
            self._request("POST", endpoint, {})
            return {"result": RESULT_OK, "data": {"DomainName": domain_name}}
        except ApiError as e:
            return self._fail(e, "APPLY_ZONE")

    def set_resource_record_set(self, domain_name, name, type_, contents, ttl=3600, apply=True):
        if not isinstance(contents, (list, tuple, dict)):
            raise TypeError("contents must be a list of record values")
        try:
            why = _unsupported_zone_type(type_)
            if why:
                return {"result": RESULT_ERROR, "error": set_error("SET_ZONE", why, why)}
            name = _relativize_record_name(name, domain_name)
            contents = [v for v in (php.strval(x) for x in php.values(contents)) if php.trim(v) != ""]
            if not contents:
                return self.delete_resource_record_set(domain_name, name, type_, apply)

            # POST creates the set when absent and overwrites every value when present.
            body = {"zoneStruct": _build_zone_struct(name, type_, contents, ttl)}
            endpoint = "domains/zones?" + php.http_build_query({"domainName": domain_name})
            self._request("POST", endpoint, body)
            if php.truthy(apply):
                self.apply_resource_records(domain_name)
            return {
                "result": RESULT_OK,
                "data": {"Name": name, "Type": php.strtoupper(type_), "TTL": php.intval(ttl), "Contents": contents},
            }
        except ApiError as e:
            return self._fail(e, "SET_ZONE")

    def delete_resource_record_set(self, domain_name, name, type_, apply=True, known_value=""):
        try:
            type_ = php.strtoupper(php.trim(type_))
            value = php.strval(known_value)
            if value == "":
                current = self.get_resource_records(domain_name)
                if php.coalesce(current.get("result"), "") != RESULT_OK:
                    return current
                fqdn = _qualify_record_name(name, domain_name)
                for rec in current["data"]["records"]:
                    if php.strcasecmp_equal(rec["Name"], fqdn) and php.strcasecmp_equal(rec["Type"], type_):
                        value = php.strval(rec["Content"])
                        break
                if value == "":
                    # Nothing to remove: success, so callers stay idempotent.
                    return {"result": RESULT_OK, "data": {"Name": name, "Type": type_, "Removed": False}}
            return self.delete_resource_record(domain_name, _qualify_record_name(name, domain_name), value, type_, apply)
        except ApiError as e:
            return self._fail(e, "DELETE_ZONE")

    def _read_resource_record_set(self, domain_name, name, type_):
        current = self.get_resource_records(domain_name)
        if php.coalesce(current.get("result"), "") != RESULT_OK:
            return current
        fqdn = _qualify_record_name(name, domain_name)
        type_ = php.strtoupper(php.trim(type_))
        contents = []
        ttl = 0
        for rec in current["data"]["records"]:
            if not php.strcasecmp_equal(rec["Name"], fqdn) or not php.strcasecmp_equal(rec["Type"], type_):
                continue
            if php.strval(rec["Content"]) != "":
                contents.append(php.strval(rec["Content"]))
            ttl = php.intval(rec["TTL"])
        return {"ttl": ttl, "contents": contents}

    def add_resource_record_value(self, domain_name, name, type_, value, ttl=None, apply=True):
        try:
            why = _unsupported_zone_type(type_)
            if why:
                return {"result": RESULT_ERROR, "error": set_error("ADD_ZONE", why, why)}
            name = _relativize_record_name(name, domain_name)
            rset = self._read_resource_record_set(domain_name, name, type_)
            if "result" in rset:
                return rset
            for existing in rset["contents"]:
                if _same_record_value(type_, existing, value):
                    return {
                        "result": RESULT_OK,
                        "data": {"Name": name, "Type": php.strtoupper(type_), "Contents": rset["contents"], "Changed": False},
                    }
            contents = list(rset["contents"])
            contents.append(php.strval(value))
            return self.set_resource_record_set(domain_name, name, type_, contents,
                                                ttl if ttl is not None else (rset["ttl"] or 3600), apply)
        except ApiError as e:
            return self._fail(e, "ADD_ZONE")

    def remove_resource_record_value(self, domain_name, name, type_, value, apply=True):
        try:
            why = _unsupported_zone_type(type_)
            if why:
                return {"result": RESULT_ERROR, "error": set_error("DELETE_ZONE", why, why)}
            name = _relativize_record_name(name, domain_name)
            rset = self._read_resource_record_set(domain_name, name, type_)
            if "result" in rset:
                return rset
            remaining = []
            found = False
            for existing in rset["contents"]:
                if not found and _same_record_value(type_, existing, value):
                    found = True
                    continue
                remaining.append(existing)
            if not found:
                return {
                    "result": RESULT_OK,
                    "data": {"Name": name, "Type": php.strtoupper(type_), "Contents": rset["contents"], "Changed": False},
                }
            if not remaining:
                return self.delete_resource_record_set(domain_name, name, type_, apply, php.strval(value))
            return self.set_resource_record_set(domain_name, name, type_, remaining, rset["ttl"] or 3600, apply)
        except ApiError as e:
            return self._fail(e, "DELETE_ZONE")

    def replace_resource_record_value(self, domain_name, name, type_, old_value, new_value, ttl=None, apply=True):
        try:
            why = _unsupported_zone_type(type_)
            if why:
                return {"result": RESULT_ERROR, "error": set_error("EDIT_ZONE", why, why)}
            name = _relativize_record_name(name, domain_name)
            rset = self._read_resource_record_set(domain_name, name, type_)
            if "result" in rset:
                return rset
            contents = []
            found = False
            for existing in rset["contents"]:
                if not found and _same_record_value(type_, existing, old_value):
                    found = True
                    contents.append(php.strval(new_value))
                    continue
                contents.append(existing)
            if not found:
                why = 'No %s record "%s" with value "%s" to edit.' % (php.strtoupper(type_), name, php.strval(old_value))
                return {"result": RESULT_ERROR, "error": set_error("EDIT_ZONE", why, why)}
            return self.set_resource_record_set(domain_name, name, type_, contents,
                                                ttl if ttl is not None else (rset["ttl"] or 3600), apply)
        except ApiError as e:
            return self._fail(e, "EDIT_ZONE")

    # ------------------------------------------------------------------
    # Forwarding
    # ------------------------------------------------------------------

    def get_forwarding(self, domain_name):
        try:
            response = self._request("GET", "domains/forwards", {"domainName": domain_name})
            alias = php.get(response, "redirectAlias")
            return {
                "result": RESULT_OK,
                "data": {
                    "Enabled": not php.empty(alias),
                    "RedirectAddress": php.strval(php.coalesce(alias, "")),
                    "ForwardType": php.strval(php.coalesce(php.get(response, "redirectType"), "")),
                },
            }
        except ApiError as e:
            raw = php.coalesce(php.get(self.last_response, "raw_response"), e.message)
            if php.stripos_found(php.strval(raw), "not found") or php.stripos_found(e.message, "not found"):
                return {"result": RESULT_OK, "data": {"Enabled": False, "RedirectAddress": "", "ForwardType": ""}}
            details = php.coalesce(php.get(self.last_parsed_response, "Details"), raw)
            return {
                "result": RESULT_ERROR,
                "error": set_error(format_error_code(e.code) or "GET_FORWARD", e.message, details),
            }

    def set_forwarding(self, domain_name, redirect_address, forward_type="Standard"):
        try:
            type_ = php.ucfirst(php.strtolower(php.trim(forward_type)))
            if type_ not in FORWARD_TYPES:
                why = 'Forward type "%s" is not supported. Supported types: %s.' % (
                    php.strval(forward_type), ", ".join(FORWARD_TYPES))
                return {"result": RESULT_ERROR, "error": set_error("SET_FORWARD", why, why)}
            if php.trim(redirect_address) == "":
                why = "Redirect address is required."
                return {"result": RESULT_ERROR, "error": set_error("SET_FORWARD", why, why)}
            self._request("POST", "domains/forwards", {
                "domainName": domain_name,
                "redirectAddress": redirect_address,
                "forwardType": type_,
            })
            return {"result": RESULT_OK, "data": {"RedirectAddress": redirect_address, "ForwardType": type_}}
        except ApiError as e:
            return self._fail(e, "SET_FORWARD")

    def delete_forwarding(self, domain_name):
        try:
            # PascalCase query key, unlike the GET.
            self._request("DELETE", "domains/forwards", {"DomainName": domain_name})
            return {"result": RESULT_OK, "data": {"DomainName": domain_name}}
        except ApiError as e:
            return self._fail(e, "DELETE_FORWARD")

    # ------------------------------------------------------------------
    # Utilities (no network)
    # ------------------------------------------------------------------

    def is_tr_tld(self, domain):
        tail = php.strval(domain).encode("utf-8")[-3:]
        return tail.translate(bytes.maketrans(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ", b"abcdefghijklmnopqrstuvwxyz")) == b".tr"

    def validate_contact(self, contact):
        """Complete and normalise a contact the way the gateway requires it."""
        defaults = {
            "FirstName": "Isimyok",
            "LastName": "Isimyok",
            "AddressLine1": "Addres yok",
            "City": "ISTANBUL",
            "State": "ISTANBUL",
            "Country": "TR",
            "ZipCode": "34000",
            "Phone": "5555555555",
            "PhoneCountryCode": "90",
        }
        contact = php.to_dict(contact)
        for key, value in defaults.items():
            if contact.get(key) is None:
                contact[key] = value

        contact["FirstName"] = _sanitize_person_name(contact["FirstName"])
        contact["LastName"] = _sanitize_person_name(contact["LastName"])

        if php.strlen(php.trim(contact["FirstName"])) == 0:
            contact["FirstName"] = defaults["FirstName"]
        if php.strlen(php.trim(contact["LastName"])) == 0:
            contact["LastName"] = contact["FirstName"]
        if php.strlen(php.trim(contact["AddressLine1"])) == 0:
            contact["AddressLine1"] = defaults["AddressLine1"]
        if php.strlen(php.trim(contact["City"])) == 0:
            contact["City"] = defaults["City"]
        if php.strlen(php.trim(contact["State"])) == 0:
            contact["State"] = contact["City"]
        contact["Country"] = _normalize_country_code(contact["Country"])
        if php.strlen(php.trim(contact["Country"])) == 0:
            contact["Country"] = defaults["Country"]
        if php.strlen(php.trim(contact["ZipCode"])) == 0:
            contact["ZipCode"] = defaults["ZipCode"]

        phone, phone_cc = _normalize_phone(contact["Phone"], contact["PhoneCountryCode"])
        contact["Phone"] = phone
        contact["PhoneCountryCode"] = phone_cc
        if php.strlen(php.trim(contact["PhoneCountryCode"])) == 0:
            contact["PhoneCountryCode"] = defaults["PhoneCountryCode"]
        if php.strlen(php.trim(contact["Phone"])) == 0:
            contact["Phone"] = defaults["Phone"]

        # Fax is optional: normalise when present, never invent one.
        fax, fax_cc = _normalize_phone(php.coalesce(contact.get("Fax"), ""), php.coalesce(contact.get("FaxCountryCode"), ""))
        contact["Fax"] = fax
        contact["FaxCountryCode"] = "" if fax == "" else fax_cc
        return contact

    # ------------------------------------------------------------------
    # Parsing helpers
    # ------------------------------------------------------------------

    def _parse_domain_info(self, data):
        if php.empty(data):
            return {"result": RESULT_ERROR, "error": set_error("RESPONSE")}
        g = lambda *k: php.get(data, *k)  # noqa: E731

        def child(ns):
            ips = [php.get(ip, "ipAddress") for ip in php.values(php.coalesce(php.get(ns, "ipAddresses"), []))]
            return {"ns": php.get(ns, "name"), "ip": ips[-1] if ips else ""}

        remaining = g("remainingDay")
        return {
            "data": {
                "ID": php.intval(php.coalesce(g("id"), 0)),
                "Status": _normalize_domain_status(php.coalesce(g("status"), "")),
                "DomainName": php.strval(php.coalesce(g("domainName"), g("name"), "")),
                "AuthCode": php.strval(php.coalesce(g("authCode"), g("eppCode"), "")),
                "LockStatus": "true" if not php.empty(g("lockStatus")) else "false",
                "PrivacyProtectionStatus": "true" if not php.empty(g("privacyProtectionStatus")) else "false",
                "IsChildNameServer": "true" if not php.empty(g("hosts")) else "false",
                "Contacts": _parse_contact_ids(php.coalesce(g("contacts"), [])),
                "Dates": {
                    "Start": _format_api_date(g("startDate")),
                    "Expiration": _format_api_date(g("expirationDate")),
                    "RemainingDays": php.intval(remaining) if remaining is not None
                    else _remaining_days_from_date(g("expirationDate")),
                },
                "NameServers": _map_values(g("nameservers"), php.strval) if g("nameservers") is not None else [],
                "Additional": php.array_cast(g("additionalAttributes")) if g("additionalAttributes") is not None else [],
                "ChildNameServers": _map_values(g("hosts"), child) if g("hosts") is not None else [],
            },
            "result": RESULT_OK,
        }

    def _parse_contact(self, contact, type_):
        """Module contact (flat or nested shape) -> gateway ContactLiteDto."""
        type_map = {"Administrative": "Admin", "Technical": "Tech", "Billing": "Billing", "Registrant": "Registrant"}
        api_type = type_map.get(type_, type_)
        g = lambda *k: php.get(contact, *k)  # noqa: E731

        address = php.coalesce(g("AddressLine1"), g("Address", "Line1"), "")
        line2 = php.coalesce(g("AddressLine2"), g("Address", "Line2"), "")
        if not php.empty(line2):
            address = php.strval(address) + " " + php.strval(line2)

        phone = php.coalesce(g("Phone"), g("Phone", "Phone", "Number"), "")
        phone_cc = php.coalesce(g("PhoneCountryCode"), g("Phone", "Phone", "CountryCode"), "")
        fax = php.coalesce(g("Fax"), g("Phone", "Fax", "Number"), "")
        fax_cc = php.coalesce(g("FaxCountryCode"), g("Phone", "Fax", "CountryCode"), "")

        # Nested shape: Phone => ['Phone' => [...], 'Fax' => [...]].
        if php.is_array(phone):
            phone_cc = php.coalesce(php.get(phone, "Phone", "CountryCode"), "")
            phone = php.coalesce(php.get(phone, "Phone", "Number"), "")
        if php.is_array(fax):
            fax_cc = php.coalesce(php.get(fax, "Fax", "CountryCode"), "")
            fax = php.coalesce(php.get(fax, "Fax", "Number"), "")

        validated = self.validate_contact({
            "FirstName": php.coalesce(g("FirstName"), ""),
            "LastName": php.coalesce(g("LastName"), ""),
            "AddressLine1": address,
            "City": php.coalesce(g("City"), g("Address", "City"), ""),
            "State": php.coalesce(g("State"), g("Address", "State"), ""),
            "Country": php.coalesce(g("Country"), g("Address", "Country"), ""),
            "ZipCode": php.coalesce(g("ZipCode"), g("Address", "ZipCode"), ""),
            "Phone": phone,
            "PhoneCountryCode": phone_cc,
            "Fax": fax,
            "FaxCountryCode": fax_cc,
        })

        return {
            "contactType": api_type,
            "firstName": validated["FirstName"],
            "lastName": validated["LastName"],
            "companyName": php.coalesce(g("Company"), ""),
            "eMail": php.coalesce(g("EMail"), ""),
            "address": validated["AddressLine1"],
            "city": validated["City"],
            "state": validated["State"],
            "country": validated["Country"],
            "postalCode": validated["ZipCode"],
            "phoneCountryCode": validated["PhoneCountryCode"],
            "phone": validated["Phone"],
            "faxCountryCode": validated["FaxCountryCode"],
            "fax": validated["Fax"],
            # Required non-nullable bool in the gateway ContactLiteDto.
            "isHidden": php.to_bool(php.coalesce(g("IsHidden"), False)),
        }
