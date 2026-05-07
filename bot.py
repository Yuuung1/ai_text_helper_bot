import os
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from text_tools import analyze_text
from ai_client import summarize_text, extract_tasks, rewrite_business_style


load_dotenv()


def get_bot_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "Не найден TELEGRAM_BOT_TOKEN. Проверь файл .env"
        )

    return token


def limit_telegram_message(message_text: str, max_length: int = 3900) -> str:
    if len(message_text) <= max_length:
        return message_text

    return (
        message_text[:max_length]
        + "\n\n...Сообщение обрезано, потому что оно слишком длинное."
    )



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Пришли мне текст, а я сделаю по нему отчёт: "
        "посчитаю строки, предложения, слова, частые слова и другие метрики."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Как пользоваться:\n"
        "1. Отправь мне любой текст.\n"
        "2. Я очищу его от лишних пробелов.\n"
        "3. Верну отчёт со статистикой.\n\n"
        "Команды:\n"
        "/start — запуск бота\n"
        "/help — помощь\n"
        "/summary <текст> — краткое AI - резюме текста\n"
        "/tasks <текст> — выделить задачи, сроки и договорённости\n"
        '/business <текст> — переписать текст в деловом стиле'
    )


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text or ""

    parts = message_text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        await update.message.reply_text(
            "Использование:\n"
            "/summary <текст для краткого резюме>"
        )
        return

    user_text = parts[1].strip()

    await update.message.reply_text("Готовлю краткое резюме...")

    try:
        summary = await asyncio.to_thread(summarize_text, user_text)
    except RuntimeError as error:
        await update.message.reply_text(f"Ошибка настройки AI: {error}")
        return
    except Exception as error:
        print(f"AI error: {error}")
        await update.message.reply_text(
            "Не удалось получить ответ от AI. Попробуй позже."
        )
        return

    summary = limit_telegram_message(summary)

    await update.message.reply_text(summary)


async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text or ""

    parts = message_text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        await update.message.reply_text(
            "Использование:\n"
            "/tasks <текст для выделения задач>"
        )
        return

    user_text = parts[1].strip()

    await update.message.reply_text("Выделяю задачи и договорённости...")

    try:
        tasks = await asyncio.to_thread(extract_tasks, user_text)
    except RuntimeError as error:
        await update.message.reply_text(f"Ошибка настройки AI: {error}")
        return
    except Exception as error:
        print(f"AI error: {error}")
        await update.message.reply_text(
            "Не удалось получить ответ от AI. Попробуй позже."
        )
        return

    tasks = limit_telegram_message(tasks)

    await update.message.reply_text(tasks)


async def business_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text or ""

    parts = message_text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        await update.message.reply_text(
            "Использование:\n"
            "/business <текст для переделывания в официальный стиль>"
        )
        return

    user_text = parts[1].strip()

    await update.message.reply_text("Переделываю текст в официальный стиль...")

    try:
        business_text = await asyncio.to_thread(rewrite_business_style, user_text)
    except RuntimeError as error:
        await update.message.reply_text(f"Ошибка настройки AI: {error}")
        return
    except Exception as error:
        print(f"AI error: {error}")
        await update.message.reply_text(
            "Не удалось получить ответ от AI. Попробуй позже."
        )
        return

    business_text = limit_telegram_message(business_text)

    await update.message.reply_text(business_text)


async def analyze_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text

    report = analyze_text(user_text, source_name="telegram_message")
    report = limit_telegram_message(report)

    await update.message.reply_text(report)


def main() -> None:
    token = get_bot_token()

    application = (
        ApplicationBuilder()
        .token(token)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .get_updates_connect_timeout(30)
        .get_updates_read_timeout(30)
        .get_updates_write_timeout(30)
        .build()
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("summary", summary_command))
    application.add_handler(CommandHandler("tasks", tasks_command))
    application.add_handler(CommandHandler("business", business_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text_message))

    print("Telegram bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()