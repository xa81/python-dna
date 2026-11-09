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


# python-dna: Python üçün DomainNameAPI klienti

[DomainNameAPI](https://www.domainnameapi.com) reseller REST API-si üçün Python klienti: domenləri axtarın, qeydiyyatdan keçirin,
transfer edin və yeniləyin; əlaqələri, nameserver-ləri, child nameserver-ləri, DNS zonalarını və URL yönləndirməsini idarə edin.
Bu, [php-dna](https://github.com/domainreseller/php-dna) kitabxanasının dəqiq portudur: eyni metodlar, eyni sorğular,
eyni qaytarılan dəyərlər; php-dna-nın uyğunluq (conformance) fixture-ları ilə yoxlanılıb.

## 📦 Yükləmə — həmişə Releases istifadə edin!

⬇️ **Ən son test edilmiş versiyanı buradan əldə edin: https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ Yaşıl **Code → Download ZIP** düyməsindən **istifadə etməyin** — bu, xam inkişaf branch-ını yükləyir. Release paketləri versiyalanmış, test edilmiş və istehsalata hazırdır.

## Quraşdırma və İnteqrasiya Təlimatı

### Minimum Tələblər

- Python 3.8 və ya daha yuxarı (3.12 tövsiyə olunur)
- Üçüncü tərəf paketlər tələb olunmur: kitabxana yalnız Python standart kitabxanasından (`urllib`, `json`, `ssl`) istifadə edir.

### A) pip ilə quraşdırma

```bash
pip install domainnameapi
```

### B) Release paketi ilə quraşdırma

Wheel faylını (`domainnameapi-1.0.0-py3-none-any.whl`) və ya mənbə arxivini
[son buraxılış](https://github.com/domainreseller/python-dna/releases/latest) səhifəsindən yükləyin və quraşdırın:

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### C) Mənbə kodundan birbaşa istifadə

`src/domainnameapi` qovluğunu kodunuzun yanına kopyalayın (və ya `src` qovluğunu `PYTHONPATH`-a əlavə edin) və import edin.
[examples](examples) qovluğunda hər metod üçün işə salına bilən bir skript var.

## 🔑 API Məlumatları — Reseller ID və API Key

Kitabxana DomainNameAPI REST API ilə əlaqə saxlayır və konstruktora ötürülən yalnız iki məlumata ehtiyac duyur:

| Parametr | Dəyər |
|---|---|
| Birinci | Reseller ID — `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` formatında UUID |
| İkinci | API Key |

> 💡 **Reseller ID** və **API Key** məlumatlarınızı DomainNameAPI panelinizdə **API Parametrləri** bölməsində tapa bilərsiniz.
> ⚠️ Bunlar **API məlumatlarıdır** — panelə giriş məlumatlarınız burada **işləməyəcək**.

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

Məlumatların əvvəlindəki və sonundakı boşluqlar avtomatik olaraq silinir.

## Sürətli Başlanğıc

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

Metod adları snake_case formatındadır (`get_details`, `register_with_contact_info`). php-dna-dakı adlar da ləqəb (alias) kimi işləyir,
beləliklə PHP-dən köçürülmüş kod `dna.GetDetails(...)` və ya `dna.getDetails(...)` istifadə etməyə davam edə bilər.

## Qaytarılan Dəyərlər və Xətaların İdarə Edilməsi

Metodlar php-dna-nın qaytardığı açarların eynisini daşıyan sadə `dict`/`list` dəyərləri qaytarır. Gateway və ya şəbəkə problemlərində
exception **atmırlar**; bunun əvəzinə `result` dəyərini yoxlayın:

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "...",
                              "GatewayCode": "Dna.DomainService:Domain:10007"}}
```

- `Code` gateway xətalarında `API_<HTTP status>` formatındadır (`API_400`, `API_404`, `API_429`, `API_500`, ...).
  Yönləndirmə (redirect) cavabı (səhv API məlumatları) `Invalid API credentials` mesajı ilə `API_302` qaytarır.
- Gateway öz xəta kodunu göndərdikdə (məsələn, `Dna.DomainService:Domain:10007`) `API_<status>` xətalarına `GatewayCode` əlavə olunur; beləliklə "domen tapılmadı" ilə "TLD dəstəklənmir" xətalarını ayırd edə bilərsiniz.
- `Message` gateway-in mesajıdır. Boş xəta gövdələri `HTTP <status> - <reason>` formatına çevrilir
  (məsələn, `HTTP 429 - Too Many Requests`).
- `Details` gateway-in təfərrüatlarını (olmadıqda isə xam cavab gövdəsini) saxlayır; validasiya xətaları sahələrin oxunaqlı siyahısına çevrilir,
  məsələn, `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`.
- Şəbəkə nasazlıqları da xəta kimi qaytarılır, heç vaxt boş uğurlu cavab kimi yox: vaxt aşımı zamanı
  `Could not reach the DomainNameAPI service: the connection timed out. (...)` mesajı ilə `CURL_28` qaytarılır; DNS, bağlantı və TLS
  nasazlıqları `Curl error during request: ...` mesajı ilə `CURL_6`, `CURL_7`, `CURL_35`/`CURL_60` qaytarır
  (curl xəta nömrələri, php-dna-nın bildirdiyi kodların eynisi). `API_` kodları yalnız HTTP statusları üçün istifadə olunur.
- Gateway HTTP 200 ilə cavab versə belə, imtina xətadır: qeydiyyat, transfer və ya yeniləmə `success: false` ilə qayıdarsa, metod gateway-in mesajı ilə `REGISTER_DOMAIN`, `TRANSFER_DOMAIN` və ya `RENEW_DOMAIN` qaytarır.
- Bayraqlar php-dna-dakı tiplərini saxlayır: `LockStatus` `"true"`/`"false"` sətir dəyəridir, qiymətlər formatlanmış sətirlərdir
  (`"11.9900"`).

Bir neçə metod php-dna-da olduğu kimi öz cavab strukturundan (envelope) istifadə edir:

| Metod | Uğurlu olduqda | Uğursuz olduqda |
|---|---|---|
| `check_availability` | nəticələrdən ibarət sadə `list` | `ERROR` strukturu |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `ErrorCode` (`API_<status>`, `CURL_<errno>` və ya hesabın bildirmədiyi valyuta üçün `BALANCE`) ilə birlikdə `OperationResult: "FAILED"` |
| `check_transfer` | yalnız domen transfer edilə bildikdə `result: "OK"` | `data` və `error` ilə birlikdə `result: "ERROR"` |
| `is_tr_tld`, `validate_contact` | sadə dəyərlər (şəbəkə çağırışı yoxdur) | — |

Yalnız proqramlaşdırma xətaları (məsələn, `set_resource_record_set` siyahı gözlədiyi yerdə sətir ötürmək)
Python exception-ı atır.

Vaxt aşımı hər çağırış üçün 30 saniyə, bağlantı qurmaq üçün isə 10 saniyədir. Yönləndirmələrə (redirect) əməl edilmir.

## Test Rejimi (OTE)

`https://ote.domainresellerapi.com/api/v1` test mühitindən istifadə etmək üçün üçüncü arqument kimi `True` ötürün.
Konfiqurasiya fayllarından gələn sətir dəyərləri də başa düşülür: `"true"`, `"1"`, `"on"`, `"yes"` test rejimini aktivləşdirir,
qalan hər şey (`"false"`, `"0"`, `"off"`, `""`) canlı mühitdə saxlayır.

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## Xəta Hesabatları (Telemetriya)

API çağırışı uğursuz olduqda kitabxana DomainNameAPI-nin öz xəta izləmə sisteminə (Sentry) xəta hesabatı
göndərə bilər. Uğurlu çağırışların təsadüfi seçilmiş kiçik bir hissəsi (4%, üstəlik 1 saniyədən uzun çəkən hər çağırış)
performans qeydi kimi göndərilir. Bu, DomainNameAPI-yə problemləri tapıb düzəltməyə kömək edir. Xəta hesabatları **standart olaraq aktivdir**.

> ℹ️ 1.0.0 versiyasında daxili Sentry ünvanı hələ boşdur, çünki python-dna üçün Sentry layihəsi
> hələ yaradılmayıb: kitabxana yeniləməsi bu ünvanı doldurana və ya siz
> `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")` ilə öz ünvanınızı ötürənə qədər **heç nə göndərilmir**.

Hesabatlar arxa fon thread-i vasitəsilə göndərilir: çağırışınızı heç vaxt yavaşlatmır və ya pozmur.
Gözlənilən, yüksək həcmli xətalar (domen tapılmadı, balans kifayət deyil, yanlış API məlumatları, yönləndirmə qurulmayıb, ...) heç vaxt
bildirilmir.

**Göndərilənlər:**

- xəta kodu və mesajı
- çağırılan endpoint yolu və HTTP metodu
- çağırışın müddəti
- kitabxananın adı (`DomainNameAPI-Python`), kitabxananın versiyası və Python versiyası
- reseller ID və domen adı
- serverin ictimai (public) IP ünvanı (`api.ipify.org` vasitəsilə müəyyən edilir) və əməliyyat sisteminin istifadəçi adı
- API sorğusu və cavabı, domenin əlaqə məlumatları daxil olmaqla; yalnız giriş məlumatları maskalanır — EPP/auth kodları, API açarları, parollar və tokenlər `***` ilə əvəz olunur

**Heç vaxt göndərilməyənlər:** oxunaqlı formada EPP/auth kodları, API açarları, parollar və ya tokenlər; stack trace-lərdəki funksiya çağırışı arqumentləri.

**Niyə və nə qədər müddətə:** məlumatlar yalnız istifadənin ölçülməsi və problemlərin erkən diaqnostikası üçün istifadə olunur, DomainNameAPI-nin öz Sentry serverində 30 gün saxlanılır, sonra avtomatik olaraq silinir.

**Necə söndürmək olar:** klienti yaratdıqdan sonra `set_error_reporting_enabled(False)` çağırın:

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**Minimal rejim:** `set_telemetry_minimal(True)` yalnız xəta kodunu və mesajını, endpoint-i, müddəti,
versiyaları və reseller ID-ni göndərir — sorğu/cavab məlumatları, domen, IP ünvanı və ya istifadəçi adı göndərilmir.

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **Təhlükəsizlik:** TLS sertifikat yoxlaması aktivdir. CA paketi köhnə olan serverdə `dna.set_ssl_verification(False)` ilə söndürülə bilər — tövsiyə edilmir; CA paketini yeniləmək daha düzgün həlldir.

## İstifadə

Aşağıdakı bütün nümunələr bunu nəzərdə tutur:

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

Nümunə çıxışlar kitabxananın real qaytardığı dəyərlərdir.

### Hesab

#### Satıcı Təfərrüatlarını Əldə Etmək

Reseller hesabının təfərrüatları: ID, ad və balanslar (USD və TL).

```python
result = dna.get_reseller_details()
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Cari Balansı Əldə Etmək

Bir valyutada cari balans: USD (standart) və ya TRY. Hesabın bildirmədiyi valyuta (EUR, GBP, ...) ErrorCode BALANCE ilə OperationResult FAILED qaytarır.

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>Nümunə çıxış</summary>

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


### Axtarış və Siyahılar

#### Domen Mövcudluğunun Yoxlanılması

Hər domen + uzantı kombinasiyasının mövcudluğu və qiyməti. Uğurlu olduqda sadə siyahı, uğursuz olduqda xəta strukturu qaytarır.

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Domen Siyahısı

Reseller hesabındakı domenlər. Filtrlər: PageNumber (0-dan başlayır), PageSize, OrderColumn, OrderDirection, DomainName ...

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>Nümunə çıxış</summary>

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

#### TLD Siyahısı

Dövrlərə görə qiymətləri ilə TLD siyahısı (qeydiyyat, yeniləmə, transfer, bərpa ...).

```python
result = dna.get_tld_list(100)
```

<details>
<summary>Nümunə çıxış</summary>

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


### Domenlər

#### Domen Qeydiyyatı

Yeni domen qeydiyyatdan keçirin. Əlaqələr düz (`AddressLine1`, `Phone`, ...) və ya iç-içə (`Address.Line1`, `Phone.Phone.Number`, ...) formada verilə bilər. Çatışmayan sahələr tamamlanır və telefon nömrələri normallaşdırılır (bax: `validate_contact`). Boş nameserver siyahısı verildikdə `ns1.domainnameapi.com` / `ns2.domainnameapi.com` istifadə olunur.

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
<summary>Nümunə çıxış</summary>

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

#### Domen Qeydiyyatı (.tr)

`.tr` domenləri 7-ci arqument kimi TRABIS atributları tələb edir. Fərdi sahib: `TRABISDOMAINCATEGORY` = `1` və `TRABISCITIZENID` (şəxsiyyət nömrəsi). Şirkət sahibi: `TRABISDOMAINCATEGORY` = `0`, `TRABISTAXOFFICE` və `TRABISTAXNUMBER`. Köhnə (legacy) açarlar (`TRABISCITIZIENID`, `TRABISNAMESURNAME`, `TRABISCOUNTRYID`, ...) qəbul edilir: REST sxeminə çevrilir, dəstəklənməyənlər atılır.

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
<summary>Nümunə çıxış</summary>

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

#### Domen Yenilənməsi

Domeni göstərilən il sayı qədər yeniləyin.

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domen Məlumatları

Bir domenin tam təfərrüatları: status, tarixlər, nameserver-lər, kilid/məxfilik bayraqları, child nameserver-lər.

```python
result = dna.get_details("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Registry-dən Sinxronizasiya

Domeni registry-dən yeniləyin (get_details ilə eyni cavab strukturu).

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Nameserver Dəyişdirmə

Domenin nameserver-lərini əvəz edin (girişlərdəki boşluqlar silinir, kiçik hərflərə çevrilir, təkrarlar çıxarılır).

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domen Kilidini Aktivləşdirmək

Qeydiyyatçı (oğurluqdan qorunma) kilidini aktivləşdirin.

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domen Kilidini Açmaq

Qeydiyyatçı (oğurluqdan qorunma) kilidini söndürün.

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domen Məxfiliyi Dəyişdirmə

WHOIS məxfilik qorumasını aktivləşdirin (True) və ya söndürün (False). 1, "1", "on", "true" və "yes" də aktiv deməkdir; qalan hər şey söndürülmüş deməkdir. reason arqumenti gateway-ə göndərilmir.

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### Əlaqələr

#### Domen Əlaqələrini Əldə Etmək

Domenin Administrative (inzibati), Billing (hesab), Registrant (sahib) və Technical (texniki) əlaqələri.

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Domen Əlaqələrini Saxlamaq

Domenin dörd əlaqəsini əvəz edin. `contacts` qeydiyyat nümunəsindəki lüğətin (dictionary) eynisidir.

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### Child Nameserver-lər

#### Child NameServer Əlavə Etmək

Domen altında child nameserver (glue qeydi) yaradın.

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Child NameServer Silmə

Child nameserver-i silin.

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Child NameServer Yeniləmə

Child nameserver-in IP ünvanını dəyişin.

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### Transferlər

#### Domen Transferi

Domenin EPP/auth kodu ilə daxil olan transferə başlayın. Transferlə heç vaxt əlaqə məlumatları göndərilmir (sorğu həmişə `"contacts": []` daşıyır): registrar onları köhnə registrardan götürür, buna görə `transfer` metodunun contacts parametri yoxdur. İmtina (`success: false`) `TRANSFER_DOMAIN` xətası qaytarır.

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Transferin Yoxlanılması

Domen bu auth kodu ilə transfer edilə bilərmi? result yalnız transfer mümkün olduqda OK olur.

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Transferi Ləğv Etmək

Gözləmədə olan daxil olan transferi ləğv edin.

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Çıxan Transferi Təsdiqləmək

Gözləmədə olan çıxan transferi təsdiqləyin.

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Çıxan Transferi Rədd Etmək

Gözləmədə olan çıxan transferi rədd edin.

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### DNS Zonası

Gateway DNS qeydlərini **set** (dəst) kimi saxlayır: bir ad + tip dəyərlər siyahısını saxlayır. Bir ad + tipi yazmaq
bütün dəsti əvəz edir, bir dəyərə görə silmək isə bütün dəsti silir. `*_record_set` və
`*_record_value` metodları bunu sizin əvəzinizə idarə edir; aşağı səviyyəli `add/edit/delete_resource_record` əvəzinə onlara üstünlük verin.

- Adlar `"@"`, `""`, `"www"`, `"www.example.com"` və ya `"www.example.com."` kimi verilə bilər; onlar gateway-in gözlədiyi
  nisbi etiket (relative label) kimi göndərilir. `get_resource_records` tam ixtisaslı adlar (`"www.example.com."`) qaytarır.
- Dəstəklənən tiplər: `A`, `AAAA`, `ALIAS`, `CAA`, `CNAME`, `DS`, `MX`, `NAPTR`, `PTR`, `SRV`, `TLSA`, `TXT`
  (digərləri heç bir çağırış edilmədən rədd edilir). TTL 1-dən 86400 saniyəyə qədərdir.
- Yazma əməliyyatları dərhal tətbiq olunur; bir neçə dəyişikliyi növbəyə qoymaq üçün `apply=False` ötürün və sonda
  `apply_resource_records` metodunu bir dəfə çağırın. Avtomatik tətbiq uğursuz olarsa, metod tətbiq xətasını qaytarır (dəyişiklik növbədə qalır, amma aktiv deyil).
- Gateway zona çağırışlarına sürət limiti (rate limit) tətbiq edir, buna görə kitabxana zona çağırışları arasında ən azı bir saniyə fasilə saxlayır
  (`dna.zone_min_interval`, saniyə ilə).


#### Qeydlərin Siyahısı

Domenin DNS zonası, hər qeyd dəyəri üçün bir sətir. Adlar tam ixtisaslı (FQDN) qaytarılır.

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Qeyd Dəstini Təyin Etmək

Bütöv bir ad + tipi verilən siyahı ilə tam eyni edin (gateway-in öz modeli). Boş siyahı dəsti silir. apply=False verilmədikcə dəyişikliklər dərhal tətbiq olunur.

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
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Bir Dəyər Əlavə Etmək

Qeyd dəstinə BİR dəyər əlavə edin və mövcud dəyərləri saxlayın (oxu-birləşdir-yaz). Artıq mövcud olan dəyəri əlavə etmək heç nə dəyişmir.

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>Nümunə çıxış</summary>

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

#### Bir Dəyəri Silmək

Qeyd dəstindən BİR dəyəri silin, digərləri yerində qalır.

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Bir Dəyəri Əvəz Etmək

Qeyd dəstindəki BİR dəyəri başqası ilə əvəz edin (DNS panelindəki 'sətri redaktə et' əməliyyatı).

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Qeyd Dəstini Silmək

Ad + tip altındakı bütün dəyərləri silin. Mövcud olmayan dəsti silmək də OK qaytarır.

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Qeyd Əlavə Etmək (aşağı səviyyə)

Aşağı səviyyə: qeyd dəstini yazır (POST). Gateway mövcud ad + tipi əvəz edir, buna görə dəyər əlavə etmək üçün add_resource_record_value() metoduna üstünlük verin.

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Qeydi Redaktə Etmək (aşağı səviyyə)

Aşağı səviyyə: mövcud qeyd dəstini cari adı ilə müəyyən edərək yenidən yazır (PUT).

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Qeydi Silmək (aşağı səviyyə)

Aşağı səviyyə: ad + dəyər + tipə görə DELETE. Gateway BÜTÜN dəsti silir, buna görə tək bir dəyəri silmək üçün remove_resource_record_value() metoduna üstünlük verin.

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Növbədəki Dəyişiklikləri Tətbiq Etmək

Növbəyə qoyulmuş zona dəyişikliklərini tətbiq edin (yalnız apply=False ilə edilmiş çağırışlardan sonra lazımdır).

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### URL Yönləndirməsi

#### Yönləndirməni Əldə Etmək

Domenin URL yönləndirməsi. Heç nə konfiqurasiya edilməyibsə, Enabled False olur.

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Yönləndirmə Təyin Etmək

Domeni URL-ə yönləndirin: 'Standard' (sadə yönləndirmə) və ya 'Frame' (maskalanmış).

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Yönləndirməni Silmək

URL yönləndirməsini silin. Heç nə qurulmayıbsa, Removed False olur (nəticə yenə OK).

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>Nümunə çıxış</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Removed': True}}
```

</details>


### Köməkçi Alətlər

#### .tr Domenidirmi?

Bu .tr domenidirmi? Lokal yoxlama, şəbəkə çağırışı yoxdur.

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>Nümunə çıxış</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Əlaqənin Yoxlanılması

Əlaqəni gateway-in gözlədiyi formada tamamlayın və normallaşdırın (lokal, şəbəkə çağırışı yoxdur): çatışmayan sahələrə yer tutucu dəyərlər verilir, adlardan rəqəmlər/durğu işarələri silinir, telefon nömrələri nömrə + ölkə koduna ayrılır, State boşdursa City istifadə olunur.

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
<summary>Nümunə çıxış</summary>

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


### Diaqnostika və Parametrlər

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

Konstruktora xüsusi HTTP transport (proxy idarəsi, loglama, testlər) ötürülə bilər: `domainnameapi.HttpResponse` qaytaran
`send(request)` metoduna malik istənilən obyekt:

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## Testlər

Test paketi heç bir API məlumatı tələb etmir və xarici şəbəkə çağırışları etmir:

```bash
python -m unittest discover -s tests -v
```

| Test faylı | Təsvir |
|-----------|-------------|
| `tests/test_conformance.py` | php-dna-nın 134 uyğunluq fixture-unun hamısını işə salır: şəbəkəyə gedən sorğular eyni, qaytarılan dəyərlər eyni |
| `tests/test_edge_cases.py` | php-dna-dan qeydə alınmış əlavə kənar hallar (qeyri-adi gateway cavabları və girişlər) |
| `tests/test_http.py` | HTTP qatı: header-lər, query string-lər, JSON gövdələri, vaxt aşımları, yönləndirmələr |
| `tests/test_errors.py` | Gateway cavablarının xəta uyğunlaşdırılması |
| `tests/test_telemetry.py` | Telemetriya məzmunu, giriş məlumatlarının maskalanması, söndürmə (opt-out) |
| `tests/test_utils.py` | Köməkçi alətlər və PHP ilə uyğun dəyər emalı |

<hr style="border: 4px solid #000; border-style: dashed;">


## Geri Dönüş və Xəta Kodları ilə Açıqlamaları

| Kod | Açıqlama | Təfərrüat |
|------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1000 | Command completed successfully | Əməliyyat uğurlu. |
| 1001 | Command completed successfully; action pending | Əməliyyat uğurlu. Bununla belə, əməliyyat hazırda tamamlanması üçün növbəyə alınıb. |
| 2003 | Required parameter missing | Parametr çatışmır xətası. Məsələn: əlaqə məlumatlarında telefon girişi yoxdur. |
| 2105 | Object is not eligible for renewal | Domen statusu yenilənmə üçün uyğun deyil, yeniləmə əməliyyatları üçün kilidlənib. Status "clientupdateprohibited" olmamalıdır. Digər status şərtlərindən də qaynaqlana bilər. |
| 2200 | Authentication error | İcazə xətası, təhlükəsizlik kodu səhvdir və ya domen başqa qeydiyyat şirkətində qeydiyyatdadır. |
| 2302 | Object exists | Domen adı və ya nameserver məlumatları verilənlər bazasında mövcuddur. Qeydiyyat edilə bilməz. |
| 2303 | Object does not exist | Domen adı və ya nameserver məlumatları verilənlər bazasında mövcud deyil. Yeni qeydiyyat tələb olunur. |
| 2304 | Object status prohibits operation | Domen statusu yeniləmələr üçün uyğun deyil, yeniləmə əməliyyatları üçün kilidlənib. Status "clientupdateprohibited" olmamalıdır. Digər status şərtlərindən də qaynaqlana bilər. |

| KOD | TƏFƏRRÜAT |
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

| KOD | TƏFƏRRÜAT |
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

| KOD | TƏFƏRRÜAT |
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


## Lisenziya

Apache License 2.0 — bax: [LICENSE](LICENSE).
