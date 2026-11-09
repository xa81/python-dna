<div align="center">
  <a href="README-TR.md"   >   TR <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/TR.png" alt="TR" height="20" /></a>
  <a href="README.md"> | EN <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/US.png" alt="EN" height="20" /></a>
   <a href="README-DE.md"> | DE <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/DE.png" alt="DE" height="20" /></a>
  <a href="README-SA.md"> | SA <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/SA.png" alt="AR" height="20" /></a>
  <a href="README-NL.md"> | NL <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/NL.png" alt="NL" height="20" /></a>
  <a href="README-AZ.md"> | AZ <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/AZ.png" alt="AZ" height="20" /></a>
  <a href="README-CN.md"> | CN <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/CN.png" alt="CN" height="20" /></a>
  <a href="README-FR.md"> | FR <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/FR.png" alt="FR" height="20" /></a>
  <a href="README-IT.md"> | IT <img style="padding-top: 8px" src="https://raw.githubusercontent.com/yammadev/flag-icons/master/png/IT.png" alt="IT" height="20" /></a>
</div>


# python-dna: DomainNameAPI client for Python

Python client for the [DomainNameAPI](https://www.domainnameapi.com) reseller REST API: search, register,
transfer and renew domains, manage contacts, nameservers, child nameservers, DNS zones and URL forwarding.
It is a faithful port of [php-dna](https://github.com/domainreseller/php-dna): same methods, same requests,
same return values, verified against php-dna's conformance fixtures.

## 📦 Download — always use Releases!

⬇️ **Get the latest tested version here: https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ Do **not** use the green **Code → Download ZIP** button — that downloads the raw development branch. Release packages are versioned, tested and production-ready.

## Installation and Integration Guide

### Minimum Requirements

- Python 3.8 or higher (3.12 recommended)
- No third-party packages: the library only uses the Python standard library (`urllib`, `json`, `ssl`).

### A) Install with pip

```bash
pip install domainnameapi
```

### B) Install a release package

Download the wheel (`domainnameapi-1.0.0-py3-none-any.whl`) or the source archive from the
[latest release](https://github.com/domainreseller/python-dna/releases/latest) and install it:

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### C) Use the source directly

Copy the `src/domainnameapi` folder next to your code (or add `src` to `PYTHONPATH`) and import it.
The [examples](examples) folder has one runnable script per method.

## 🔑 API Credentials — Reseller ID & API Key

The library talks to the DomainNameAPI REST API and needs exactly two credentials, passed to the constructor:

| Parameter | Value |
|---|---|
| First | Reseller ID — UUID like `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| Second | API Key |

> 💡 Find your **Reseller ID** and **API Key** in your DomainNameAPI panel under **API Settings**.
> ⚠️ These are **API credentials** — your panel login details will **not** work here.

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

Leading and trailing whitespace around the credentials is removed automatically.

## Quick Start

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

Method names are snake_case (`get_details`, `register_with_contact_info`). The php-dna names also work as
aliases, so code ported from PHP can keep `dna.GetDetails(...)` or `dna.getDetails(...)`.

## Return Values and Error Handling

Methods return plain `dict`/`list` values with exactly the keys php-dna returns. They do **not** raise
exceptions for gateway or network problems; check `result` instead:

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "...",
                              "GatewayCode": "Dna.DomainService:Domain:10007"}}
```

- `Code` is `API_<HTTP status>` for gateway errors (`API_400`, `API_404`, `API_429`, `API_500`, ...).
  A redirect answer (wrong credentials) gives `API_302` with the message `Invalid API credentials`.
- `GatewayCode` is added to `API_<status>` errors when the gateway sent its own error code
  (for example `Dna.DomainService:Domain:10007`), so you can tell "domain not found" from "TLD not supported".
- `Message` is the gateway's message. Empty error bodies become `HTTP <status> - <reason>`
  (for example `HTTP 429 - Too Many Requests`).
- `Details` holds the gateway's details (or the raw response body when there are none); validation errors
  are flattened into a readable list of fields, for example
  `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`.
- Network failures are errors too, never an empty success: a timeout returns `CURL_28` with
  `Could not reach the DomainNameAPI service: the connection timed out. (...)`; DNS, connection and TLS
  failures return `CURL_6`, `CURL_7`, `CURL_35`/`CURL_60` with `Curl error during request: ...`
  (curl error numbers, the same codes php-dna reports). `API_` codes are only used for HTTP statuses.
- A refusal is an error even when the gateway answers HTTP 200: if registration, transfer or renewal comes
  back with `success: false`, the method returns `REGISTER_DOMAIN`, `TRANSFER_DOMAIN` or `RENEW_DOMAIN`
  with the gateway's message.
- Flags keep php-dna's types: `LockStatus` is the string `"true"`/`"false"`, prices are formatted strings
  (`"11.9900"`).

A few methods use their own envelope, exactly as in php-dna:

| Method | On success | On failure |
|---|---|---|
| `check_availability` | a plain `list` of results | the `ERROR` envelope |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `OperationResult: "FAILED"` with `ErrorCode` (`API_<status>`, `CURL_<errno>`, or `BALANCE` for a currency the account does not report) |
| `check_transfer` | `result: "OK"` only when the domain is transferable | `result: "ERROR"` with `data` and `error` |
| `is_tr_tld`, `validate_contact` | plain values (no network) | — |

Only programming errors (for example passing a string where `set_resource_record_set` expects a list)
raise a Python exception.

The timeouts are 30 seconds per call and 10 seconds to connect. Redirects are not followed.

## Test Mode (OTE)

Pass `True` as the third argument to use the test environment `https://ote.domainresellerapi.com/api/v1`.
String values from configuration files are understood: `"true"`, `"1"`, `"on"`, `"yes"` enable test mode,
anything else (`"false"`, `"0"`, `"off"`, `""`) keeps the live environment.

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## Error Reporting (Telemetry)

When an API call fails, the library can send an error report to DomainNameAPI's own error tracker
(Sentry). A small random share of successful calls (4%, plus every call slower than 1 second) is sent as a
performance record. This helps DomainNameAPI find and fix problems. Error reporting is **on by default**.

> ℹ️ In version 1.0.0 the built-in Sentry address is still empty, because the Sentry project for
> python-dna has not been created yet: **nothing is sent** until a library update fills it in, or until you
> pass your own address with `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")`.

Reports are sent from a background thread: they never slow down or break your call.
Expected, high-volume errors (domain not found, insufficient balance, invalid credentials, no forwarding
configured, ...) are never reported.

**What is sent:**

- error code and message
- called endpoint path and HTTP method
- call duration
- library name (`DomainNameAPI-Python`), library version and Python version
- reseller ID and domain name
- the server's public IP address (looked up via `api.ipify.org`) and the operating-system user name
- the API request and response, including the domain's contact details; only credentials are masked — EPP/auth codes, API keys, passwords and tokens are replaced with `***`

**What is never sent:** EPP/auth codes, API keys, passwords or tokens in readable form; function call arguments in stack traces.

**Why and how long:** the data is used only for usage measurement and early diagnosis of problems, and is kept for 30 days on DomainNameAPI's own Sentry server, after which it is deleted automatically.

**How to turn it off:** call `set_error_reporting_enabled(False)` after constructing the client:

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**Minimal mode:** `set_telemetry_minimal(True)` sends only the error code and message, endpoint, timing,
versions and reseller ID — no request/response data, domain, IP address or user name.

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **Security:** TLS certificate verification is on. On a host with an outdated CA bundle it can be switched off with `dna.set_ssl_verification(False)` — this is not recommended; updating the CA bundle is the better fix.

## Usage

All examples below assume:

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

The sample outputs are real return values of the library.

### Account

#### Get Reseller Details

Reseller account details: ID, name and balances (USD and TL).

```python
result = dna.get_reseller_details()
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'id': '00000000-0000-4000-8000-000000000001',
 'active': True,
 'name': 'example-reseller',
 'balance': '601.64',
 'currency': 'USD',
 'symbol': '$',
 'balances': [{'balance': '601.64', 'currency': 'USD', 'symbol': '$'},
              {'balance': '1250.50', 'currency': 'TL', 'symbol': 'TL'}]}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Get Current Balance

Current balance in one currency: USD (default) or TRY. A currency the account does not report (EUR, GBP, ...) returns OperationResult FAILED with ErrorCode BALANCE.

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>Sample output</summary>

```python
{'ErrorCode': 0,
 'OperationMessage': 'Command completed succesfully.',
 'OperationResult': 'SUCCESS',
 'Balance': '601.64',
 'CurrencyId': 2,
 'CurrencyInfo': None,
 'CurrencyName': 'USD',
 'CurrencySymbol': '$'}
```

</details>


### Search and Lists

#### Domain Availability Check

Availability and price of every domain + extension combination. Returns a plain list on success, an error envelope on failure.

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>Sample output</summary>

```python
[{'TLD': 'com',
  'DomainName': 'dnaprobexyz123',
  'Status': 'available',
  'Command': 'create',
  'Period': 1,
  'IsFee': False,
  'Price': '11.9900',
  'Currency': 'USD',
  'Reason': None},
 {'TLD': 'net',
  'DomainName': 'dnaprobexyz123',
  'Status': 'available',
  'Command': 'create',
  'Period': 1,
  'IsFee': False,
  'Price': '13.9900',
  'Currency': 'USD',
  'Reason': None},
 {'TLD': 'com',
  'DomainName': 'google',
  'Status': 'notavailable',
  'Command': 'create',
  'Period': 1,
  'IsFee': False,
  'Price': '11.9900',
  'Currency': 'USD',
  'Reason': 'Domain exists'},
 {'TLD': 'net',
  'DomainName': 'premium',
  'Status': 'available',
  'Command': 'create',
  'Period': 1,
  'IsFee': True,
  'Price': '2500.0000',
  'Currency': 'USD',
  'Reason': None}]
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain List

Domains in the reseller account. Filters: PageNumber (0-based), PageSize, OrderColumn, OrderDirection, DomainName ...

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>Sample output</summary>

```python
{'data': {'Domains': [{'ID': 11,
                       'Status': 'ok',
                       'DomainName': 'example.com',
                       'AuthCode': '',
                       'LockStatus': 'true',
                       'PrivacyProtectionStatus': 'true',
                       'IsChildNameServer': 'false',
                       'Contacts': {'Billing': {'ID': ''},
                                    'Technical': {'ID': ''},
                                    'Administrative': {'ID': ''},
                                    'Registrant': {'ID': ''}},
                       'Dates': {'Start': '2024-03-15T10:20:30',
                                 'Expiration': '2027-03-15T10:20:30',
                                 'RemainingDays': 126},
                       'NameServers': ['ns1.example.net', 'ns2.example.net'],
                       'Additional': [],
                       'ChildNameServers': []},
                      {'ID': 12,
                       'Status': 'Deleted',
                       'DomainName': 'example.net',
                       'AuthCode': '',
                       'LockStatus': 'false',
                       'PrivacyProtectionStatus': 'false',
                       'IsChildNameServer': 'false',
                       'Contacts': {'Billing': {'ID': ''},
                                    'Technical': {'ID': ''},
                                    'Administrative': {'ID': ''},
                                    'Registrant': {'ID': ''}},
                       'Dates': {'Start': '2023-01-01T00:00:00',
                                 'Expiration': '2026-01-01T00:00:00',
                                 'RemainingDays': 0},
                       'NameServers': [],
                       'Additional': [],
                       'ChildNameServers': []},
                      {'ID': 13,
                       'Status': 'WaitingForRegistration',
                       'DomainName': 'example.org',
                       'AuthCode': '',
                       'LockStatus': 'false',
                       'PrivacyProtectionStatus': 'false',
                       'IsChildNameServer': 'false',
                       'Contacts': {'Billing': {'ID': ''},
                                    'Technical': {'ID': ''},
                                    'Administrative': {'ID': ''},
                                    'Registrant': {'ID': ''}},
                       'Dates': {'Start': '', 'Expiration': '', 'RemainingDays': 0},
                       'NameServers': [],
                       'Additional': [],
                       'ChildNameServers': []}]},
 'result': 'OK',
 'TotalCount': 3}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### TLD List

TLD list with prices per period (registration, renew, transfer, restore ...).

```python
result = dna.get_tld_list(100)
```

<details>
<summary>Sample output</summary>

```python
{'data': [{'id': 1,
           'status': 'Active',
           'maxchar': 63,
           'maxperiod': 10,
           'minchar': 1,
           'minperiod': 1,
           'tld': 'aero',
           'pricing': {'registration': {'1': '44.9900',
                                        '2': '94.9100',
                                        '3': '144.8300'},
                       'renew': {'1': '49.9200', '2': '99.8400'},
                       'transfer': {'1': '44.9900'}},
           'currencies': {'registration': 'USD', 'renew': 'USD', 'transfer': 'USD'}},
          {'id': 2,
           'status': 'Passive',
           'maxchar': 50,
           'maxperiod': 10,
           'minchar': 2,
           'minperiod': 1,
           'tld': 'com.tr',
           'pricing': {'registration': {'1': '15.5000', '2': '30.0000'},
                       'renew': {'1': '15.5000'},
                       'transfer': {'1': '0.0000'}},
           'currencies': {'registration': 'TRY', 'renew': 'TRY', 'transfer': 'USD'}},
          {'id': 3,
           'status': 'Active',
           'maxchar': 63,
           'maxperiod': 10,
           'minchar': 1,
           'minperiod': 1,
           'tld': 'xyz',
           'pricing': {},
           'currencies': {}}],
 'result': 'OK'}
```

</details>


### Domains

#### Domain Registration

Register a new domain. Contacts can be given flat (`AddressLine1`, `Phone`, ...) or nested (`Address.Line1`, `Phone.Phone.Number`, ...). Missing fields are completed and phone numbers are normalised (see `validate_contact`). An empty nameserver list falls back to `ns1.domainnameapi.com` / `ns2.domainnameapi.com`.

```python
contact = {
    "FirstName": "Ahmet",
    "LastName": "Yilmaz",
    "Company": "",
    "EMail": "ahmet.yilmaz@example.com",
    "AddressLine1": "Ornek Sokak No: 123",
    "AddressLine2": "Daire 4",
    "AddressLine3": "",
    "City": "Istanbul",
    "Country": "TR",
    "Fax": "2121234567",
    "FaxCountryCode": "90",
    "Phone": "5551234567",
    "PhoneCountryCode": 90,
    "Type": "Contact",
    "ZipCode": "34000",
    "State": "Istanbul",
}

contacts = {
    "Administrative": contact,
    "Billing": contact,
    "Technical": contact,
    "Registrant": contact,
}

result = dna.register_with_contact_info(
    "example.com",
    1,                                       # period (years)
    contacts,
    ["ns1.example.com", "ns2.example.com"],  # empty list -> default nameservers
    True,                                    # theft protection lock
    False,                                   # privacy protection
)
```

<details>
<summary>Sample output</summary>

```python
{'data': {'ID': 0,
          'Status': 'Active',
          'DomainName': '',
          'AuthCode': '',
          'LockStatus': 'false',
          'PrivacyProtectionStatus': 'false',
          'IsChildNameServer': 'false',
          'Contacts': {'Billing': {'ID': 0},
                       'Technical': {'ID': 0},
                       'Administrative': {'ID': 0},
                       'Registrant': {'ID': 0}},
          'Dates': {'Start': '',
                    'Expiration': '2027-11-09T12:00:00',
                    'RemainingDays': 366},
          'NameServers': [],
          'Additional': [],
          'ChildNameServers': []},
 'result': 'OK'}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain Registration (.tr)

`.tr` domains need TRABIS attributes as the 7th argument. Individual owner: `TRABISDOMAINCATEGORY` = `1` and `TRABISCITIZENID` (identity number). Company owner: `TRABISDOMAINCATEGORY` = `0`, `TRABISTAXOFFICE` and `TRABISTAXNUMBER`. Legacy keys (`TRABISCITIZIENID`, `TRABISNAMESURNAME`, `TRABISCOUNTRYID`, ...) are accepted: they are converted to the REST schema, unsupported ones are dropped.

```python
individual = {
    "TRABISDOMAINCATEGORY": 1,
    "TRABISCITIZIENID": "11111111111",
}

commercial = {
    "TRABISDOMAINCATEGORY": 0,
    "TRABISTAXOFFICE": "Istanbul VD",
    "TRABISTAXNUMBER": "1234567890",
}

result = dna.register_with_contact_info(
    "example.com.tr",
    1,
    contacts,
    ["ns1.example.com", "ns2.example.com"],
    True,
    False,
    individual,  # or commercial
)
```

<details>
<summary>Sample output</summary>

```python
{'data': {'ID': 0,
          'Status': 'Active',
          'DomainName': '',
          'AuthCode': '',
          'LockStatus': 'false',
          'PrivacyProtectionStatus': 'false',
          'IsChildNameServer': 'false',
          'Contacts': {'Billing': {'ID': 0},
                       'Technical': {'ID': 0},
                       'Administrative': {'ID': 0},
                       'Registrant': {'ID': 0}},
          'Dates': {'Start': '',
                    'Expiration': '2027-11-09T12:00:00',
                    'RemainingDays': 366},
          'NameServers': [],
          'Additional': [],
          'ChildNameServers': []},
 'result': 'OK'}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain Renewal

Renew a domain for the given number of years.

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain Details

Full details of one domain: status, dates, nameservers, lock/privacy flags, child nameservers.

```python
result = dna.get_details("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'data': {'ID': 4321,
          'Status': 'Active',
          'DomainName': 'example.com',
          'AuthCode': 'Ab1!xyZ9',
          'LockStatus': 'true',
          'PrivacyProtectionStatus': 'false',
          'IsChildNameServer': 'true',
          'Contacts': {'Billing': {'ID': 'DNA-B-4'},
                       'Technical': {'ID': 'DNA-T-3'},
                       'Administrative': {'ID': 'DNA-A-2'},
                       'Registrant': {'ID': 'DNA-R-1'}},
          'Dates': {'Start': '2024-03-15T10:20:30',
                    'Expiration': '2027-03-15T10:20:30',
                    'RemainingDays': 126},
          'NameServers': ['ns1.example.net', 'ns2.example.net'],
          'Additional': {'TRABISDOMAINCATEGORY': '1'},
          'ChildNameServers': [{'ns': 'ns1.example.com', 'ip': '192.0.2.11'},
                               {'ns': 'ns2.example.com', 'ip': ''}]},
 'result': 'OK'}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Sync From Registry

Refresh a domain from the registry (same envelope as get_details).

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'data': {'ID': 4321,
          'Status': 'Active',
          'DomainName': 'example.com',
          'AuthCode': 'Ab1!xyZ9',
          'LockStatus': 'true',
          'PrivacyProtectionStatus': 'false',
          'IsChildNameServer': 'true',
          'Contacts': {'Billing': {'ID': 'DNA-B-4'},
                       'Technical': {'ID': 'DNA-T-3'},
                       'Administrative': {'ID': 'DNA-A-2'},
                       'Registrant': {'ID': 'DNA-R-1'}},
          'Dates': {'Start': '2024-03-15T10:20:30',
                    'Expiration': '2027-03-15T10:20:30',
                    'RemainingDays': 126},
          'NameServers': ['ns1.example.net', 'ns2.example.net'],
          'Additional': {'TRABISDOMAINCATEGORY': '1'},
          'ChildNameServers': [{'ns': 'ns1.example.com', 'ip': '192.0.2.11'},
                               {'ns': 'ns2.example.com', 'ip': ''}]},
 'result': 'OK'}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Nameserver Modification

Replace the nameservers of a domain (entries are trimmed, lower-cased, de-duplicated).

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Enable Domain Lock

Turn the registrar (theft protection) lock on.

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Disable Domain Lock

Turn the registrar (theft protection) lock off.

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Modify Domain Privacy

Turn WHOIS privacy protection on (True) or off (False). 1, "1", "on", "true" and "yes" also mean on; anything else means off. The reason argument is not sent to the gateway.

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>Sample output</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### Contacts

#### Get Domain Contacts

Administrative, Billing, Registrant and Technical contacts of a domain.

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'data': {'contacts': {'Administrative': {'ID': 'DNA-A-2',
                                          'Status': 'Active',
                                          'AuthCode': '',
                                          'FirstName': 'Grace',
                                          'LastName': 'Hopper',
                                          'Company': '',
                                          'EMail': 'grace@example.com',
                                          'Type': 'Administrative',
                                          'Address': {'Line1': 'Example Street 2',
                                                      'Line2': '',
                                                      'Line3': '',
                                                      'State': 'DC',
                                                      'City': 'Washington',
                                                      'Country': 'US',
                                                      'ZipCode': '20001'},
                                          'Phone': {'Phone': {'Number': '2025550100',
                                                              'CountryCode': '1'},
                                                    'Fax': {'Number': '2025550101',
                                                            'CountryCode': '1'}},
                                          'Additional': []},
                       'Billing': {'ID': 'DNA-B-4',
                                   'Status': 'Active',
                                   'AuthCode': '',
                                   'FirstName': 'Ada',
                                   'LastName': 'Lovelace',
                                   'Company': 'Example Ltd',
                                   'EMail': 'billing@example.com',
                                   'Type': 'Billing',
                                   'Address': {'Line1': 'Example Street 1',
                                               'Line2': '',
                                               'Line3': '',
                                               'State': 'Istanbul',
                                               'City': 'Istanbul',
                                               'Country': 'TR',
                                               'ZipCode': '34000'},
                                   'Phone': {'Phone': {'Number': '5551234567',
                                                       'CountryCode': '90'},
                                             'Fax': {'Number': '', 'CountryCode': ''}},
                                   'Additional': []},
                       'Registrant': {'ID': 'DNA-R-1',
                                      'Status': 'Active',
                                      'AuthCode': '',
                                      'FirstName': 'Ada',
                                      'LastName': 'Lovelace',
                                      'Company': 'Example Ltd',
                                      'EMail': 'ada@example.com',
                                      'Type': 'Registrant',
                                      'Address': {'Line1': 'Example Street 1',
                                                  'Line2': '',
                                                  'Line3': '',
                                                  'State': 'Istanbul',
                                                  'City': 'Istanbul',
                                                  'Country': 'TR',
                                                  'ZipCode': '34000'},
                                      'Phone': {'Phone': {'Number': '5551234567',
                                                          'CountryCode': '90'},
                                                'Fax': {'Number': '',
                                                        'CountryCode': ''}},
                                      'Additional': []},
                       'Technical': {'ID': 'DNA-T-3',
                                     'Status': 'Active',
                                     'AuthCode': '',
                                     'FirstName': 'Alan',
                                     'LastName': 'Turing',
                                     'Company': '',
                                     'EMail': 'alan@example.com',
                                     'Type': 'Technical',
                                     'Address': {'Line1': 'Example Street 3',
                                                 'Line2': '',
                                                 'Line3': '',
                                                 'State': '',
                                                 'City': 'London',
                                                 'Country': 'GB',
                                                 'ZipCode': 'SW1A 1AA'},
                                     'Phone': {'Phone': {'Number': '2071234567',
                                                         'CountryCode': '44'},
                                               'Fax': {'Number': '',
                                                       'CountryCode': ''}},
                                     'Additional': []}}},
 'result': 'OK'}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Save Domain Contacts

