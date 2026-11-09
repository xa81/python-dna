"""Error mapping of non-2xx responses (DNARest::request())."""

import unittest

from tests.support import API_KEY, RESELLER, FakeTransport

from domainnameapi import DomainNameAPI


def call(status, body):
    api = DomainNameAPI(RESELLER, API_KEY, transport=FakeTransport().push(status, body))
    api.set_error_reporting_enabled(False)
    return api.get_details("example.com")["error"]


class ErrorMappingTest(unittest.TestCase):
    def test_message_from_top_level(self):
        e = call(404, '{"code":"X","message":"Domain not found","details":"nope"}')
        self.assertEqual(e, {"Code": "API_404", "Message": "Domain not found", "Details": "nope"})

    def test_message_from_error_object(self):
        e = call(400, '{"error":{"code":"C","message":"Bad thing","details":"why"}}')
        self.assertEqual(e, {"Code": "API_400", "Message": "Bad thing", "Details": "why"})

    def test_raw_body_when_not_json(self):
        e = call(503, "upstream down")
        self.assertEqual(e, {"Code": "API_503", "Message": "upstream down", "Details": "upstream down"})

    def test_empty_body_gets_status_message(self):
        self.assertEqual(call(429, ""), {"Code": "API_429", "Message": "HTTP 429 - Too Many Requests",
                                         "Details": "HTTP 429 - Too Many Requests"})
        self.assertEqual(call(418, "")["Message"], "HTTP 418 - Client Error")
        self.assertEqual(call(599, "")["Message"], "HTTP 599 - Server Error")

    def test_boilerplate_prefers_details(self):
        e = call(500, '{"error":{"code":"Dna.X:1","message":"Exception of type \'Volo.Abp.BusinessException\' was thrown.","details":"Dna Host is linked"}}')
        self.assertEqual(e["Message"], "Host is linked")

    def test_boilerplate_without_details_is_synthesised(self):
        e = call(500, '{"error":{"code":"Dna.X:1","message":"Exception of type \'A\' was thrown.","details":null}}')
        self.assertEqual(e["Message"], "The operation could not be completed by the registry (error: Dna.X:1). "
                                       "Please try again or contact support.")

    def test_message_equal_to_code(self):
        e = call(500, '{"error":{"code":"Dna.DomainService:Dns:10024","message":"Dna.DomainService:Dns:10024","details":""}}')
        self.assertIn("(error: Dna.DomainService:Dns:10024)", e["Message"])

    def test_message_equal_to_code_without_details_uses_raw_body(self):
        # php-dna parity: missing details fall back to the raw body, which then
        # replaces the bare-code message.
        body = '{"error":{"code":"Dna.DomainService:Dns:10024","message":"Dna.DomainService:Dns:10024"}}'
        self.assertEqual(call(500, body)["Message"], body)

    def test_validation_errors_are_flattened(self):
        body = ('{"error":{"message":"Validation failed.","validationErrors":['
                '{"members":["$.contacts[0].administrativeContact.postalCode","$.technicalContact.postalCode"],'
                '"message":"\'PostalCode\' is required"},'
                '{"members":["$.tldAttributes.TRABISCOUNTRYID"]},'
                '{"message":"Plain message"},'
                '"string entry",'
                '{"message":"Plain message"}]}}')
        e = call(400, body)
        self.assertEqual(e["Message"], "Validation failed.")
        self.assertEqual(e["Details"], "Contacts Admin PostalCode, Tech PostalCode - 'PostalCode' is required"
                                       " | TldAttributes TRABISCOUNTRYID | Plain message | string entry")

    def test_redirect_is_credentials(self):
        e = call(302, "")
        self.assertEqual(e["Code"], "API_302")
        self.assertEqual(e["Message"], "Invalid API credentials")
        self.assertEqual(e["Details"], "Authentication failed. Check your API key and reseller ID.")

    def test_success_with_empty_body_is_response_error(self):
        api = DomainNameAPI(RESELLER, API_KEY, transport=FakeTransport().push(200, ""))
        api.set_error_reporting_enabled(False)
        out = api.get_details("example.com")
        self.assertEqual(out["error"]["Code"], "RESPONSE")
        self.assertEqual(out["error"]["Message"], "Invalid response received from server! Response is empty.")

    def test_get_forwarding_not_found_is_ok(self):
        api = DomainNameAPI(RESELLER, API_KEY, transport=FakeTransport().push(404, '{"error":{"message":"Redirect information not found"}}'))
        api.set_error_reporting_enabled(False)
        self.assertEqual(api.get_forwarding("example.com"),
                         {"result": "OK", "data": {"Enabled": False, "RedirectAddress": "", "ForwardType": ""}})


if __name__ == "__main__":
    unittest.main()
