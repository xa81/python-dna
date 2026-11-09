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


# python-dna: عميل DomainNameAPI للغة Python

عميل Python لواجهة REST API الخاصة بالموزعين من [DomainNameAPI](https://www.domainnameapi.com): البحث عن النطاقات وتسجيلها ونقلها وتجديدها، وإدارة جهات الاتصال وخوادم الأسماء وخوادم الأسماء الفرعية ومناطق DNS وإعادة توجيه عناوين URL. وهو نقل أمين لمكتبة [php-dna](https://github.com/domainreseller/php-dna): الدوال نفسها، والطلبات نفسها، وقيم الإرجاع نفسها، وقد تم التحقق منه باستخدام حالات اختبار التوافق (conformance fixtures) الخاصة بـ php-dna.

## 📦 التنزيل — استخدم دائمًا صفحة الإصدارات (Releases)!

⬇️ **احصل على أحدث نسخة مختبَرة من هنا: https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ **لا** تستخدم الزر الأخضر **Code → Download ZIP** — فهو ينزّل فرع التطوير الخام. حزم الإصدارات مرقّمة الإصدار ومختبَرة وجاهزة لبيئة الإنتاج.

## دليل التثبيت والتكامل

### الحد الأدنى من المتطلبات

- Python 3.8 أو أعلى (يوصى بـ 3.12)
- لا حاجة إلى حزم خارجية: تستخدم المكتبة مكتبة Python القياسية فقط (`urllib` و `json` و `ssl`).

### أ) التثبيت باستخدام pip

```bash
pip install domainnameapi
```

### ب) تثبيت حزمة إصدار

نزّل ملف wheel ‏(`domainnameapi-1.0.0-py3-none-any.whl`) أو أرشيف الشيفرة المصدرية من [أحدث إصدار](https://github.com/domainreseller/python-dna/releases/latest) ثم ثبّته:

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### ج) استخدام الشيفرة المصدرية مباشرة

انسخ المجلد `src/domainnameapi` بجوار شيفرتك (أو أضف `src` إلى `PYTHONPATH`) ثم استورده. يحتوي المجلد [examples](examples) على سكربت جاهز للتشغيل لكل دالة.

## 🔑 بيانات اعتماد API — Reseller ID و API Key

تتواصل المكتبة مع DomainNameAPI REST API وتحتاج فقط إلى بيانات اعتماد اثنتين تُمرَّران إلى الدالة الإنشائية (constructor):

| المُعامِل | القيمة |
|---|---|
| الأول | Reseller ID — بصيغة UUID مثل `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| الثاني | API Key |

> 💡 ستجد **Reseller ID** و **API Key** في لوحة DomainNameAPI الخاصة بك ضمن **إعدادات API**.
> ⚠️ هذه **بيانات اعتماد API** — بيانات تسجيل الدخول إلى اللوحة **لن تعمل** هنا.

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

تتم إزالة المسافات البيضاء في بداية بيانات الاعتماد ونهايتها تلقائيًا.

## البدء السريع

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

تُكتب أسماء الدوال بنمط snake_case ‏(`get_details` و `register_with_contact_info`). كما تعمل أسماء php-dna كأسماء بديلة (aliases)، لذا يمكن للشيفرة المنقولة من PHP الإبقاء على `dna.GetDetails(...)` أو `dna.getDetails(...)`.

## قيم الإرجاع ومعالجة الأخطاء

تُرجع الدوال قيمًا بسيطة من نوع `dict`/`list` بالمفاتيح نفسها التي تُرجعها php-dna تمامًا. وهي **لا** تطلق استثناءات عند مشكلات البوابة أو الشبكة؛ بدلًا من ذلك تحقّق من `result`:

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "...",
                              "GatewayCode": "Dna.DomainService:Domain:10007"}}
```

- يكون `Code` بصيغة `API_<HTTP status>` لأخطاء البوابة (`API_400` و `API_404` و `API_429` و `API_500` ...). أما استجابة إعادة التوجيه (بيانات اعتماد خاطئة) فتُعطي `API_302` مع الرسالة `Invalid API credentials`.
- يُضاف `GatewayCode` إلى أخطاء `API_<status>` عندما ترسل البوابة رمز الخطأ الخاص بها (على سبيل المثال `Dna.DomainService:Domain:10007`)، حتى تتمكن من التمييز بين "النطاق غير موجود" و"TLD غير مدعوم".
- `Message` هي رسالة البوابة. أما أجسام الأخطاء الفارغة فتصبح `HTTP <status> - <reason>` (على سبيل المثال `HTTP 429 - Too Many Requests`).
- يحتوي `Details` على تفاصيل البوابة (أو نص الاستجابة الخام عند عدم وجودها)؛ وتُحوَّل أخطاء التحقق إلى قائمة حقول سهلة القراءة، على سبيل المثال `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`.
- أعطال الشبكة هي أخطاء أيضًا، ولا تكون أبدًا نجاحًا فارغًا: انتهاء المهلة يُرجع `CURL_28` مع `Could not reach the DomainNameAPI service: the connection timed out. (...)`؛ وأعطال DNS والاتصال و TLS تُرجع `CURL_6` و `CURL_7` و `CURL_35`/`CURL_60` مع `Curl error during request: ...` (أرقام أخطاء curl، وهي الرموز نفسها التي تُبلغ عنها php-dna). تُستخدم رموز `API_` لحالات HTTP فقط.
- الرفض خطأ حتى عندما تُجيب البوابة بـ HTTP 200: إذا عاد التسجيل أو النقل أو التجديد بـ `success: false`، تُرجع الدالة `REGISTER_DOMAIN` أو `TRANSFER_DOMAIN` أو `RENEW_DOMAIN` مع رسالة البوابة.
- تحتفظ الأعلام (flags) بأنواع php-dna: `LockStatus` هو السلسلة النصية `"true"`/`"false"`، والأسعار سلاسل نصية منسّقة (`"11.9900"`).

تستخدم بعض الدوال بنية إرجاع خاصة بها، تمامًا كما في php-dna:

| الدالة | عند النجاح | عند الفشل |
|---|---|---|
| `check_availability` | قائمة `list` بسيطة من النتائج | بنية `ERROR` |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `OperationResult: "FAILED"` مع `ErrorCode` (`API_<status>` أو `CURL_<errno>` أو `BALANCE` لعملة لا يُبلغ عنها الحساب) |
| `check_transfer` | `result: "OK"` فقط عندما يكون النطاق قابلًا للنقل | `result: "ERROR"` مع `data` و `error` |
| `is_tr_tld` و `validate_contact` | قيم بسيطة (بدون اتصال بالشبكة) | — |

أخطاء البرمجة فقط (مثل تمرير سلسلة نصية حيث تتوقع `set_resource_record_set` قائمة) هي التي تطلق استثناءً في Python.

مهلة الانتظار 30 ثانية لكل استدعاء و 10 ثوانٍ لإنشاء الاتصال. لا تتم متابعة عمليات إعادة التوجيه.

## وضع الاختبار (OTE)

مرّر `True` كوسيط ثالث لاستخدام بيئة الاختبار `https://ote.domainresellerapi.com/api/v1`. كما تُفهم القيم النصية القادمة من ملفات الإعداد: القيم `"true"` و `"1"` و `"on"` و `"yes"` تفعّل وضع الاختبار، وأي قيمة أخرى (`"false"` و `"0"` و `"off"` و `""`) تُبقي على البيئة الحية.

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## تقارير الأخطاء (القياس عن بُعد)

عندما يفشل استدعاء API، يمكن للمكتبة إرسال تقرير خطأ إلى نظام تتبع الأخطاء الخاص بـ DomainNameAPI ‏(Sentry). كما يُرسَل جزء صغير عشوائي من الاستدعاءات الناجحة (4%، بالإضافة إلى كل استدعاء تتجاوز مدته ثانية واحدة) كسجل أداء. يساعد ذلك DomainNameAPI على اكتشاف المشكلات وإصلاحها. تقارير الأخطاء **مفعّلة افتراضيًا**.

> ℹ️ في الإصدار 1.0.0 لا يزال عنوان Sentry المدمج فارغًا، لأن مشروع Sentry الخاص بـ python-dna لم يُنشأ بعد: **لا يتم إرسال أي شيء** حتى يملأه تحديث للمكتبة، أو حتى تمرّر عنوانك الخاص باستخدام `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")`.

تُرسَل التقارير من خيط (thread) في الخلفية: فهي لا تُبطئ استدعاءك ولا تعطّله أبدًا. ولا يتم أبدًا الإبلاغ عن الأخطاء المتوقعة كثيرة التكرار (نطاق غير موجود، رصيد غير كافٍ، بيانات اعتماد غير صالحة، لا توجد إعادة توجيه مُعدّة، ...).

**ما يتم إرساله:**

- رمز الخطأ ورسالته
- مسار نقطة النهاية المستدعاة وطريقة HTTP
- مدة الاستدعاء
- اسم المكتبة (`DomainNameAPI-Python`) وإصدار المكتبة وإصدار Python
- معرّف الموزع (Reseller ID) واسم النطاق
- عنوان IP العام للخادم (يتم الحصول عليه عبر `api.ipify.org`) واسم مستخدم نظام التشغيل
- طلب API والاستجابة، بما في ذلك بيانات الاتصال الخاصة بالنطاق؛ يتم إخفاء بيانات الاعتماد فقط — تُستبدل رموز EPP/auth ومفاتيح API وكلمات المرور والرموز المميزة (tokens) بـ `***`

**ما لا يتم إرساله أبدًا:** رموز EPP/auth أو مفاتيح API أو كلمات المرور أو الرموز المميزة (tokens) بصيغة مقروءة؛ وسائط استدعاءات الدوال في تتبع المكدس (stack traces).

**لماذا وإلى متى:** تُستخدم البيانات فقط لقياس الاستخدام والتشخيص المبكر للمشكلات، وتُحفظ لمدة 30 يومًا على خادم Sentry الخاص بـ DomainNameAPI، ثم تُحذف تلقائيًا.

**كيفية الإيقاف:** استدعِ `set_error_reporting_enabled(False)` بعد إنشاء العميل:

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**الوضع المختصر:** يرسل `set_telemetry_minimal(True)` رمز الخطأ ورسالته ونقطة النهاية والتوقيت والإصدارات ومعرّف الموزع فقط — دون بيانات الطلب/الاستجابة أو النطاق أو عنوان IP أو اسم المستخدم.

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **الأمان:** التحقق من شهادة TLS مفعّل. على خادم تكون حزمة شهادات CA فيه قديمة، يمكن إيقافه باستخدام `dna.set_ssl_verification(False)` — غير مستحسن؛ تحديث حزمة CA هو الحل الأفضل.

## الاستخدام

تفترض جميع الأمثلة أدناه ما يلي:

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

أمثلة المخرجات هي قيم إرجاع حقيقية من المكتبة.

### الحساب

#### الحصول على معلومات الموزع

تفاصيل حساب الموزع: المعرّف والاسم والأرصدة (USD و TL).

```python
result = dna.get_reseller_details()
```

<details>
<summary>مثال على المخرجات</summary>

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

#### الحصول على الرصيد الحالي

الرصيد الحالي بعملة واحدة: USD (افتراضيًا) أو TRY. العملة التي لا يُبلغ عنها الحساب (EUR و GBP ...) تُرجع OperationResult FAILED مع ErrorCode BALANCE.

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>مثال على المخرجات</summary>

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


### البحث والقوائم

#### التحقق من توفر النطاق

التوفر والسعر لكل تركيبة من اسم النطاق والامتداد. تُرجع قائمة بسيطة عند النجاح، وبنية خطأ عند الفشل.

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>مثال على المخرجات</summary>

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

#### قائمة النطاقات

النطاقات الموجودة في حساب الموزع. عوامل التصفية: PageNumber (يبدأ من 0) و PageSize و OrderColumn و OrderDirection و DomainName ...

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>مثال على المخرجات</summary>

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

#### قائمة امتدادات النطاقات (TLD)

قائمة TLD مع الأسعار لكل مدة (التسجيل، التجديد، النقل، الاستعادة ...).

```python
result = dna.get_tld_list(100)
```

<details>
<summary>مثال على المخرجات</summary>

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


### النطاقات

#### تسجيل النطاق

تسجيل نطاق جديد. يمكن تمرير جهات الاتصال بصيغة مسطّحة (`AddressLine1` و `Phone` ...) أو متداخلة (`Address.Line1` و `Phone.Phone.Number` ...). تُستكمل الحقول الناقصة وتُوحَّد صيغة أرقام الهواتف (انظر `validate_contact`). وإذا كانت قائمة خوادم الأسماء فارغة، تُستخدم `ns1.domainnameapi.com` / `ns2.domainnameapi.com` بدلًا منها.

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
<summary>مثال على المخرجات</summary>

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

#### تسجيل النطاق (.tr)

تحتاج نطاقات `.tr` إلى سمات TRABIS كوسيط سابع. المالك الفرد: `TRABISDOMAINCATEGORY` = `1` و `TRABISCITIZENID` (رقم الهوية). المالك الشركة: `TRABISDOMAINCATEGORY` = `0` و `TRABISTAXOFFICE` و `TRABISTAXNUMBER`. المفاتيح القديمة (`TRABISCITIZIENID` و `TRABISNAMESURNAME` و `TRABISCOUNTRYID` ...) مقبولة: إذ تُحوَّل إلى مخطط REST، وتُحذف المفاتيح غير المدعومة.

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
<summary>مثال على المخرجات</summary>

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

#### تجديد النطاق

تجديد النطاق لعدد السنوات المحدد.

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### تفاصيل النطاق

التفاصيل الكاملة لنطاق واحد: الحالة والتواريخ وخوادم الأسماء وأعلام القفل/الخصوصية وخوادم الأسماء الفرعية.

```python
result = dna.get_details("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

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

#### المزامنة من السجل (Registry)

تحديث بيانات النطاق من السجل (بنية الإرجاع نفسها الخاصة بـ get_details).

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

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

#### تعديل خوادم الأسماء

استبدال خوادم الأسماء الخاصة بالنطاق (تُزال المسافات من الإدخالات وتُحوَّل إلى أحرف صغيرة ويُزال التكرار).

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### تفعيل قفل النطاق

تفعيل قفل المسجّل (الحماية من السرقة).

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### إلغاء قفل النطاق

إيقاف قفل المسجّل (الحماية من السرقة).

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### تعديل خصوصية النطاق

تفعيل حماية خصوصية WHOIS ‏(True) أو إيقافها (False). القيم 1 و"1" و"on" و"true" و"yes" تعني التفعيل أيضًا؛ وأي قيمة أخرى تعني الإيقاف. لا يُرسَل الوسيط reason إلى البوابة.

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### جهات الاتصال

#### الحصول على جهات اتصال النطاق

جهات الاتصال الإدارية (Administrative) والفوترة (Billing) والمسجِّل (Registrant) والتقنية (Technical) للنطاق.

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

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

#### حفظ جهات اتصال النطاق

استبدال جهات الاتصال الأربع للنطاق. `contacts` هو القاموس نفسه المستخدم في مثال التسجيل.

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### خوادم الأسماء الفرعية

#### إضافة خادم أسماء فرعي

إنشاء خادم أسماء فرعي (سجل glue) تحت نطاق.

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### حذف خادم أسماء فرعي

حذف خادم أسماء فرعي.

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### تحديث خادم الأسماء الفرعي

تغيير عنوان IP لخادم أسماء فرعي.

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### عمليات النقل

#### نقل النطاق

بدء عملية نقل واردة باستخدام رمز EPP/auth الخاص بالنطاق. لا تُرسَل جهات الاتصال أبدًا مع النقل (يحمل الطلب دائمًا `"contacts": []`): يتسلّمها المسجّل من المسجّل السابق، لذلك لا تحتوي `transfer` على وسيط لجهات الاتصال. الرفض (`success: false`) يُرجع الخطأ `TRANSFER_DOMAIN`.

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>مثال على المخرجات</summary>

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

#### التحقق من إمكانية النقل

هل يمكن نقل النطاق باستخدام رمز auth هذا؟ تكون قيمة result هي OK فقط عندما يكون ذلك ممكنًا.

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>مثال على المخرجات</summary>

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

#### إلغاء النقل

إلغاء عملية نقل واردة معلّقة.

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### الموافقة على النقل الصادر

الموافقة على عملية نقل صادرة معلّقة.

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### رفض النقل الصادر

رفض عملية نقل صادرة معلّقة.

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### منطقة DNS

تخزّن البوابة سجلات DNS على شكل **مجموعات (sets)**: الاسم + النوع الواحد يحمل قائمة من القيم. كتابة اسم + نوع تستبدل المجموعة بأكملها، والحذف بقيمة واحدة يزيل المجموعة بأكملها. تتولى الدوال `*_record_set` و `*_record_value` معالجة ذلك نيابةً عنك؛ فضّلها على الدوال منخفضة المستوى `add/edit/delete_resource_record`.

- يمكن تمرير الأسماء بالصيغ `"@"` أو `""` أو `"www"` أو `"www.example.com"` أو `"www.example.com."`؛ وتُرسَل على شكل التسمية النسبية التي تتوقعها البوابة. تُرجع `get_resource_records` أسماءً مؤهلة بالكامل (`"www.example.com."`).
- الأنواع المدعومة: `A` و `AAAA` و `ALIAS` و `CAA` و `CNAME` و `DS` و `MX` و `NAPTR` و `PTR` و `SRV` و `TLSA` و `TXT` (تُرفض الأنواع الأخرى قبل إجراء أي استدعاء). قيمة TTL من 1 إلى 86400 ثانية.
- تُطبَّق عمليات الكتابة فورًا؛ مرّر `apply=False` لتجهيز عدة تغييرات ثم استدعِ `apply_resource_records` مرة واحدة. إذا فشل التطبيق التلقائي، تُرجع الدالة خطأ التطبيق (يبقى التغيير مُجهّزًا لكنه غير مُفعّل).
- تفرض البوابة حدًا لمعدل استدعاءات المنطقة، لذا تُبقي المكتبة فاصلًا لا يقل عن ثانية واحدة بين استدعاءات المنطقة (`dna.zone_min_interval`، بالثواني).


#### عرض السجلات

منطقة DNS الخاصة بالنطاق، صف واحد لكل قيمة سجل. تُرجَع الأسماء مؤهلة بالكامل.

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

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

#### تعيين مجموعة سجلات

جعل اسم + نوع كامل مطابقًا تمامًا للقائمة المعطاة (وهو نموذج البوابة نفسها). القائمة الفارغة تزيل المجموعة. تُطبَّق التغييرات فورًا ما لم يُمرَّر apply=False.

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
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### إضافة قيمة واحدة

إضافة قيمة واحدة إلى مجموعة سجلات مع الإبقاء على القيم الموجودة (قراءة-دمج-كتابة). إضافة قيمة موجودة مسبقًا لا تُحدث أي تغيير.

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>مثال على المخرجات</summary>

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

#### إزالة قيمة واحدة

إزالة قيمة واحدة من مجموعة سجلات مع إبقاء القيم الأخرى في مكانها.

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### استبدال قيمة واحدة

استبدال قيمة واحدة من مجموعة سجلات بقيمة أخرى (ما يعادل «تعديل الصف» في لوحة DNS).

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### حذف مجموعة سجلات

إزالة جميع القيم تحت اسم + نوع. إزالة مجموعة غير موجودة تُعدّ OK.

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### إضافة سجل (منخفض المستوى)

منخفض المستوى: كتابة مجموعة سجلات (POST). تستبدل البوابة أي اسم + نوع موجود، لذا فضّل add_resource_record_value() لإلحاق قيمة.

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### تعديل سجل (منخفض المستوى)

منخفض المستوى: إعادة كتابة مجموعة سجلات موجودة (PUT)، تُحدَّد باسمها الحالي.

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### حذف سجل (منخفض المستوى)

منخفض المستوى: حذف (DELETE) حسب الاسم + القيمة + النوع. تزيل البوابة المجموعة **بأكملها**، لذا فضّل remove_resource_record_value() لحذف قيمة واحدة.

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### تطبيق التغييرات المجهّزة

اعتماد تغييرات المنطقة المجهّزة (مطلوب فقط بعد الاستدعاءات التي تمت باستخدام apply=False).

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### إعادة توجيه URL

#### الحصول على إعادة التوجيه

إعادة توجيه URL الخاصة بالنطاق. تكون قيمة Enabled هي False عندما لا يكون هناك أي إعداد.

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### تعيين إعادة التوجيه

إعادة توجيه النطاق إلى عنوان URL: ‏'Standard' (إعادة توجيه عادية) أو 'Frame' (مقنّعة).

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### حذف إعادة التوجيه

إزالة إعادة توجيه URL. تكون قيمة Removed هي False (والنتيجة OK) عندما لا يكون هناك أي إعداد.

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>مثال على المخرجات</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Removed': True}}
```

</details>


### أدوات مساعدة

#### هل النطاق .tr

هل هذا نطاق .tr؟ فحص محلي، بدون استدعاء عبر الشبكة.

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>مثال على المخرجات</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### التحقق من جهة الاتصال

استكمال جهة اتصال وتوحيد صيغتها بالطريقة التي تتوقعها البوابة (محليًا، بدون شبكة): تحصل الحقول الناقصة على قيم بديلة، وتُزال الأرقام وعلامات الترقيم من الأسماء، وتُقسَّم أرقام الهواتف إلى رقم + رمز الدولة، ويُستخدم City بدلًا من State عند غيابه.

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
<summary>مثال على المخرجات</summary>

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


### التشخيص والإعدادات

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

يمكن تمرير طبقة نقل HTTP مخصصة (لمعالجة الوكيل proxy، أو التسجيل، أو الاختبارات) إلى الدالة الإنشائية: أي كائن يحتوي على دالة `send(request)` تُرجع `domainnameapi.HttpResponse`:

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## الاختبارات

لا تحتاج مجموعة الاختبارات إلى بيانات اعتماد ولا تُجري أي استدعاءات شبكة خارجية:

```bash
python -m unittest discover -s tests -v
```

| ملف الاختبار | الوصف |
|-----------|-------------|
| `tests/test_conformance.py` | يشغّل جميع حالات اختبار التوافق الـ 134 الخاصة بـ php-dna: الطلبات نفسها على الشبكة، وقيم الإرجاع نفسها |
| `tests/test_edge_cases.py` | حالات حدّية إضافية مسجّلة من php-dna (استجابات ومدخلات غير معتادة من البوابة) |
| `tests/test_http.py` | طبقة HTTP: الترويسات، سلاسل الاستعلام، أجسام JSON، المهل، إعادة التوجيه |
| `tests/test_errors.py` | ربط أخطاء استجابات البوابة |
| `tests/test_telemetry.py` | بيانات القياس عن بُعد، إخفاء بيانات الاعتماد، إلغاء الاشتراك |
| `tests/test_utils.py` | الأدوات المساعدة ومعالجة القيم المتوافقة مع PHP |

<hr style="border: 4px solid #000; border-style: dashed;">


## رموز العودة والأخطاء مع تفسيراتها

| الرمز | الوصف | التفاصيل |
|------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1000 | تم تنفيذ الأمر بنجاح | العملية ناجحة. |
| 1001 | تم تنفيذ الأمر بنجاح؛ الإجراء معلّق | العملية ناجحة، ولكنها حاليًا في قائمة الانتظار للإكمال. |
| 2003 | معلمة مطلوبة مفقودة | خطأ معلمة مفقودة، على سبيل المثال عدم إدخال رقم الهاتف في معلومات الاتصال. |
| 2105 | الكائن غير مؤهل للتجديد | حالة النطاق غير مناسبة للتجديد، فهو مقفل أمام عمليات التحديث. يجب ألا تكون الحالة "clientupdateprohibited". وقد يرجع ذلك إلى شروط حالة أخرى. |
| 2200 | خطأ في المصادقة | خطأ في التفويض، رمز الأمان غير صحيح أو النطاق مسجّل لدى مسجّل آخر. |
| 2302 | الكائن موجود | اسم النطاق أو معلومات خادم الأسماء موجودة مسبقًا في قاعدة البيانات. لا يمكن التسجيل. |
| 2303 | الكائن غير موجود | اسم النطاق أو معلومات خادم الأسماء غير موجودة في قاعدة البيانات. يلزم تسجيل جديد. |
| 2304 | حالة الكائن تمنع العملية | حالة النطاق غير مناسبة للتحديث، فهو مقفل أمام عمليات التحديث. يجب ألا تكون الحالة "clientupdateprohibited". وقد يرجع ذلك إلى شروط حالة أخرى. |

| الرمز | التفاصيل (نص رسالة البوابة الأصلي)                                                                                                    |
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
| –    | تأكد من إرسال جميع كائنات جهات الاتصال كاملة                                                                                          |
| 340  | Price definition not found ({0}[{1}]-{2}{3}).                                                                                        |
| 350  | Insufficient reseller balance. (Reseller Id : {0} - Current Balance : {1} {2}).                                                      |
| 350  | Accounting currency does not match or the balance is not sufficient.                                                                 |
| 360  | Invalid API request for field ({0}).                                                                                                 |
| 360  | API quota exceeded!                                                                                                                  |
| 361  | Throttled error!                                                                                                                     |
| 362  | Premium domain is not available to register right now.                                                                               |
| 363  | Operation cancelled because domain in auto-renewal period                                                                            |
| 364  | This domain is currently unavailable for transaction due to a problem with the registry                                              |

| الرمز | التفاصيل (نص رسالة البوابة الأصلي)                                                          |
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

| الرمز | التفاصيل (نص رسالة البوابة الأصلي)                                                                                                    |
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


## الترخيص

Apache License 2.0 — انظر [LICENSE](LICENSE).
