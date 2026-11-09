"""PHP value semantics used by php-dna, re-implemented for Python.

php-dna is the reference implementation. Its results depend on a handful of
PHP rules that differ from Python's: ``??`` treats ``null`` as missing,
``empty()`` treats ``"0"`` as empty, ``(int)"12abc"`` is ``12``, string
functions such as ``strtolower`` and ``trim`` are ASCII/byte based, and so on.
Everything in this module exists so that the client returns exactly what
php-dna returns for the same input. It is internal API.
"""

import calendar
import json
import math
import re
import time
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from urllib.parse import quote_plus

# Characters stripped by PHP's trim()/rtrim()/ltrim() without a char list.
PHP_TRIM_CHARS = " \t\n\r\0\x0b"

_ASCII_UPPER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")
_ASCII_LOWER = str.maketrans("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

_NUMERIC_RE = re.compile(r"^[ \t\n\r\x0b\f]*[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?[ \t\n\r\x0b\f]*$")
_NUMERIC_PREFIX_RE = re.compile(r"^[ \t\n\r\x0b\f]*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)")
_INT_PREFIX_RE = re.compile(r"^[+-]?\d+$")


class JsonObject(dict):
    """A dict that is always JSON-encoded as an object, even when empty.

    PHP encodes an empty array as ``[]``; php-dna uses ``new stdClass()`` /
    ``(object)`` where the gateway needs ``{}``. This marks those places.
    """


_MISSING = object()


def get(value, *keys):
    """Null-safe nested read with PHP ``isset``/``??`` semantics.

    Returns ``None`` when any step is missing, ``None``, or not an array.
    Integer and numeric-string keys are interchangeable, like PHP array keys.
    """
    for key in keys:
        if isinstance(value, dict):
            found = value.get(key, _MISSING)
            if found is _MISSING:
                if isinstance(key, int) and not isinstance(key, bool):
                    found = value.get(str(key), _MISSING)
                elif isinstance(key, str) and re.match(r"^(0|-?[1-9]\d*)$", key):
                    found = value.get(int(key), _MISSING)
            if found is _MISSING:
                return None
            value = found
        elif isinstance(value, list):
            idx = key
            if isinstance(idx, str) and re.match(r"^(0|[1-9]\d*)$", idx):
                idx = int(idx)
            if isinstance(idx, int) and not isinstance(idx, bool) and 0 <= idx < len(value):
                value = value[idx]
            else:
                return None
        else:
            return None
        if value is None:
            return None
    return value


def coalesce(*values):
    """PHP ``a ?? b ?? c``: the first value that is not ``None``."""
    for v in values:
        if v is not None:
            return v
    return None


def is_array(value):
    return isinstance(value, (dict, list))


def empty(value):
    """PHP ``empty()``."""
    if value is None or value is False:
        return True
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return value == 0
    if isinstance(value, str):
        return value == "" or value == "0"
    if isinstance(value, (list, dict, tuple)):
        return len(value) == 0
    return False


def truthy(value):
    """PHP boolean conversion."""
    return not empty(value)


def values(value):
    """The values a PHP ``foreach`` over ``value`` would visit."""
    if isinstance(value, dict):
        return list(value.values())
    if isinstance(value, (list, tuple)):
        return list(value)
    return []


def items(value):
    """The ``key => value`` pairs a PHP ``foreach`` over ``value`` would visit."""
    if isinstance(value, dict):
        return list(value.items())
    if isinstance(value, (list, tuple)):
        return list(enumerate(value))
    return []


def array_cast(value):
    """PHP ``(array) $value``."""
    if value is None:
        return []
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def to_dict(value):
    """A PHP array as an ordered ``dict`` (lists become ``{0: .., 1: ..}``)."""
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, (list, tuple)):
        return dict(enumerate(value))
    if value is None:
        return {}
    return {0: value}


def float_to_string(value):
    """PHP 8 ``(string)$float``: 14 significant digits (``precision`` ini),
    exponent notation below 1e-4 and from 1e15 on (``1.0E+15``)."""
    if math.isnan(value):
        return "NAN"
    if math.isinf(value):
        return "INF" if value > 0 else "-INF"
    if value == 0:
        return "-0" if math.copysign(1.0, value) < 0 else "0"
    precision = 14
    mantissa, exp = ("%.*e" % (precision - 1, value)).split("e")
    exp = int(exp)
    if exp < -4 or exp >= precision:
        if "." in mantissa:
            mantissa = mantissa.rstrip("0").rstrip(".")
        if "." not in mantissa:
            mantissa += ".0"
        return "%sE%s%d" % (mantissa, "+" if exp >= 0 else "-", abs(exp))
    text = "%.*f" % (max(0, precision - 1 - exp), value)
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def strval(value):
    """PHP ``(string) $value``."""
    if value is None:
        return ""
    if value is True:
        return "1"
    if value is False:
        return ""
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return float_to_string(value)
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict, tuple)):
        return "Array"
    return str(value)