Replace the four contacts of a domain. `contacts` is the same dictionary as in the registration example.

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### Child Nameservers

#### Add Child Nameserver

Create a child nameserver (glue record) under a domain.

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Delete Child Nameserver

Delete a child nameserver.

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Update Child Nameserver

Change the IP address of a child nameserver.

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### Transfers

#### Domain Transfer

Start an incoming transfer with the domain's EPP/auth code. Contacts are never sent with a transfer (the request always carries `"contacts": []`): the registrar takes them over from the losing registrar, so `transfer` has no contacts parameter. A refusal (`success: false`) returns a `TRANSFER_DOMAIN` error.

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>Sample output</summary>

```python
{'data': {'ID': 0,
          'Status': 'Active',
          'DomainName': '',
          'AuthCode': '',
          'LockStatus': 'false',
          'PrivacyProtectionStatus': 'false',
          'IsChildNameServer': 'false',
          'Contacts': {'Billing': {'ID': 0},
                       'Technical': {'ID': 0},
                       'Administrative': {'ID': 0},
                       'Registrant': {'ID': 0}},
          'Dates': {'Start': '',
                    'Expiration': '2027-11-09T12:00:00',
                    'RemainingDays': 366},
          'NameServers': [],
          'Additional': [],
          'ChildNameServers': []},
 'result': 'OK'}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Check Transfer

Can the domain be transferred with this auth code? result is OK only when it can.

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'TransferAvailabilityStatus': True,
          'AuthCodeIsRequired': True,
          'AuthCodeIsValid': True,
          'UserTransferRequired': False,
          'TransferLock': False,
          'Message': 'Domain can be transferred',
          'MessageKey': 'TransferAvailable',
          'Additional': []}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Cancel Transfer

Cancel a pending incoming transfer.

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Approve Outgoing Transfer

Approve a pending outgoing transfer.

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Reject Outgoing Transfer

Reject a pending outgoing transfer.

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### DNS Zone

The gateway stores DNS records as **sets**: one name + type holds a list of values. Writing a name + type
replaces the whole set, and deleting by one value removes the whole set. The `*_record_set` and
`*_record_value` methods handle this for you; prefer them over the low-level `add/edit/delete_resource_record`.

- Names may be given as `"@"`, `""`, `"www"`, `"www.example.com"` or `"www.example.com."`; they are sent as the
  relative label the gateway expects. `get_resource_records` returns fully qualified names (`"www.example.com."`).
- Supported types: `A`, `AAAA`, `ALIAS`, `CAA`, `CNAME`, `DS`, `MX`, `NAPTR`, `PTR`, `SRV`, `TLSA`, `TXT`
  (others are rejected before any call is made). TTL is 1 to 86400 seconds.
- Writes are applied immediately; pass `apply=False` to stage several changes and call
  `apply_resource_records` once. If the automatic apply fails, the method returns the apply error (the change
  stays staged but is not live).
- The gateway rate-limits zone calls, so the library keeps zone calls at least one second apart
  (`dna.zone_min_interval`, in seconds).


#### List Records

DNS zone of a domain, one row per record value. Names come back fully qualified.

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'records': [{'Name': 'example.com.',
                       'Type': 'A',
                       'TTL': 3600,
                       'Content': '192.0.2.1',
                       'Disabled': False},
                      {'Name': 'www.example.com.',
                       'Type': 'CNAME',
                       'TTL': 300,
                       'Content': 'example.com.',
                       'Disabled': False},
                      {'Name': 'example.com.',
                       'Type': 'MX',
                       'TTL': 3600,
                       'Content': '10 mx1.example.com.',
                       'Disabled': False},
                      {'Name': 'example.com.',
                       'Type': 'MX',
                       'TTL': 3600,
                       'Content': '20 mx2.example.com.',
                       'Disabled': True},
                      {'Name': 'example.com.',
                       'Type': 'TXT',
                       'TTL': 3600,
                       'Content': '"v=spf1 include:_spf.example.net ~all"',
                       'Disabled': False},
                      {'Name': 'empty.example.com.',
                       'Type': 'AAAA',
                       'TTL': 60,
                       'Content': '',
                       'Disabled': False}]}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Set a Record Set

Make a whole name + type look exactly like the given list (the gateway's own model). An empty list removes the set. Changes are applied immediately unless apply=False.

```python
result = dna.set_resource_record_set(
    "example.com",
    "@",                                         # apex; "www", "www.example.com" also work
    "MX",
    ["10 mx1.example.com", "20 mx2.example.com"],
    3600,                                        # TTL (1..86400)
)
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Add One Value

