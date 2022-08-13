import logging

from google.cloud import dialogflow


logger = logging.getLogger('dialogflow')


def detect_intent_texts(project_id, session_id, text, language_code):
    try:
        logger.debug('Request dialogflow')
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        return {
            'text': response.query_result.fulfillment_text,
            'is_fallback': response.query_result.intent.is_fallback,
        }
    except Exception as err:
        logger.exception('Error on detect_intent', exc_info=err)
        return {
            'text': '',
            'is_fallback': True,
        }
