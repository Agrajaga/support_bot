import logging
import os

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_api import detect_intent_texts


logger = logging.getLogger("dialogflow")


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot: Bot, chat_id: int) -> None:
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


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

    update.message.reply_text(dialogflow_answer['text'])


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
