"""python-dna example: GetTldList

TLD list with prices per period (registration, renew, transfer, restore ...).
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

result = dna.get_tld_list(100)
pprint(result, sort_dicts=False)

# Sample output:
# {'data': [{'id': 1,
#            'status': 'Active',
#            'maxchar': 63,
#            'maxperiod': 10,
#            'minchar': 1,
#            'minperiod': 1,
#            'tld': 'aero',
#            'pricing': {'registration': {'1': '44.9900',
#                                         '2': '94.9100',
#                                         '3': '144.8300'},
#                        'renew': {'1': '49.9200', '2': '99.8400'},
#                        'transfer': {'1': '44.9900'}},
#            'currencies': {'registration': 'USD', 'renew': 'USD', 'transfer': 'USD'}},
#           {'id': 2,
#            'status': 'Passive',
#            'maxchar': 50,
#            'maxperiod': 10,
#            'minchar': 2,
#            'minperiod': 1,
#            'tld': 'com.tr',
#            'pricing': {'registration': {'1': '15.5000', '2': '30.0000'},
#                        'renew': {'1': '15.5000'},
#                        'transfer': {'1': '0.0000'}},
#            'currencies': {'registration': 'TRY', 'renew': 'TRY', 'transfer': 'USD'}},
#           {'id': 3,
#            'status': 'Active',
#            'maxchar': 63,
#            'maxperiod': 10,
#            'minchar': 1,
#            'minperiod': 1,
#            'tld': 'xyz',
#            'pricing': {},
#            'currencies': {}}],
#  'result': 'OK'}
