# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionFoodDirec(Action):

    def name(self) -> Text:
        return "food_direc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons={
            {"payload": '/amerik{"food_category":"amerikanisch"}', "title": "Amerikanisch"},
            {"payload": '/ital{"food_category":"italienisch"}', "title": "Italienisch"},
        }

        dispatcher.utter_message(text="Auf welche Essensrichtung hast du denn heute Lust?")


        return []
