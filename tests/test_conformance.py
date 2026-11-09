"""Runs every php-dna conformance fixture (tests/testdata/conformance/*.json).

Each fixture is php-dna's own behaviour against a mock gateway: the queued
responses, the requests php-dna sent and the value it returned. The port
must send the same requests and return the same value.
"""

import glob
import json
import os
import re
import unittest

from tests.support import API_KEY, FIXTURE_DIR, RESELLER, FakeTransport, diff, split_url

from domainnameapi import DomainNameAPI


def snake(name):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def load_fixtures():
    paths = sorted(glob.glob(os.path.join(FIXTURE_DIR, "*.json")))
    out = []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            out.append((os.path.basename(p)[:-5], json.load(fh)))
    return out


FIXTURES = load_fixtures()

# php-dna's transfer() still has an optional contacts argument that its facade
# never forwards. python-dna has no such parameter at all (transfer never sends
# contacts), so the fixture passing one runs with the first three arguments;
# the fixture still checks that the request carries "contacts": [].
ARG_LIMITS = {"transfer": 3}


def run_fixture(fx):
    """Run one fixture; returns a list of problems (empty = pass)."""
    transport = FakeTransport(fx["responses"])
    api = DomainNameAPI(RESELLER, API_KEY, False, transport=transport)
    api.set_error_reporting_enabled(False)
    api.zone_min_interval = 0

    method = getattr(api, snake(fx["call"]))
    args = fx["args"][:ARG_LIMITS[fx["call"]]] if fx["call"] in ARG_LIMITS else fx["args"]
    output = method(*args)

    problems = []
    if len(transport.requests) != len(fx["requests"]):
        problems.append("expected %d request(s), sent %d: %s" % (
            len(fx["requests"]), len(transport.requests),
            [(r.method, r.url) for r in transport.requests]))
    for i, (want, got) in enumerate(zip(fx["requests"], transport.requests)):
        path, query = split_url(got.url)
        body = json.loads(got.body) if got.body not in (None, "") else None
        tag = "request %d" % i
        if got.method != want["method"]:
            problems.append("%s: method %s != %s" % (tag, got.method, want["method"]))
        if path != want["path"]:
            problems.append("%s: path %s != %s" % (tag, path, want["path"]))
        problems.extend("%s query: %s" % (tag, d) for d in diff(want["query"], query))
        problems.extend("%s body: %s" % (tag, d) for d in diff(want["body"], body))
        for h in ("X-API-KEY", "__reseller"):
            if got.headers.get(h) != want["headers"][h]:
                problems.append("%s: header %s %r != %r" % (tag, h, got.headers.get(h), want["headers"][h]))

    actual = json.loads(json.dumps(output))
    problems.extend("output: " + d for d in diff(fx["output"], actual, ignore=tuple(fx.get("ignore", []))))
    return problems


class ConformanceTest(unittest.TestCase):
    def test_fixture_count(self):
        self.assertEqual(len(FIXTURES), 134)

    def test_all_fixtures(self):
        failures = {}
        for name, fx in FIXTURES:
            with self.subTest(fixture=name):
                problems = run_fixture(fx)
                if problems:
                    failures[name] = problems
                self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
