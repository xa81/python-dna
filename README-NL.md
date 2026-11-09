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


# python-dna: DomainNameAPI-client voor Python

Python-client voor de reseller-REST API van [DomainNameAPI](https://www.domainnameapi.com): domeinen zoeken, registreren,
transfereren en verlengen, en contacten, nameservers, child nameservers, DNS-zones en URL-doorverwijzingen beheren.
Het is een getrouwe port van [php-dna](https://github.com/domainreseller/php-dna): dezelfde methoden, dezelfde verzoeken,
dezelfde retourwaarden, gecontroleerd aan de hand van de conformiteitsfixtures van php-dna.

## 📦 Downloaden — gebruik altijd de Releases!

⬇️ **Download hier de nieuwste geteste versie: https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ Gebruik **niet** de groene knop **Code → Download ZIP** — daarmee downloadt u de ruwe ontwikkelbranch. Release-pakketten zijn geversioneerd, getest en klaar voor productie.

## Installatie en Integratie Gids

### Minimale Vereisten

- Python 3.8 of hoger (aanbevolen 3.12)
- Geen pakketten van derden: de bibliotheek gebruikt alleen de standaardbibliotheek van Python (`urllib`, `json`, `ssl`).

### A) Installeren met pip

```bash
pip install domainnameapi
```

### B) Een release-pakket installeren

Download de wheel (`domainnameapi-1.0.0-py3-none-any.whl`) of het bronarchief van de
[nieuwste release](https://github.com/domainreseller/python-dna/releases/latest) en installeer deze:

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### C) De broncode direct gebruiken

Kopieer de map `src/domainnameapi` naast uw code (of voeg `src` toe aan `PYTHONPATH`) en importeer deze.
De map [examples](examples) bevat per methode één uitvoerbaar script.

## 🔑 API-inloggegevens — Reseller ID en API Key

De bibliotheek communiceert met de DomainNameAPI REST API en heeft precies twee gegevens nodig, die aan de constructor worden meegegeven:

| Parameter | Waarde |
|---|---|
| Eerste | Reseller ID — UUID zoals `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| Tweede | API Key |

> 💡 U vindt uw **Reseller ID** en **API Key** in uw DomainNameAPI-panel onder **API-instellingen**.
> ⚠️ Dit zijn **API-inloggegevens** — de gegevens waarmee u op het panel inlogt, werken hier **niet**.

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

Spaties aan het begin en einde van de inloggegevens worden automatisch verwijderd.

## Snel aan de slag

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

Methodenamen zijn in snake_case (`get_details`, `register_with_contact_info`). De namen uit php-dna werken ook als
aliassen, zodat uit PHP overgezette code `dna.GetDetails(...)` of `dna.getDetails(...)` kan blijven gebruiken.

## Retourwaarden en foutafhandeling

Methoden geven gewone `dict`-/`list`-waarden terug met precies de sleutels die php-dna teruggeeft. Bij gateway- of
netwerkproblemen gooien ze **geen** exceptions; controleer in plaats daarvan `result`:

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "..."}}
```

- `Code` is `API_<HTTP-status>` bij gatewayfouten (`API_400`, `API_404`, `API_429`, `API_500`, ...).
  Een redirect-antwoord (verkeerde inloggegevens) levert `API_302` op met de melding `Invalid API credentials`.
- `Message` is de melding van de gateway. Lege foutantwoorden worden `HTTP <status> - <reason>`
  (bijvoorbeeld `HTTP 429 - Too Many Requests`).
- `Details` bevat de details van de gateway; validatiefouten worden samengevoegd tot een leesbare lijst van velden,
  bijvoorbeeld `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`.
- Netwerkstoringen zijn ook fouten, nooit een leeg succes: een time-out geeft `API_28` met
  `Could not reach the DomainNameAPI service: the connection timed out. (...)`; DNS-, verbindings- en TLS-fouten
  geven `API_6`, `API_7`, `API_35`/`API_60` met `Curl error during request: ...`
  (curl-foutnummers, dezelfde codes die php-dna rapporteert).
- Flags behouden de typen van php-dna: `LockStatus` is de string `"true"`/`"false"`, prijzen zijn opgemaakte strings
  (`"11.9900"`).

Enkele methoden gebruiken hun eigen antwoordformaat, precies zoals in php-dna:

| Methode | Bij succes | Bij een fout |
|---|---|---|
| `check_availability` | een gewone `list` met resultaten | het `ERROR`-formaat |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `OperationResult: "FAILED"` met `ErrorCode` |
| `check_transfer` | `result: "OK"` alleen als het domein transfereerbaar is | `result: "ERROR"` met `data` en `error` |
| `is_tr_tld`, `validate_contact` | gewone waarden (geen netwerk) | — |

Alleen programmeerfouten (bijvoorbeeld een string doorgeven waar `set_resource_record_set` een lijst verwacht)
leiden tot een Python-exception.

De time-outs zijn 30 seconden per aanroep en 10 seconden voor het opzetten van de verbinding. Redirects worden niet gevolgd.

## Testmodus (OTE)

Geef `True` mee als derde argument om de testomgeving `https://ote.domainresellerapi.com/api/v1` te gebruiken.
Stringwaarden uit configuratiebestanden worden begrepen: `"true"`, `"1"`, `"on"`, `"yes"` schakelen de testmodus in,
al het andere (`"false"`, `"0"`, `"off"`, `""`) houdt de live-omgeving aan.

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## Foutrapportage (telemetrie)

Wanneer een API-aanroep mislukt, kan de bibliotheek een foutrapport sturen naar de eigen fouttracker van DomainNameAPI
(Sentry). Een klein, willekeurig deel van de geslaagde aanroepen (4%, plus elke aanroep die langer dan 1 seconde duurt) wordt als
prestatiegegeven verstuurd. Dit helpt DomainNameAPI problemen te vinden en op te lossen. Foutrapportage staat **standaard aan**.

> ℹ️ In versie 1.0.0 is het ingebouwde Sentry-adres nog leeg, omdat het Sentry-project voor
> python-dna nog niet is aangemaakt: **er wordt niets verstuurd** totdat een update van de bibliotheek het invult, of totdat u
> uw eigen adres meegeeft met `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")`.

Rapporten worden vanuit een achtergrondthread verstuurd: ze vertragen of verstoren uw aanroep nooit.
Verwachte fouten die vaak voorkomen (domein niet gevonden, onvoldoende saldo, ongeldige inloggegevens, ...) worden nooit
gerapporteerd.

**Wat wordt verstuurd:**

- foutcode en -melding
- pad van het aangeroepen endpoint en HTTP-methode
- duur van de aanroep
- bibliotheeknaam (`DomainNameAPI-Python`), bibliotheekversie en Python-versie
- reseller-ID en domeinnaam
- het publieke IP-adres van de server (opgevraagd via `api.ipify.org`) en de gebruikersnaam van het besturingssysteem
- het API-verzoek en -antwoord, inclusief de contactgegevens van het domein; alleen inloggegevens worden gemaskeerd — EPP-/auth-codes, API-keys, wachtwoorden en tokens worden vervangen door `***`

**Wat nooit wordt verstuurd:** EPP-/auth-codes, API-keys, wachtwoorden of tokens in leesbare vorm; functieargumenten in stacktraces.

**Waarom en hoe lang:** de gegevens worden alleen gebruikt voor gebruiksmeting en het vroegtijdig opsporen van problemen, en worden 30 dagen bewaard op de eigen Sentry-server van DomainNameAPI, waarna ze automatisch worden verwijderd.

**Uitschakelen:** roep `set_error_reporting_enabled(False)` aan nadat u de client hebt aangemaakt:

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**Minimale modus:** `set_telemetry_minimal(True)` verstuurt alleen de foutcode en -melding, het endpoint, de timing,
de versies en het reseller-ID — geen verzoek-/antwoordgegevens, domein, IP-adres of gebruikersnaam.

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **Beveiliging:** TLS-certificaatverificatie staat aan. Op een server met een verouderde CA-bundle kan deze worden uitgeschakeld met `dna.set_ssl_verification(False)` — niet aanbevolen; de CA-bundle bijwerken is de betere oplossing.

## Gebruik

Alle onderstaande voorbeelden gaan uit van:

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

De voorbeelduitvoer bestaat uit echte retourwaarden van de bibliotheek.

### Account

#### Resellergegevens ophalen

Gegevens van het reselleraccount: ID, naam en saldi (USD en TL).

```python
result = dna.get_reseller_details()
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'id': '00000000-0000-4000-8000-000000000001',
 'active': True,
 'name': 'example-reseller',
 'balance': '601.64',
 'currency': 'USD',
 'symbol': '$',
 'balances': [{'balance': '601.64', 'currency': 'USD', 'symbol': '$'},
              {'balance': '1250.5', 'currency': 'TL', 'symbol': 'TL'}]}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Huidig saldo ophalen

Huidig saldo in één valuta: USD (standaard), TRY, EUR of GBP.

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>Voorbeelduitvoer</summary>

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


### Zoeken en lijsten

#### Domein beschikbaarheid controleren

Beschikbaarheid en prijs van elke combinatie van domein + extensie. Geeft bij succes een gewone lijst terug, bij een fout een foutformaat.

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### Domeinlijst

Domeinen in het reselleraccount. Filters: PageNumber (vanaf 0), PageSize, OrderColumn, OrderDirection, DomainName ...

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### TLD-lijst

TLD-lijst met prijzen per periode (registratie, verlenging, transfer, herstel ...).

```python
result = dna.get_tld_list(100)
```

<details>
<summary>Voorbeelduitvoer</summary>

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


### Domeinen

#### Domein Registratie

Een nieuw domein registreren. Contacten kunnen plat (`AddressLine1`, `Phone`, ...) of genest (`Address.Line1`, `Phone.Phone.Number`, ...) worden opgegeven. Ontbrekende velden worden aangevuld en telefoonnummers worden genormaliseerd (zie `validate_contact`). Bij een lege lijst met nameservers wordt teruggevallen op `ns1.domainnameapi.com` / `ns2.domainnameapi.com`.

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
<summary>Voorbeelduitvoer</summary>

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

#### Domein Registratie (.tr)

`.tr`-domeinen hebben TRABIS-attributen nodig als 7e argument. Particuliere eigenaar: `TRABISDOMAINCATEGORY` = `1` en `TRABISCITIZENID` (identiteitsnummer). Bedrijf als eigenaar: `TRABISDOMAINCATEGORY` = `0`, `TRABISTAXOFFICE` en `TRABISTAXNUMBER`. Oude sleutels (`TRABISCITIZIENID`, `TRABISNAMESURNAME`, `TRABISCOUNTRYID`, ...) worden geaccepteerd: ze worden omgezet naar het REST-schema, niet-ondersteunde sleutels worden weggelaten.

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
<summary>Voorbeelduitvoer</summary>

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

#### Domein Verlenging

Een domein verlengen met het opgegeven aantal jaren.

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domein Informatie

Volledige gegevens van één domein: status, datums, nameservers, vergrendelings-/privacyflags, child nameservers.

```python
result = dna.get_details("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### Synchroniseren met de registry

Een domein bijwerken vanuit de registry (hetzelfde antwoordformaat als get_details).

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### Nameserver Wijzigen

De nameservers van een domein vervangen (items worden getrimd, naar kleine letters omgezet en ontdubbeld).

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domein Vergrendeling inschakelen

De registrar-vergrendeling (diefstalbeveiliging) inschakelen.

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domein Vergrendeling uitschakelen

De registrar-vergrendeling (diefstalbeveiliging) uitschakelen.

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domein Privacy Wijzigen

WHOIS-privacybescherming inschakelen (True) of uitschakelen (False).

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### Contacten

#### Domeincontacten ophalen

Administratief contact, factuurcontact, registrant en technisch contact van een domein.

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### Domein Contact Opslaan

De vier contacten van een domein vervangen. `contacts` is dezelfde dictionary als in het registratievoorbeeld.

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### Child Nameservers

#### Child NameServer Toevoegen

Een child nameserver (glue record) onder een domein aanmaken.

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Child NameServer Verwijderen

Een child nameserver verwijderen.

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Child NameServer Wijzigen

Het IP-adres van een child nameserver wijzigen.

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### Transfers

#### Domein Transfer

Een inkomende transfer starten met de EPP-/auth-code van het domein. Net als bij de facade van php-dna wordt het optionele vierde argument (`contacts`) geaccepteerd maar niet verstuurd; gebruik `dna.client.transfer(domain, code, period, contacts)` om contacten met de transfer mee te sturen.

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### Transfer controleren

Kan het domein met deze auth-code worden getransfereerd? result is alleen OK als dat kan.

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### Transfer annuleren

Een lopende inkomende transfer annuleren.

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Uitgaande transfer goedkeuren

Een lopende uitgaande transfer goedkeuren.

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Uitgaande transfer weigeren

Een lopende uitgaande transfer weigeren.

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### DNS-zone

De gateway slaat DNS-records op als **sets**: één naam + type bevat een lijst met waarden. Het schrijven van een naam + type
vervangt de hele set, en verwijderen op basis van één waarde verwijdert de hele set. De methoden `*_record_set` en
`*_record_value` regelen dit voor u; gebruik ze bij voorkeur in plaats van de low-level `add/edit/delete_resource_record`.

- Namen kunnen worden opgegeven als `"@"`, `""`, `"www"`, `"www.example.com"` of `"www.example.com."`; ze worden verstuurd als het
  relatieve label dat de gateway verwacht. `get_resource_records` geeft volledig gekwalificeerde namen terug (`"www.example.com."`).
- Ondersteunde typen: `A`, `AAAA`, `ALIAS`, `CAA`, `CNAME`, `DS`, `MX`, `NAPTR`, `PTR`, `SRV`, `TLSA`, `TXT`
  (andere worden geweigerd voordat er een aanroep wordt gedaan). De TTL is 1 tot 86400 seconden.
- Schrijfacties worden direct toegepast; geef `apply=False` mee om meerdere wijzigingen klaar te zetten en roep daarna
  één keer `apply_resource_records` aan.
- De gateway beperkt het aantal zone-aanroepen (rate limiting), daarom houdt de bibliotheek minstens één seconde tussen zone-aanroepen
  (`dna.zone_min_interval`, in seconden).


#### Records weergeven

DNS-zone van een domein, één rij per recordwaarde. Namen worden volledig gekwalificeerd teruggegeven.

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### Een recordset instellen

Een volledige naam + type precies gelijk maken aan de opgegeven lijst (het eigen model van de gateway). Een lege lijst verwijdert de set. Wijzigingen worden direct toegepast, tenzij apply=False.

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
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eén waarde toevoegen

ÉÉN waarde aan een recordset toevoegen en de bestaande waarden behouden (lezen-samenvoegen-schrijven). Het toevoegen van een waarde die al aanwezig is, heeft geen effect.

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

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

#### Eén waarde verwijderen

ÉÉN waarde uit een recordset verwijderen; de andere blijven staan.

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eén waarde vervangen

ÉÉN waarde van een recordset vervangen door een andere (de 'rij bewerken' van een DNS-panel).

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Een recordset verwijderen

Alle waarden onder een naam + type verwijderen. Het verwijderen van een set die niet bestaat, is geen fout.

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Record toevoegen (low-level)

Low-level: een recordset schrijven (POST). De gateway vervangt een bestaande naam + type, gebruik dus bij voorkeur add_resource_record_value() om een waarde toe te voegen.

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'a', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Record bewerken (low-level)

Low-level: een bestaande recordset herschrijven (PUT), geïdentificeerd aan de hand van de huidige naam.

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Record verwijderen (low-level)

Low-level: DELETE op basis van naam + waarde + type. De gateway verwijdert de HELE set, gebruik dus bij voorkeur remove_resource_record_value() om één waarde te verwijderen.

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Klaargezette wijzigingen toepassen

Klaargezette zonewijzigingen doorvoeren (alleen nodig na aanroepen met apply=False).

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### URL-doorverwijzing

#### Doorverwijzing ophalen

URL-doorverwijzing van een domein. Enabled is False als er niets is ingesteld.

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Doorverwijzing instellen

Het domein doorverwijzen naar een URL: 'Standard' (gewone redirect) of 'Frame' (gemaskeerd).

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Doorverwijzing verwijderen

URL-doorverwijzing verwijderen.

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### Hulpfuncties

#### Is .tr-domein

Is dit een .tr-domein? Lokale controle, geen netwerkaanroep.

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>Voorbeelduitvoer</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Contact valideren

Een contact aanvullen en normaliseren zoals de gateway het verwacht (lokaal, geen netwerk): ontbrekende velden krijgen plaatsaanduidingen, cijfers en leestekens worden uit namen verwijderd, telefoonnummers worden gesplitst in nummer + landcode, State valt terug op City.

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
<summary>Voorbeelduitvoer</summary>

```python
{'FirstName': 'Jo',
 'Phone': '12025550100',
 'Country': 'TR',
 'City': 'ISTANBUL',
 'Fax': '2121234567',
 'LastName': 'Isimyok',
 'AddressLine1': 'Addres yok',
 'State': 'ISTANBUL',
 'ZipCode': '34000',
 'PhoneCountryCode': '90',
 'FaxCountryCode': '90'}
```

</details>


### Diagnose en instellingen

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

Een eigen HTTP-transport (proxyafhandeling, logging, tests) kan aan de constructor worden meegegeven: elk object met een
methode `send(request)` die een `domainnameapi.HttpResponse` teruggeeft:

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## Tests

De testsuite heeft geen inloggegevens nodig en doet geen externe netwerkaanroepen:

```bash
python -m unittest discover -s tests -v
```

| Testbestand | Beschrijving |
|-----------|-------------|
| `tests/test_conformance.py` | Voert alle 126 conformiteitsfixtures van php-dna uit: dezelfde verzoeken over de lijn, dezelfde retourwaarden |
| `tests/test_edge_cases.py` | Extra randgevallen opgenomen uit php-dna (ongebruikelijke gateway-antwoorden en invoer) |
| `tests/test_http.py` | HTTP-laag: headers, querystrings, JSON-bodies, time-outs, redirects |
| `tests/test_errors.py` | Foutvertaling van gateway-antwoorden |
| `tests/test_telemetry.py` | Telemetrie-payloads, maskering van inloggegevens, opt-out |
| `tests/test_utils.py` | Hulpfuncties en PHP-compatibele verwerking van waarden |

<hr style="border: 4px solid #000; border-style: dashed;">


## Return en Foutcodes met Beschrijvingen

| Code | Beschrijving                                         | Details                                                                                                                                                         |
|------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1000 | Opdracht succesvol voltooid                          | Bewerking geslaagd.                                                                                                                                             |
| 1001 | Opdracht succesvol voltooid; actie in behandeling    | Bewerking geslaagd. De bewerking staat echter nog in de wachtrij om te worden voltooid.                                                                         |
| 2003 | Vereiste parameter ontbreekt                         | Fout door ontbrekende parameter. Bijvoorbeeld: geen telefoonnummer in de contactgegevens.                                                                       |
| 2105 | Object komt niet in aanmerking voor verlenging       | De domeinstatus staat geen verlenging toe; het domein is vergrendeld voor wijzigingen. De status mag niet "clientupdateprohibited" zijn. Kan ook door andere statuscondities komen. |
| 2200 | Authenticatiefout                                    | Autorisatiefout: de beveiligingscode is onjuist of het domein is bij een andere registrar geregistreerd.                                                        |
| 2302 | Object bestaat al                                    | Domeinnaam of nameserverinformatie bestaat al in de database. Kan niet worden geregistreerd.                                                                    |
| 2303 | Object bestaat niet                                  | Domeinnaam of nameserverinformatie bestaat niet in de database. Nieuwe registratie vereist.                                                                     |
| 2304 | Objectstatus verhindert de bewerking                 | De domeinstatus staat geen wijzigingen toe; het domein is vergrendeld voor wijzigingen. De status mag niet "clientupdateprohibited" zijn. Kan ook door andere statuscondities komen. |

| CODE | MELDING                                                                                                                              |
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

| CODE | MELDING                                                                                     |
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

| CODE | MELDING                                                                                                                              |
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


## Licentie

Apache License 2.0 — zie [LICENSE](LICENSE).
