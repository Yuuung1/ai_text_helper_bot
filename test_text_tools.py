import unittest

from text_tools import clean_text, get_words, count_sentences, analyze_text


class TextToolsTests(unittest.TestCase):
    def test_clean_text(self):
        source_text = "Привет.   Это   тест.\n\nНовая    строка."
        expected_text = "Привет. Это тест.\nНовая строка."

        result = clean_text(source_text)

        self.assertEqual(result, expected_text)


    def test_get_words(self):
        source_text = "Python, python! Текст."
        expected_text = ["python", "python", "текст"]

        result = get_words(source_text)

        self.assertEqual(result, expected_text)


    def test_count_sentences(self):
        source_text = "Привет. Как дела? Всё хорошо!"
        expected_result = 3

        result = count_sentences(source_text)

        self.assertEqual(result, expected_result)


    def test_count_sentences_without_end_punctuation(self):
        source_text = "Привет это текст без точки"
        expected_result = 0

        result = count_sentences(source_text)

        self.assertEqual(result, expected_result)

    def test_analyze_text(self):
        source_text = "Python Python бот."
        result = analyze_text(source_text, "test_source")

        self.assertIn("Исходный файл: test_source", result)
        self.assertIn("Количество слов: 3", result)
        self.assertIn("python: 2", result)
        self.assertIn("бот: 1", result)


if __name__ == "__main__":
    unittest.main()