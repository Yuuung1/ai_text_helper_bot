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


def build_tasks_prompt(text: str) -> str:
    return (
        "Проанализируй текст на русском языке и выдели из него задачи, "
        "договорённости, сроки и ответственных.\n\n"
        "Формат ответа:\n"
        "1. Краткий контекст — 1–2 предложения.\n"
        "2. Задачи списком:\n"
        "   - Задача: ...\n"
        "     Ответственный: ... или 'не указан'\n"
        "     Срок: ... или 'не указан'\n"
        "3. Договорённости — отдельным списком.\n"
        "4. Если задач нет, прямо напиши: 'Явных задач в тексте не найдено.'\n\n"
        "Текст для анализа:\n"
        f"{text}"
    )


def build_business_style_prompt(text: str) -> str:
    return (
        'Перепиши текст в деловом стиле на русском языке.\n'
        'Сохрани исходный смысл.\n'
        'Не добавляй новых фактов.\n'
        'Не пиши объяснений.\n'
        'Верни только готовый вариант текста.\n'
        "Текст для переписывания:\n"
        f"{text}"
    )


def generate_ai_response(prompt: str) -> str:
    api_key = get_gemini_api_key()

    client = genai.Client()
    model = get_ai_model()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    if not response.text:
        return "AI не вернул текстовый ответ."
    return response.text.strip()

def summarize_text(text: str) -> str:
    cleaned_text = text.strip()

    if not cleaned_text:
        return "Текст для суммаризации пустой."

    prompt = build_summary_prompt(cleaned_text)

    return generate_ai_response(prompt)


def extract_tasks(text: str) -> str:
    cleaned_text = text.strip()

    if not cleaned_text:
        return "Текст для выделения задач пустой."


    prompt = build_tasks_prompt(cleaned_text)

    return generate_ai_response(prompt)


def rewrite_business_style(text: str) -> str:
    cleaned_text = text.strip()

    if not cleaned_text:
        return "Текст для переписывания в деловом стиле пустой."

    prompt = build_business_style_prompt(cleaned_text)

    return generate_ai_response(prompt)


def main() -> None:
    test_text = (
        "Сегодня на совещании обсудили запуск нового Telegram-бота. "
        "Решили сначала подключить AI-суммаризацию, потом добавить выделение задач. "
        "Также договорились хранить API-ключи только в .env и не коммитить их в GitHub."
    )

    tasks = extract_tasks(test_text)

    print("AI TASKS:")
    print(tasks)


if __name__ == "__main__":
    main()