import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_api import detect_intent_texts
from logs_handling import TelegramLogsHandler

logger = logging.getLogger("dialogflow")


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Здравствуйте!")


def answer(update: Update, context: CallbackContext) -> None:
    """Answer to user"""
    session_id = update.effective_chat.id
    dialogflow_project_id = context.bot_data['dialogflow_project_id']

    dialogflow_answer = detect_intent_texts(
        dialogflow_project_id,
        session_id,
        update.message.text,
        "ru-RU"
    )
    text = dialogflow_answer['text']
    if text:
        update.message.reply_text(text)


def main() -> None:
    """Start the bot."""
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    dialogflow_project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
    tg_admin_id = os.getenv("TG_ADMIN_ID")

    updater = Updater(tg_token)
    logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s")
    logger.setLevel(logging.WARNING)
    logger.addHandler(
        TelegramLogsHandler(
            tg_bot=updater.bot,
            chat_id=tg_admin_id,
        )
    )
    logger.warning("TG-bot started")

    dispatcher = updater.dispatcher
    dispatcher.bot_data['dialogflow_project_id'] = dialogflow_project_id
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
