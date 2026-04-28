from pathlib import Path
from collections import Counter
import re


INPUT_FILE = Path("sample.txt")
OUTPUT_FILE = Path("report.txt")


def read_text(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    return file_path.read_text(encoding="utf-8")


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


def build_report(cleaned_text: str) -> str:
    words = get_words(cleaned_text)
    word_counter = Counter(words)

    lines_count = len(cleaned_text.splitlines())
    words_count = len(words)
    chars_count = len(cleaned_text)
    unique_words_count = len(set(words))

    if words:
        longest_word = max(words, key=len)
    else:
        longest_word = ""

    report_lines = [
        "ОТЧЁТ ПО ТЕКСТУ",
        "=" * 40,
        f"Исходный файл: {INPUT_FILE}",
        f"Количество строк: {lines_count}",
        f"Количество слов: {words_count}",
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


def save_report(report: str, file_path: Path) -> None:
    file_path.write_text(report, encoding="utf-8")


def main() -> None:
    original_text = read_text(INPUT_FILE)
    cleaned_text = clean_text(original_text)
    report = build_report(cleaned_text)

    save_report(report, OUTPUT_FILE)

    print("Готово.")
    print(f"Отчёт сохранён в файл: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()