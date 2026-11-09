"""HTTP layer: headers, query strings, JSON bodies, transport failures."""

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from tests.support import API_KEY, RESELLER, FakeTransport, split_url

from domainnameapi import URL_OTE, URL_PROD, USER_AGENT, DomainNameAPI
from domainnameapi.transport import HttpRequest, TransportError, UrllibTransport


def make(transport, test_mode=False):
    api = DomainNameAPI(RESELLER, API_KEY, test_mode, transport=transport)
    api.set_error_reporting_enabled(False)
    api.zone_min_interval = 0
    return api


class HeadersAndUrlTest(unittest.TestCase):
    def test_headers_and_user_agent(self):
        t = FakeTransport().push(200, '{"resellerId":"r"}')
        make(t).get_reseller_details()
        h = t.requests[0].headers
        self.assertEqual(h["X-API-KEY"], API_KEY)
        self.assertEqual(h["__reseller"], RESELLER)
        self.assertEqual(h["Content-Type"], "application/json")
        self.assertEqual(h["Accept"], "application/json")
        self.assertEqual(h["User-Agent"], USER_AGENT)
        self.assertEqual(USER_AGENT, "DomainNameAPI-Python/1.0.0")

    def test_base_urls(self):
        self.assertEqual(make(FakeTransport()).get_service_url(), URL_PROD)
        self.assertEqual(make(FakeTransport(), True).get_service_url(), URL_OTE)
        self.assertEqual(make(FakeTransport(), "yes").get_service_url(), URL_OTE)
        self.assertEqual(make(FakeTransport(), " On ").get_service_url(), URL_OTE)
        self.assertEqual(make(FakeTransport(), "false").get_service_url(), URL_PROD)
        self.assertEqual(make(FakeTransport(), "off").get_service_url(), URL_PROD)
        self.assertEqual(make(FakeTransport(), "0").get_service_url(), URL_PROD)
        self.assertEqual(make(FakeTransport(), "").get_service_url(), URL_PROD)

    def test_credentials_are_trimmed(self):
        t = FakeTransport().push(200, "{}")
        api = DomainNameAPI("  %s\n" % RESELLER, "\t%s  " % API_KEY, transport=t)
        api.set_error_reporting_enabled(False)
        api.get_details("example.com")
        self.assertEqual(t.requests[0].headers["__reseller"], RESELLER)
        self.assertEqual(t.requests[0].headers["X-API-KEY"], API_KEY)

    def test_set_service_url(self):
        t = FakeTransport().push(200, "{}")
        api = make(t)
        api.set_service_url("http://127.0.0.1:9/api/v1")
        api.get_details("example.com")
        self.assertTrue(t.requests[0].url.startswith("http://127.0.0.1:9/api/v1/domains/info?"))

    def test_get_query_uses_php_semantics(self):
        t = FakeTransport().push(200, '{"items":[],"totalCount":0}')
        make(t).get_list({"Flag": True, "Off": False, "Gone": None, "Name": "a b~c/d"})
        url = t.requests[0].url
        self.assertIn("Flag=1", url)
        self.assertIn("Off=0", url)
        self.assertNotIn("Gone", url)
        self.assertIn("Name=a+b%7Ec%2Fd", url)
        self.assertIsNone(t.requests[0].body)

    def test_nested_query_arrays(self):
        t = FakeTransport().push(200, '{"items":[]}')
        make(t).get_list({"Ids": [3, 4]})
        _, query = split_url(t.requests[0].url)
        self.assertEqual(query["Ids"], {"0": "3", "1": "4"})

    def test_transfer_never_sends_contacts(self):
        t = FakeTransport().push(200, '{"status":"Active","expirationDate":"2030-01-01T00:00:00"}')
        make(t).transfer("example.com", "code", 1)
        self.assertEqual(json.loads(t.requests[0].body)["contacts"], [])
        with self.assertRaises(TypeError):
            make(FakeTransport()).transfer("example.com", "code", 1, {"Registrant": {}})

    def test_privacy_status_parsing(self):
        for value, expected in ((True, True), (1, True), ("on", True), (" yes ", True), ("off", False),
                                (0, False), (None, False), ("", False)):
            t = FakeTransport().push(200, "")
            out = make(t).modify_privacy_protection_status("example.com", value, "ignored")
            body = json.loads(t.requests[0].body)
            self.assertEqual(body, {"domainName": "example.com", "privacyStatus": expected}, repr(value))
            self.assertIs(out["data"]["PrivacyProtectionStatus"], expected)

    def test_post_sends_json_body(self):
        t = FakeTransport().push(200, "{}")
        make(t).enable_theft_protection_lock("example.com")
        req = t.requests[0]
        self.assertEqual(req.method, "POST")
        self.assertEqual(json.loads(req.body), {"domainName": "example.com"})

    def test_zone_post_keeps_query_in_endpoint(self):
        t = FakeTransport().push(200, "").push(200, "")
        api = make(t)
        api.add_resource_record("example.com", "www", "A", "192.0.2.1")
        path, query = split_url(t.requests[0].url)
        self.assertEqual((path, query), ("domains/zones", {"domainName": "example.com"}))
        self.assertEqual(api.get_last_function(), "request:POST domains/zones/apply")
        self.assertEqual(t.requests[1].body, "[]")

    def test_empty_tld_attributes_are_an_object(self):
        t = FakeTransport().push(200, '{"expirationDate":"2030-01-01T00:00:00"}')
        make(t).register_with_contact_info("example.com", 1, {"Registrant": {}})
        self.assertIn('"tldAttributes":{}', t.requests[0].body)

    def test_timeouts_and_ssl_flag_are_passed(self):
        t = FakeTransport().push(200, "{}")
        api = make(t)
        api.set_ssl_verification(False)
        api.get_details("example.com")
        req = t.requests[0]
        self.assertEqual((req.timeout, req.connect_timeout, req.verify_ssl), (30, 10, False))

    def test_diagnostics(self):
        t = FakeTransport().push(200, '{"id": 7, "status": "Active"}')
        api = make(t)
        api.get_details("example.com")
        self.assertEqual(api.get_request_data()["method"], "GET")
        self.assertEqual(api.get_request_data()["payload"], {"DomainName": "example.com"})
        self.assertEqual(api.get_response_data(), {"id": 7, "status": "Active"})
        self.assertEqual(api.get_parsed_response_data(), {"id": 7, "status": "Active"})
        self.assertEqual(api.get_response_headers()["http_code"], 200)
        self.assertEqual(api.get_last_function(), "request:GET domains/info")


