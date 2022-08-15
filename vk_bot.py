import logging
import os
import random

import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_api import detect_intent_texts
from logs_handling import TelegramLogsHandler

logger = logging.getLogger("dialogflow")


def answer(event, vk_api, dialogflow_project_id):
    dialogflow_answer = detect_intent_texts(
        project_id=dialogflow_project_id,
        session_id=event.user_id,
        text=event.text,
        language_code="ru-RU",
    )
    text = dialogflow_answer["text"]
    if dialogflow_answer["is_fallback"]:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv("VK_BOT_TOKEN")
    dialogflow_project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
    tg_token = os.getenv("TG_BOT_TOKEN")
    tg_admin_id = os.getenv("TG_ADMIN_ID")

    bot = telegram.Bot(token=tg_token)
    logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s")
    logger.setLevel(logging.WARNING)
    logger.addHandler(
        TelegramLogsHandler(
            tg_bot=bot,
            chat_id=tg_admin_id,
        )
    )

    logger.warning("Start VK-bot")
    try:
        vk_session = vk.VkApi(token=vk_token)
        longpoll = VkLongPoll(vk_session)
        vk_api = vk_session.get_api()
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer(event, vk_api, dialogflow_project_id)
    except Exception as err:
        logger.exception('VK-bot crashed', exc_info=err)
