"""python-dna example: ReplaceResourceRecordValue

Swap ONE value of a record set for another (the 'edit row' of a DNS panel).
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

result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
pprint(result, sort_dicts=False)

# Sample output:
# {'result': 'OK',
#  'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
