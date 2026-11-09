# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-09

First release: a faithful Python port of [php-dna](https://github.com/domainreseller/php-dna) 4.0.4.

### Added

- `DomainNameAPI` client (alias `DomainNameApi`) with all 45 php-dna methods in snake_case;
  the php-dna camelCase/PascalCase names work as aliases.
  - Account: `get_reseller_details`, `get_current_balance`.
  - Search and lists: `check_availability`, `get_list`, `get_tld_list`.
  - Domains: `get_details`, `sync_from_registry`, `get_contacts`, `save_contacts`, `modify_name_server`,
    `enable_theft_protection_lock`, `disable_theft_protection_lock`, `modify_privacy_protection_status`,
    `renew`, `register_with_contact_info` (including `.tr` TRABIS attribute normalisation).
  - Child nameservers: `add_child_name_server`, `delete_child_name_server`, `modify_child_name_server`.
  - Transfers: `transfer`, `cancel_transfer`, `approve_transfer`, `reject_transfer`, `check_transfer`.
  - DNS zone: `get_resource_records`, `add/edit/delete_resource_record`, `apply_resource_records`,
    `set_resource_record_set`, `delete_resource_record_set`, `add/remove/replace_resource_record_value`,
    with zone call pacing against the gateway's rate limit.
  - URL forwarding: `get_forwarding`, `set_forwarding`, `delete_forwarding`.
  - Utilities: `is_tr_tld`, `validate_contact`; diagnostics (`get_request_data`, `get_response_data`, ...)
    and settings (`set_error_reporting_enabled`, `set_telemetry_minimal`, `set_ssl_verification`).
- Same return values as php-dna (plain `dict`/`list`, string flags, formatted prices) and the same error
  envelope; gateway and network failures are returned, never raised.
- Zero runtime dependencies: standard-library `urllib` transport with 30 s / 10 s connect timeouts, no
  redirect following, `User-Agent: DomainNameAPI-Python/1.0.0`; the transport is injectable.
- Test mode (OTE) with string values (`"true"`, `"1"`, `"on"`, `"yes"`) understood.
- Telemetry port (background, credentials masked, minimal mode, opt-out). The built-in Sentry DSN is
  empty until the python-dna Sentry project exists, so nothing is sent by default yet; `sentry_dsn=`
  overrides it.
- Test suite: all 126 php-dna conformance fixtures, extra php-dna edge cases, and unit tests for the HTTP
  layer, error mapping, telemetry and utilities. Runnable examples for every method.
- README in English, Turkish, German, French, Italian, Dutch, Azerbaijani, Arabic and Simplified Chinese.

[1.0.0]: https://github.com/domainreseller/python-dna/releases/tag/v1.0.0
