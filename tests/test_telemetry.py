"""Telemetry: DSN handling, masking, ignored errors, payload shape."""

import json
import unittest

from tests.support import API_KEY, RESELLER, FakeTransport

from domainnameapi import DomainNameAPI
from domainnameapi import telemetry as tm

DSN = "https://publickey:secret@sentry.example.test/42"


def client(transport, dsn=DSN, minimal=False):
    api = DomainNameAPI(RESELLER, API_KEY, transport=transport, sentry_dsn=dsn)
    tel = api.client.telemetry
    tel.synchronous = True
    sent = []
    tel.poster = lambda url, payload, auth: sent.append((url, json.loads(payload), auth))
    api.set_telemetry_minimal(minimal)
    return api, sent


class DsnTest(unittest.TestCase):
    def test_default_dsn_is_empty_noop(self):
        self.assertEqual(tm.DEFAULT_SENTRY_DSN, "")
        api, sent = client(FakeTransport().push(500, '{"error":{"message":"boom"}}'), dsn=None)
        api.get_details("example.com")
        self.assertEqual(sent, [])

    def test_parse_dsn(self):
        p = tm.parse_dsn(DSN)
        self.assertEqual(p["store_url"], "https://sentry.example.test/api/42/store/")
        self.assertEqual((p["public_key"], p["secret_key"]), ("publickey", "secret"))
        self.assertIsNone(tm.parse_dsn(""))
        self.assertIsNone(tm.parse_dsn("not a dsn"))


class MaskTest(unittest.TestCase):
    def test_only_credentials_are_masked(self):
        data = {
            "url": "https://api/x",
            "payload": {
                "domainName": "example.com",
                "authCode": "Ab1!",
                "eppCode": "",
                "apiKey": "k",
                "api-key": "k",
                "password": "p",
                "token": None,
                "contacts": [{"firstName": "Ada", "eMail": "ada@example.com"}],
            },
        }
        out = tm.telemetry_mask(data)
        p = out["payload"]
        self.assertEqual(p["authCode"], "***")
        self.assertEqual(p["eppCode"], "")
        self.assertEqual(p["apiKey"], "***")
        self.assertEqual(p["api-key"], "***")
        self.assertEqual(p["password"], "***")
        self.assertIsNone(p["token"])
        self.assertEqual(p["domainName"], "example.com")
        self.assertEqual(p["contacts"][0]["eMail"], "ada@example.com")
        self.assertEqual(out["url"], "https://api/x")


class ErrorEventTest(unittest.TestCase):
    def test_error_event(self):
        api, sent = client(FakeTransport().push(500, '{"error":{"message":"Registry exploded at 10.0.0.1"}}'))
        api.transfer("example.com", "SECRET-EPP", 1)
        self.assertEqual(len(sent), 1)
        url, ev, auth = sent[0]
        self.assertEqual(url, "https://sentry.example.test/api/42/store/")
        self.assertIn("sentry_key=publickey", auth)
        self.assertIn("sentry_secret=secret", auth)
        self.assertIn("sentry_client=DomainNameAPI-Python/1.0.0", auth)
        self.assertEqual(ev["tags"]["application"], "DomainNameAPI-Python")
        self.assertEqual(ev["tags"]["library_version"], "1.0.0")
        self.assertEqual(ev["release"], "1.0.0")
        self.assertEqual(ev["tags"]["api_code"], "API_500")
        self.assertEqual(ev["tags"]["domain"], "example.com")
        self.assertEqual(ev["tags"]["reseller"], RESELLER)
        self.assertEqual(ev["tags"]["operation"], "request:POST domains/transfer")
        self.assertEqual(ev["tags"]["ip_value"], "10.0.0.1")
        self.assertEqual(ev["message"]["formatted"], "API_500: Registry exploded at {ip}")
        self.assertEqual(ev["extra"]["request_data"]["payload"]["authCode"], "***")
        self.assertEqual(ev["extra"]["original_message"], "Registry exploded at 10.0.0.1")
        self.assertEqual(ev["environment"], "production")
        self.assertNotIn(API_KEY, json.dumps(ev))
        self.assertNotIn("SECRET-EPP", json.dumps(ev))

    def test_ignored_errors_are_not_sent(self):
        api, sent = client(FakeTransport().push(404, '{"error":{"message":"Domain not found"}}'))
        api.get_details("example.com")
        self.assertEqual(sent, [])

    def test_forward_not_set_is_not_sent(self):
        api, sent = client(FakeTransport().push(404, '{"error":{"message":"Redirect information not found"}}'))
        self.assertEqual(api.get_forwarding("example.com")["data"]["Enabled"], False)
        self.assertEqual(sent, [])

    def test_disabled(self):
        api, sent = client(FakeTransport().push(500, '{"error":{"message":"boom"}}'))
        api.set_error_reporting_enabled(False)
        api.get_details("example.com")
        self.assertEqual(sent, [])

    def test_minimal_payload(self):
        api, sent = client(FakeTransport().push(500, '{"error":{"message":"boom"}}'), minimal=True)
        api.get_details("example.com")
        ev = sent[0][1]
        self.assertNotIn("domain", ev["tags"])
        self.assertNotIn("ip_address", ev["tags"])
        self.assertNotIn("vhost_user", ev["tags"])
        self.assertNotIn("url", ev["tags"])
        self.assertEqual(ev["extra"]["request_data"], {"method": "GET", "endpoint": "/api/v1/domains/info"})
        self.assertEqual(ev["extra"]["response_data"], {"http_code": 500})

    def test_telemetry_never_raises(self):
        api, _ = client(FakeTransport().push(500, '{"error":{"message":"boom"}}'))

        def broken(*a):
            raise RuntimeError("sentry down")

        api.client.telemetry.poster = broken
        self.assertEqual(api.get_details("example.com")["result"], "ERROR")

    def test_ote_environment(self):
        api, sent = client(FakeTransport().push(500, '{"error":{"message":"boom"}}'))
        api.set_service_url("https://ote.domainresellerapi.com/api/v1")
        api.get_details("example.com")
        self.assertEqual(sent[0][1]["environment"], "ote")


class PerformanceEventTest(unittest.TestCase):
    def test_slow_success_is_sampled(self):
        api, sent = client(FakeTransport().push(200, '{"id":1}'))
        api.client.telemetry.should_sample = lambda duration: True
        api.get_details("example.com")
        self.assertEqual(len(sent), 1)
        ev = sent[0][1]
        self.assertEqual(ev["type"], "transaction")
        self.assertEqual(ev["transaction"], "API.request:GET domains/info")
        self.assertEqual(ev["contexts"]["trace"]["status"], "ok")
        self.assertEqual(ev["spans"][0]["description"], "GET https://api.domainresellerapi.com")
        self.assertEqual(ev["spans"][0]["data"]["http.response.status_code"], 200)
        self.assertEqual(ev["tags"]["application"], "DomainNameAPI-Python")

    def test_classification_and_status_mapping(self):
        self.assertEqual(tm.map_trace_status(False, "API_404"), "not_found")
        self.assertEqual(tm.map_trace_status(False, "API_503"), "internal_error")
        self.assertEqual(tm.map_trace_status(False, "API_422"), "invalid_argument")
        self.assertEqual(tm.map_trace_status(False, None), "unknown")
        self.assertEqual(tm.map_trace_status(True, None), "ok")


if __name__ == "__main__":
    unittest.main()
