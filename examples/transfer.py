"""python-dna example: Transfer

Start an incoming transfer with the domain's EPP/auth code. Contacts are never sent:
the registrar takes them over. A refusal (success: false) returns a TRANSFER_DOMAIN error.
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

result = dna.transfer("example.com", "Ab1!xyZ9", 1)
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
