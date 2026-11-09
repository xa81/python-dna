"""python-dna example: ValidateContact

Complete and normalise a contact the way the gateway expects it (local, no network):
missing fields get placeholders, names lose digits/punctuation, phone numbers are split
into number + country code, State falls back to City.
"""
import os
import sys
from pprint import pprint

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))  # run from a checkout

from domainnameapi import DomainNameAPI  # noqa: E402

# Credentials: your Reseller ID (UUID) + API Key from Panel -> API Settings
# (or set DNA_RESELLER_ID / DNA_API_KEY). Panel login credentials will NOT work.
RESELLER_ID = os.environ.get("DNA_RESELLER_ID", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
API_KEY = os.environ.get("DNA_API_KEY", "your-api-key")

dna = DomainNameAPI(RESELLER_ID, API_KEY)  # DomainNameAPI(RESELLER_ID, API_KEY, True) -> test (OTE) environment

result = dna.validate_contact({
    "FirstName": " Jo ",
    "Phone": "+1 (202) 555-0100",
    "Country": "Turkey",
    "City": "",
    "Fax": "0090 212 123 45 67",
})
pprint(result, sort_dicts=False)

# Sample output:
# {'FirstName': 'Jo',
#  'Phone': '12025550100',
#  'Country': 'TR',
#  'City': 'ISTANBUL',
#  'Fax': '2121234567',
#  'LastName': 'Isimyok',
#  'AddressLine1': 'Addres yok',
#  'State': 'ISTANBUL',
#  'ZipCode': '34000',
#  'PhoneCountryCode': '90',
#  'FaxCountryCode': '90'}
