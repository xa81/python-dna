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


# python-dna: Python için DomainNameAPI istemcisi

[DomainNameAPI](https://www.domainnameapi.com) reseller REST API'si için Python istemcisi: alan adı sorgulama, kayıt,
transfer ve yenileme işlemlerini yapın; kontakları, nameserver'ları, child nameserver'ları, DNS zone'larını ve URL yönlendirmeyi yönetin.
[php-dna](https://github.com/domainreseller/php-dna) kütüphanesinin birebir sadık bir uyarlamasıdır: aynı metotlar, aynı istekler,
aynı dönüş değerleri; php-dna'nın uyumluluk (conformance) fixture'larıyla doğrulanmıştır.

## 📦 İndirme — her zaman Releases kullanın!

⬇️ **En güncel test edilmiş sürümü buradan indirin: https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ Yeşil **Code → Download ZIP** butonunu **kullanmayın** — bu buton ham geliştirme dalını (development branch) indirir. Release paketleri sürümlenmiş, test edilmiş ve canlı kullanıma hazırdır.

## Kurulum ve Entegrasyon Rehberi

### Minimum Gereksinimler

- Python 3.8 veya daha üstü (önerilen 3.12)
- Üçüncü parti paket gerekmez: kütüphane yalnızca Python standart kütüphanesini (`urllib`, `json`, `ssl`) kullanır.

### A) pip ile kurulum

```bash
pip install domainnameapi
```

### B) Release paketi ile kurulum

Wheel dosyasını (`domainnameapi-1.0.0-py3-none-any.whl`) veya kaynak arşivini
[son sürüm](https://github.com/domainreseller/python-dna/releases/latest) sayfasından indirip kurun:

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### C) Kaynak kodu doğrudan kullanma

`src/domainnameapi` klasörünü kodunuzun yanına kopyalayın (veya `src` klasörünü `PYTHONPATH`'e ekleyin) ve import edin.
[examples](examples) klasöründe her metot için çalıştırılabilir bir örnek betik bulunur.

## 🔑 API Bilgileri — Reseller ID ve API Key

Kütüphane DomainNameAPI REST API ile konuşur ve constructor'a verilen yalnızca iki bilgiye ihtiyaç duyar:

| Parametre | Değer |
|---|---|
| Birinci | Reseller ID — `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` biçiminde UUID |
| İkinci | API Key |

> 💡 **Reseller ID** ve **API Key** bilgilerinizi DomainNameAPI panelinizdeki **API Ayarları** bölümünde bulabilirsiniz.
> ⚠️ Bunlar **API bilgileridir** — panel giriş bilgileriniz burada **ÇALIŞMAZ**.

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

Bilgilerin başındaki ve sonundaki boşluklar otomatik olarak temizlenir.

## Hızlı Başlangıç

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

Metot adları snake_case biçimindedir (`get_details`, `register_with_contact_info`). php-dna'daki adlar da takma ad (alias) olarak çalışır;
böylece PHP'den taşınan kod `dna.GetDetails(...)` veya `dna.getDetails(...)` kullanmaya devam edebilir.

## Dönüş Değerleri ve Hata Yönetimi

Metotlar, php-dna'nın döndürdüğü anahtarların birebir aynısını içeren düz `dict`/`list` değerleri döndürür. Gateway veya ağ sorunlarında
exception **fırlatmazlar**; bunun yerine `result` değerini kontrol edin:

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "...",
                              "GatewayCode": "Dna.DomainService:Domain:10007"}}
```

- `Code`, gateway hatalarında `API_<HTTP durum kodu>` biçimindedir (`API_400`, `API_404`, `API_429`, `API_500`, ...).
  Yönlendirme (redirect) yanıtı (hatalı API bilgileri) `Invalid API credentials` mesajıyla birlikte `API_302` döndürür.
- `GatewayCode`: gateway kendi hata kodunu gönderdiğinde (örneğin `Dna.DomainService:Domain:10007`) `API_<status>` hatalarına eklenir; böylece "alan adı bulunamadı" ile "TLD desteklenmiyor" ayırt edilebilir.
- `Message`, gateway'in mesajıdır. Boş hata gövdeleri `HTTP <status> - <reason>` biçimine dönüştürülür
  (örneğin `HTTP 429 - Too Many Requests`).
- `Details`, gateway'in ayrıntılarını (yoksa ham yanıt gövdesini) içerir; doğrulama (validation) hataları okunabilir bir alan listesine dönüştürülür,
  örneğin `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`.
- Ağ hataları da hata olarak döner, asla boş bir başarı yanıtı olarak değil: zaman aşımında
  `Could not reach the DomainNameAPI service: the connection timed out. (...)` mesajıyla `CURL_28` döner; DNS, bağlantı ve TLS
  hataları `Curl error during request: ...` mesajıyla `CURL_6`, `CURL_7`, `CURL_35`/`CURL_60` döndürür
  (curl hata numaraları; php-dna'nın raporladığı kodların aynısı). `API_` kodları yalnızca HTTP durum kodları için kullanılır.
- Gateway HTTP 200 ile yanıt verse bile ret bir hatadır: kayıt, transfer veya yenileme `success: false` ile dönerse metot gateway'in mesajıyla birlikte `REGISTER_DOMAIN`, `TRANSFER_DOMAIN` veya `RENEW_DOMAIN` döndürür.
- Bayraklar php-dna'daki tiplerini korur: `LockStatus` `"true"`/`"false"` string değeridir, fiyatlar biçimlendirilmiş string'lerdir
  (`"11.9900"`).

Birkaç metot, php-dna'da olduğu gibi kendi yanıt yapısını (envelope) kullanır:

| Metot | Başarılı olduğunda | Başarısız olduğunda |
|---|---|---|
| `check_availability` | sonuçlardan oluşan düz bir `list` | `ERROR` yapısı |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `ErrorCode` (`API_<status>`, `CURL_<errno>` veya hesabın bildirmediği bir para birimi için `BALANCE`) ile birlikte `OperationResult: "FAILED"` |
| `check_transfer` | yalnızca alan adı transfer edilebiliyorsa `result: "OK"` | `data` ve `error` ile birlikte `result: "ERROR"` |
| `is_tr_tld`, `validate_contact` | düz değerler (ağ çağrısı yok) | — |

Yalnızca programlama hataları (örneğin `set_resource_record_set` bir liste beklerken string verilmesi)
Python exception'ı fırlatır.

Zaman aşımı süreleri çağrı başına 30 saniye, bağlantı kurmak için 10 saniyedir. Yönlendirmeler (redirect) takip edilmez.

## Test Modu (OTE)

`https://ote.domainresellerapi.com/api/v1` test ortamını kullanmak için üçüncü argüman olarak `True` verin.
Yapılandırma dosyalarından gelen string değerler de anlaşılır: `"true"`, `"1"`, `"on"`, `"yes"` test modunu açar,
diğer her değer (`"false"`, `"0"`, `"off"`, `""`) canlı ortamda kalır.

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## Hata Raporlama (Telemetri)

Bir API çağrısı başarısız olduğunda kütüphane, DomainNameAPI'nin kendi hata takip sistemine (Sentry) bir hata raporu
gönderebilir. Başarılı çağrıların rastgele seçilen küçük bir kısmı (%4, ayrıca 1 saniyeden uzun süren her çağrı)
performans kaydı olarak gönderilir. Bu, DomainNameAPI'nin sorunları bulup düzeltmesine yardımcı olur. Hata raporlama **varsayılan olarak açıktır**.

> ℹ️ 1.0.0 sürümünde yerleşik Sentry adresi henüz boştur, çünkü python-dna için Sentry projesi
> henüz oluşturulmamıştır: bir kütüphane güncellemesi bu adresi doldurana veya siz
> `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")` ile kendi adresinizi verene kadar **hiçbir şey gönderilmez**.

Raporlar arka planda çalışan bir thread üzerinden gönderilir: çağrınızı asla yavaşlatmaz veya bozmaz.
Beklenen ve yüksek hacimli hatalar (alan adı bulunamadı, yetersiz bakiye, geçersiz API bilgileri, yapılandırılmamış yönlendirme, ...) hiçbir zaman
raporlanmaz.

**Gönderilenler:**

- hata kodu ve mesajı
- çağrılan uç nokta (endpoint) yolu ve HTTP yöntemi
- çağrı süresi
- kütüphane adı (`DomainNameAPI-Python`), kütüphane sürümü ve Python sürümü
- bayi kimliği (Reseller ID) ve alan adı
- sunucunun genel (public) IP adresi (`api.ipify.org` üzerinden öğrenilir) ve işletim sistemi kullanıcı adı
- API isteği ve yanıtı, alan adının kişi bilgileri dahil; yalnızca kimlik bilgileri maskelenir — EPP/transfer kodları, API anahtarları, parolalar ve token'lar `***` ile değiştirilir

**Asla gönderilmeyenler:** okunabilir biçimde EPP/transfer kodları, API anahtarları, parolalar veya token'lar; hata izlerindeki (stack trace) fonksiyon çağrısı argümanları.

**Neden ve ne kadar süre:** veriler yalnızca kullanım ölçümü ve sorunların erken teşhisi için kullanılır; DomainNameAPI'nin kendi Sentry sunucusunda 30 gün saklanır, ardından otomatik olarak silinir.

**Nasıl kapatılır:** istemciyi oluşturduktan sonra `set_error_reporting_enabled(False)` çağırın:

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**Minimal mod:** `set_telemetry_minimal(True)` yalnızca hata kodunu ve mesajını, uç noktayı, süreyi,
sürümleri ve Reseller ID'yi gönderir — istek/yanıt verisi, alan adı, IP adresi veya kullanıcı adı gönderilmez.

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **Güvenlik:** TLS sertifika doğrulaması açıktır. CA paketi güncel olmayan bir sunucuda `dna.set_ssl_verification(False)` ile kapatılabilir — önerilmez; CA paketini güncellemek daha doğru çözümdür.

## Kullanım

Aşağıdaki tüm örneklerde şu kurulum varsayılmıştır:

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

Örnek çıktılar, kütüphanenin gerçek dönüş değerleridir.

### Hesap

#### Reseller Bilgilerini Alma

Reseller hesap bilgileri: ID, ad ve bakiyeler (USD ve TL).

```python
result = dna.get_reseller_details()
```

<details>
<summary>Örnek çıktı</summary>

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

#### Güncel Bakiyeyi Alma

Tek bir para birimindeki güncel bakiye: USD (varsayılan) veya TRY. Hesabın bildirmediği bir para birimi (EUR, GBP, ...) ErrorCode BALANCE ile OperationResult FAILED döndürür.

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>Örnek çıktı</summary>

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


### Sorgulama ve Listeler

#### Alan Adı Uygunluk Kontrolü

Her alan adı + uzantı kombinasyonunun uygunluğu ve fiyatı. Başarılı olduğunda düz bir liste, başarısız olduğunda hata yapısı döndürür.

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>Örnek çıktı</summary>

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

#### Alan Adları Listesi

Reseller hesabındaki alan adları. Filtreler: PageNumber (0'dan başlar), PageSize, OrderColumn, OrderDirection, DomainName ...

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>Örnek çıktı</summary>

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

#### TLD Listesi

Dönem bazında fiyatlarıyla TLD listesi (kayıt, yenileme, transfer, geri yükleme ...).

```python
result = dna.get_tld_list(100)
```

<details>
<summary>Örnek çıktı</summary>

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


### Alan Adları

#### Domain Kaydı

Yeni bir alan adı kaydedin. Kontaklar düz (`AddressLine1`, `Phone`, ...) veya iç içe (`Address.Line1`, `Phone.Phone.Number`, ...) biçimde verilebilir. Eksik alanlar tamamlanır ve telefon numaraları normalize edilir (bkz. `validate_contact`). Boş bir nameserver listesi verilirse `ns1.domainnameapi.com` / `ns2.domainnameapi.com` kullanılır.

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
<summary>Örnek çıktı</summary>

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

#### Domain Kaydı (.tr)

`.tr` alan adları 7. argüman olarak TRABIS özniteliklerine ihtiyaç duyar. Bireysel sahip: `TRABISDOMAINCATEGORY` = `1` ve `TRABISCITIZENID` (T.C. kimlik numarası). Kurumsal sahip: `TRABISDOMAINCATEGORY` = `0`, `TRABISTAXOFFICE` ve `TRABISTAXNUMBER`. Eski (legacy) anahtarlar (`TRABISCITIZIENID`, `TRABISNAMESURNAME`, `TRABISCOUNTRYID`, ...) kabul edilir: REST şemasına dönüştürülür, desteklenmeyenler atılır.

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
<summary>Örnek çıktı</summary>

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

#### Domain Yenileme

Bir alan adını belirtilen yıl sayısı kadar yenileyin.

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Alan Adı Detayları

Bir alan adının tüm detayları: durum, tarihler, nameserver'lar, kilit/gizlilik bayrakları, child nameserver'lar.

```python
result = dna.get_details("example.com")
```

<details>
<summary>Örnek çıktı</summary>

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

#### Registry'den Senkronizasyon

Bir alan adını registry'den güncelleyin (get_details ile aynı yanıt yapısı).

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>Örnek çıktı</summary>

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

#### Nameserver Düzenlemesi

Bir alan adının nameserver'larını değiştirin (girdilerin boşlukları temizlenir, küçük harfe çevrilir, tekrarlar ayıklanır).

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain Kilidini Aktifleştirme

Kayıt firması (hırsızlık koruması) kilidini açın.

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain Kilidini Kaldırma

Kayıt firması (hırsızlık koruması) kilidini kapatın.

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Domain Gizliliğini Değiştirme

WHOIS gizlilik korumasını açın (True) veya kapatın (False). 1, "1", "on", "true" ve "yes" de açık anlamına gelir; diğer her şey kapalıdır. reason argümanı gateway'e gönderilmez.

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### Kontaklar

#### Domain Kontaklarını Alma

Bir alan adının Administrative (yönetici), Billing (fatura), Registrant (sahip) ve Technical (teknik) kontakları.

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>Örnek çıktı</summary>

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

#### Domain Kontaklarını Kaydetme

Bir alan adının dört kontağını değiştirin. `contacts`, kayıt örneğindeki sözlüğün (dictionary) aynısıdır.

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### Child Nameserver'lar

#### Child Nameserver Ekleme

Bir alan adı altında child nameserver (glue kaydı) oluşturun.

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Child Nameserver Silme

Bir child nameserver'ı silin.

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Child Nameserver Güncelleme

Bir child nameserver'ın IP adresini değiştirin.

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### Transferler

#### Domain Transferi

Alan adının EPP/transfer koduyla gelen bir transfer başlatın. Transferde kontak bilgileri hiçbir zaman gönderilmez (istek her zaman `"contacts": []` içerir): kontaklar kaybeden registrar'dan devralınır, bu yüzden `transfer` metodunun contacts parametresi yoktur. Ret (`success: false`) `TRANSFER_DOMAIN` hatası döndürür.

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>Örnek çıktı</summary>

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

#### Transfer Kontrolü

Alan adı bu transfer koduyla transfer edilebilir mi? result yalnızca transfer edilebiliyorsa OK olur.

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>Örnek çıktı</summary>

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

#### Transferi İptal Etme

Bekleyen bir gelen transferi iptal edin.

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Giden Transferi Onaylama

Bekleyen bir giden transferi onaylayın.

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Giden Transferi Reddetme

Bekleyen bir giden transferi reddedin.

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### DNS Zone

Gateway, DNS kayıtlarını **set** olarak saklar: bir ad + tip, bir değerler listesi tutar. Bir ad + tip yazmak
tüm set'in yerini alır, tek bir değere göre silmek ise tüm set'i kaldırır. `*_record_set` ve
`*_record_value` metotları bunu sizin için halleder; düşük seviyeli `add/edit/delete_resource_record` yerine bunları tercih edin.

- Adlar `"@"`, `""`, `"www"`, `"www.example.com"` veya `"www.example.com."` biçiminde verilebilir; gateway'in beklediği
  göreli etiket (relative label) olarak gönderilir. `get_resource_records` tam nitelikli adlar (`"www.example.com."`) döndürür.
- Desteklenen tipler: `A`, `AAAA`, `ALIAS`, `CAA`, `CNAME`, `DS`, `MX`, `NAPTR`, `PTR`, `SRV`, `TLSA`, `TXT`
  (diğerleri herhangi bir çağrı yapılmadan reddedilir). TTL 1 ile 86400 saniye arasındadır.
- Yazma işlemleri hemen uygulanır; birden fazla değişikliği sıraya almak için `apply=False` verin ve sonunda
  `apply_resource_records` metodunu bir kez çağırın. Otomatik uygulama başarısız olursa metot uygulama hatasını döndürür (değişiklik sırada kalır ama yayında değildir).
- Gateway, zone çağrılarına hız sınırı (rate limit) uygular; bu yüzden kütüphane zone çağrıları arasında en az bir saniye bırakır
  (`dna.zone_min_interval`, saniye cinsinden).


#### Kayıtları Listeleme

Bir alan adının DNS zone'u; her kayıt değeri için bir satır. Adlar tam nitelikli (FQDN) olarak döner.

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>Örnek çıktı</summary>

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

#### Kayıt Set'ini Ayarlama

Bir ad + tipin tamamını verilen listeyle birebir aynı hale getirin (gateway'in kendi modeli). Boş liste set'i kaldırır. apply=False verilmedikçe değişiklikler hemen uygulanır.

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
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Tek Değer Ekleme

Bir kayıt set'ine TEK bir değer ekleyin ve mevcut değerleri koruyun (oku-birleştir-yaz). Zaten var olan bir değeri eklemek hiçbir şey yapmaz.

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>Örnek çıktı</summary>

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

#### Tek Değer Kaldırma

Bir kayıt set'inden TEK bir değeri kaldırın, diğerleri yerinde kalır.

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Tek Değeri Değiştirme

Bir kayıt set'indeki TEK bir değeri başka bir değerle değiştirin (bir DNS panelindeki 'satırı düzenle' işlemi).

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Kayıt Set'ini Silme

Bir ad + tip altındaki tüm değerleri kaldırın. Var olmayan bir set'i kaldırmak da OK döner.

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Kayıt Ekleme (düşük seviye)

Düşük seviye: bir kayıt set'i yazar (POST). Gateway mevcut bir ad + tipin yerine yenisini yazar; bu yüzden değer eklemek için add_resource_record_value() tercih edin.

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Kayıt Düzenleme (düşük seviye)

Düşük seviye: mevcut bir kayıt set'ini, mevcut adıyla belirleyerek yeniden yazar (PUT).

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Kayıt Silme (düşük seviye)

Düşük seviye: ad + değer + tipe göre DELETE. Gateway set'in TAMAMINI kaldırır; bu yüzden tek bir değeri silmek için remove_resource_record_value() tercih edin.

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Bekleyen Değişiklikleri Uygulama

Sıraya alınmış zone değişikliklerini uygulayın (yalnızca apply=False ile yapılan çağrılardan sonra gereklidir).

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### URL Yönlendirme

#### Yönlendirmeyi Alma

Bir alan adının URL yönlendirmesi. Hiçbir şey yapılandırılmamışsa Enabled False olur.

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Yönlendirme Ayarlama

Alan adını bir URL'ye yönlendirin: 'Standard' (düz yönlendirme) veya 'Frame' (maskeli).

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Yönlendirmeyi Silme

URL yönlendirmesini kaldırın. Hiçbir şey yapılandırılmamışsa Removed False olur (sonuç yine OK).

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>Örnek çıktı</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Removed': True}}
```

</details>


### Yardımcı Araçlar

#### .tr Alan Adı mı?

Bu bir .tr alan adı mı? Yerel kontrol, ağ çağrısı yapılmaz.

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>Örnek çıktı</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### Kontak Doğrulama

Bir kontağı gateway'in beklediği biçimde tamamlayın ve normalize edin (yerel, ağ çağrısı yok): eksik alanlara yer tutucu değerler atanır, adlardan rakam/noktalama işaretleri temizlenir, telefon numaraları numara + ülke koduna ayrılır, State boşsa City kullanılır.

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
<summary>Örnek çıktı</summary>

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


### Tanılama ve Ayarlar

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

Constructor'a özel bir HTTP transport (proxy yönetimi, loglama, testler) verilebilir: `domainnameapi.HttpResponse` döndüren
bir `send(request)` metoduna sahip herhangi bir nesne:

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## Testler

Test paketi herhangi bir API bilgisine ihtiyaç duymaz ve dışarıya ağ çağrısı yapmaz:

```bash
python -m unittest discover -s tests -v
```

| Test dosyası | Açıklama |
|-----------|-------------|
| `tests/test_conformance.py` | php-dna'nın 134 uyumluluk fixture'ının tamamını çalıştırır: kabloya giden istekler aynı, dönüş değerleri aynı |
| `tests/test_edge_cases.py` | php-dna'dan kaydedilmiş ek uç durumlar (alışılmadık gateway yanıtları ve girdiler) |
| `tests/test_http.py` | HTTP katmanı: header'lar, query string'ler, JSON gövdeleri, zaman aşımları, yönlendirmeler |
| `tests/test_errors.py` | Gateway yanıtlarının hata eşlemesi |
| `tests/test_telemetry.py` | Telemetri içerikleri, kimlik bilgisi maskeleme, devre dışı bırakma (opt-out) |
| `tests/test_utils.py` | Yardımcı araçlar ve PHP uyumlu değer işleme |

<hr style="border: 4px solid #000; border-style: dashed;">


## Dönüş ve Hata Kodları ile Açıklamaları

| Kod | Açıklama | Detay |
|------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1000 | Command completed successfully | İşlem başarılı. |
| 1001 | Command completed successfully; action pending | İşlem başarılı. Fakat işlem şu an tamamlanmak için kuyruğa alındı. |
| 2003 | Required parameter missing | Parametre eksik hatası. Örneğin; kontak bilgisinde telefon girişi yapılmaması. |
| 2105 | Object is not eligible for renewal | Domain durumu yenilemeye müsait değil, güncelleme işlemlerine kilitlenmiştir. Durum "clientupdateprohibited" olmamalıdır. Başka durum koşullarından da kaynaklanabilir. |
| 2200 | Authentication error | Yetki hatası, güvenlik kodu hatalı veya domain başka bir kayıt firmasında bulunuyor. |
| 2302 | Object exists | Domain adı veya nameserver bilgisi veritabanında mevcut. Kayıt edilemez. |
| 2303 | Object does not exist | Domain adı veya nameserver bilgisi veritabanında mevcut değil. Yeni kayıt oluşturulmalı. |
| 2304 | Object status prohibits operation | Domain durumu güncellemeye müsait değildir, güncelleme işlemlerine kilitlenmiştir. Durum "clientupdateprohibited" olmamalıdır. Başka durum koşullarından da kaynaklanabilir. |

| KOD | DETAY |
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

| KOD | DETAY |
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

| KOD | DETAY |
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


## Lisans

Apache License 2.0 — bkz. [LICENSE](LICENSE).
