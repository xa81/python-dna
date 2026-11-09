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


# python-dna: DomainNameAPI-Client für Python

Python-Client für die Reseller-REST-API von [DomainNameAPI](https://www.domainnameapi.com): Domains suchen, registrieren,
transferieren und verlängern, Kontakte, Nameserver, Child-Nameserver, DNS-Zonen und URL-Weiterleitungen verwalten.
Es handelt sich um eine originalgetreue Portierung von [php-dna](https://github.com/domainreseller/php-dna): dieselben Methoden, dieselben Anfragen,
dieselben Rückgabewerte, geprüft anhand der Konformitäts-Fixtures von php-dna.

## 📦 Download — immer die Releases verwenden!

⬇️ **Die neueste getestete Version erhalten Sie hier: https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ Verwenden Sie **nicht** den grünen Button **Code → Download ZIP** — damit laden Sie den rohen Entwicklungszweig herunter. Release-Pakete sind versioniert, getestet und produktionsreif.

## Installations- und Integrationsanleitung

### Mindestanforderungen

- Python 3.8 oder höher (empfohlen 3.12)
- Keine Pakete von Drittanbietern: Die Bibliothek verwendet ausschließlich die Python-Standardbibliothek (`urllib`, `json`, `ssl`).

### A) Installation mit pip

```bash
pip install domainnameapi
```

### B) Installation eines Release-Pakets

Laden Sie das Wheel (`domainnameapi-1.0.0-py3-none-any.whl`) oder das Quellarchiv aus dem
[neuesten Release](https://github.com/domainreseller/python-dna/releases/latest) herunter und installieren Sie es:

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### C) Den Quellcode direkt verwenden

Kopieren Sie den Ordner `src/domainnameapi` neben Ihren Code (oder fügen Sie `src` zum `PYTHONPATH` hinzu) und importieren Sie ihn.
Der Ordner [examples](examples) enthält für jede Methode ein ausführbares Skript.

## 🔑 API-Zugangsdaten — Reseller-ID & API-Key

Die Bibliothek kommuniziert mit der DomainNameAPI REST-API und benötigt genau zwei Zugangsdaten, die dem Konstruktor übergeben werden:

| Parameter | Wert |
|---|---|
| Erster | Reseller-ID — UUID wie `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| Zweiter | API-Key |

> 💡 Ihre **Reseller-ID** und Ihren **API-Key** finden Sie in Ihrem DomainNameAPI-Panel unter **API-Einstellungen**.
> ⚠️ Dies sind **API-Zugangsdaten** — Ihre Panel-Anmeldedaten funktionieren hier **nicht**.

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

Leerzeichen am Anfang und Ende der Zugangsdaten werden automatisch entfernt.

## Schnellstart

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

Die Methodennamen sind in snake_case geschrieben (`get_details`, `register_with_contact_info`). Die Namen aus php-dna funktionieren
ebenfalls als Aliase, sodass aus PHP portierter Code `dna.GetDetails(...)` oder `dna.getDetails(...)` beibehalten kann.

## Rückgabewerte und Fehlerbehandlung

Die Methoden geben einfache `dict`-/`list`-Werte mit genau den Schlüsseln zurück, die auch php-dna liefert. Bei Gateway- oder
Netzwerkproblemen lösen sie **keine** Exceptions aus; prüfen Sie stattdessen `result`:

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "...",
                              "GatewayCode": "Dna.DomainService:Domain:10007"}}
```

- `Code` ist bei Gateway-Fehlern `API_<HTTP-Status>` (`API_400`, `API_404`, `API_429`, `API_500`, ...).
  Eine Weiterleitungsantwort (falsche Zugangsdaten) ergibt `API_302` mit der Meldung `Invalid API credentials`.
- `GatewayCode` wird `API_<status>`-Fehlern hinzugefügt, wenn das Gateway einen eigenen Fehlercode gesendet hat (zum Beispiel `Dna.DomainService:Domain:10007`); so lässt sich „Domain nicht gefunden“ von „TLD nicht unterstützt“ unterscheiden.
- `Message` ist die Meldung des Gateways. Leere Fehlerantworten werden zu `HTTP <status> - <reason>`
  (zum Beispiel `HTTP 429 - Too Many Requests`).
- `Details` enthält die Details des Gateways (oder den rohen Antworttext, wenn keine vorhanden sind); Validierungsfehler werden zu einer lesbaren Liste von Feldern zusammengefasst,
  zum Beispiel `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`.
- Netzwerkfehler sind ebenfalls Fehler, niemals ein leerer Erfolg: Eine Zeitüberschreitung liefert `CURL_28` mit
  `Could not reach the DomainNameAPI service: the connection timed out. (...)`; DNS-, Verbindungs- und TLS-Fehler
  liefern `CURL_6`, `CURL_7`, `CURL_35`/`CURL_60` mit `Curl error during request: ...`
  (curl-Fehlernummern, dieselben Codes, die auch php-dna meldet). `API_`-Codes werden nur für HTTP-Status verwendet.
- Eine Ablehnung ist ein Fehler, auch wenn das Gateway mit HTTP 200 antwortet: Kommen Registrierung, Transfer oder Verlängerung mit `success: false` zurück, liefert die Methode `REGISTER_DOMAIN`, `TRANSFER_DOMAIN` oder `RENEW_DOMAIN` mit der Meldung des Gateways.
- Flags behalten die Typen von php-dna: `LockStatus` ist der String `"true"`/`"false"`, Preise sind formatierte Strings
  (`"11.9900"`).

Einige Methoden verwenden ein eigenes Antwortformat, genau wie in php-dna:

| Methode | Bei Erfolg | Bei Fehler |
|---|---|---|
| `check_availability` | eine einfache `list` mit Ergebnissen | das `ERROR`-Format |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `OperationResult: "FAILED"` mit `ErrorCode` (`API_<status>`, `CURL_<errno>` oder `BALANCE` für eine Währung, die das Konto nicht meldet) |
| `check_transfer` | `result: "OK"` nur, wenn die Domain transferierbar ist | `result: "ERROR"` mit `data` und `error` |
| `is_tr_tld`, `validate_contact` | einfache Werte (kein Netzwerk) | — |

Nur Programmierfehler (zum Beispiel ein String, wo `set_resource_record_set` eine Liste erwartet)
lösen eine Python-Exception aus.

Die Timeouts betragen 30 Sekunden pro Aufruf und 10 Sekunden für den Verbindungsaufbau. Weiterleitungen werden nicht verfolgt.

## Testmodus (OTE)

Übergeben Sie `True` als drittes Argument, um die Testumgebung `https://ote.domainresellerapi.com/api/v1` zu verwenden.
String-Werte aus Konfigurationsdateien werden verstanden: `"true"`, `"1"`, `"on"`, `"yes"` aktivieren den Testmodus,
alles andere (`"false"`, `"0"`, `"off"`, `""`) behält die Live-Umgebung bei.

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## Fehlerberichte (Telemetrie)

Wenn ein API-Aufruf fehlschlägt, kann die Bibliothek einen Fehlerbericht an den eigenen Fehler-Tracker von DomainNameAPI
(Sentry) senden. Ein kleiner, zufällig gewählter Anteil erfolgreicher Aufrufe (4 %, dazu jeder Aufruf, der länger als 1 Sekunde dauert) wird als
Performance-Datensatz gesendet. Das hilft DomainNameAPI, Probleme zu finden und zu beheben. Fehlerberichte sind **standardmäßig aktiviert**.

> ℹ️ In Version 1.0.0 ist die eingebaute Sentry-Adresse noch leer, da das Sentry-Projekt für
> python-dna noch nicht angelegt wurde: **Es wird nichts gesendet**, bis ein Bibliotheks-Update sie einträgt oder bis Sie
> mit `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")` Ihre eigene Adresse übergeben.

Berichte werden aus einem Hintergrund-Thread gesendet: Sie verlangsamen oder unterbrechen Ihren Aufruf niemals.
Erwartete, häufig auftretende Fehler (Domain nicht gefunden, unzureichendes Guthaben, ungültige Zugangsdaten, keine Weiterleitung eingerichtet, ...) werden nie
gemeldet.

**Was gesendet wird:**

- Fehlercode und -meldung
- Pfad des aufgerufenen Endpunkts und HTTP-Methode
- Dauer des Aufrufs
- Bibliotheksname (`DomainNameAPI-Python`), Bibliotheksversion und Python-Version
- Reseller-ID und Domainname
- die öffentliche IP-Adresse des Servers (ermittelt über `api.ipify.org`) und der Benutzername des Betriebssystems
- API-Anfrage und -Antwort, einschließlich der Kontaktdaten der Domain; nur Zugangsdaten werden maskiert — EPP-/Auth-Codes, API-Keys, Passwörter und Tokens werden durch `***` ersetzt

**Was nie gesendet wird:** EPP-/Auth-Codes, API-Keys, Passwörter oder Tokens in lesbarer Form; Funktionsargumente in Stacktraces.

**Wozu und wie lange:** Die Daten werden ausschließlich zur Nutzungsmessung und zur frühzeitigen Erkennung von Problemen verwendet und 30 Tage lang auf dem eigenen Sentry-Server von DomainNameAPI gespeichert; danach werden sie automatisch gelöscht.

**So schalten Sie es ab:** Rufen Sie nach dem Erstellen des Clients `set_error_reporting_enabled(False)` auf:

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**Minimalmodus:** `set_telemetry_minimal(True)` sendet nur Fehlercode und -meldung, Endpunkt, Zeitmessung,
Versionen und Reseller-ID — keine Anfrage-/Antwortdaten, keine Domain, keine IP-Adresse und keinen Benutzernamen.

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **Sicherheit:** Die TLS-Zertifikatsprüfung ist aktiviert. Auf einem Server mit veraltetem CA-Bundle kann sie mit `dna.set_ssl_verification(False)` abgeschaltet werden — nicht empfohlen; besser ist es, das CA-Bundle zu aktualisieren.

## Verwendung

Alle folgenden Beispiele setzen voraus:

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

Die Beispielausgaben sind echte Rückgabewerte der Bibliothek.

### Konto

#### Reseller-Details abrufen

Details des Reseller-Kontos: ID, Name und Guthaben (USD und TL).

```python
result = dna.get_reseller_details()
```

<details>
<summary>Beispielausgabe</summary>

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

#### Aktuelles Guthaben abrufen

Aktuelles Guthaben in einer Währung: USD (Standard) oder TRY. Eine Währung, die das Konto nicht meldet (EUR, GBP, ...), liefert OperationResult FAILED mit ErrorCode BALANCE.

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>Beispielausgabe</summary>

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


### Suche und Listen

#### Domain-Verfügbarkeit prüfen

Verfügbarkeit und Preis jeder Kombination aus Domain und Endung. Gibt bei Erfolg eine einfache Liste zurück, bei einem Fehler ein Fehlerformat.

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>Beispielausgabe</summary>

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

#### Domain-Liste

Domains im Reseller-Konto. Filter: PageNumber (ab 0), PageSize, OrderColumn, OrderDirection, DomainName ...

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>Beispielausgabe</summary>

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

#### TLD-Liste

TLD-Liste mit Preisen pro Laufzeit (Registrierung, Verlängerung, Transfer, Wiederherstellung ...).

```python
result = dna.get_tld_list(100)
```

<details>
<summary>Beispielausgabe</summary>

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

#### Domain-Registrierung

Eine neue Domain registrieren. Kontakte können flach (`AddressLine1`, `Phone`, ...) oder verschachtelt (`Address.Line1`, `Phone.Phone.Number`, ...) angegeben werden. Fehlende Felder werden ergänzt und Telefonnummern normalisiert (siehe `validate_contact`). Bei einer leeren Nameserver-Liste werden `ns1.domainnameapi.com` / `ns2.domainnameapi.com` verwendet.

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
<summary>Beispielausgabe</summary>

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

#### Domain-Registrierung (.tr)

`.tr`-Domains benötigen TRABIS-Attribute als 7. Argument. Privatperson als Inhaber: `TRABISDOMAINCATEGORY` = `1` und `TRABISCITIZENID` (Identitätsnummer). Unternehmen als Inhaber: `TRABISDOMAINCATEGORY` = `0`, `TRABISTAXOFFICE` und `TRABISTAXNUMBER`. Alte Schlüssel (`TRABISCITIZIENID`, `TRABISNAMESURNAME`, `TRABISCOUNTRYID`, ...) werden akzeptiert: Sie werden in das REST-Schema umgewandelt, nicht unterstützte werden verworfen.

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
<summary>Beispielausgabe</summary>

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

#### Domain-Verlängerung

Eine Domain um die angegebene Anzahl von Jahren verlängern.

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain-Details

Vollständige Details einer Domain: Status, Daten, Nameserver, Sperr-/Privacy-Flags, Child-Nameserver.

```python
result = dna.get_details("example.com")
```

<details>
<summary>Beispielausgabe</summary>

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

#### Mit der Registry synchronisieren

Eine Domain aus der Registry aktualisieren (gleiches Antwortformat wie get_details).

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>Beispielausgabe</summary>

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

#### Nameserver ändern

Die Nameserver einer Domain ersetzen (Einträge werden getrimmt, in Kleinbuchstaben umgewandelt und von Duplikaten bereinigt).

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain-Sperre aktivieren

Die Registrar-Sperre (Diebstahlschutz) einschalten.

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain-Sperre deaktivieren

Die Registrar-Sperre (Diebstahlschutz) ausschalten.

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain-Privacy ändern

Den WHOIS-Datenschutz einschalten (True) oder ausschalten (False). 1, "1", "on", "true" und "yes" bedeuten ebenfalls ein; alles andere bedeutet aus. Das Argument reason wird nicht an das Gateway gesendet.

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### Kontakte

#### Domain-Kontakte abrufen

Administrativer, Rechnungs-, Inhaber- und technischer Kontakt einer Domain.

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>Beispielausgabe</summary>

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

#### Domain-Kontakte speichern

Die vier Kontakte einer Domain ersetzen. `contacts` ist dasselbe Dictionary wie im Registrierungsbeispiel.

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### Child-Nameserver

#### Child-Nameserver hinzufügen

Einen Child-Nameserver (Glue-Record) unter einer Domain anlegen.

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Child-Nameserver löschen

Einen Child-Nameserver löschen.

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Child-Nameserver aktualisieren

Die IP-Adresse eines Child-Nameservers ändern.

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### Transfers

#### Domain-Transfer

Einen eingehenden Transfer mit dem EPP-/Auth-Code der Domain starten. Bei einem Transfer werden nie Kontakte gesendet (die Anfrage enthält immer `"contacts": []`): Der Registrar übernimmt sie vom abgebenden Registrar, daher hat `transfer` keinen Kontakte-Parameter. Eine Ablehnung (`success: false`) liefert einen `TRANSFER_DOMAIN`-Fehler.

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>Beispielausgabe</summary>

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

#### Transfer prüfen

Kann die Domain mit diesem Auth-Code transferiert werden? result ist nur dann OK, wenn dies möglich ist.

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>Beispielausgabe</summary>

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

#### Transfer abbrechen

Einen ausstehenden eingehenden Transfer abbrechen.

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Ausgehenden Transfer genehmigen

Einen ausstehenden ausgehenden Transfer genehmigen.

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Ausgehenden Transfer ablehnen

Einen ausstehenden ausgehenden Transfer ablehnen.

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### DNS-Zone

Das Gateway speichert DNS-Einträge als **Sets**: Ein Name + Typ enthält eine Liste von Werten. Das Schreiben eines Namens + Typs
ersetzt das gesamte Set, und das Löschen anhand eines einzelnen Werts entfernt das gesamte Set. Die Methoden `*_record_set` und
`*_record_value` erledigen das für Sie; verwenden Sie sie bevorzugt statt der Low-Level-Methoden `add/edit/delete_resource_record`.

- Namen können als `"@"`, `""`, `"www"`, `"www.example.com"` oder `"www.example.com."` angegeben werden; sie werden als das
  relative Label gesendet, das das Gateway erwartet. `get_resource_records` gibt vollqualifizierte Namen zurück (`"www.example.com."`).
- Unterstützte Typen: `A`, `AAAA`, `ALIAS`, `CAA`, `CNAME`, `DS`, `MX`, `NAPTR`, `PTR`, `SRV`, `TLSA`, `TXT`
  (andere werden abgelehnt, bevor ein Aufruf erfolgt). Die TTL liegt zwischen 1 und 86400 Sekunden.
- Schreibvorgänge werden sofort angewendet; übergeben Sie `apply=False`, um mehrere Änderungen vorzumerken, und rufen Sie
  anschließend einmal `apply_resource_records` auf. Schlägt das automatische Anwenden fehl, liefert die Methode diesen Fehler (die Änderung bleibt vorgemerkt, ist aber nicht live).
- Das Gateway begrenzt die Rate der Zonen-Aufrufe, daher hält die Bibliothek zwischen Zonen-Aufrufen mindestens eine Sekunde Abstand
  (`dna.zone_min_interval`, in Sekunden).


#### Einträge auflisten

DNS-Zone einer Domain, eine Zeile pro Eintragswert. Namen werden vollqualifiziert zurückgegeben.

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>Beispielausgabe</summary>

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

#### Ein Record-Set setzen

Einen ganzen Namen + Typ exakt auf die angegebene Liste setzen (das eigene Modell des Gateways). Eine leere Liste entfernt das Set. Änderungen werden sofort angewendet, sofern nicht apply=False angegeben ist.

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
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Einen Wert hinzufügen

EINEN Wert zu einem Record-Set hinzufügen und die bereits vorhandenen Werte beibehalten (Lesen-Zusammenführen-Schreiben). Das Hinzufügen eines bereits vorhandenen Werts bewirkt nichts.

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>Beispielausgabe</summary>

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

#### Einen Wert entfernen

EINEN Wert aus einem Record-Set entfernen, die übrigen bleiben erhalten.

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Einen Wert ersetzen

EINEN Wert eines Record-Sets gegen einen anderen austauschen (die „Zeile bearbeiten“-Funktion eines DNS-Panels).

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Ein Record-Set löschen

Alle Werte unter einem Namen + Typ entfernen. Das Entfernen eines nicht vorhandenen Sets ist kein Fehler.

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eintrag hinzufügen (Low-Level)

Low-Level: ein Record-Set schreiben (POST). Das Gateway ersetzt einen vorhandenen Namen + Typ, verwenden Sie daher zum Anhängen eines Werts bevorzugt add_resource_record_value().

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eintrag bearbeiten (Low-Level)

Low-Level: ein vorhandenes Record-Set neu schreiben (PUT), identifiziert über seinen aktuellen Namen.

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eintrag löschen (Low-Level)

Low-Level: DELETE anhand von Name + Wert + Typ. Das Gateway entfernt das GESAMTE Set, verwenden Sie daher zum Entfernen eines einzelnen Werts bevorzugt remove_resource_record_value().

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Vorgemerkte Änderungen anwenden

Vorgemerkte Zonenänderungen übernehmen (nur nach Aufrufen mit apply=False erforderlich).

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### URL-Weiterleitung

#### Weiterleitung abrufen

URL-Weiterleitung einer Domain. Enabled ist False, wenn nichts konfiguriert ist.

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Weiterleitung einrichten

Die Domain an eine URL weiterleiten: 'Standard' (einfache Weiterleitung) oder 'Frame' (maskiert).

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Weiterleitung löschen

URL-Weiterleitung entfernen. Removed ist False (und das Ergebnis OK), wenn nichts eingerichtet war.

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>Beispielausgabe</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Removed': True}}
```

</details>


### Hilfsfunktionen

#### Ist .tr-Domain

Ist dies eine .tr-Domain? Lokale Prüfung, kein Netzwerkaufruf.

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>Beispielausgabe</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Kontakt validieren

Einen Kontakt so vervollständigen und normalisieren, wie das Gateway ihn erwartet (lokal, kein Netzwerk): Fehlende Felder erhalten Platzhalter, aus Namen werden Ziffern/Satzzeichen entfernt, Telefonnummern werden in Nummer + Ländervorwahl aufgeteilt, State fällt auf City zurück.

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
<summary>Beispielausgabe</summary>

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


### Diagnose und Einstellungen

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

Ein eigener HTTP-Transport (Proxy-Behandlung, Logging, Tests) kann dem Konstruktor übergeben werden: jedes Objekt mit einer
Methode `send(request)`, die eine `domainnameapi.HttpResponse` zurückgibt:

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## Tests

Die Test-Suite benötigt keine Zugangsdaten und führt keine externen Netzwerkaufrufe aus:

```bash
python -m unittest discover -s tests -v
```

| Testdatei | Beschreibung |
|-----------|-------------|
| `tests/test_conformance.py` | Führt alle 134 Konformitäts-Fixtures von php-dna aus: dieselben Anfragen auf der Leitung, dieselben Rückgabewerte |
| `tests/test_edge_cases.py` | Zusätzliche, aus php-dna aufgezeichnete Grenzfälle (ungewöhnliche Gateway-Antworten und Eingaben) |
| `tests/test_http.py` | HTTP-Schicht: Header, Query-Strings, JSON-Bodys, Timeouts, Weiterleitungen |
| `tests/test_errors.py` | Fehlerzuordnung der Gateway-Antworten |
| `tests/test_telemetry.py` | Telemetrie-Payloads, Maskierung von Zugangsdaten, Opt-out |
| `tests/test_utils.py` | Hilfsfunktionen und PHP-kompatible Verarbeitung von Werten |

<hr style="border: 4px solid #000; border-style: dashed;">


## Rückgabe- und Fehlercodes mit Erklärungen

| Code | Beschreibung                                         | Details                                                                                                                                                         |
|------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1000 | Befehl erfolgreich abgeschlossen                     | Vorgang erfolgreich.                                                                                                                                            |
| 1001 | Befehl erfolgreich abgeschlossen; Aktion ausstehend  | Vorgang erfolgreich. Der Vorgang befindet sich jedoch derzeit zur Fertigstellung in der Warteschlange.                                                          |
| 2003 | Erforderlicher Parameter fehlt                       | Fehler wegen fehlendem Parameter. Zum Beispiel: keine Telefonnummer in den Kontaktinformationen.                                                                |
| 2105 | Objekt ist nicht für eine Verlängerung geeignet      | Der Domain-Status erlaubt keine Verlängerung, die Domain ist für Aktualisierungen gesperrt. Der Status darf nicht "clientupdateprohibited" sein. Kann auch an anderen Statusbedingungen liegen. |
| 2200 | Authentifizierungsfehler                             | Berechtigungsfehler: Der Sicherheitscode ist falsch oder die Domain ist bei einem anderen Registrar registriert.                                                 |
| 2302 | Objekt existiert bereits                             | Domainname oder Nameserver-Information existiert bereits in der Datenbank. Kann nicht registriert werden.                                                       |
| 2303 | Objekt existiert nicht                               | Domainname oder Nameserver-Information existiert nicht in der Datenbank. Eine Neuregistrierung ist erforderlich.                                                |
| 2304 | Objektstatus verhindert den Vorgang                  | Der Domain-Status erlaubt keine Aktualisierung, die Domain ist für Aktualisierungen gesperrt. Der Status darf nicht "clientupdateprohibited" sein. Kann auch an anderen Statusbedingungen liegen. |

| CODE | MELDUNG                                                                                                                              |
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

| CODE | MELDUNG                                                                                     |
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

| CODE | MELDUNG                                                                                                                              |
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


## Lizenz

Apache License 2.0 — siehe [LICENSE](LICENSE).
