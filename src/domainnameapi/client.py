"""Public facade: :class:`DomainNameAPI`.

Port of php-dna ``DomainNameAPI_PHPLibrary``. Authenticates with a Reseller
ID (UUID) and an API Key and delegates to :class:`~domainnameapi.rest.DNARest`.
"""

import re

from . import _php as php
from .rest import DNARest

_TRUE_STRINGS = ("1", "true", "on", "yes")


def _parse_test_mode(value):
    """Panels store checkboxes as strings; ``"false"``/``"off"`` must stay off (BUG-10284)."""
    if isinstance(value, str):
        return php.trim(value).lower() in _TRUE_STRINGS
    return php.to_bool(value)


def _snake_case(name):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


class DomainNameAPI(object):
    """DomainNameAPI client.

    :param reseller_id: Reseller ID (UUID) from the DomainNameAPI panel, API Settings.
    :param api_key: API Key from the same page. Panel login credentials do not work.
    :param test_mode: ``True`` (or ``"true"``, ``"1"``, ``"on"``, ``"yes"``) uses the
        OTE test environment.
    :param transport: optional object with ``send(HttpRequest) -> HttpResponse``,
        replaces the default ``urllib`` transport (proxies, tests).
    :param sentry_dsn: optional Sentry DSN overriding the built-in telemetry target.

    Every network method returns a ``dict``/``list`` exactly like php-dna and
    never raises for gateway or network failures: check ``result`` (``'OK'``
    or ``'ERROR'``) and ``error`` (``Code``, ``Message``, ``Details``).
    Methods are snake_case (``get_details``); the php-dna camelCase and
    PascalCase names (``getDetails``, ``GetDetails``) work as aliases.
    """

    def __init__(self, reseller_id="", api_key="", test_mode=False, transport=None, sentry_dsn=None):
        reseller_id = php.trim(reseller_id)
        api_key = php.trim(api_key)
        self._client = DNARest(reseller_id, api_key, _parse_test_mode(test_mode),
                               transport=transport, sentry_dsn=sentry_dsn)

    @property
    def client(self):
        """The underlying :class:`~domainnameapi.rest.DNARest` instance."""
        return self._client

    def __getattr__(self, name):
        # php-dna style names: getDetails / GetDetails -> get_details.
        if name.startswith("_"):
            raise AttributeError(name)
        snake = _snake_case(name)
        if snake != name and snake in type(self).__dict__:
            return getattr(self, snake)
        raise AttributeError("Method %s does not exist" % name)

    # -- account ----------------------------------------------------------

    def get_reseller_details(self):
        """Reseller account: id, name and balances (USD and TL)."""
        return self._client.get_reseller_details()

    def get_current_balance(self, currency_id="USD"):
        """Balance in one currency (``USD``, ``TRY``, ``EUR``, ``GBP``)."""
        return self._client.get_current_balance(currency_id)

    # -- search and lists ---------------------------------------------------

    def check_availability(self, domains, extensions, period, command="create"):
        """Availability and price of every ``domain.extension`` combination."""
        return self._client.check_availability(domains, extensions, period, command)

    def get_list(self, extra_parameters=None):
        """Domains in the account (``PageNumber``/``PageSize``/``OrderColumn``/... filters)."""
        return self._client.get_list(extra_parameters if extra_parameters is not None else {})

    def get_tld_list(self, count=20):
        """TLDs with prices per period."""
        return self._client.get_tld_list(count)

    # -- domain -------------------------------------------------------------

    def get_details(self, domain_name):
        return self._client.get_details(domain_name)

    def sync_from_registry(self, domain_name):
        return self._client.sync_from_registry(domain_name)

    def get_contacts(self, domain_name):
        return self._client.get_contacts(domain_name)

    def save_contacts(self, domain_name, contacts):
        return self._client.save_contacts(domain_name, contacts)

    def modify_name_server(self, domain_name, name_servers):
        return self._client.modify_name_server(domain_name, name_servers)

    def enable_theft_protection_lock(self, domain_name):
        return self._client.enable_theft_protection_lock(domain_name)

    def disable_theft_protection_lock(self, domain_name):
        return self._client.disable_theft_protection_lock(domain_name)

    def modify_privacy_protection_status(self, domain_name, status, reason="Owner request"):
        return self._client.modify_privacy_protection_status(domain_name, status, reason)

    def renew(self, domain_name, period):
        return self._client.renew(domain_name, period)

    def register_with_contact_info(self, domain_name, period, contacts, name_servers=None,
                                   epp_lock=True, privacy_lock=False, additional_attributes=None):
        return self._client.register_with_contact_info(
            domain_name, period, contacts,
            name_servers if name_servers is not None else [],
            epp_lock, privacy_lock,
            additional_attributes if additional_attributes is not None else [],
        )

    # -- child nameservers --------------------------------------------------

    def add_child_name_server(self, domain_name, name_server, ip_address):
        return self._client.add_child_name_server(domain_name, name_server, ip_address)

    def delete_child_name_server(self, domain_name, name_server):
        return self._client.delete_child_name_server(domain_name, name_server)

    def modify_child_name_server(self, domain_name, name_server, ip_address):
        return self._client.modify_child_name_server(domain_name, name_server, ip_address)

    # -- transfers ------------------------------------------------------------

    def transfer(self, domain_name, epp_code, period, contacts=None):
        """Start an incoming transfer.

        ``contacts`` is accepted for signature compatibility but, exactly like
        the php-dna 4.0.4 facade, it is not forwarded: the request always
        carries ``"contacts": []``. Use ``client.transfer(...)`` on the
        underlying :class:`DNARest` to send contacts.
        """
        return self._client.transfer(domain_name, epp_code, period)

    def cancel_transfer(self, domain_name):
        return self._client.cancel_transfer(domain_name)

    def approve_transfer(self, domain_name):
        return self._client.approve_transfer(domain_name)

    def reject_transfer(self, domain_name):
        return self._client.reject_transfer(domain_name)

    def check_transfer(self, domain_name, auth_code):
        return self._client.check_transfer(domain_name, auth_code)

    # -- DNS zone -------------------------------------------------------------

    def get_resource_records(self, domain_name):
        return self._client.get_resource_records(domain_name)

    def add_resource_record(self, domain_name, name, type, content, ttl=3600, apply=True):  # noqa: A002
        return self._client.add_resource_record(domain_name, name, type, content, ttl, apply)

    def edit_resource_record(self, domain_name, record_name, name, type, content, ttl=3600, apply=True):  # noqa: A002
        return self._client.edit_resource_record(domain_name, record_name, name, type, content, ttl, apply)

    def delete_resource_record(self, domain_name, name, record, record_type, apply=True):
        return self._client.delete_resource_record(domain_name, name, record, record_type, apply)

    def apply_resource_records(self, domain_name):
        return self._client.apply_resource_records(domain_name)

    def set_resource_record_set(self, domain_name, name, type, contents, ttl=3600, apply=True):  # noqa: A002
        return self._client.set_resource_record_set(domain_name, name, type, contents, ttl, apply)

    def delete_resource_record_set(self, domain_name, name, type, apply=True, known_value=""):  # noqa: A002
        return self._client.delete_resource_record_set(domain_name, name, type, apply, known_value)

    def add_resource_record_value(self, domain_name, name, type, value, ttl=None, apply=True):  # noqa: A002
        return self._client.add_resource_record_value(domain_name, name, type, value, ttl, apply)

    def remove_resource_record_value(self, domain_name, name, type, value, apply=True):  # noqa: A002
        return self._client.remove_resource_record_value(domain_name, name, type, value, apply)

    def replace_resource_record_value(self, domain_name, name, type, old_value, new_value, ttl=None, apply=True):  # noqa: A002
        return self._client.replace_resource_record_value(domain_name, name, type, old_value, new_value, ttl, apply)

    # -- forwarding -----------------------------------------------------------

    def get_forwarding(self, domain_name):
        return self._client.get_forwarding(domain_name)

    def set_forwarding(self, domain_name, redirect_address, forward_type="Standard"):
        """Point the domain at a URL: ``'Standard'`` redirect or ``'Frame'`` (masked)."""
        return self._client.set_forwarding(domain_name, redirect_address, forward_type)

    def delete_forwarding(self, domain_name):
        return self._client.delete_forwarding(domain_name)

    # -- utilities (no network) -----------------------------------------------

    def is_tr_tld(self, domain):
        return self._client.is_tr_tld(domain)

    def validate_contact(self, contact):
        return self._client.validate_contact(contact)

    # -- diagnostics ----------------------------------------------------------

    def get_request_data(self):
        return self._client.get_request_data()

    def set_request_data(self, request):
        self._client.set_request_data(request)
        return self

    def get_response_data(self):
        return self._client.get_response_data()

    def set_response_data(self, response):
        self._client.set_response_data(response)
        return self

    def get_response_headers(self):
        return self._client.get_response_headers()

    def set_response_headers(self, headers):
        self._client.set_response_headers(headers)
        return self

    def get_parsed_response_data(self):
        return self._client.get_parsed_response_data()

    def set_parsed_response_data(self, response):
        self._client.set_parsed_response_data(response)
        return self

    def get_last_function(self):
        return self._client.get_last_function()

    def set_last_function(self, function):
        self._client.set_last_function(function)
        return self

    def get_service_url(self):
        return self._client.get_service_url()

    def set_service_url(self, url):
        self._client.set_service_url(url)

    # -- settings -------------------------------------------------------------

    def set_error_reporting_enabled(self, enabled):
        """Turn telemetry (error and performance reports) on or off."""
        self._client.set_error_reporting_enabled(enabled)

    def set_telemetry_minimal(self, minimal):
        """Send only error code/message, endpoint, timing, versions and reseller ID."""
        self._client.set_telemetry_minimal(minimal)

    def set_ssl_verification(self, enabled):
        """TLS certificate verification (on by default; switch off only for an outdated CA bundle)."""
        self._client.set_ssl_verification(enabled)

    @property
    def zone_min_interval(self):
        """Minimum seconds between two DNS zone calls (default 1.0)."""
        return self._client.zone_min_interval

    @zone_min_interval.setter
    def zone_min_interval(self, seconds):
        self._client.zone_min_interval = float(seconds)
