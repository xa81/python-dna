"""python-dna example: CheckAvailability

Availability and price of every domain + extension combination.
Returns a plain list on success, an error envelope on failure.
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

result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
pprint(result, sort_dicts=False)

# Sample output:
# [{'TLD': 'com',
#   'DomainName': 'dnaprobexyz123',
#   'Status': 'available',
#   'Command': 'create',
#   'Period': 1,
#   'IsFee': False,
#   'Price': '11.9900',
#   'Currency': 'USD',
#   'Reason': None},
#  {'TLD': 'net',
#   'DomainName': 'dnaprobexyz123',
#   'Status': 'available',
#   'Command': 'create',
#   'Period': 1,
#   'IsFee': False,
#   'Price': '13.9900',
#   'Currency': 'USD',
#   'Reason': None},
#  {'TLD': 'com',
#   'DomainName': 'google',
#   'Status': 'notavailable',
#   'Command': 'create',
#   'Period': 1,
#   'IsFee': False,
#   'Price': '11.9900',
#   'Currency': 'USD',
#   'Reason': 'Domain exists'},
#  {'TLD': 'net',
#   'DomainName': 'premium',
#   'Status': 'available',
#   'Command': 'create',
#   'Period': 1,
#   'IsFee': True,
#   'Price': '2500.0000',
#   'Currency': 'USD',
#   'Reason': None}]
