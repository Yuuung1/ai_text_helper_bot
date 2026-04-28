from text_tools import clean_text, build_report
from pathlib import Path
import argparse


INPUT_FILE = Path("sample.txt")
OUTPUT_FILE = Path("report.txt")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Создаёт отчёт по текстовому файлу"
    )

    parser.add_argument(
        "input_file",
        nargs="?",
        default=INPUT_FILE,
        type=Path,
        help="Путь к входному текстовому файлу"
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        default=OUTPUT_FILE,
        type=Path,
        help="Путь к файлу отчёта"
    )

    return parser.parse_args()


def read_text(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    return file_path.read_text(encoding="utf-8")


def save_report(report: str, file_path: Path) -> None:
    file_path.write_text(report, encoding="utf-8")


def main() -> None:
    args = parse_args()

    original_text = read_text(args.input_file)
    cleaned_text = clean_text(original_text)
    report = build_report(cleaned_text, args.input_file)

    save_report(report, args.output_file)

    print("Готово.")
    print(f"Отчёт сохранён в файл: {args.output_file}")


if __name__ == "__main__":
    main()