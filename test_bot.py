import unittest

from bot import limit_report_length


class BotTests(unittest.TestCase):
    def test_limit_report_length_returns_short_report_unchanged(self):
        report = "Короткий отчёт"

        result = limit_report_length(report, max_length=100)

        self.assertEqual(result, report)

    def test_limit_report_length_truncates_long_report(self):
        report = "A" * 20

        result = limit_report_length(report, max_length=10)

        self.assertTrue(result.startswith("A" * 10))
        self.assertIn("Отчёт обрезан", result)


if __name__ == "__main__":
    unittest.main()