Add ONE value to a record set and keep the values already there (read-merge-write). Adding a value that is already present is a no-op.

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com.',
                       '20 mx2.example.com.',
                       '30 mx3.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Remove One Value

Remove ONE value from a record set, leaving the others in place.

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Replace One Value

Swap ONE value of a record set for another (the 'edit row' of a DNS panel).

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Delete a Record Set

Remove every value under a name + type. Removing a set that does not exist is OK.

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Add Record (low-level)

Low-level: write a record set (POST). The gateway replaces an existing name + type, so prefer add_resource_record_value() to append a value.

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Edit Record (low-level)

Low-level: rewrite an existing record set (PUT), identified by its current name.

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Delete Record (low-level)

Low-level: DELETE by name + value + type. The gateway removes the WHOLE set, so prefer remove_resource_record_value() to drop a single value.

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Apply Staged Changes

Commit staged zone changes (only needed after calls made with apply=False).

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### URL Forwarding

#### Get Forwarding

URL forwarding of a domain. Enabled is False when nothing is configured.

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Set Forwarding

Forward the domain to a URL: 'Standard' (plain redirect) or 'Frame' (masked).

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Delete Forwarding

Remove URL forwarding. Removed is False (and result OK) when nothing was configured.

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>Sample output</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Removed': True}}
```

</details>


### Utilities

#### Is .tr Domain

Is this a .tr domain? Local check, no network call.

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>Sample output</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Validate Contact

Complete and normalise a contact the way the gateway expects it (local, no network): missing fields get placeholders, names lose digits/punctuation, phone numbers are split into number + country code, State falls back to City.

```python
result = dna.validate_contact({
    "FirstName": " Jo ",
    "Phone": "+1 (202) 555-0100",
    "Country": "Turkey",
    "City": "",
    "Fax": "0090 212 123 45 67",
})
```

<details>
<summary>Sample output</summary>

```python
{'FirstName': 'Jo',
 'Phone': '2025550100',
 'Country': 'TR',
 'City': 'ISTANBUL',
 'Fax': '2121234567',
 'LastName': 'Isimyok',
 'AddressLine1': 'Addres yok',
 'ZipCode': '34000',
 'PhoneCountryCode': '1',
 'State': 'ISTANBUL',
 'FaxCountryCode': '90'}
