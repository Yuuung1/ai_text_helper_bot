import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from text_tools import analyze_text


load_dotenv()


def get_bot_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "Не найден TELEGRAM_BOT_TOKEN. Проверь файл .env"
        )

    return token


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
        "/help — помощь"
    )


async def analyze_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text

    report = analyze_text(user_text, "telegram_message")

    if len(report) > 3900:
        report = report[:3900] + "\n\n...Отчёт обрезан, потому что сообщение слишком длинное."

    await update.message.reply_text(report)


def main() -> None:
    token = get_bot_token()

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text_message))

    print("Telegram bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()