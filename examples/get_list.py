"""python-dna example: GetList

Domains in the reseller account.
Filters: PageNumber (0-based), PageSize, OrderColumn, OrderDirection, DomainName ...
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

result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
pprint(result, sort_dicts=False)

# Sample output:
# {'data': {'Domains': [{'ID': 11,
#                        'Status': 'ok',
#                        'DomainName': 'example.com',
#                        'AuthCode': '',
#                        'LockStatus': 'true',
#                        'PrivacyProtectionStatus': 'true',
#                        'IsChildNameServer': 'false',
#                        'Contacts': {'Billing': {'ID': ''},
#                                     'Technical': {'ID': ''},
#                                     'Administrative': {'ID': ''},
#                                     'Registrant': {'ID': ''}},
#                        'Dates': {'Start': '2024-03-15T10:20:30',
#                                  'Expiration': '2027-03-15T10:20:30',
#                                  'RemainingDays': 126},
#                        'NameServers': ['ns1.example.net', 'ns2.example.net'],
#                        'Additional': [],
#                        'ChildNameServers': []},
#                       {'ID': 12,
#                        'Status': 'Deleted',
#                        'DomainName': 'example.net',
#                        'AuthCode': '',
#                        'LockStatus': 'false',
#                        'PrivacyProtectionStatus': 'false',
#                        'IsChildNameServer': 'false',
#                        'Contacts': {'Billing': {'ID': ''},
#                                     'Technical': {'ID': ''},
#                                     'Administrative': {'ID': ''},
#                                     'Registrant': {'ID': ''}},
#                        'Dates': {'Start': '2023-01-01T00:00:00',
#                                  'Expiration': '2026-01-01T00:00:00',
#                                  'RemainingDays': 0},
#                        'NameServers': [],
#                        'Additional': [],
#                        'ChildNameServers': []},
#                       {'ID': 13,
#                        'Status': 'WaitingForRegistration',
#                        'DomainName': 'example.org',
#                        'AuthCode': '',
#                        'LockStatus': 'false',
#                        'PrivacyProtectionStatus': 'false',
#                        'IsChildNameServer': 'false',
#                        'Contacts': {'Billing': {'ID': ''},
#                                     'Technical': {'ID': ''},
#                                     'Administrative': {'ID': ''},
#                                     'Registrant': {'ID': ''}},
#                        'Dates': {'Start': '', 'Expiration': '', 'RemainingDays': 0},
#                        'NameServers': [],
#                        'Additional': [],
#                        'ChildNameServers': []}]},
#  'result': 'OK',
#  'TotalCount': 3}
