"""Extra php-dna edge cases: odd gateway shapes and loosely typed inputs.

Same format as the conformance fixtures. They were produced by running
php-dna 4.0.4 itself (its conformance generator and mock gateway) on extra
scenarios: numeric strings, assoc arrays, unusual price/zone/list shapes,
error bodies without messages and similar inputs a PHP caller may pass.
"""

import glob
import json
import os
import unittest

from tests.support import ROOT
from tests.test_conformance import run_fixture

EDGE_DIR = os.path.join(ROOT, "tests", "testdata", "php-edge-cases")


class PhpEdgeCaseTest(unittest.TestCase):
    def test_edge_cases(self):
        paths = sorted(glob.glob(os.path.join(EDGE_DIR, "*.json")))
        self.assertGreater(len(paths), 0)
        for path in paths:
            with open(path, encoding="utf-8") as fh:
                fx = json.load(fh)
            with self.subTest(fixture=fx["id"]):
                problems = run_fixture(fx)
                self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
