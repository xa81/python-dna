"""python-dna example: AddResourceRecord

Low-level: write a record set (POST). The gateway replaces an existing name + type,
so prefer add_resource_record_value() to append a value.
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

result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
pprint(result, sort_dicts=False)

# Sample output:
# {'result': 'OK',
#  'data': {'Name': 'www', 'Type': 'A', 'TTL': 300, 'Content': '192.0.2.5'}}
