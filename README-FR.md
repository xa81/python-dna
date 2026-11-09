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


# python-dna : client DomainNameAPI pour Python

Client Python pour l'API REST revendeur de [DomainNameAPI](https://www.domainnameapi.com) : recherche, enregistrement,
transfert et renouvellement de domaines, gestion des contacts, des serveurs de noms, des serveurs de noms enfants, des zones DNS et de la redirection d'URL.
Il s'agit d'un portage fidèle de [php-dna](https://github.com/domainreseller/php-dna) : mêmes méthodes, mêmes requêtes,
mêmes valeurs de retour, vérifié à l'aide des fixtures de conformité de php-dna.

## 📦 Téléchargement — utilisez toujours les Releases !

⬇️ **Téléchargez la dernière version testée ici : https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ N'utilisez **pas** le bouton vert **Code → Download ZIP** — il télécharge la branche de développement brute. Les paquets de release sont versionnés, testés et prêts pour la production.

## Guide d'Installation et d'Intégration

### Exigences Minimales

- Python 3.8 ou supérieur (3.12 recommandé)
- Aucun paquet tiers : la bibliothèque n'utilise que la bibliothèque standard de Python (`urllib`, `json`, `ssl`).

### A) Installation avec pip

```bash
pip install domainnameapi
```

### B) Installation d'un paquet de release

Téléchargez le wheel (`domainnameapi-1.0.0-py3-none-any.whl`) ou l'archive des sources depuis la
[dernière release](https://github.com/domainreseller/python-dna/releases/latest) et installez-le :

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### C) Utilisation directe des sources

Copiez le dossier `src/domainnameapi` à côté de votre code (ou ajoutez `src` à `PYTHONPATH`) et importez-le.
Le dossier [examples](examples) contient un script exécutable par méthode.

## 🔑 Identifiants API — Reseller ID et API Key

La bibliothèque communique avec l'API REST DomainNameAPI et n'a besoin que de deux identifiants, transmis au constructeur :

| Paramètre | Valeur |
|---|---|
| Premier | Reseller ID — UUID de la forme `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| Second | API Key |

> 💡 Vous trouverez votre **Reseller ID** et votre **API Key** dans votre panel DomainNameAPI, sous **Paramètres API**.
> ⚠️ Ce sont des **identifiants API** — vos identifiants de connexion au panel **ne fonctionneront pas** ici.

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

Les espaces en début et en fin d'identifiants sont supprimés automatiquement.

## Démarrage Rapide

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

Les noms de méthodes sont en snake_case (`get_details`, `register_with_contact_info`). Les noms de php-dna fonctionnent aussi
comme alias : le code porté depuis PHP peut conserver `dna.GetDetails(...)` ou `dna.getDetails(...)`.

## Valeurs de Retour et Gestion des Erreurs

Les méthodes renvoient de simples valeurs `dict`/`list` avec exactement les mêmes clés que php-dna. Elles ne lèvent **pas**
d'exception en cas de problème de passerelle ou de réseau ; vérifiez plutôt `result` :

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "...",
                              "GatewayCode": "Dna.DomainService:Domain:10007"}}
```

- `Code` vaut `API_<statut HTTP>` pour les erreurs de la passerelle (`API_400`, `API_404`, `API_429`, `API_500`, ...).
  Une réponse de redirection (identifiants incorrects) donne `API_302` avec le message `Invalid API credentials`.
- `GatewayCode` est ajouté aux erreurs `API_<status>` lorsque la passerelle a envoyé son propre code d'erreur (par exemple `Dna.DomainService:Domain:10007`), ce qui permet de distinguer « domaine introuvable » de « TLD non pris en charge ».
- `Message` est le message de la passerelle. Les corps d'erreur vides deviennent `HTTP <status> - <reason>`
  (par exemple `HTTP 429 - Too Many Requests`).
- `Details` contient les détails fournis par la passerelle (ou le corps brut de la réponse s'il n'y en a pas) ; les erreurs de validation sont aplaties en une liste lisible de champs,
  par exemple `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`.
- Les pannes réseau sont elles aussi des erreurs, jamais un succès vide : un délai dépassé renvoie `CURL_28` avec
  `Could not reach the DomainNameAPI service: the connection timed out. (...)` ; les échecs DNS, de connexion et TLS
  renvoient `CURL_6`, `CURL_7`, `CURL_35`/`CURL_60` avec `Curl error during request: ...`
  (numéros d'erreur curl, les mêmes codes que ceux renvoyés par php-dna). Les codes `API_` sont réservés aux statuts HTTP.
- Un refus est une erreur même lorsque la passerelle répond HTTP 200 : si l'enregistrement, le transfert ou le renouvellement revient avec `success: false`, la méthode renvoie `REGISTER_DOMAIN`, `TRANSFER_DOMAIN` ou `RENEW_DOMAIN` avec le message de la passerelle.
- Les indicateurs conservent les types de php-dna : `LockStatus` est la chaîne `"true"`/`"false"`, les prix sont des chaînes formatées
  (`"11.9900"`).

Quelques méthodes utilisent leur propre enveloppe, exactement comme dans php-dna :

| Méthode | En cas de succès | En cas d'échec |
|---|---|---|
| `check_availability` | une simple `list` de résultats | l'enveloppe `ERROR` |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `OperationResult: "FAILED"` avec `ErrorCode` (`API_<status>`, `CURL_<errno>` ou `BALANCE` pour une devise que le compte ne fournit pas) |
| `check_transfer` | `result: "OK"` uniquement si le domaine est transférable | `result: "ERROR"` avec `data` et `error` |
| `is_tr_tld`, `validate_contact` | valeurs simples (sans réseau) | — |

Seules les erreurs de programmation (par exemple passer une chaîne là où `set_resource_record_set` attend une liste)
lèvent une exception Python.

Les délais d'attente sont de 30 secondes par appel et de 10 secondes pour la connexion. Les redirections ne sont pas suivies.

## Mode Test (OTE)

Passez `True` comme troisième argument pour utiliser l'environnement de test `https://ote.domainresellerapi.com/api/v1`.
Les valeurs sous forme de chaîne issues de fichiers de configuration sont comprises : `"true"`, `"1"`, `"on"`, `"yes"` activent le mode test,
toute autre valeur (`"false"`, `"0"`, `"off"`, `""`) conserve l'environnement de production.

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## Rapports d'erreurs (télémétrie)

Lorsqu'un appel API échoue, la bibliothèque peut envoyer un rapport d'erreur au système de suivi des erreurs propre à DomainNameAPI
(Sentry). Une petite part aléatoire des appels réussis (4 %, plus chaque appel de plus d'une seconde) est envoyée comme
enregistrement de performance. Cela aide DomainNameAPI à trouver et corriger les problèmes. Les rapports d'erreurs sont **activés par défaut**.

> ℹ️ Dans la version 1.0.0, l'adresse Sentry intégrée est encore vide, car le projet Sentry pour
> python-dna n'a pas encore été créé : **rien n'est envoyé** tant qu'une mise à jour de la bibliothèque ne l'a pas renseignée, ou tant que vous
> ne fournissez pas votre propre adresse avec `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")`.

Les rapports sont envoyés depuis un thread d'arrière-plan : ils ne ralentissent ni n'interrompent jamais votre appel.
Les erreurs attendues et très fréquentes (domaine introuvable, solde insuffisant, identifiants invalides, aucune redirection configurée, ...) ne sont jamais
signalées.

**Ce qui est envoyé :**

- le code et le message d'erreur
- le chemin du point de terminaison appelé et la méthode HTTP
- la durée de l'appel
- le nom de la bibliothèque (`DomainNameAPI-Python`), la version de la bibliothèque et la version de Python
- l'ID revendeur et le nom de domaine
- l'adresse IP publique du serveur (obtenue via `api.ipify.org`) et le nom d'utilisateur du système d'exploitation
- la requête et la réponse API, y compris les coordonnées de contact du domaine ; seuls les identifiants sont masqués — les codes EPP/auth, clés API, mots de passe et jetons sont remplacés par `***`

**Ce qui n'est jamais envoyé :** les codes EPP/auth, clés API, mots de passe ou jetons sous forme lisible ; les arguments des appels de fonction dans les traces de pile (stack traces).

**Pourquoi et combien de temps :** les données servent uniquement à mesurer l'utilisation et à diagnostiquer les problèmes au plus tôt ; elles sont conservées 30 jours sur le serveur Sentry propre à DomainNameAPI, puis supprimées automatiquement.

**Comment le désactiver :** appelez `set_error_reporting_enabled(False)` après avoir créé le client :

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**Mode minimal :** `set_telemetry_minimal(True)` n'envoie que le code et le message d'erreur, le point de terminaison, la durée,
les versions et l'ID revendeur — aucune donnée de requête/réponse, ni domaine, ni adresse IP, ni nom d'utilisateur.

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **Sécurité :** la vérification des certificats TLS est activée. Sur un serveur dont le bundle CA est obsolète, elle peut être désactivée avec `dna.set_ssl_verification(False)` — déconseillé ; mettre à jour le bundle CA est la meilleure solution.

## Utilisation

Tous les exemples ci-dessous supposent :

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

Les exemples de sortie sont de véritables valeurs de retour de la bibliothèque.

### Compte

#### Obtenir les Détails du Revendeur

Détails du compte revendeur : ID, nom et soldes (USD et TL).

```python
result = dna.get_reseller_details()
```

<details>
<summary>Exemple de sortie</summary>

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

#### Obtenir le Solde Actuel

Solde actuel dans une devise : USD (par défaut) ou TRY. Une devise que le compte ne fournit pas (EUR, GBP, ...) renvoie OperationResult FAILED avec ErrorCode BALANCE.

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>Exemple de sortie</summary>

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


### Recherche et Listes

#### Vérification de Disponibilité de Domaine

Disponibilité et prix de chaque combinaison domaine + extension. Renvoie une simple liste en cas de succès, une enveloppe d'erreur en cas d'échec.

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>Exemple de sortie</summary>

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

#### Liste des Domaines

Domaines du compte revendeur. Filtres : PageNumber (à partir de 0), PageSize, OrderColumn, OrderDirection, DomainName ...

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>Exemple de sortie</summary>

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

#### Liste des TLD

Liste des TLD avec les prix par période (enregistrement, renouvellement, transfert, restauration ...).

```python
result = dna.get_tld_list(100)
```

<details>
<summary>Exemple de sortie</summary>

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


### Domaines

#### Enregistrement de Domaine

Enregistre un nouveau domaine. Les contacts peuvent être fournis à plat (`AddressLine1`, `Phone`, ...) ou imbriqués (`Address.Line1`, `Phone.Phone.Number`, ...). Les champs manquants sont complétés et les numéros de téléphone sont normalisés (voir `validate_contact`). Une liste de serveurs de noms vide se rabat sur `ns1.domainnameapi.com` / `ns2.domainnameapi.com`.

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
<summary>Exemple de sortie</summary>

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

#### Enregistrement de Domaine (.tr)

Les domaines `.tr` nécessitent des attributs TRABIS comme 7e argument. Titulaire particulier : `TRABISDOMAINCATEGORY` = `1` et `TRABISCITIZENID` (numéro d'identité). Titulaire société : `TRABISDOMAINCATEGORY` = `0`, `TRABISTAXOFFICE` et `TRABISTAXNUMBER`. Les anciennes clés (`TRABISCITIZIENID`, `TRABISNAMESURNAME`, `TRABISCOUNTRYID`, ...) sont acceptées : elles sont converties vers le schéma REST, celles qui ne sont pas prises en charge sont ignorées.

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
<summary>Exemple de sortie</summary>

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

#### Renouvellement de Domaine

Renouvelle un domaine pour le nombre d'années indiqué.

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Détails du Domaine

Détails complets d'un domaine : statut, dates, serveurs de noms, indicateurs de verrouillage/confidentialité, serveurs de noms enfants.

```python
result = dna.get_details("example.com")
```

<details>
<summary>Exemple de sortie</summary>

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

#### Synchronisation depuis le Registre

Actualise un domaine depuis le registre (même enveloppe que get_details).

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>Exemple de sortie</summary>

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

#### Modifier les Serveurs de Noms

Remplace les serveurs de noms d'un domaine (les entrées sont épurées des espaces, mises en minuscules et dédoublonnées).

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Activer le Verrouillage de Domaine

Active le verrou du registraire (protection contre le vol).

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Désactiver le Verrouillage de Domaine

Désactive le verrou du registraire (protection contre le vol).

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Modifier la Protection de la Vie Privée

Active (True) ou désactive (False) la protection de la confidentialité WHOIS. 1, "1", "on", "true" et "yes" signifient aussi activé ; toute autre valeur signifie désactivé. L'argument reason n'est pas envoyé à la passerelle.

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### Contacts

#### Obtenir les Contacts du Domaine

Contacts administratif, de facturation, titulaire et technique d'un domaine.

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>Exemple de sortie</summary>

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

#### Sauvegarder les Contacts du Domaine

Remplace les quatre contacts d'un domaine. `contacts` est le même dictionnaire que dans l'exemple d'enregistrement.

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### Serveurs de Noms Enfants

#### Ajouter un Serveur de Noms Enfant

Crée un serveur de noms enfant (enregistrement glue) sous un domaine.

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Supprimer un Serveur de Noms Enfant

Supprime un serveur de noms enfant.

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Modifier un Serveur de Noms Enfant

Modifie l'adresse IP d'un serveur de noms enfant.

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### Transferts

#### Transfert de Domaine

Lance un transfert entrant avec le code EPP/auth du domaine. Aucun contact n'est jamais envoyé avec un transfert (la requête contient toujours `"contacts": []`) : le registraire les reprend du registraire sortant, `transfer` n'a donc pas de paramètre contacts. Un refus (`success: false`) renvoie une erreur `TRANSFER_DOMAIN`.

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>Exemple de sortie</summary>

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

#### Vérifier le Transfert

Le domaine peut-il être transféré avec ce code d'autorisation ? result vaut OK uniquement si c'est le cas.

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>Exemple de sortie</summary>

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

#### Annuler le Transfert

Annule un transfert entrant en attente.

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Approuver un Transfert Sortant

Approuve un transfert sortant en attente.

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Rejeter un Transfert Sortant

Rejette un transfert sortant en attente.

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### Zone DNS

La passerelle stocke les enregistrements DNS sous forme d'**ensembles** : un nom + type contient une liste de valeurs. Écrire un nom + type
remplace l'ensemble entier, et supprimer par une seule valeur supprime l'ensemble entier. Les méthodes `*_record_set` et
`*_record_value` gèrent cela pour vous ; préférez-les aux méthodes bas niveau `add/edit/delete_resource_record`.

- Les noms peuvent être donnés sous la forme `"@"`, `""`, `"www"`, `"www.example.com"` ou `"www.example.com."` ; ils sont envoyés sous forme
  du libellé relatif attendu par la passerelle. `get_resource_records` renvoie des noms pleinement qualifiés (`"www.example.com."`).
- Types pris en charge : `A`, `AAAA`, `ALIAS`, `CAA`, `CNAME`, `DS`, `MX`, `NAPTR`, `PTR`, `SRV`, `TLSA`, `TXT`
  (les autres sont rejetés avant tout appel). Le TTL va de 1 à 86400 secondes.
- Les écritures sont appliquées immédiatement ; passez `apply=False` pour préparer plusieurs modifications puis appelez
  `apply_resource_records` une seule fois. Si l'application automatique échoue, la méthode renvoie l'erreur d'application (la modification reste préparée mais n'est pas active).
- La passerelle limite le débit des appels de zone ; la bibliothèque espace donc les appels de zone d'au moins une seconde
  (`dna.zone_min_interval`, en secondes).


#### Lister les Enregistrements

Zone DNS d'un domaine, une ligne par valeur d'enregistrement. Les noms sont renvoyés pleinement qualifiés.

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>Exemple de sortie</summary>

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

#### Définir un Ensemble d'Enregistrements

Rend un nom + type entier exactement identique à la liste fournie (le modèle propre à la passerelle). Une liste vide supprime l'ensemble. Les modifications sont appliquées immédiatement, sauf avec apply=False.

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
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Ajouter une Valeur

Ajoute UNE valeur à un ensemble d'enregistrements en conservant les valeurs déjà présentes (lecture-fusion-écriture). Ajouter une valeur déjà présente n'a aucun effet.

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>Exemple de sortie</summary>

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

#### Supprimer une Valeur

Supprime UNE valeur d'un ensemble d'enregistrements en laissant les autres en place.

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Remplacer une Valeur

Remplace UNE valeur d'un ensemble d'enregistrements par une autre (la « modification de ligne » d'un panneau DNS).

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Supprimer un Ensemble d'Enregistrements

Supprime toutes les valeurs d'un nom + type. Supprimer un ensemble inexistant ne pose pas de problème.

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Ajouter un Enregistrement (bas niveau)

Bas niveau : écrit un ensemble d'enregistrements (POST). La passerelle remplace un nom + type existant ; préférez donc add_resource_record_value() pour ajouter une valeur.

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Modifier un Enregistrement (bas niveau)

Bas niveau : réécrit un ensemble d'enregistrements existant (PUT), identifié par son nom actuel.

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Supprimer un Enregistrement (bas niveau)

Bas niveau : DELETE par nom + valeur + type. La passerelle supprime l'ensemble ENTIER ; préférez donc remove_resource_record_value() pour retirer une seule valeur.

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Appliquer les Modifications en Attente

Valide les modifications de zone préparées (nécessaire uniquement après des appels effectués avec apply=False).

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### Redirection d'URL

#### Obtenir la Redirection

Redirection d'URL d'un domaine. Enabled vaut False lorsque rien n'est configuré.

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Définir la Redirection

Redirige le domaine vers une URL : 'Standard' (redirection simple) ou 'Frame' (masquée).

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Supprimer la Redirection

Supprime la redirection d'URL. Removed vaut False (et le résultat est OK) lorsque rien n'était configuré.

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>Exemple de sortie</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Removed': True}}
```

</details>


### Utilitaires

#### Est-ce un Domaine .tr

S'agit-il d'un domaine .tr ? Vérification locale, sans appel réseau.

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>Exemple de sortie</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Valider un Contact

Complète et normalise un contact tel que la passerelle l'attend (en local, sans réseau) : les champs manquants reçoivent des valeurs par défaut, les noms perdent leurs chiffres et leur ponctuation, les numéros de téléphone sont séparés en numéro + indicatif pays, State se rabat sur City.

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
<summary>Exemple de sortie</summary>

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


### Diagnostic et Paramètres

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

Un transport HTTP personnalisé (gestion de proxy, journalisation, tests) peut être passé au constructeur : n'importe quel objet doté d'une
méthode `send(request)` qui renvoie un `domainnameapi.HttpResponse` :

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## Tests

La suite de tests ne nécessite aucun identifiant et n'effectue aucun appel réseau externe :

```bash
python -m unittest discover -s tests -v
```

| Fichier de test | Description |
|-----------------|-------------|
| `tests/test_conformance.py` | Exécute les 134 fixtures de conformité de php-dna : mêmes requêtes sur le réseau, mêmes valeurs de retour |
| `tests/test_edge_cases.py` | Cas limites supplémentaires enregistrés depuis php-dna (réponses et entrées inhabituelles de la passerelle) |
| `tests/test_http.py` | Couche HTTP : en-têtes, chaînes de requête, corps JSON, délais d'attente, redirections |
| `tests/test_errors.py` | Correspondance des erreurs pour les réponses de la passerelle |
| `tests/test_telemetry.py` | Données de télémétrie, masquage des identifiants, désactivation |
| `tests/test_utils.py` | Utilitaires et gestion des valeurs compatible PHP |

<hr style="border: 4px solid #000; border-style: dashed;">


## Codes de Retour et d'Erreur avec Descriptions

| Code | Description | Détail |
|------|-------------|--------|
| 1000 | Commande complétée avec succès | Opération réussie. |
| 1001 | Commande complétée avec succès ; action en attente | Opération réussie. Cependant, l'opération est actuellement en file d'attente pour être finalisée. |
| 2003 | Paramètre requis manquant | Erreur de paramètre manquant. Par exemple : aucun numéro de téléphone dans les informations de contact. |
| 2105 | L'objet n'est pas éligible pour le renouvellement | Le statut du domaine n'est pas adapté au renouvellement, verrouillé pour les opérations de mise à jour. Le statut ne doit pas être "clientupdateprohibited". Peut être dû à d'autres conditions de statut. |
| 2200 | Erreur d'authentification | Erreur d'autorisation, code de sécurité incorrect ou domaine enregistré auprès d'un autre registraire. |
| 2302 | L'objet existe | Le nom de domaine ou les informations de serveur de noms existent déjà dans la base de données. Enregistrement impossible. |
| 2303 | L'objet n'existe pas | Le nom de domaine ou les informations de serveur de noms n'existent pas dans la base de données. Un nouvel enregistrement est requis. |
| 2304 | Le statut de l'objet interdit l'opération | Le statut du domaine n'est pas adapté aux mises à jour, verrouillé pour les opérations de mise à jour. Le statut ne doit pas être "clientupdateprohibited". Peut être dû à d'autres conditions de statut. |

| CODE | DÉTAIL                                                                                                                               |
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

| CODE | DÉTAIL                                                                                      |
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

| CODE | DÉTAIL                                                                                                                               |
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


## Licence

Apache License 2.0 — voir [LICENSE](LICENSE).
