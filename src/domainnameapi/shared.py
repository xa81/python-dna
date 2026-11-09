"""Constants and helpers shared by the client and the telemetry layer.

Port of php-dna ``SharedApiConfigAndUtilsTrait``.
"""

import re

from . import _php as php
from ._version import VERSION

APPLICATION = "DomainNameAPI-Python"
USER_AGENT = "DomainNameAPI-Python/" + VERSION

PERFORMANCE_SAMPLE_RATE = 40  # 4% (40 out of 1000)
RESULT_OK = "OK"
RESULT_ERROR = "ERROR"
RESULT_SUCCESS = "SUCCESS"

DEFAULT_NAMESERVERS = [
    "ns1.domainnameapi.com",
    "ns2.domainnameapi.com",
]

# Error messages that are expected, high-volume noise and are never reported.
DEFAULT_IGNORED_ERRORS = [
    "Domain not found",
    "ERR_DOMAIN_NOT_FOUND",
    "Reseller not found",
    "Domain is not in updateable status",
    "balance is not sufficient",
    "Price definition not found",
    "TLD is not supported",
    "Invalid API credentials",
    "could not be found",  # API_404 "The domain name you requested could not be found"
    "Insufficent reseller balance",  # (sic) matches the gateway's spelling
    "Redirect information not found",  # no forwarding configured: get_forwarding reports it as disabled
]

DEFAULT_ERRORS = {
    "DOMAIN_DETAILS": {
        "code": "DOMAIN_DETAILS",
        "message": "Invalid domain details! Details format is not valid",
        "description": "The provided domain details are not in the expected format",
    },
    "CREDENTIALS": {
        "code": "CREDENTIALS",
        "message": "Invalid reseller ID or API key",
        "description": "The provided API credentials are invalid",
    },
    "DOMAIN_LIST": {
        "code": "DOMAIN_LIST",
        "message": "The domain list is invalid or contains multiple entries!",
        "description": "The domain list response format is incorrect or unexpected",
    },
    "TLD_LIST": {
        "code": "TLD_LIST",
        "message": "TLD info is not a valid array or more than one TLD info has returned!",
        "description": "The TLD list response is not in the expected format",
    },
    "RESPONSE": {
        "code": "RESPONSE",
        "message": "Invalid response received from server! Response is empty.",
        "description": "The API response is empty or null",
    },
    "RESPONSE_FORMAT": {
        "code": "RESPONSE_FORMAT",
        "message": "Invalid response received from server! Response format is not valid.",
        "description": "The API response format is not in the expected structure",
    },
    "RESPONSE_COUNT": {
        "code": "RESPONSE_COUNT",
        "message": "Invalid parameters passed to function! Response data contains more than one result!",
        "description": "The API response contains multiple results when only one was expected",
    },
    "RESPONSE_CODE": {
        "code": "RESPONSE_CODE",
        "message": "Invalid parameters passed to function! Operation result or Error code not received from server",
        "description": "The API response is missing required operation result or error code fields",
    },
    "RESPONSE_REST": {
        "code": "RESPONSE_REST",
        "message": "Invalid parameters passed to function! REST return is not a valid array!",
        "description": "The REST response is not in a valid array format",
    },
    "CONTACT_INFO": {
        "code": "CONTACT_INFO",
        "message": "Invalid response received from server! Contact info is not a valid array or more than one contact info has returned!",
        "description": "The contact information response is not in the expected format",
    },
    "CONTACT_SAVE": {
        "code": "CONTACT_SAVE",
        "message": "Invalid response received from server! Contact info could not be saved!",
        "description": "The contact information could not be saved on the server",
    },
    "DOMAIN_TRANSFER_REQUEST": {
        "code": "DOMAIN_TRANSFER_REQUEST",
        "message": "Invalid response received from server! Domain transfer request could not be completed!",
        "description": "The domain transfer request failed to complete",
    },
    "DOMAIN_RENEW": {
        "code": "DOMAIN_RENEW",
        "message": "Invalid response received from server! Domain renew request could not be completed!",
        "description": "The domain renewal request failed to complete",
    },
    "DOMAIN_REGISTER": {
        "code": "DOMAIN_REGISTER",
        "message": "Invalid response received from server! Domain register request could not be completed!",
        "description": "The domain registration request failed to complete",
    },
    "DOMAIN_SYNC": {
        "code": "DOMAIN_SYNC",
        "message": "Invalid response received from server! Domain sync request could not be completed!",
        "description": "The domain synchronization request failed to complete",
    },
}

DEFAULT_CACHE_TTL = 512
DEFAULT_TIMEOUT = 30
DEFAULT_CONNECT_TIMEOUT = 10
DEFAULT_REASON = "Owner request"


class ApiError(Exception):
    """Internal failure of one gateway call.

    Mirrors the ``Exception($message, $code)`` php-dna throws inside
    ``request()``: ``code`` is the HTTP status, or a curl-style error number
    for transport failures. Every public method catches it and returns the
    error envelope, so it never reaches the caller.
    """

    def __init__(self, message, code=0):
        super().__init__(message)
        self.message = message
        self.code = code


def set_error(code, message="", details="", gateway_code=""):
    """Build the ``{'Code', 'Message', 'Details'}`` error dict.

    For a known code the caller's message/details win and the predefined text
    is only the fallback when they are blank. An ``API_<status>`` error also
    carries the gateway's own code as ``GatewayCode`` when there is one.
    """
    known = DEFAULT_ERRORS.get(code) if isinstance(code, str) else None
    if known is not None:
        result = {
            "Code": known["code"],
            "Message": message if php.trim(message) != "" else known["message"],
            "Details": details if php.trim(details) != "" else known["description"],
        }
    else:
        result = {"Code": code, "Message": message, "Details": details}
    if gateway_code and isinstance(result["Code"], str) and re.match(r"^API_\d+$", result["Code"]):
        result["GatewayCode"] = gateway_code
    return result


def format_error_code(code, transport_failed=False):
    """HTTP statuses become ``API_<status>``, transport errors ``CURL_<errno>``."""
    if php.is_numeric(code):
        return ("CURL_" if transport_failed else "API_") + php.strval(code)
    return php.strval(code)


def normalize_host_name(host_name):
    """Trim, drop the FQDN trailing dot and lowercase a host name."""
    return php.strtolower(php.rtrim(php.trim(host_name), "."))


def normalize_host_name_list(host_names):
    """Normalise each entry, drop empties, non-strings and duplicates; keep order."""
    if not isinstance(host_names, (list, dict, tuple)):
        return []
    normalized = []
    for host_name in php.values(host_names):
        if not isinstance(host_name, str):
            continue
        host_name = normalize_host_name(host_name)
        if host_name != "" and host_name not in normalized:
            normalized.append(host_name)
    return normalized
