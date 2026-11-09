"""python-dna example: RegisterWithContactInfo-TR

Register a .tr domain. .tr needs TRABIS attributes (7th argument):

* individual owner: TRABISDOMAINCATEGORY = 1 (Owner) + TRABISCITIZENID (T.C. identity number)
* company owner:    TRABISDOMAINCATEGORY = 0 (Corporate) + TRABISTAXOFFICE + TRABISTAXNUMBER

Legacy keys (the TRABISCITIZIENID spelling, TRABISNAMESURNAME, TRABISCOUNTRYID ...) are
accepted and normalised to the REST schema; unsupported ones are dropped.
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

contact = {
    "FirstName": "Ahmet",
    "LastName": "Yilmaz",
    "Company": "",
    "EMail": "ahmet.yilmaz@example.com",
    "AddressLine1": "Ornek Sokak No: 123",
    "AddressLine2": "Daire 4",
    "AddressLine3": "",
    "City": "Istanbul",
    "Country": "TR",
    "Fax": "2121234567",
    "FaxCountryCode": "90",
    "Phone": "5551234567",
    "PhoneCountryCode": 90,
    "Type": "Contact",
    "ZipCode": "34000",
    "State": "Istanbul",
}

contacts = {
    "Administrative": contact,
    "Billing": contact,
    "Technical": contact,
    "Registrant": contact,
}

individual = {
    "TRABISDOMAINCATEGORY": 1,
    "TRABISCITIZIENID": "11111111111",
    "TRABISNAMESURNAME": "Ahmet Yilmaz",
    "TRABISCOUNTRYID": "215",
    "TRABISCITYID": "34",
}

commercial = {
    "TRABISDOMAINCATEGORY": 0,
    "TRABISORGANIZATION": "Example Ltd. Sti.",
    "TRABISTAXOFFICE": "Istanbul VD",
    "TRABISTAXNUMBER": "1234567890",
}

result = dna.register_with_contact_info(
    "example.com.tr",
    1,
    contacts,
    ["ns1.example.com", "ns2.example.com"],
    True,
    False,
    individual,  # or commercial
)
pprint(result, sort_dicts=False)

# Sample output:
# {'data': {'ID': 0,
#           'Status': 'Active',
#           'DomainName': '',
#           'AuthCode': '',
#           'LockStatus': 'false',
#           'PrivacyProtectionStatus': 'false',
#           'IsChildNameServer': 'false',
#           'Contacts': {'Billing': {'ID': 0},
#                        'Technical': {'ID': 0},
#                        'Administrative': {'ID': 0},
#                        'Registrant': {'ID': 0}},
#           'Dates': {'Start': '',
#                     'Expiration': '2027-11-09T12:00:00',
#                     'RemainingDays': 366},
#           'NameServers': [],
#           'Additional': [],
#           'ChildNameServers': []},
#  'result': 'OK'}