class TransportFailureTest(unittest.TestCase):
    def test_timeout_is_an_error(self):
        t = FakeTransport().push_error(28, "Operation timed out after 30001 milliseconds")
        api = make(t)
        out = api.modify_name_server("example.com", ["ns1.example.com"])
        self.assertEqual(out["result"], "ERROR")
        self.assertEqual(out["error"]["Code"], "CURL_28")
        self.assertNotIn("GatewayCode", out["error"])
        self.assertTrue(out["error"]["Message"].startswith(
            "Could not reach the DomainNameAPI service: the connection timed out. ("))
        self.assertEqual(api.get_parsed_response_data()["Code"], "CURL_28")
        self.assertEqual(api.get_response_data(), {"raw_response": False})

    def test_dns_failure_is_an_error(self):
        t = FakeTransport().push_error(6, "Could not resolve host: api.example")
        out = make(t).enable_theft_protection_lock("example.com")
        self.assertEqual(out["result"], "ERROR")
        self.assertEqual(out["error"]["Code"], "CURL_6")
        self.assertEqual(out["error"]["Message"], "Curl error during request: Could not resolve host: api.example")

    def test_balance_envelope_on_failure(self):
        t = FakeTransport().push_error(7, "Failed to connect")
        out = make(t).get_current_balance("EUR")
        self.assertEqual(out["OperationResult"], "FAILED")
        self.assertEqual(out["ErrorCode"], "CURL_7")
        self.assertEqual(out["CurrencySymbol"], "€")


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path.startswith("/redirect"):
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()
            return
        if self.path.startswith("/slow"):
            import time
            time.sleep(1.5)
        body = json.dumps({"ua": self.headers.get("User-Agent"), "key": self.headers.get("X-API-KEY")}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class UrllibTransportTest(unittest.TestCase):
    """Real sockets against a local server (no external network)."""

    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), _Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def url(self, path):
        return "http://127.0.0.1:%d%s" % (self.port, path)

    def test_ok(self):
        resp = UrllibTransport().send(HttpRequest("GET", self.url("/ok"), {"User-Agent": USER_AGENT, "X-API-KEY": "k"}))
        self.assertEqual(resp.status, 200)
        self.assertEqual(json.loads(resp.body), {"ua": USER_AGENT, "key": "k"})

    def test_redirect_is_not_followed(self):
        resp = UrllibTransport().send(HttpRequest("GET", self.url("/redirect"), {}))
        self.assertEqual(resp.status, 302)

    def test_redirect_maps_to_credentials_error(self):
        api = DomainNameAPI(RESELLER, API_KEY)
        api.set_error_reporting_enabled(False)
        api.set_service_url(self.url("/redirect"))
        out = api.get_details("example.com")
        self.assertEqual(out["error"]["Code"], "API_302")
        self.assertEqual(out["error"]["Message"], "Invalid API credentials")

    def test_timeout(self):
        with self.assertRaises(TransportError) as ctx:
            UrllibTransport().send(HttpRequest("GET", self.url("/slow"), {}, timeout=0.3, connect_timeout=0.3))
        self.assertEqual(ctx.exception.errno, 28)

    def test_connection_refused(self):
        with self.assertRaises(TransportError) as ctx:
            UrllibTransport().send(HttpRequest("GET", "http://127.0.0.1:1/x", {}, timeout=2, connect_timeout=2))
        self.assertEqual(ctx.exception.errno, 7)


if __name__ == "__main__":
    unittest.main()