def floatval(value):
    """PHP ``(float) $value``."""
    if value is None or value is False:
        return 0.0
    if value is True:
        return 1.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        m = _NUMERIC_PREFIX_RE.match(value)
        if not m:
            return 0.0
        try:
            return float(m.group(1))
        except (ValueError, OverflowError):
            return 0.0
    if isinstance(value, (list, dict, tuple)):
        return 1.0 if value else 0.0
    return 0.0


_INT_MAX = 2 ** 63 - 1
_INT_MIN = -(2 ** 63)


def _float_to_int(value, saturate=False):
    if math.isnan(value) or math.isinf(value):
        return 0 if not saturate or math.isnan(value) else (_INT_MAX if value > 0 else _INT_MIN)
    if not (_INT_MIN <= value < 2.0 ** 63):
        if saturate:
            return _INT_MAX if value > 0 else _INT_MIN
        # PHP 8 wraps out-of-range floats modulo 2**64.
        r = int(value) % (2 ** 64)
        return r - 2 ** 64 if r >= 2 ** 63 else r
    return int(value)


def intval(value):
    """PHP ``(int) $value``."""
    if value is None or value is False:
        return 0
    if value is True:
        return 1
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return _float_to_int(value)
    if isinstance(value, str):
        m = _NUMERIC_PREFIX_RE.match(value)
        if not m:
            return 0
        num = m.group(1)
        if _INT_PREFIX_RE.match(num):
            return max(_INT_MIN, min(_INT_MAX, int(num)))
        try:
            return _float_to_int(float(num), saturate=True)
        except (ValueError, OverflowError):
            return 0
    if isinstance(value, (list, dict, tuple)):
        return 1 if value else 0
    return 0


def filter_bool(value):
    """``filter_var($value, FILTER_VALIDATE_BOOLEAN)``: "1"/"true"/"on"/"yes" -> True."""
    if value is True:
        return True
    if value is None or value is False or isinstance(value, (list, dict, tuple)):
        return False
    return strval(value).strip(" \t\n\r\x0b\f\0").lower() in ("1", "true", "on", "yes")


def to_bool(value):
    """PHP ``(bool) $value``."""
    return truthy(value)


def is_numeric(value):
    """PHP 8 ``is_numeric()``."""
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        return bool(_NUMERIC_RE.match(value))
    return False


def trim(value, chars=PHP_TRIM_CHARS):
    return strval(value).strip(chars)


def rtrim(value, chars=PHP_TRIM_CHARS):
    return strval(value).rstrip(chars)


def ltrim(value, chars=PHP_TRIM_CHARS):
    return strval(value).lstrip(chars)


def strtolower(value):
    """ASCII-only lowercase, like PHP 8 ``strtolower``."""
    return strval(value).translate(_ASCII_UPPER)


def strtoupper(value):
    """ASCII-only uppercase, like PHP 8 ``strtoupper``."""
    return strval(value).translate(_ASCII_LOWER)


def ucfirst(value):
    s = strval(value)
    if not s:
        return s
    return strtoupper(s[0]) + s[1:]


def strlen(value):
    """Byte length (PHP strings are byte strings)."""
    return len(strval(value).encode("utf-8"))


def strcasecmp_equal(a, b):
    """``strcasecmp($a, $b) === 0``."""
    return strtolower(a) == strtolower(b)


def stripos_found(haystack, needle):
    """``stripos($haystack, $needle) !== false``."""
    return strtolower(needle) in strtolower(haystack)


def loose_equals_string(a, b):
    """PHP 8 ``==`` between two strings (numeric strings compare as numbers)."""
    if a == b:
        return True
    if is_numeric(a) and is_numeric(b):
        return float(a.strip(" \t\n\r\x0b\f")) == float(b.strip(" \t\n\r\x0b\f"))
    return False


def number_format(value, decimals):
    """``number_format($value, $decimals, '.', '')`` (round half away from zero)."""
    value = float(value)
    if math.isnan(value) or math.isinf(value):
        return strval(value).lower() if math.isnan(value) else ("inf" if value > 0 else "-inf")
    try:
        d = Decimal(repr(value))
    except InvalidOperation:  # pragma: no cover - repr() of a finite float is always valid
        d = Decimal(value)
    q = Decimal(1).scaleb(-decimals)
    rounded = d.quantize(q, rounding=ROUND_HALF_UP)
    if rounded == 0:
        rounded = abs(rounded)
    return "{0:.{1}f}".format(rounded, decimals)