```

</details>


### Diagnostics and Settings

```python
dna.get_details("example.com")

dna.get_request_data()           # {'url': ..., 'method': 'GET', 'payload': {...}} of the last call
dna.get_response_data()          # decoded response body of the last call ({'raw_response': ...} if not JSON)
dna.get_parsed_response_data()   # body on success, {'Code', 'Message', 'Details'} on failure
dna.get_response_headers()       # {'url', 'http_code', 'content_type', 'total_time', 'headers'}
dna.get_last_function()          # 'request:GET domains/info'
dna.get_service_url()            # 'https://api.domainresellerapi.com/api/v1'

dna.set_service_url("https://ote.domainresellerapi.com/api/v1")
dna.set_error_reporting_enabled(False)
dna.set_telemetry_minimal(True)
dna.set_ssl_verification(True)
dna.zone_min_interval = 1.0
```

A custom HTTP transport (proxy handling, logging, tests) can be passed to the constructor: any object with a
`send(request)` method that returns a `domainnameapi.HttpResponse`:

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## Testing

The test suite needs no credentials and makes no external network calls:

```bash
python -m unittest discover -s tests -v
```

| Test file | Description |
|-----------|-------------|
| `tests/test_conformance.py` | Runs all 134 php-dna conformance fixtures: same requests on the wire, same return values |
| `tests/test_edge_cases.py` | Extra edge cases recorded from php-dna (unusual gateway responses and inputs) |
| `tests/test_http.py` | HTTP layer: headers, query strings, JSON bodies, timeouts, redirects |
| `tests/test_errors.py` | Error mapping of gateway responses |
| `tests/test_telemetry.py` | Telemetry payloads, credential masking, opt-out |
| `tests/test_utils.py` | Utilities and PHP-compatible value handling |

<hr style="border: 4px solid #000; border-style: dashed;">


## Return and Error Codes with Descriptions

| Code | Description                                    | Detail                                                                                                                                                         |
|------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1000 | Command completed successfully                 | Operation successful.                                                                                                                                          |
| 1001 | Command completed successfully; action pending | Operation successful. However, the operation is currently queued for completion.                                                                               |
| 2003 | Required parameter missing                     | Parameter missing error. For example, no phone entry in contact information.                                                                                   |
| 2105 | Object is not eligible for renewal             | Domain status is not suitable for renewal, locked for update operations. Status should not be "clientupdateprohibited". May be due to other status conditions. |
| 2200 | Authentication error                           | Authorization error, security code is incorrect or domain is registered with another registrar.                                                                |
| 2302 | Object exists                                  | Domain name or nameserver information already exists in database. Cannot be registered.                                                                        |
| 2303 | Object does not exist                          | Domain name or nameserver information does not exist in database. New registration required.                                                                   |
| 2304 | Object status prohibits operation              | Domain status is not suitable for updates, locked for update operations. Status should not be "clientupdateprohibited". May be due to other status conditions. |

| CODE | DETAIL                                                                                                                               |
|------|--------------------------------------------------------------------------------------------------------------------------------------|
| 101  | System Error Detailed For ({0})!                                                                                                     |
| 102  | Multiple Errors Detailed For ({0})!                                                                                                  |
| 103  | Unknown Errors Detailed For ({0})!                                                                                                   |
| 200  | API command not found ({0})!                                                                                                         |
| 210  | API service not found ({0})!                                                                                                         |
| 211  | API service provider not set!                                                                                                        |
| 300  | Reseller not found!                                                                                                                  |
| 301  | Your current IP address is not authorized to access. Please make sure you are connecting from an authorized IP address and try again |
| 310  | TLD is not supported!                                                                                                                |
| 320  | API not found!                                                                                                                       |
| 321  | Currency is not supported!                                                                                                           |
| 330  | Required parameter(s) not set ({0}).                                                                                                 |
| –    | Make sure you send all contact objects full                                                                                          |
| 340  | Price definition not found ({0}[{1}]-{2}{3}).                                                                                        |
| 350  | Insufficient reseller balance. (Reseller Id : {0} - Current Balance : {1} {2}).                                                      |
| 350  | Accounting currency does not match or the balance is not sufficient.                                                                 |
| 360  | Invalid API request for field ({0}).                                                                                                 |
| 360  | API quota exceeded!                                                                                                                  |
| 361  | Throttled error!                                                                                                                     |
| 362  | Premium domain is not available to register right now.                                                                               |
| 363  | Operation cancelled because domain in auto-renewal period                                                                            |
| 364  | This domain is currently unavailable for transaction due to a problem with the registry                                              |

| CODE | DETAIL                                                                                      |
|------|---------------------------------------------------------------------------------------------|
| 400  | Invalid contact ({0}).                                                                      |
| 401  | Contact info can not sync.                                                                  |
| 402  | No access to contact information from registry.                                             |
| 403  | THE SYSTEM HAS MISSING INFORMATION. ENTER YOUR DEFAULT INFORMATION OR CONTACT SUPPORT TEAM. |
| 404  | DOMAIN CONTACT CANNOT UPDATE. PERMISSION FROM THE REGISTRY.                                 |
| 410  | Contact not found.                                                                          |
| 410  | Contact not found ({0}).                                                                    |
| 420  | Invalid Api command for contact {0}.                                                        |
| 430  | Contact api not found.                                                                      |
| 440  | Contact is not synced.                                                                      |
| 450  | Too many domain contacts!                                                                   |
| 451  | Failed to proceed with contact update.                                                      |

| CODE | DETAIL                                                                                                                               |
|------|--------------------------------------------------------------------------------------------------------------------------------------|
| 500  | Invalid domain id.                                                                                                                   |
| 500  | Invalid domain id ({0}).                                                                                                             |
| 501  | Domain could not synchronized({0})                                                                                                   |
| 502  | Internal transfer failed                                                                                                             |
| 503  | Domain registration is not available.                                                                                                |
| 504  | Domain information does not match. Before :{0}                                                                                       |
| 505  | Enter the Ip Address.                                                                                                                |
| 506  | Domain Transfer Has Been Started But Contact Info Not Read.                                                                          |
| 507  | Authorization error.                                                                                                                 |
| 510  | Domain not found.                                                                                                                    |
| 511  | Expired domains cannot be found.                                                                                                     |
| 512  | Domain is not renewable.                                                                                                             |
| 513  | Domain is not in updateable status. It must be active for to be updated                                                              |
| 514  | Redemption Period Expected.                                                                                                          |
| 520  | Invalid Api command for domain "{0}".                                                                                                |
| 530  | Invalid domain period. Period must be {0} to {1} years. Requested period is {2} years.                                               |
| 540  | Domain cannot be extended beyond {0} years from current date.                                                                        |
| 550  | Invalid domain name. Domain must be {0} to {1} characters length. Requested domain name is {2} characters.                           |
| 560  | Invalid name server count. Domain must have {0} to {1} name servers. Requested name server count is {2}.                             |
| 561  | No name server information found in the incoming request                                                                             |
| 570  | Idn not supported for tld "{0}".                                                                                                     |
| 571  | Period invalid.                                                                                                                      |
| 572  | Command invalid.                                                                                                                     |
| 573  | Domain names not found.                                                                                                              |
| 574  | TLD names not found.                                                                                                                 |
| 575  | Domain is not in updateable status. It must be active for name servers to be updated                                                 |
| 576  | Domain can be renewed in the last 1 month before the expire date                                                                     |
| 580  | Transfer not supported for tld "{0}".                                                                                                |
| 581  | Child name server not found                                                                                                          |
| 582  | Transfer started by other reseller.                                                                                                  |
| 583  | Transfer not initialized. Please contact the support team.                                                                           |
| 584  | Object status prohibits operation                                                                                                    |
| 590  | Auth code is required for this transfer.                                                                                             |
| 591  | Auth code is not valid.                                                                                                              |
| 592  | Transfer lock exists on domain.                                                                                                      |
| 593  | Domain cannot be transferred, Status Information and Transfer Lock must comply with the required criteria. (Status Information: #ok) |
| 594  | Domain name server address could not resolved ({0})                                                                                  |
| 595  | Contact information can not be read (whois.registrar.tld) Please make sure that privacy protection status open                       |
| 596  | Contact information could not verified                                                                                               |
| 597  | Tld Not Found                                                                                                                        |
| 598  | Unknown error occurred                                                                                                               |
| 599  | Domain Forward Not Found                                                                                                             |


## License

Apache License 2.0 — see [LICENSE](LICENSE).
