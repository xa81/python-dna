"""python-dna example: GetDetails

Full details of one domain: status, dates, nameservers, lock/privacy flags, child nameservers.
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

result = dna.get_details("example.com")
pprint(result, sort_dicts=False)

# Sample output:
# {'data': {'ID': 4321,
#           'Status': 'Active',
#           'DomainName': 'example.com',
#           'AuthCode': 'Ab1!xyZ9',
#           'LockStatus': 'true',
#           'PrivacyProtectionStatus': 'false',
#           'IsChildNameServer': 'true',
#           'Contacts': {'Billing': {'ID': 'DNA-B-4'},
#                        'Technical': {'ID': 'DNA-T-3'},
#                        'Administrative': {'ID': 'DNA-A-2'},
#                        'Registrant': {'ID': 'DNA-R-1'}},
#           'Dates': {'Start': '2024-03-15T10:20:30',
#                     'Expiration': '2027-03-15T10:20:30',
#                     'RemainingDays': 126},
#           'NameServers': ['ns1.example.net', 'ns2.example.net'],
#           'Additional': {'TRABISDOMAINCATEGORY': '1'},
#           'ChildNameServers': [{'ns': 'ns1.example.com', 'ip': '192.0.2.11'},
#                                {'ns': 'ns2.example.com', 'ip': ''}]},
#  'result': 'OK'}
