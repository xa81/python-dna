"""python-dna example: GetResellerDetails

Reseller account details: ID, name and balances (USD and TL).
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

result = dna.get_reseller_details()
pprint(result, sort_dicts=False)

# Sample output:
# {'result': 'OK',
#  'id': '00000000-0000-4000-8000-000000000001',
#  'active': True,
#  'name': 'example-reseller',
#  'balance': '601.64',
#  'currency': 'USD',
#  'symbol': '$',
#  'balances': [{'balance': '601.64', 'currency': 'USD', 'symbol': '$'},
#               {'balance': '1250.5', 'currency': 'TL', 'symbol': 'TL'}]}
