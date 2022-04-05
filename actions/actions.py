# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# Import of Excel DB
import restaurantData.dataImport

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionFoodDirect(Action):
    # return the name of the action - pay attention to the spelling
    def name(self) -> Text:
        return "food_direct"

    # collectingDispatcher allows to send back messages to the user
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = {
            {"payload": '/amerik{{"food_category":"amerikanisch"}}', "title": "Amerikanisch"},
            {"payload": '/ital{{"food_category":"italienisch"}}', "title": "Italienisch"},
        }

        dispatcher.utter_message(text="Auf welche Essensrichtung hast du denn heute Lust?", buttons=buttons)

        return []
