"""python-dna example: GetContacts

Administrative, Billing, Registrant and Technical contacts of a domain.
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

result = dna.get_contacts("example.com")
pprint(result, sort_dicts=False)

# Sample output:
# {'data': {'contacts': {'Administrative': {'ID': 'DNA-A-2',
#                                           'Status': 'Active',
#                                           'AuthCode': '',
#                                           'FirstName': 'Grace',
#                                           'LastName': 'Hopper',
#                                           'Company': '',
#                                           'EMail': 'grace@example.com',
#                                           'Type': 'Administrative',
#                                           'Address': {'Line1': 'Example Street 2',
#                                                       'Line2': '',
#                                                       'Line3': '',
#                                                       'State': 'DC',
#                                                       'City': 'Washington',
#                                                       'Country': 'US',
#                                                       'ZipCode': '20001'},
#                                           'Phone': {'Phone': {'Number': '2025550100',
#                                                               'CountryCode': '1'},
#                                                     'Fax': {'Number': '2025550101',
#                                                             'CountryCode': '1'}},
#                                           'Additional': []},
#                        'Billing': {'ID': 'DNA-B-4',
#                                    'Status': 'Active',
#                                    'AuthCode': '',
#                                    'FirstName': 'Ada',
#                                    'LastName': 'Lovelace',
#                                    'Company': 'Example Ltd',
#                                    'EMail': 'billing@example.com',
#                                    'Type': 'Billing',
#                                    'Address': {'Line1': 'Example Street 1',
#                                                'Line2': '',
#                                                'Line3': '',
#                                                'State': 'Istanbul',
#                                                'City': 'Istanbul',
#                                                'Country': 'TR',
#                                                'ZipCode': '34000'},
#                                    'Phone': {'Phone': {'Number': '5551234567',
#                                                        'CountryCode': '90'},
#                                              'Fax': {'Number': '', 'CountryCode': ''}},
#                                    'Additional': []},
#                        'Registrant': {'ID': 'DNA-R-1',
#                                       'Status': 'Active',
#                                       'AuthCode': '',
#                                       'FirstName': 'Ada',
#                                       'LastName': 'Lovelace',
#                                       'Company': 'Example Ltd',
#                                       'EMail': 'ada@example.com',
#                                       'Type': 'Registrant',
#                                       'Address': {'Line1': 'Example Street 1',
#                                                   'Line2': '',
#                                                   'Line3': '',
#                                                   'State': 'Istanbul',
#                                                   'City': 'Istanbul',
#                                                   'Country': 'TR',
#                                                   'ZipCode': '34000'},
#                                       'Phone': {'Phone': {'Number': '5551234567',
#                                                           'CountryCode': '90'},
#                                                 'Fax': {'Number': '',
#                                                         'CountryCode': ''}},
#                                       'Additional': []},
#                        'Technical': {'ID': 'DNA-T-3',
#                                      'Status': 'Active',
#                                      'AuthCode': '',
#                                      'FirstName': 'Alan',
#                                      'LastName': 'Turing',
#                                      'Company': '',
#                                      'EMail': 'alan@example.com',
#                                      'Type': 'Technical',
#                                      'Address': {'Line1': 'Example Street 3',
#                                                  'Line2': '',
#                                                  'Line3': '',
#                                                  'State': '',
#                                                  'City': 'London',
#                                                  'Country': 'GB',
#                                                  'ZipCode': 'SW1A 1AA'},
#                                      'Phone': {'Phone': {'Number': '2071234567',
#                                                          'CountryCode': '44'},
#                                                'Fax': {'Number': '',
#                                                        'CountryCode': ''}},
#                                      'Additional': []}}},
#  'result': 'OK'}
