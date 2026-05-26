from django.test import TestCase


class SimpleMathTest(TestCase):
    def test_one_plus_one(self):
        """A tiny smoke test to ensure the test runner picks up tests."""
        self.assertEqual(1 + 1, 2)
