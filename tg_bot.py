import os

from dotenv import load_dotenv
from google.cloud import dialogflow, storage
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Здравствуйте!")


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    session_id = update.effective_chat.id

    update.message.reply_text(
        detect_intent_texts(
            os.getenv("PROJECT_ID"),
            session_id,
            update.message.text,
            "ru-RU"
        )
    )


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def main() -> None:
    """Start the bot."""
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
