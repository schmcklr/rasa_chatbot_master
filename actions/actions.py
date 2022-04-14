# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# Import of Excel DB


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionFoodDirect(Action):
    # return the name of the action - pay attention to the spelling
    def name(self) -> Text:
        return 'food_direct'

    # collectingDispatcher allows to send back messages to the user
    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Bitte wähle eine Richtung oder klicke auf weiter:", buttons=[
            {"payload": "/ital", "title": "italienisch"},
            {"payload": "/amerik", "title": "amerikanisch"},
            {"payload": "/skip_direction", "title": "Weiter"},
        ])
        return []


class ActionCarousel(Action):
    def name(self) -> Text:
        return "action_carousels"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) \
            -> List[Dict[Text, Any]]:
        carousel = {
            "payload": 'cardsCarousel',
            "data": [
                {
                    "image": "https://image.jimcdn.com/app/cms/image/transf/dimension=890x10000:format=jpg"
                             "/path/s08487bbdb796bdb9/image/i602f6404db8c165c/version/1614547865/rezepte-aus"
                             "-essen-trinken.jpg",
                    "title": "Leckeres Essen",
                    "description": "Hier siehst du eines unserer Essen",
                    "buttons": [
                        {
                            "title": "Nehme ich",
                            "payload": "/choose_food",
                            "type": "postback"
                        },

                        {
                            "title": "Weiter",
                            "payload": "/next_food",
                            "type": "postback"
                        }
                    ]
                },

            ]
        }
        dispatcher.utter_message(json_message=carousel)
        return []


class ActionImage(Action):
    def name(self) -> Text:
        return "action_images"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Text]:
        dispatcher.utter_message(image="https://img.freepik.com/vektoren-kostenlos/netter-box-charakter-laeuft_161751"
                                       "-1640.jpg")
        return []


class ActionNoAdvice(Action):
    def name(self) -> Text:
        return "action_no_advice"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Text]:
        dispatcher.utter_message(text="Was du brauchst meine Hilfe gar nicht, dann vielleicht beim nächsten Mal!",
                                 image="https://img.freepik.com/vektoren-kostenlos/netter-box-charakter-laeuft_161751"
                                       "-1640.jpg")
        return []
