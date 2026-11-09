"""HTTP transport.

The client talks to the gateway through a *transport*: any object with a
``send(request)`` method that takes an :class:`HttpRequest` and returns an
:class:`HttpResponse`, or raises :class:`TransportError` when the gateway
could not be reached at all. The default :class:`UrllibTransport` uses only
the standard library; tests replace it with a fake.
"""

import functools
import http.client
import socket
import ssl
import time
import urllib.error
import urllib.request

# curl error numbers, so transport failures carry the same codes as php-dna.
CURLE_COULDNT_RESOLVE_HOST = 6
CURLE_COULDNT_CONNECT = 7
CURLE_PARTIAL_FILE = 18
CURLE_OPERATION_TIMEDOUT = 28
CURLE_SSL_CONNECT_ERROR = 35
CURLE_GOT_NOTHING = 52
CURLE_RECV_ERROR = 56
CURLE_PEER_FAILED_VERIFICATION = 60


class HttpRequest(object):
    """One outgoing gateway call."""

    __slots__ = ("method", "url", "headers", "body", "timeout", "connect_timeout", "verify_ssl")

    def __init__(self, method, url, headers, body=None, timeout=30, connect_timeout=10, verify_ssl=True):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        self.timeout = timeout
        self.connect_timeout = connect_timeout
        self.verify_ssl = verify_ssl

    def __repr__(self):
        return "HttpRequest(%r, %r)" % (self.method, self.url)


class HttpResponse(object):
    """Status, raw body text and response headers of one call."""

    __slots__ = ("status", "body", "headers")

    def __init__(self, status, body="", headers=None):
        self.status = int(status)
        self.body = body if body is not None else ""
        self.headers = headers or {}

    def __repr__(self):
        return "HttpResponse(%d, %d bytes)" % (self.status, len(self.body))


class TransportError(Exception):
    """The request never produced an HTTP response (timeout, DNS, TLS, reset).

    ``errno`` follows curl's numbering (28 = timeout, 6 = DNS, 7 = connect,
    35/60 = TLS, 52/56 = connection dropped).
    """

    def __init__(self, errno, message):
        super().__init__(message)
        self.errno = errno
        self.message = message


class _ConnectTimeoutMixin(object):
    """Use a shorter timeout for connect (+ TLS handshake) than for the rest."""

    def __init__(self, *args, **kwargs):
        self._connect_timeout = kwargs.pop("connect_timeout", None)
        super(_ConnectTimeoutMixin, self).__init__(*args, **kwargs)

    def connect(self):
        total = self.timeout
        if self._connect_timeout is not None:
            self.timeout = self._connect_timeout
        try:
            super(_ConnectTimeoutMixin, self).connect()
        finally:
            self.timeout = total
        if self.sock is not None:
            self.sock.settimeout(total)


class _HTTPConnection(_ConnectTimeoutMixin, http.client.HTTPConnection):
    pass


class _HTTPSConnection(_ConnectTimeoutMixin, http.client.HTTPSConnection):
    pass


class _HTTPHandler(urllib.request.HTTPHandler):
    def __init__(self, connect_timeout):
        super(_HTTPHandler, self).__init__()
        self._connect_timeout = connect_timeout

    def http_open(self, req):
        return self.do_open(functools.partial(_HTTPConnection, connect_timeout=self._connect_timeout), req)


class _HTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, connect_timeout, context):
        super(_HTTPSHandler, self).__init__(context=context)
        self._connect_timeout = connect_timeout
        self._ctx = context

    def https_open(self, req):
        return self.do_open(
            functools.partial(_HTTPSConnection, connect_timeout=self._connect_timeout),
            req,
            context=self._ctx,
        )


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """curl does not follow redirects; a 301/302 must reach the client as is."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _classify(exc):
    """Map a Python networking exception to (curl errno, curl-like message)."""
    reason = exc
    if isinstance(exc, urllib.error.URLError) and not isinstance(exc, urllib.error.HTTPError):
        reason = exc.reason if exc.reason is not None else exc
    text = str(reason) or reason.__class__.__name__
    if isinstance(reason, (socket.timeout, TimeoutError)) or "timed out" in text.lower():
        return CURLE_OPERATION_TIMEDOUT, text
    if isinstance(reason, socket.gaierror):
        return CURLE_COULDNT_RESOLVE_HOST, "Could not resolve host: " + text
    if hasattr(ssl, "SSLCertVerificationError") and isinstance(reason, ssl.SSLCertVerificationError):
        return CURLE_PEER_FAILED_VERIFICATION, "SSL certificate problem: " + text
    if isinstance(reason, ssl.SSLError):
        return CURLE_SSL_CONNECT_ERROR, "SSL connect error: " + text
    if isinstance(reason, ConnectionRefusedError):
        return CURLE_COULDNT_CONNECT, "Failed to connect: " + text
    if isinstance(reason, http.client.RemoteDisconnected):
        return CURLE_GOT_NOTHING, "Empty reply from server"
    if isinstance(reason, http.client.IncompleteRead):
        return CURLE_PARTIAL_FILE, "Transferred a partial file"
    if isinstance(reason, ConnectionResetError):
        return CURLE_RECV_ERROR, "Recv failure: Connection reset by peer"
    if isinstance(reason, (http.client.HTTPException, ConnectionError)):
        return CURLE_RECV_ERROR, "Recv failure: " + text
    return CURLE_COULDNT_CONNECT, text


def _read_body(fp, deadline):
    chunks = []
    while True:
        if time.monotonic() > deadline:
            raise socket.timeout("Operation timed out while reading the response body")
        chunk = fp.read(65536)
        if not chunk:
            break
        chunks.append(chunk)
    return b"".join(chunks).decode("utf-8", errors="replace")


class UrllibTransport(object):
    """Standard-library transport (``urllib.request``).

    No redirects are followed (a 301/302 is reported to the client, as with
    curl), the connect + TLS handshake must finish within ``connect_timeout``
    seconds and the whole call within ``timeout`` seconds. Proxy environment
    variables (``HTTPS_PROXY`` ...) are honoured.
    """

    def send(self, request):
        if request.verify_ssl:
            context = ssl.create_default_context()
        else:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        opener = urllib.request.build_opener(
            _NoRedirect(),
            _HTTPHandler(request.connect_timeout),
            _HTTPSHandler(request.connect_timeout, context),
        )
        data = request.body.encode("utf-8") if isinstance(request.body, str) else request.body
        req = urllib.request.Request(request.url, data=data, method=request.method)
        for name, value in request.headers.items():
            req.add_header(name, value)

        deadline = time.monotonic() + request.timeout
        try:
            try:
                resp = opener.open(req, timeout=request.timeout)
            except urllib.error.HTTPError as err:
                # Non-2xx statuses are responses, not transport failures.
                body = _read_body(err, deadline) if err.fp is not None else ""
                headers = dict(err.headers.items()) if err.headers is not None else {}
                err.close()
                return HttpResponse(err.code, body, headers)
            with resp:
                body = _read_body(resp, deadline)
                return HttpResponse(resp.status, body, dict(resp.headers.items()))
        except TransportError:
            raise
        except (urllib.error.URLError, OSError, http.client.HTTPException, ValueError) as exc:
            if isinstance(exc, ValueError) and not isinstance(exc, (urllib.error.URLError,)):
                # Malformed URL (e.g. a bad setServiceUrl value).
                raise TransportError(3, "URL using bad/illegal format or missing URL: " + str(exc))
            errno, message = _classify(exc)
            raise TransportError(errno, message)
