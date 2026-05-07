import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


DEFAULT_MODEL = "gemini-3-flash-preview"


def get_gemini_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Не найден GEMINI_API_KEY. Проверь файл .env"
        )

    return api_key


def get_ai_model() -> str:
    return os.getenv("AI_MODEL", DEFAULT_MODEL)


def build_summary_prompt(text: str) -> str:
    return (
        "Сделай краткое резюме текста на русском языке.\n"
        "Формат ответа:\n"
        "1. Краткая суть в 1–2 предложениях.\n"
        "2. Основные пункты списком.\n"
        "3. Если есть задачи или договорённости — выдели их отдельно.\n\n"
        "Текст для анализа:\n"
        f"{text}"
    )


def summarize_text(text: str) -> str:
    cleaned_text = text.strip()

    if not cleaned_text:
        return "Текст для суммаризации пустой."

    get_gemini_api_key()

    client = genai.Client()
    model = get_ai_model()
    prompt = build_summary_prompt(cleaned_text)

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    if not response.text:
        return "AI не вернул текстовый ответ."

    return response.text.strip()


def main() -> None:
    test_text = (
        "Сегодня на совещании обсудили запуск нового Telegram-бота. "
        "Решили сначала подключить AI-суммаризацию, потом добавить выделение задач. "
        "Также договорились хранить API-ключи только в .env и не коммитить их в GitHub."
    )

    summary = summarize_text(test_text)

    print("AI SUMMARY:")
    print(summary)


if __name__ == "__main__":
    main()