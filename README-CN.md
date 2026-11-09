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


# python-dna：适用于 Python 的 DomainNameAPI 客户端

适用于 [DomainNameAPI](https://www.domainnameapi.com) 经销商 REST API 的 Python 客户端：查询、注册、转移和续费域名，管理联系人、名称服务器、子名称服务器、DNS 区域和 URL 转发。它是 [php-dna](https://github.com/domainreseller/php-dna) 的忠实移植版本：相同的方法、相同的请求、相同的返回值，并已通过 php-dna 一致性测试用例（conformance fixtures）的验证。

## 📦 下载 — 请务必使用 Releases！

⬇️ **在此获取最新的经过测试的版本：https://github.com/domainreseller/python-dna/releases/latest**

> ⚠️ 请**不要**使用绿色的 **Code → Download ZIP** 按钮 — 它下载的是未经测试的开发分支。Release 包经过版本管理和测试，可直接用于生产环境。

## 安装和集成指南

### 最低要求

- Python 3.8 或更高版本（推荐 3.12）
- 无需第三方包：本库仅使用 Python 标准库（`urllib`、`json`、`ssl`）。

### A) 使用 pip 安装

```bash
pip install domainnameapi
```

### B) 安装 Release 包

从[最新版本](https://github.com/domainreseller/python-dna/releases/latest)下载 wheel 文件（`domainnameapi-1.0.0-py3-none-any.whl`）或源码压缩包，然后进行安装：

```bash
pip install domainnameapi-1.0.0-py3-none-any.whl
```

### C) 直接使用源码

将 `src/domainnameapi` 文件夹复制到您的代码旁边（或将 `src` 添加到 `PYTHONPATH`），然后导入即可。[examples](examples) 文件夹中为每个方法都提供了一个可直接运行的脚本。

## 🔑 API 凭据 — Reseller ID 与 API Key

本库通过 DomainNameAPI REST API 通信，只需向构造函数传入两项凭据：

| 参数 | 值 |
|---|---|
| 第一个 | Reseller ID — 形如 `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` 的 UUID |
| 第二个 | API Key |

> 💡 您可以在 DomainNameAPI 面板的 **API 设置** 中找到您的 **Reseller ID** 和 **API Key**。
> ⚠️ 这些是 **API 凭据** — 面板登录信息在此**无法使用**。

```python
from domainnameapi import DomainNameAPI

reseller_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
api_key = "your-api-key"

# Live environment
dna = DomainNameAPI(reseller_id, api_key)

# Test (OTE) environment
dna = DomainNameAPI(reseller_id, api_key, True)
```

凭据前后的空白字符会被自动去除。

## 快速入门

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")

details = dna.get_details("example.com")
if details["result"] == "OK":
    print(details["data"]["Dates"]["Expiration"])
else:
    print(details["error"]["Code"], details["error"]["Message"])
```

方法名采用 snake_case 风格（`get_details`、`register_with_contact_info`）。php-dna 的方法名也可作为别名使用，因此从 PHP 移植过来的代码可以继续使用 `dna.GetDetails(...)` 或 `dna.getDetails(...)`。

## 返回值与错误处理

各方法返回普通的 `dict`/`list` 值，其键与 php-dna 返回的完全一致。对于网关或网络问题，方法**不会**抛出异常；请检查 `result`：

```python
# Success
{"result": "OK", "data": {...}}

# Failure
{"result": "ERROR", "error": {"Code": "API_404", "Message": "...", "Details": "..."}}
```

- 对于网关错误，`Code` 为 `API_<HTTP status>`（HTTP 状态码）（`API_400`、`API_404`、`API_429`、`API_500` 等）。重定向响应（凭据错误）会返回 `API_302`，消息为 `Invalid API credentials`。
- `Message` 为网关返回的消息。错误响应体为空时，会变为 `HTTP <status> - <reason>`（例如 `HTTP 429 - Too Many Requests`）。
- `Details` 包含网关返回的详细信息；校验错误会被整理成易读的字段列表，例如 `Admin PostalCode, Tech PostalCode - 'PostalCode' is required`。
- 网络故障同样作为错误返回，绝不会返回空的成功结果：超时返回 `API_28`，消息为 `Could not reach the DomainNameAPI service: the connection timed out. (...)`；DNS、连接和 TLS 故障返回 `API_6`、`API_7`、`API_35`/`API_60`，消息为 `Curl error during request: ...`（即 curl 错误编号，与 php-dna 报告的代码相同）。
- 标志位保留 php-dna 的类型：`LockStatus` 是字符串 `"true"`/`"false"`，价格是格式化后的字符串（`"11.9900"`）。

少数方法使用自己的返回结构，与 php-dna 完全一致：

| 方法 | 成功时 | 失败时 |
|---|---|---|
| `check_availability` | 结果组成的普通 `list` | `ERROR` 返回结构 |
| `get_current_balance` | `OperationResult: "SUCCESS"` | `OperationResult: "FAILED"`，附带 `ErrorCode` |
| `check_transfer` | 仅当域名可转移时为 `result: "OK"` | `result: "ERROR"`，附带 `data` 和 `error` |
| `is_tr_tld`、`validate_contact` | 普通值（不访问网络） | — |

只有编程错误（例如在 `set_resource_record_set` 需要列表的地方传入了字符串）才会抛出 Python 异常。

超时时间为每次调用 30 秒、建立连接 10 秒。不会跟随重定向。

## 测试模式（OTE）

将 `True` 作为第三个参数传入即可使用测试环境 `https://ote.domainresellerapi.com/api/v1`。来自配置文件的字符串值也能被识别：`"true"`、`"1"`、`"on"`、`"yes"` 会启用测试模式，其他任何值（`"false"`、`"0"`、`"off"`、`""`）则保持正式环境。

```python
dna = DomainNameAPI(reseller_id, api_key, True)
dna = DomainNameAPI(reseller_id, api_key, os.environ.get("DNA_TEST_MODE", "false"))
```

## 错误报告（遥测）

当 API 调用失败时，本库可以向 DomainNameAPI 自己的错误跟踪系统（Sentry）发送一份错误报告。成功调用中会随机抽取一小部分（4%，另外所有耗时超过 1 秒的调用）作为性能记录发送。这有助于 DomainNameAPI 发现并修复问题。错误报告**默认开启**。

> ℹ️ 在 1.0.0 版本中，内置的 Sentry 地址仍为空，因为 python-dna 的 Sentry 项目尚未创建：在库的后续更新填入该地址之前，或在您通过 `DomainNameAPI(..., sentry_dsn="https://key@sentry.example.com/1")` 传入自己的地址之前，**不会发送任何数据**。

报告通过后台线程发送：绝不会拖慢或中断您的调用。预期内的高频错误（域名未找到、余额不足、凭据无效等）永远不会被报告。

**发送的内容：**

- 错误代码和消息
- 所调用端点的路径和 HTTP 方法
- 调用耗时
- 库名称（`DomainNameAPI-Python`）、库版本和 Python 版本
- 经销商 ID（Reseller ID）和域名
- 服务器的公网 IP 地址（通过 `api.ipify.org` 获取）以及操作系统用户名
- API 请求和响应，包括域名的联系人信息；仅凭据会被屏蔽——EPP/授权码、API 密钥、密码和令牌会被替换为 `***`

**绝不发送的内容：** 可读形式的 EPP/授权码、API 密钥、密码或令牌；堆栈跟踪中的函数调用参数。

**用途与保留期限：** 这些数据仅用于使用情况统计和问题的早期诊断，在 DomainNameAPI 自己的 Sentry 服务器上保存 30 天，之后自动删除。

**如何关闭：** 在创建客户端之后调用 `set_error_reporting_enabled(False)`：

```python
dna = DomainNameAPI(reseller_id, api_key)
dna.set_error_reporting_enabled(False)
```

**精简模式：** `set_telemetry_minimal(True)` 仅发送错误代码和消息、端点、耗时、版本信息和经销商 ID——不包含请求/响应数据、域名、IP 地址或用户名。

```python
dna.set_telemetry_minimal(True)
```

> 🔒 **安全：** TLS 证书验证默认开启。在 CA 证书包过旧的服务器上，可以通过 `dna.set_ssl_verification(False)` 关闭——不建议这样做；更新 CA 证书包才是更好的解决办法。

## 使用方法

以下所有示例均假定：

```python
from domainnameapi import DomainNameAPI

dna = DomainNameAPI("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "your-api-key")
```

示例输出均为本库真实的返回值。

### 账户

#### 获取经销商详细信息

经销商账户详细信息：ID、名称和余额（USD 和 TL）。

```python
result = dna.get_reseller_details()
```

<details>
<summary>示例输出</summary>

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

#### 获取当前余额

以单一货币表示的当前余额：USD（默认）、TRY、EUR 或 GBP。

```python
result = dna.get_current_balance("USD")
```

<details>
<summary>示例输出</summary>

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


### 查询与列表

#### 域名可用性检查

查询每个域名与后缀组合的可用性和价格。成功时返回普通列表，失败时返回错误结构。

```python
result = dna.check_availability(
    ["dnaprobexyz123", "google", "premium"],  # names without extension
    ["com", "net"],                           # extensions
    1,                                        # period (years)
    "create",                                 # command: create / renew / transfer
)
```

<details>
<summary>示例输出</summary>

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

#### 域名列表

经销商账户中的域名。筛选条件：PageNumber（从 0 开始）、PageSize、OrderColumn、OrderDirection、DomainName ……

```python
result = dna.get_list({
    "PageNumber": 0,
    "PageSize": 50,
    "OrderColumn": "ExpirationDate",
    "OrderDirection": "DESC",
})
```

<details>
<summary>示例输出</summary>

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

#### TLD 列表

TLD 列表，包含各期限的价格（注册、续费、转移、赎回 ……）。

```python
result = dna.get_tld_list(100)
```

<details>
<summary>示例输出</summary>

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


### 域名

#### 域名注册

注册新域名。联系人可以以扁平形式（`AddressLine1`、`Phone` ……）或嵌套形式（`Address.Line1`、`Phone.Phone.Number` ……）提供。缺失的字段会被自动补全，电话号码会被规范化（参见 `validate_contact`）。名称服务器列表为空时，将回退为 `ns1.domainnameapi.com` / `ns2.domainnameapi.com`。

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
<summary>示例输出</summary>

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

#### 域名注册（.tr）

`.tr` 域名需要将 TRABIS 属性作为第 7 个参数传入。个人持有者：`TRABISDOMAINCATEGORY` = `1` 以及 `TRABISCITIZENID`（身份证号码）。企业持有者：`TRABISDOMAINCATEGORY` = `0`、`TRABISTAXOFFICE` 和 `TRABISTAXNUMBER`。旧版键名（`TRABISCITIZIENID`、`TRABISNAMESURNAME`、`TRABISCOUNTRYID` ……）同样可以使用：它们会被转换为 REST 结构，不受支持的键会被丢弃。

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
<summary>示例输出</summary>

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

#### 域名续费

按指定年数为域名续费。

```python
result = dna.renew("example.com", 1)
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'ExpirationDate': '2027-11-09T12:00:00'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 域名详细信息

单个域名的完整信息：状态、日期、名称服务器、锁定/隐私标志、子名称服务器。

```python
result = dna.get_details("example.com")
```

<details>
<summary>示例输出</summary>

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

#### 从注册局同步

从注册局刷新域名信息（返回结构与 get_details 相同）。

```python
result = dna.sync_from_registry("example.com")
```

<details>
<summary>示例输出</summary>

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

#### 修改名称服务器

替换域名的名称服务器（各条目会被去除首尾空白、转为小写并去重）。

```python
result = dna.modify_name_server("example.com", ["ns1.example.net", "ns2.example.net"])
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'NameServers': ['ns1.example.net', 'ns2.example.net']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 启用域名锁定

开启注册商锁（防盗保护）。

```python
result = dna.enable_theft_protection_lock("example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'LockStatus': True}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 禁用域名锁定

关闭注册商锁（防盗保护）。

```python
result = dna.disable_theft_protection_lock("example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'LockStatus': False}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 修改域名隐私保护

开启（True）或关闭（False）WHOIS 隐私保护。

```python
result = dna.modify_privacy_protection_status("example.com", True, "Owner request")
```

<details>
<summary>示例输出</summary>

```python
{'data': {'PrivacyProtectionStatus': True}, 'result': 'OK'}
```

</details>


### 联系人

#### 获取域名联系人

域名的管理（Administrative）、账单（Billing）、注册人（Registrant）和技术（Technical）联系人。

```python
result = dna.get_contacts("example.com")
```

<details>
<summary>示例输出</summary>

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

#### 保存域名联系人

替换域名的四个联系人。`contacts` 与注册示例中的字典相同。

```python
result = dna.save_contacts("example.com", contacts)
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'contacts': {}}}
```

</details>


### 子名称服务器

#### 添加子名称服务器

在域名下创建子名称服务器（glue 记录）。

```python
result = dna.add_child_name_server("example.com", "ns1.example.com", "192.0.2.10")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.10']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 删除子名称服务器

删除子名称服务器。

```python
result = dna.delete_child_name_server("example.com", "ns1.example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'NameServer': 'ns1.example.com'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 修改子名称服务器

修改子名称服务器的 IP 地址。

```python
result = dna.modify_child_name_server("example.com", "ns1.example.com", "192.0.2.20")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'NameServer': 'ns1.example.com', 'IPAdresses': ['192.0.2.20']}}
```

</details>


### 转移

#### 域名转移

使用域名的 EPP/授权码发起转入。与 php-dna 的外观类（facade）一样，可选的第四个参数（`contacts`）会被接受但不会被发送；如需随转移一起发送联系人，请使用 `dna.client.transfer(domain, code, period, contacts)`。

```python
result = dna.transfer("example.com", "Ab1!xyZ9", 1)
```

<details>
<summary>示例输出</summary>

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

#### 检查转移

该域名能否使用此授权码进行转移？仅当可以转移时 result 才为 OK。

```python
result = dna.check_transfer("example.com", "Ab1!xyZ9")
```

<details>
<summary>示例输出</summary>

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

#### 取消转移

取消待处理的转入。

```python
result = dna.cancel_transfer("example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Cancelled'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 批准转出

批准待处理的转出。

```python
result = dna.approve_transfer("example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Approved'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 拒绝转出

拒绝待处理的转出。

```python
result = dna.reject_transfer("example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com', 'Status': 'Rejected'}}
```

</details>


### DNS 区域

网关以**记录集**（set）的形式存储 DNS 记录：一个名称 + 类型对应一个值列表。写入某个名称 + 类型会替换整个记录集，而按单个值删除会删除整个记录集。`*_record_set` 和 `*_record_value` 方法会替您处理这些细节；请优先使用它们，而不是底层的 `add/edit/delete_resource_record`。

- 名称可以写作 `"@"`、`""`、`"www"`、`"www.example.com"` 或 `"www.example.com."`；它们会以网关所需的相对标签形式发送。`get_resource_records` 返回的是完全限定名称（`"www.example.com."`）。
- 支持的类型：`A`、`AAAA`、`ALIAS`、`CAA`、`CNAME`、`DS`、`MX`、`NAPTR`、`PTR`、`SRV`、`TLSA`、`TXT`（其他类型会在发起任何调用之前被拒绝）。TTL 为 1 到 86400 秒。
- 写入操作会立即生效；传入 `apply=False` 可暂存多项更改，然后调用一次 `apply_resource_records`。
- 网关对区域调用有速率限制，因此本库会让区域调用之间至少间隔一秒（`dna.zone_min_interval`，单位为秒）。


#### 列出记录

域名的 DNS 区域，每个记录值占一行。返回的名称为完全限定名称。

```python
result = dna.get_resource_records("example.com")
```

<details>
<summary>示例输出</summary>

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

#### 设置记录集

使某个名称 + 类型与给定列表完全一致（即网关自身的模型）。传入空列表会删除该记录集。除非指定 apply=False，否则更改会立即生效。

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
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'Name': '',
          'Type': 'MX',
          'TTL': 3600,
          'Contents': ['10 mx1.example.com', '20 mx2.example.com']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 添加单个值

向记录集中添加一个值，并保留已有的值（读取-合并-写入）。添加已存在的值不会产生任何操作。

```python
result = dna.add_resource_record_value("example.com", "@", "MX", "30 mx3.example.com")
```

<details>
<summary>示例输出</summary>

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

#### 删除单个值

从记录集中删除一个值，其他值保持不变。

```python
result = dna.remove_resource_record_value("example.com", "@", "MX", "20 mx2.example.com.")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'MX', 'TTL': 3600, 'Contents': ['10 mx1.example.com.']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 替换单个值

将记录集中的一个值替换为另一个值（相当于 DNS 面板中的“编辑行”）。

```python
result = dna.replace_resource_record_value("example.com", "@", "A", "192.0.2.1", "192.0.2.2")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'Name': '', 'Type': 'A', 'TTL': 3600, 'Contents': ['192.0.2.2']}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 删除记录集

删除某个名称 + 类型下的所有值。删除不存在的记录集也会返回 OK。

```python
result = dna.delete_resource_record_set("example.com", "@", "MX")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'Name': 'example.com.', 'Type': 'MX', 'Content': '10 mx1.example.com.'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 添加记录（底层）

底层方法：写入一个记录集（POST）。网关会替换已存在的名称 + 类型，因此如需追加值，请优先使用 add_resource_record_value()。

```python
result = dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300)
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'a', 'TTL': 300, 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 编辑记录（底层）

底层方法：重写一个已有的记录集（PUT），通过其当前名称来定位。

```python
result = dna.edit_resource_record("example.com", "www", "www", "A", "192.0.2.6", 600)
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'Name': 'www', 'Type': 'A', 'TTL': 600, 'Content': '192.0.2.6'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 删除记录（底层）

底层方法：按名称 + 值 + 类型执行 DELETE。网关会删除**整个**记录集，因此如需删除单个值，请优先使用 remove_resource_record_value()。

```python
result = dna.delete_resource_record("example.com", "www", "192.0.2.5", "A")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'Name': 'www', 'Type': 'A', 'Content': '192.0.2.5'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 应用暂存的更改

提交暂存的区域更改（仅在使用 apply=False 进行调用后才需要）。

```python
dna.add_resource_record("example.com", "www", "A", "192.0.2.5", 300, False)
dna.add_resource_record("example.com", "api", "A", "192.0.2.6", 300, False)
result = dna.apply_resource_records("example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### URL 转发

#### 获取转发设置

域名的 URL 转发。未进行任何配置时，Enabled 为 False。

```python
result = dna.get_forwarding("example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'Enabled': True,
          'RedirectAddress': 'https://www.example.org/landing',
          'ForwardType': 'Frame'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 设置转发

将域名转发到某个 URL：'Standard'（普通重定向）或 'Frame'（隐藏式转发）。

```python
result = dna.set_forwarding("example.com", "https://www.example.org", "Standard")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK',
 'data': {'RedirectAddress': 'https://www.example.org', 'ForwardType': 'Standard'}}
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 删除转发

删除 URL 转发。

```python
result = dna.delete_forwarding("example.com")
```

<details>
<summary>示例输出</summary>

```python
{'result': 'OK', 'data': {'DomainName': 'example.com'}}
```

</details>


### 实用工具

#### 是否为 .tr 域名

这是 .tr 域名吗？本地检查，不发起网络调用。

```python
result = dna.is_tr_tld("example.com.tr")
```

<details>
<summary>示例输出</summary>

```python
True
```

</details>


<hr style="border: 4px solid #000; border-style: dashed;">

#### 校验联系人

按照网关期望的方式补全并规范化联系人（本地执行，不访问网络）：缺失的字段会填入占位值，姓名中的数字和标点会被去除，电话号码会被拆分为号码 + 国家代码，State 为空时回退为 City。

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
<summary>示例输出</summary>

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


### 诊断与设置

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

可以向构造函数传入自定义的 HTTP 传输层（用于代理处理、日志记录、测试）：任何具有 `send(request)` 方法并返回 `domainnameapi.HttpResponse` 的对象均可：

```python
from domainnameapi import DomainNameAPI, HttpResponse, UrllibTransport


class LoggingTransport(UrllibTransport):
    def send(self, request):
        print(request.method, request.url)
        return super().send(request)


dna = DomainNameAPI(reseller_id, api_key, transport=LoggingTransport())
```

## 测试

测试套件无需任何凭据，也不会发起任何外部网络调用：

```bash
python -m unittest discover -s tests -v
```

| 测试文件 | 说明 |
|-----------|-------------|
| `tests/test_conformance.py` | 运行全部 126 个 php-dna 一致性测试用例：线路上的请求相同，返回值也相同 |
| `tests/test_edge_cases.py` | 从 php-dna 记录的额外边界情况（不常见的网关响应和输入） |
| `tests/test_http.py` | HTTP 层：请求头、查询字符串、JSON 请求体、超时、重定向 |
| `tests/test_errors.py` | 网关响应的错误映射 |
| `tests/test_telemetry.py` | 遥测数据、凭据屏蔽、关闭选项 |
| `tests/test_utils.py` | 实用工具以及与 PHP 兼容的值处理 |

<hr style="border: 4px solid #000; border-style: dashed;">


## 返回和错误代码及说明

| 代码 | 描述 | 详细 |
|------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1000 | 命令成功完成 | 操作成功。 |
| 1001 | 命令成功完成；操作待处理 | 操作成功。但是，操作当前已排队等待完成。 |
| 2003 | 缺少必需参数 | 参数缺失错误。例如：联系信息中没有电话输入。 |
| 2105 | 对象不符合续费条件 | 域名状态不适合续费，已锁定更新操作。状态不应为 "clientupdateprohibited"。也可能由其他状态条件导致。 |
| 2200 | 身份验证错误 | 授权错误，安全代码不正确或域名在另一个注册商处注册。 |
| 2302 | 对象已存在 | 域名或名称服务器信息已存在于数据库中。无法注册。 |
| 2303 | 对象不存在 | 域名或名称服务器信息在数据库中不存在。需要新注册。 |
| 2304 | 对象状态禁止操作 | 域名状态不适合更新，已锁定更新操作。状态不应为 "clientupdateprohibited"。也可能由其他状态条件导致。 |

| 代码 | 详细（网关消息原文）                                                                                                                 |
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
| –    | 请确保发送完整的所有联系人对象                                                                                                       |
| 340  | Price definition not found ({0}[{1}]-{2}{3}).                                                                                        |
| 350  | Insufficient reseller balance. (Reseller Id : {0} - Current Balance : {1} {2}).                                                      |
| 350  | Accounting currency does not match or the balance is not sufficient.                                                                 |
| 360  | Invalid API request for field ({0}).                                                                                                 |
| 360  | API quota exceeded!                                                                                                                  |
| 361  | Throttled error!                                                                                                                     |
| 362  | Premium domain is not available to register right now.                                                                               |
| 363  | Operation cancelled because domain in auto-renewal period                                                                            |
| 364  | This domain is currently unavailable for transaction due to a problem with the registry                                              |

| 代码 | 详细（网关消息原文）                                                                        |
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

| 代码 | 详细（网关消息原文）                                                                                                                 |
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


## 许可证

Apache License 2.0 — 参见 [LICENSE](LICENSE)。
