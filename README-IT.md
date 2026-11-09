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


# python-dna: client DomainNameAPI per Python

Client Python per l'API REST per rivenditori di [DomainNameAPI](https://www.domainnameapi.com): ricerca, registrazione,
trasferimento e rinnovo di domini, gestione di contatti, name server, child name server, zone DNS e inoltro URL.
È un porting fedele di [php-dna](https://github.com/domainreseller/php-dna): stessi metodi, stesse richieste,
stessi valori di ritorno, verificato con le fixture di conformità di php-dna.

## 📦 Download — usa sempre le Releases!

⬇️ **Scarica l'ultima versione testata qui: https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ **Non** usare il pulsante verde **Code → Download ZIP** — scarica il branch di sviluppo grezzo. I pacchetti di release sono versionati, testati e pronti per la produzione.

## Guida all'Installazione e Integrazione

### Requisiti Minimi

- Python 3.8 o superiore (consigliato 3.12)
- Nessun pacchetto di terze parti: la libreria usa solo la libreria standard di Python (`urllib`, `json`, `ssl`).

### A) Installazione con pip

```bash
pip install domainnameapi
```

### B) Installazione da un pacchetto di release

Scarica il wheel (`domainnameapi-1.0.0-py3-none-any.whl`) o l'archivio dei sorgenti dall'
[ultima release](https://github.com/domainreseller/python-dna/releases/latest) e installalo:

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### C) Uso diretto dei sorgenti

Copia la cartella `src/domainnameapi` accanto al tuo codice (oppure aggiungi `src` a `PYTHONPATH`) e importala.
La cartella [examples](examples) contiene uno script eseguibile per ogni metodo.

## 🔑 Credenziali API — Reseller ID e API Key

La libreria comunica con l'API REST di DomainNameAPI e richiede esattamente due credenziali, passate al costruttore:

| Parametro | Valore |
|---|---|
| Primo | Reseller ID — UUID nel formato `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| Secondo | API Key |

> 💡 Trovi il tuo **Reseller ID** e la tua **API Key** nel pannello DomainNameAPI, in **Impostazioni API**.
> ⚠️ Queste sono **credenziali API** — i dati di accesso al pannello **non** funzioneranno qui.

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

Gli spazi iniziali e finali delle credenziali vengono rimossi automaticamente.

## Avvio Rapido

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

I nomi dei metodi sono in snake_case (`get_details`, `register_with_contact_info`). Anche i nomi di php-dna funzionano come
alias, quindi il codice portato da PHP può mantenere `dna.GetDetails(...)` o `dna.getDetails(...)`.

## Valori di Ritorno e Gestione degli Errori

I metodi restituiscono semplici valori `dict`/`list` con esattamente le stesse chiavi di php-dna. **Non** sollevano
eccezioni per problemi del gateway o di rete; controlla invece `result`:

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "..."}}
```

- `Code` è `API_<stato HTTP>` per gli errori del gateway (`API_400`, `API_404`, `API_429`, `API_500`, ...).
  Una risposta di reindirizzamento (credenziali errate) restituisce `API_302` con il messaggio `Invalid API credentials`.
- `Message` è il messaggio del gateway. I corpi di errore vuoti diventano `HTTP <status> - <reason>`
  (ad esempio `HTTP 429 - Too Many Requests`).
- `Details` contiene i dettagli del gateway; gli errori di validazione vengono appiattiti in un elenco leggibile di campi,
  ad esempio `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`.
- Anche i guasti di rete sono errori, mai un successo vuoto: un timeout restituisce `API_28` con
  `Could not reach the DomainNameAPI service: the connection timed out. (...)`; gli errori DNS, di connessione e TLS
  restituiscono `API_6`, `API_7`, `API_35`/`API_60` con `Curl error during request: ...`
  (numeri di errore curl, gli stessi codici riportati da php-dna).
- I flag mantengono i tipi di php-dna: `LockStatus` è la stringa `"true"`/`"false"`, i prezzi sono stringhe formattate
  (`"11.9900"`).

Alcuni metodi usano una propria struttura di risposta, esattamente come in php-dna:

| Metodo | In caso di successo | In caso di errore |
|---|---|---|
| `check_availability` | una semplice `list` di risultati | la struttura `ERROR` |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `OperationResult: "FAILED"` con `ErrorCode` |
| `check_transfer` | `result: "OK"` solo quando il dominio è trasferibile | `result: "ERROR"` con `data` e `error` |
| `is_tr_tld`, `validate_contact` | valori semplici (nessuna chiamata di rete) | — |

Solo gli errori di programmazione (ad esempio passare una stringa dove `set_resource_record_set` si aspetta una lista)
sollevano un'eccezione Python.

I timeout sono di 30 secondi per chiamata e di 10 secondi per la connessione. I reindirizzamenti non vengono seguiti.

## Modalità Test (OTE)

Passa `True` come terzo argomento per usare l'ambiente di test `https://ote.domainresellerapi.com/api/v1`.
Vengono riconosciuti anche i valori stringa provenienti dai file di configurazione: `"true"`, `"1"`, `"on"`, `"yes"` attivano la modalità test,
qualsiasi altro valore (`"false"`, `"0"`, `"off"`, `""`) mantiene l'ambiente live.

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## Segnalazione errori (telemetria)

Quando una chiamata API fallisce, la libreria può inviare una segnalazione di errore al sistema di tracciamento errori di DomainNameAPI
(Sentry). Una piccola quota casuale delle chiamate riuscite (4%, più ogni chiamata che dura più di 1 secondo) viene inviata come
record di prestazioni. Questo aiuta DomainNameAPI a trovare e correggere i problemi. La segnalazione errori è **attiva per impostazione predefinita**.

> ℹ️ Nella versione 1.0.0 l'indirizzo Sentry integrato è ancora vuoto, perché il progetto Sentry per
> python-dna non è ancora stato creato: **non viene inviato nulla** finché un aggiornamento della libreria non lo imposta, oppure finché non
> passi un tuo indirizzo con `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")`.

Le segnalazioni vengono inviate da un thread in background: non rallentano né interrompono mai la tua chiamata.
Gli errori previsti e molto frequenti (dominio non trovato, saldo insufficiente, credenziali non valide, ...) non vengono mai
segnalati.

**Cosa viene inviato:**

- codice e messaggio di errore
- percorso dell'endpoint chiamato e metodo HTTP
- durata della chiamata
- nome della libreria (`DomainNameAPI-Python`), versione della libreria e versione di Python
- ID rivenditore e nome di dominio
- l'indirizzo IP pubblico del server (ricavato tramite `api.ipify.org`) e il nome utente del sistema operativo
- la richiesta e la risposta API, inclusi i dati di contatto del dominio; vengono mascherate solo le credenziali — codici EPP/auth, chiavi API, password e token vengono sostituiti con `***`

**Cosa non viene mai inviato:** codici EPP/auth, chiavi API, password o token in forma leggibile; argomenti delle chiamate di funzione negli stack trace.

**Perché e per quanto tempo:** i dati vengono usati solo per misurare l'utilizzo e diagnosticare tempestivamente i problemi, e sono conservati per 30 giorni sul server Sentry di DomainNameAPI, dopodiché vengono eliminati automaticamente.

**Come disattivarla:** chiama `set_error_reporting_enabled(False)` dopo aver creato il client:

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**Modalità minima:** `set_telemetry_minimal(True)` invia solo codice e messaggio di errore, endpoint, tempi,
versioni e ID rivenditore — nessun dato di richiesta/risposta, dominio, indirizzo IP o nome utente.

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **Sicurezza:** la verifica dei certificati TLS è attiva. Su un server con un bundle CA obsoleto può essere disattivata con `dna.set_ssl_verification(False)` — sconsigliato; aggiornare il bundle CA è la soluzione migliore.

## Utilizzo

Tutti gli esempi seguenti presuppongono:

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

Gli output di esempio sono valori di ritorno reali della libreria.

### Account

#### Ottenere Dettagli Rivenditore

Dettagli dell'account rivenditore: ID, nome e saldi (USD e TL).

```python
result = dna.get_reseller_details()
```

<details>
<summary>Output di esempio</summary>

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

#### Ottenere il Saldo Attuale

Saldo attuale in una valuta: USD (predefinita), TRY, EUR o GBP.

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>Output di esempio</summary>

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


### Ricerca ed Elenchi

#### Verifica Disponibilità Dominio

Disponibilità e prezzo di ogni combinazione dominio + estensione. Restituisce una semplice lista in caso di successo, una struttura di errore in caso di errore.

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>Output di esempio</summary>

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

#### Elenco Domini

Domini presenti nell'account rivenditore. Filtri: PageNumber (a partire da 0), PageSize, OrderColumn, OrderDirection, DomainName ...

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>Output di esempio</summary>

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

#### Elenco TLD

Elenco dei TLD con i prezzi per periodo (registrazione, rinnovo, trasferimento, ripristino ...).

```python
result = dna.get_tld_list(100)
```

<details>
<summary>Output di esempio</summary>

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


### Domini

#### Registrazione Dominio

Registra un nuovo dominio. I contatti possono essere forniti in forma piatta (`AddressLine1`, `Phone`, ...) o annidata (`Address.Line1`, `Phone.Phone.Number`, ...). I campi mancanti vengono completati e i numeri di telefono normalizzati (vedi `validate_contact`). Se l'elenco dei name server è vuoto, vengono usati `ns1.domainnameapi.com` / `ns2.domainnameapi.com`.

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
<summary>Output di esempio</summary>

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

#### Registrazione Dominio (.tr)

I domini `.tr` richiedono gli attributi TRABIS come 7° argomento. Titolare persona fisica: `TRABISDOMAINCATEGORY` = `1` e `TRABISCITIZENID` (numero di identità). Titolare azienda: `TRABISDOMAINCATEGORY` = `0`, `TRABISTAXOFFICE` e `TRABISTAXNUMBER`. Le chiavi legacy (`TRABISCITIZIENID`, `TRABISNAMESURNAME`, `TRABISCOUNTRYID`, ...) sono accettate: vengono convertite nello schema REST e quelle non supportate vengono scartate.

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
<summary>Output di esempio</summary>

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

#### Rinnovo Dominio

Rinnova un dominio per il numero di anni indicato.

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Dettagli Dominio

Dettagli completi di un dominio: stato, date, name server, flag di blocco/privacy, child name server.

```python
result = dna.get_details("example.com")
```

<details>
<summary>Output di esempio</summary>

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

#### Sincronizzazione dal Registro

Aggiorna un dominio dal registro (stessa struttura di get_details).

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>Output di esempio</summary>

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

#### Modifica Name Server

Sostituisce i name server di un dominio (le voci vengono ripulite dagli spazi, convertite in minuscolo e deduplicate).

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Attivare il Blocco Dominio

Attiva il blocco del registrar (protezione contro il furto).

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Disattivare il Blocco Dominio

Disattiva il blocco del registrar (protezione contro il furto).

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Modificare Protezione Privacy

Attiva (True) o disattiva (False) la protezione della privacy WHOIS.

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>Output di esempio</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### Contatti

#### Ottenere i Contatti del Dominio

Contatti amministrativo, di fatturazione, titolare e tecnico di un dominio.

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>Output di esempio</summary>

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

#### Salvare i Contatti del Dominio

Sostituisce i quattro contatti di un dominio. `contacts` è lo stesso dizionario dell'esempio di registrazione.

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### Child Name Server

#### Aggiungere Child Name Server

Crea un child name server (record glue) sotto un dominio.

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eliminare Child Name Server

Elimina un child name server.

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Modificare Child Name Server

Cambia l'indirizzo IP di un child name server.

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### Trasferimenti

#### Trasferimento Dominio

Avvia un trasferimento in entrata con il codice EPP/auth del dominio. Come nella facade di php-dna, il quarto argomento opzionale (`contacts`) viene accettato ma non inviato; usa `dna.client.transfer(domain, code, period, contacts)` per inviare i contatti insieme al trasferimento.

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>Output di esempio</summary>

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

#### Verifica Trasferimento

Il dominio può essere trasferito con questo codice auth? result è OK solo quando è possibile.

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>Output di esempio</summary>

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

#### Annullare il Trasferimento

Annulla un trasferimento in entrata in sospeso.

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Approvare un Trasferimento in Uscita

Approva un trasferimento in uscita in sospeso.

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Rifiutare un Trasferimento in Uscita

Rifiuta un trasferimento in uscita in sospeso.

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### Zona DNS

Il gateway memorizza i record DNS come **insiemi**: un nome + tipo contiene un elenco di valori. Scrivere un nome + tipo
sostituisce l'intero insieme, ed eliminare tramite un singolo valore rimuove l'intero insieme. I metodi `*_record_set` e
`*_record_value` gestiscono tutto questo per te; preferiscili ai metodi di basso livello `add/edit/delete_resource_record`.

- I nomi possono essere indicati come `"@"`, `""`, `"www"`, `"www.example.com"` o `"www.example.com."`; vengono inviati come
  l'etichetta relativa che il gateway si aspetta. `get_resource_records` restituisce nomi completamente qualificati (`"www.example.com."`).
- Tipi supportati: `A`, `AAAA`, `ALIAS`, `CAA`, `CNAME`, `DS`, `MX`, `NAPTR`, `PTR`, `SRV`, `TLSA`, `TXT`
  (gli altri vengono rifiutati prima di qualsiasi chiamata). Il TTL va da 1 a 86400 secondi.
- Le scritture vengono applicate immediatamente; passa `apply=False` per preparare più modifiche e chiama poi
  `apply_resource_records` una sola volta.
- Il gateway limita la frequenza delle chiamate sulla zona, quindi la libreria distanzia le chiamate sulla zona di almeno un secondo
  (`dna.zone_min_interval`, in secondi).


#### Elencare i Record

Zona DNS di un dominio, una riga per ogni valore di record. I nomi vengono restituiti completamente qualificati.

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>Output di esempio</summary>

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

#### Impostare un Insieme di Record

Rende un intero nome + tipo esattamente uguale all'elenco fornito (il modello proprio del gateway). Un elenco vuoto rimuove l'insieme. Le modifiche vengono applicate immediatamente, a meno di apply=False.

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
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Aggiungere un Valore

Aggiunge UN valore a un insieme di record mantenendo i valori già presenti (lettura-unione-scrittura). Aggiungere un valore già presente non ha alcun effetto.

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>Output di esempio</summary>

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

#### Rimuovere un Valore

Rimuove UN valore da un insieme di record, lasciando invariati gli altri.

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Sostituire un Valore

Sostituisce UN valore di un insieme di record con un altro (la "modifica riga" di un pannello DNS).

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eliminare un Insieme di Record

Rimuove tutti i valori di un nome + tipo. Rimuovere un insieme inesistente non è un errore.

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Aggiungere un Record (basso livello)

Basso livello: scrive un insieme di record (POST). Il gateway sostituisce un nome + tipo esistente, quindi per aggiungere un valore preferisci add_resource_record_value().

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'a', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Modificare un Record (basso livello)

Basso livello: riscrive un insieme di record esistente (PUT), identificato dal suo nome attuale.

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eliminare un Record (basso livello)

Basso livello: DELETE per nome + valore + tipo. Il gateway rimuove l'INTERO insieme, quindi per eliminare un singolo valore preferisci remove_resource_record_value().

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Applicare le Modifiche in Sospeso

Conferma le modifiche alla zona preparate (necessario solo dopo chiamate eseguite con apply=False).

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### Inoltro URL

#### Ottenere l'Inoltro

Inoltro URL di un dominio. Enabled è False quando non è configurato nulla.

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Impostare l'Inoltro

Inoltra il dominio a un URL: 'Standard' (reindirizzamento semplice) o 'Frame' (mascherato).

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Eliminare l'Inoltro

Rimuove l'inoltro URL.

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>Output di esempio</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### Utilità

#### È un Dominio .tr

Si tratta di un dominio .tr? Verifica locale, nessuna chiamata di rete.

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>Output di esempio</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Validare un Contatto

Completa e normalizza un contatto nel formato atteso dal gateway (in locale, senza rete): i campi mancanti ricevono valori segnaposto, dai nomi vengono rimosse cifre e punteggiatura, i numeri di telefono vengono separati in numero + prefisso internazionale, State ricade su City.

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
<summary>Output di esempio</summary>

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


### Diagnostica e Impostazioni

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

Al costruttore si può passare un trasporto HTTP personalizzato (gestione proxy, logging, test): qualsiasi oggetto con un
metodo `send(request)` che restituisce un `domainnameapi.HttpResponse`:

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## Test

La suite di test non richiede credenziali e non effettua chiamate di rete esterne:

```bash
python -m unittest discover -s tests -v
```

| File di test | Descrizione |
|--------------|-------------|
| `tests/test_conformance.py` | Esegue tutte le 126 fixture di conformità di php-dna: stesse richieste in rete, stessi valori di ritorno |
| `tests/test_edge_cases.py` | Casi limite aggiuntivi registrati da php-dna (risposte e input insoliti del gateway) |
| `tests/test_http.py` | Livello HTTP: header, query string, corpi JSON, timeout, reindirizzamenti |
| `tests/test_errors.py` | Mappatura degli errori delle risposte del gateway |
| `tests/test_telemetry.py` | Payload di telemetria, mascheramento delle credenziali, disattivazione |
| `tests/test_utils.py` | Utilità e gestione dei valori compatibile con PHP |

<hr style="border: 4px solid #000; border-style: dashed;">


## Codici di Ritorno ed Errore con Descrizioni

| Codice | Descrizione | Dettaglio |
|--------|-------------|-----------|
| 1000 | Comando completato con successo | Operazione riuscita. |
| 1001 | Comando completato con successo; azione in sospeso | Operazione riuscita. Tuttavia, l'operazione è attualmente in coda per il completamento. |
| 2003 | Parametro richiesto mancante | Errore di parametro mancante. Ad esempio: nessun numero di telefono nelle informazioni di contatto. |
| 2105 | L'oggetto non è idoneo al rinnovo | Lo stato del dominio non è adatto al rinnovo, bloccato per le operazioni di aggiornamento. Lo stato non dovrebbe essere "clientupdateprohibited". Potrebbe dipendere da altre condizioni di stato. |
| 2200 | Errore di autenticazione | Errore di autorizzazione, codice di sicurezza errato o dominio registrato presso un altro registrar. |
| 2302 | L'oggetto esiste | Il nome di dominio o le informazioni del name server esistono già nel database. Non può essere registrato. |
| 2303 | L'oggetto non esiste | Il nome di dominio o le informazioni del name server non esistono nel database. È necessaria una nuova registrazione. |
| 2304 | Lo stato dell'oggetto vieta l'operazione | Lo stato del dominio non è adatto agli aggiornamenti, bloccato per le operazioni di aggiornamento. Lo stato non dovrebbe essere "clientupdateprohibited". Potrebbe dipendere da altre condizioni di stato. |

| CODICE | DETTAGLIO                                                                                                                            |
|--------|--------------------------------------------------------------------------------------------------------------------------------------|
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

| CODICE | DETTAGLIO                                                                                   |
|--------|---------------------------------------------------------------------------------------------|
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

| CODICE | DETTAGLIO                                                                                                                            |
|--------|--------------------------------------------------------------------------------------------------------------------------------------|
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


## Licenza

Apache License 2.0 — vedi [LICENSE](LICENSE).
