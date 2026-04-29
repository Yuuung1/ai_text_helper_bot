from pathlib import Path
from collections import Counter
import re


def clean_text(text: str) -> str:
    lines = text.splitlines()

    cleaned_lines = []
    for line in lines:
        cleaned_line = " ".join(line.split())
        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    return "\n".join(cleaned_lines)


def get_words(text: str) -> list[str]:
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", text.lower())


def count_sentences(text: str) -> int:
    sentences = re.findall(r"[^.!?]+[.!?]+", text)
    return len(sentences)


def build_report(cleaned_text: str, input_file: Path) -> str:
    words = get_words(cleaned_text)
    sentences_count = count_sentences(cleaned_text)
    word_counter = Counter(words)

    lines_count = len(cleaned_text.splitlines())
    words_count = len(words)
    chars_count = len(cleaned_text)
    unique_words_count = len(set(words))

    if words:
        longest_word = max(words, key=len)
    else:
        longest_word = ""

    if words:
        average_word_length = round(sum(len(word) for word in words)/words_count,2)
    else:
        average_word_length = 0

    report_lines = [
        "ОТЧЁТ ПО ТЕКСТУ",
        "=" * 40,
        f"Исходный файл: {input_file}",
        f"Количество строк: {lines_count}",
        f"Количество предложений: {sentences_count}",
        f"Количество слов: {words_count}",
        f"Средняя длина слова: {average_word_length}",
        f"Количество уникальных слов: {unique_words_count}",
        f"Самое длинное слово: {longest_word}",
        f"Количество символов: {chars_count}",
        "",
        "Топ-10 частых слов:",
    ]

    for word, count in word_counter.most_common(10):
        report_lines.append(f"{word}: {count}")

    report_lines.extend(
        [
            "",
            "Очищенный текст:",
            "-" * 40,
            cleaned_text,
        ]
    )

    return "\n".join(report_lines)


def analyze_text(text: str, source_name: str = "text") -> str:
    cleaned_text = clean_text(text)
    report = build_report(cleaned_text, Path(source_name))
    return report