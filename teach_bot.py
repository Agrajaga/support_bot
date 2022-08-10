import os

from dotenv import load_dotenv
from google.cloud import dialogflow

import json
import argparse


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    parser = argparse.ArgumentParser()
    parser.add_argument("json_filename")
    args = parser.parse_args()

    with open(args.json_filename, "r") as my_file:
        intents_json = my_file.read()

    intents = json.loads(intents_json)
    for intent_name, intent_params in iter(intents.items()):
        create_intent(
            project_id=project_id,
            display_name=intent_name,
            training_phrases_parts=intent_params['questions'],
            message_texts=[intent_params['answer'],],
        )

