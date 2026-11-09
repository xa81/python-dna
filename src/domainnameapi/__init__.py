"""DomainNameAPI client for Python.

Faithful port of php-dna (https://github.com/domainreseller/php-dna)::

    from domainnameapi import DomainNameAPI

    dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
    print(dna.get_details("example.com"))
"""

from ._version import VERSION, __version__
from .client import DomainNameAPI
from .rest import DNARest, FORWARD_TYPES, URL_OTE, URL_PROD, ZONE_RECORD_TYPES
from .shared import APPLICATION, RESULT_ERROR, RESULT_OK, USER_AGENT
from .transport import HttpRequest, HttpResponse, TransportError, UrllibTransport

#: Alias with php-dna's capitalisation.
DomainNameApi = DomainNameAPI

__all__ = [
    "APPLICATION",
    "DNARest",
    "DomainNameAPI",
    "DomainNameApi",
    "FORWARD_TYPES",
    "HttpRequest",
    "HttpResponse",
    "RESULT_ERROR",
    "RESULT_OK",
    "TransportError",
    "URL_OTE",
    "URL_PROD",
    "USER_AGENT",
    "UrllibTransport",
    "VERSION",
    "ZONE_RECORD_TYPES",
    "__version__",
]
