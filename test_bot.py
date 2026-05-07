import unittest

from bot import limit_telegram_message


class BotTests(unittest.TestCase):
    def test_limit_telegram_message_returns_short_message_unchanged(self):
        message = "Короткое сообщение"

        result = limit_telegram_message(message, max_length=100)

        self.assertEqual(result, message)

    def test_limit_telegram_message_truncates_long_message(self):
        message = "A" * 20

        result = limit_telegram_message(message, max_length=10)

        self.assertTrue(result.startswith("A" * 10))
        self.assertIn("Сообщение обрезано", result)


if __name__ == "__main__":
    unittest.main()