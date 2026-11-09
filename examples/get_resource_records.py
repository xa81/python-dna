"""python-dna example: GetResourceRecords

DNS zone of a domain, one row per record value. Names come back fully qualified.
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

result = dna.get_resource_records("example.com")
pprint(result, sort_dicts=False)

# Sample output:
# {'result': 'OK',
#  'data': {'records': [{'Name': 'example.com.',
#                        'Type': 'A',
#                        'TTL': 3600,
#                        'Content': '192.0.2.1',
#                        'Disabled': False},
#                       {'Name': 'www.example.com.',
#                        'Type': 'CNAME',
#                        'TTL': 300,
#                        'Content': 'example.com.',
#                        'Disabled': False},
#                       {'Name': 'example.com.',
#                        'Type': 'MX',
#                        'TTL': 3600,
#                        'Content': '10 mx1.example.com.',
#                        'Disabled': False},
#                       {'Name': 'example.com.',
#                        'Type': 'MX',
#                        'TTL': 3600,
#                        'Content': '20 mx2.example.com.',
#                        'Disabled': True},
#                       {'Name': 'example.com.',
#                        'Type': 'TXT',
#                        'TTL': 3600,
#                        'Content': '"v=spf1 include:_spf.example.net ~all"',
#                        'Disabled': False},
#                       {'Name': 'empty.example.com.',
#                        'Type': 'AAAA',
#                        'TTL': 60,
#                        'Content': '',
#                        'Disabled': False}]}}
