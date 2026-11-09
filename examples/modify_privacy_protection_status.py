"""python-dna example: ModifyPrivacyProtectionStatus

Turn WHOIS privacy protection on (True) or off (False). 1, "1", "on", "true" and "yes"
also mean on; anything else means off. The reason argument is not sent to the gateway.
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

result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
pprint(result, sort_dicts=False)

# Sample output:
# {'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
