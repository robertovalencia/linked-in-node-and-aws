"""Regression for the real CI Kafka cluster-ID option parsing failure; no AWS."""
import base64
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("prepare", Path(__file__).with_name("aws-ecs-prepare-secrets.py"))
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class ClusterIdTest(unittest.TestCase):
    def test_retries_leading_hyphen_encoding(self):
        rejected = b"\xf8" + b"\x00" * 15
        accepted = b"\x00" * 16
        self.assertTrue(base64.urlsafe_b64encode(rejected).startswith(b"-"))
        with patch.object(prepare.secrets, "token_bytes", side_effect=[rejected, accepted]) as random:
            value = prepare.generate_cluster_id()
        self.assertEqual(random.call_count, 2)
        self.assertEqual(base64.urlsafe_b64decode(value + "=="), accepted)
        self.assertRegex(value, r"^[A-Za-z0-9_][A-Za-z0-9_-]{21}$")

    def test_preserves_allowed_urlsafe_characters(self):
        accepted = b"\xfc" * 16
        with patch.object(prepare.secrets, "token_bytes", return_value=accepted):
            value = prepare.generate_cluster_id()
        self.assertTrue(value.startswith("_"))
        self.assertEqual(base64.urlsafe_b64decode(value + "=="), accepted)


if __name__ == "__main__":
    unittest.main()