# --------------------------------------------------------------------------
# Query strings and JSON
# --------------------------------------------------------------------------

def urlencode(value):
    """PHP ``urlencode()`` (spaces as ``+``, everything but ``A-Za-z0-9-_.`` escaped)."""
    return quote_plus(strval(value), safe="").replace("~", "%7E")


def _query_scalar(value):
    if value is True:
        return "1"
    if value is False:
        return "0"
    return strval(value)


def http_build_query(data):
    """PHP ``http_build_query()``: ``true``/``false`` as ``1``/``0``, ``null`` skipped,
    nested arrays as ``key[sub]=..`` (brackets percent-encoded)."""
    parts = []

    def walk(prefix, value):
        if value is None:
            return
        if isinstance(value, (dict, list, tuple)):
            for k, v in items(value):
                walk("%s[%s]" % (prefix, strval(k)), v)
            return
        parts.append(urlencode(prefix) + "=" + urlencode(_query_scalar(value)))

    for key, value in items(data):
        if value is None:
            continue
        if isinstance(value, (dict, list, tuple)):
            for k, v in items(value):
                walk("%s[%s]" % (strval(key), strval(k)), v)
        else:
            parts.append(urlencode(strval(key)) + "=" + urlencode(_query_scalar(value)))
    return "&".join(parts)


def _jsonable(value):
    if isinstance(value, JsonObject):
        return {strval(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, dict):
        if not value:
            return []
        keys = list(value.keys())
        if all(isinstance(k, int) and not isinstance(k, bool) for k in keys) and keys == list(range(len(keys))):
            return [_jsonable(v) for v in value.values()]
        return {strval(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return value


def json_encode(value):
    """PHP ``json_encode()`` with default flags (``\\/`` and ``\\uXXXX`` escapes)."""
    text = json.dumps(_jsonable(value), separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return text.replace("/", "\\/")


def _reject_constant(name):
    raise ValueError("invalid JSON constant " + name)


def json_decode(text):
    """PHP ``json_decode($text, true)``: ``None`` for empty or invalid input."""
    if text is None or text is False:
        return None
    if isinstance(text, bytes):
        try:
            text = text.decode("utf-8")
        except UnicodeDecodeError:
            return None
    if not isinstance(text, str) or text.strip(" \t\n\r") == "":
        return None
    try:
        return json.loads(text, parse_constant=_reject_constant)
    except (ValueError, RecursionError):
        return None


# --------------------------------------------------------------------------
# Dates
# --------------------------------------------------------------------------

_DATE_RE = re.compile(
    r"^\s*(\d{4})-(\d{1,2})-(\d{1,2})"
    r"(?:[Tt ]+(\d{1,2}):(\d{2})(?::(\d{2})(?:[.,](\d+))?)?)?"
    r"\s*(Z|z|UTC|GMT|[+-]\d{2}:?\d{2}|[+-]\d{2})?\s*$"
)


def strtotime(value):
    """Subset of PHP ``strtotime()`` covering the date formats the gateway emits.

    Returns a Unix timestamp (UTC) or ``None`` when the value cannot be parsed
    (PHP returns ``false``). Dates without an offset are read as UTC, the
    timezone the conformance fixtures were generated in.
    """
    s = strval(value)
    m = _DATE_RE.match(s)
    if not m:
        return None
    year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
    hour = int(m.group(4) or 0)
    minute = int(m.group(5) or 0)
    second = int(m.group(6) or 0)
    if not (1 <= month <= 12) or not (1 <= day <= 31) or hour > 24 or minute > 59 or second > 60:
        return None
    # PHP rolls over out-of-range days (2023-02-30 -> 2023-03-02); timegm does too.
    ts = calendar.timegm((year, month, 1, hour, minute, second, 0, 0, 0)) + (day - 1) * 86400
    tz = m.group(8)
    if tz and tz.upper() not in ("Z", "UTC", "GMT"):
        sign = 1 if tz[0] == "+" else -1
        digits = tz[1:].replace(":", "")
        hours = int(digits[:2])
        minutes = int(digits[2:4]) if len(digits) >= 4 else 0
        ts -= sign * (hours * 3600 + minutes * 60)
    return ts


def format_timestamp(ts):
    """``date('Y-m-d\\TH:i:s', $ts)`` in UTC, years before 1000 zero-padded."""
    days, rem = divmod(int(ts), 86400)
    # 719163 = days from 0001-01-01 to 1970-01-01 (proleptic Gregorian ordinal).
    from datetime import date

    d = date.fromordinal(days + 719163)
    hh, rem = divmod(rem, 3600)
    mm, ss = divmod(rem, 60)
    return "%04d-%02d-%02dT%02d:%02d:%02d" % (d.year, d.month, d.day, hh, mm, ss)


def now():
    return time.time()
