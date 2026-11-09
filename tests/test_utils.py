"""Utilities without network: is_tr_tld, validate_contact, PHP semantics helpers."""

import unittest

from tests.support import FakeTransport

from domainnameapi import DomainNameAPI, DomainNameApi, VERSION, __version__
from domainnameapi import _php as php


def api():
    a = DomainNameAPI("r", "k", transport=FakeTransport())
    a.set_error_reporting_enabled(False)
    return a


class FacadeTest(unittest.TestCase):
    def test_version(self):
        self.assertEqual(VERSION, "1.0.0")
        self.assertEqual(__version__, "1.0.0")
        self.assertIs(DomainNameApi, DomainNameAPI)

    def test_php_style_aliases(self):
        a = api()
        self.assertTrue(a.isTrTLD("example.com.tr"))
        self.assertTrue(a.IsTrTLD("example.com.tr"))
        self.assertEqual(a.GetServiceUrl(), a.get_service_url())
        with self.assertRaises(AttributeError):
            a.NoSuchMethod()

    def test_set_resource_record_set_requires_a_list(self):
        with self.assertRaises(TypeError):
            api().set_resource_record_set("example.com", "www", "A", "1.2.3.4")


class IsTrTldTest(unittest.TestCase):
    def test_cases(self):
        a = api()
        self.assertTrue(a.is_tr_tld("example.com.tr"))
        self.assertTrue(a.is_tr_tld("EXAMPLE.TR"))
        self.assertFalse(a.is_tr_tld("example.com"))
        self.assertFalse(a.is_tr_tld("tr"))
        self.assertFalse(a.is_tr_tld("example.tr "))
        self.assertFalse(a.is_tr_tld("example.trx"))


class ValidateContactTest(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(api().validate_contact({}), {
            "FirstName": "Isimyok",
            "LastName": "Isimyok",
            "AddressLine1": "Addres yok",
            "City": "ISTANBUL",
            "State": "ISTANBUL",
            "Country": "TR",
            "ZipCode": "34000",
            "Phone": "5555555555",
            "PhoneCountryCode": "90",
            "Fax": "",
            "FaxCountryCode": "",
        })

    def test_messy_contact(self):
        out = api().validate_contact({
            "FirstName": "  Jane 3rd ",
            "LastName": "",
            "City": "Izmir",
            "State": "",
            "Country": "Türkiye",
            "Phone": "+90 (532) 374 33 88",
            "PhoneCountryCode": "",
            "Fax": "0212 000 00 00",
            "EMail": "jane@example.com",
        })
        self.assertEqual(out["FirstName"], "Jane rd")
        self.assertEqual(out["LastName"], "Jane rd")
        self.assertEqual(out["State"], "Izmir")
        self.assertEqual(out["Country"], "TR")
        self.assertEqual((out["Phone"], out["PhoneCountryCode"]), ("5323743388", "90"))
        self.assertEqual((out["Fax"], out["FaxCountryCode"]), ("2120000000", "90"))
        self.assertEqual(out["EMail"], "jane@example.com")

    def test_unicode_names_survive(self):
        out = api().validate_contact({"FirstName": "Ömer", "LastName": "Çelik-O'Neil"})
        self.assertEqual((out["FirstName"], out["LastName"]), ("Ömer", "Çelik-O'Neil"))

    def test_original_types_are_kept(self):
        out = api().validate_contact({"ZipCode": 34000, "AddressLine1": 7})
        self.assertEqual(out["ZipCode"], 34000)
        self.assertEqual(out["AddressLine1"], 7)


class PhpSemanticsTest(unittest.TestCase):
    def test_empty_and_casts(self):
        for v in (None, False, 0, 0.0, "", "0", [], {}):
            self.assertTrue(php.empty(v), repr(v))
        for v in ("0.0", " ", "a", 1, [0], True):
            self.assertFalse(php.empty(v), repr(v))
        self.assertEqual(php.intval("12abc"), 12)
        self.assertEqual(php.intval("1e3"), 1000)
        self.assertEqual(php.intval(" 7"), 7)
        self.assertEqual(php.intval("x"), 0)
        self.assertEqual(php.intval("9999999999999999999"), 9223372036854775807)
        self.assertEqual(php.floatval("1234.567abc"), 1234.567)
        self.assertEqual(php.strval(True), "1")
        self.assertEqual(php.strval(False), "")
        self.assertEqual(php.strval(500.0), "500")
        self.assertEqual(php.strval(1 / 3), "0.33333333333333")
        self.assertEqual(php.strval(1e15), "1.0E+15")
        self.assertEqual(php.strval(1.5e-7), "1.5E-7")

    def test_is_numeric(self):
        for v in (1, 1.5, "1", " 1", "1 ", "-1.5e3", ".5"):
            self.assertTrue(php.is_numeric(v), repr(v))
        for v in (True, "", "abc", "0x1A", ".", None, [1]):
            self.assertFalse(php.is_numeric(v), repr(v))

    def test_number_format(self):
        self.assertEqual(php.number_format(11.99, 4), "11.9900")
        self.assertEqual(php.number_format(1.005, 2), "1.01")
        self.assertEqual(php.number_format(2.675, 2), "2.68")
        self.assertEqual(php.number_format(-1.5, 0), "-2")
        self.assertEqual(php.number_format(0, 2), "0.00")

    def test_strings_are_ascii_case_mapped(self):
        self.assertEqual(php.strtolower("TÜRKİYE"), "tÜrkİye")
        self.assertEqual(php.strtoupper("türk"), "TüRK")
        self.assertEqual(php.trim(" x  \n"), " x ")

    def test_http_build_query(self):
        self.assertEqual(php.http_build_query({"a": True, "b": False, "c": None, "d": "x y~/"}),
                         "a=1&b=0&d=x+y%7E%2F")
        self.assertEqual(php.http_build_query({"e": [1, {"k": 2}]}), "e%5B0%5D=1&e%5B1%5D%5Bk%5D=2")

    def test_json_encode(self):
        self.assertEqual(php.json_encode({}), "[]")
        self.assertEqual(php.json_encode(php.JsonObject()), "{}")
        self.assertEqual(php.json_encode({"u": "/é"}), '{"u":"\\/\\u00e9"}')

    def test_dates(self):
        self.assertEqual(php.format_timestamp(php.strtotime("2024-03-15T10:20:30")), "2024-03-15T10:20:30")
        self.assertEqual(php.format_timestamp(php.strtotime("0001-01-01T00:00:00")), "0001-01-01T00:00:00")
        self.assertEqual(php.format_timestamp(php.strtotime("2024-03-15T10:20:30+03:00")), "2024-03-15T07:20:30")
        self.assertEqual(php.format_timestamp(php.strtotime("2024-02-30")), "2024-03-01T00:00:00")
        self.assertIsNone(php.strtotime("not-a-date"))

    def test_get(self):
        data = {"a": {"0": "x", "b": None}, "l": [1, 2]}
        self.assertEqual(php.get(data, "a", 0), "x")
        self.assertIsNone(php.get(data, "a", "b", "c"))
        self.assertEqual(php.get(data, "l", 1), 2)
        self.assertIsNone(php.get("string", "a"))


if __name__ == "__main__":
    unittest.main()
