import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_api import detect_intent_texts


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

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['dialogflow_project_id'] = dialogflow_project_id
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
