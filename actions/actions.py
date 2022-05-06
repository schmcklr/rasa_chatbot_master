# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# Import of Excel DB - Data


from actions import dataImport

# Rasa SDK Imports
from typing import Any, Text, Dict, List, Tuple
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.types import DomainDict
import random

# imports from dataImport
sc = dataImport.sub_cats
cb = dataImport.categories.Bezeichnung


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


# TODO: langsamer Nachrichten ans FE schicken
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

                {
                    "image": "https://image.jimcdn.com/app/cms/image/transf/dimension=890x10000:format=jpg"
                             "/path/s08487bbdb796bdb9/image/i602f6404db8c165c/version/1614547865/rezepte-aus"
                             "-essen-trinken.jpg",
                    "title": "Leckeres Essen",
                    "description": "Hier siehst du eines unserer Essen",
                    "buttons": [
                        {
                            "title": "Zweites Beispiel",
                            "payload": "/choose_food",
                            "type": "postback"
                        },

                        {
                            "title": "Hallo",
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


# function for asking user for being vegan, vegetarian - send buttons to the FE
class ActionAskForVegetarian(Action):

    def name(self) -> Text:
        return "ask_for_veg"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="Bist du Vegetarier, Vegan oder Allesesser?:",
            buttons=[{"payload": "/choose{\"veg_ent\": \"eat_all\"}", "title": "Allesesser"},
                     {"payload": "/choose{\"veg_ent\": \"vegan\"}", "title": "Vegan"},
                     {"payload": "/choose{\"veg_ent\": \"vegetarian\"}", "title": "Vegetarier"}]

        )
        return []


# function which saves decision from above function to a slot and reply to the user
class ActionReplyToVegetarian(Action):

    def name(self) -> Text:
        return "reply_to_veg"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> List[EventType]:
        get_veg_slot = tracker.get_slot('veg_slot')

        # reply to the user that veg decision is saved in a slot - bot will remember
        if get_veg_slot == "eat_all":
            reply = "Allesesser"
        elif get_veg_slot == "vegan":
            reply = "ein Veganer"
        elif get_veg_slot == "vegetarian":
            reply = "Vegetarier"
        else:
            reply = "no_valid_veg_slot_recognized_failure"

        dispatcher.utter_message(
            text=f"Gut ich merke mir, dass du {reply} bist!"
        )
        return []


#
class ActionAskForCategory(Action):
    # return the name of the action - pay attention to the spelling
    def name(self) -> Text:
        return "ask_for_category"

    # collectingDispatcher allows to send back messages to the user
    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        cat_buttons = [{"title": i, "payload": i} for i in cb]

        label_cat = {

            "payload": 'choose_category',
            "buttons": cat_buttons,
            "meta_data": {
                "intent": '/keep_on_category{"cat_ent": ',
                "Badge": "Schritt 1:",
                "title": "Wähle deine gewünschten Kategorien",
                "subtitle": 'Falls du dich noch nicht festlegen willst, klicke auf "Weiter"'

            }}

        dispatcher.utter_message(
            text="Bitte wähle eine Essensrichtung oder klicke auf weiter:", buttons=cat_buttons,
            json_message=label_cat

        )
        return []


class ActionAskForProtein(Action):
    # return the name of the action - pay attention to the spelling
    def name(self) -> Text:
        return "ask_for_protein"

    # collectingDispatcher allows to send back messages to the user
    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        # TODO: alter Bezeichung to Bezeichnung typo
        protein_array = sc[(sc['Kategorie_ID'] == 2) & (sc['Bezeichung'])]

        prot_buttons = [{"title": i, "payload": i} for i in
                        protein_array.Bezeichung]

        label_protein = {

            "payload": 'choose_protein',
            "buttons": prot_buttons,
            "meta_data": {
                "intent": '/keep_on_protein{"prot_ent": ',
                "Badge": "Schritt 2:",
                "title": "Wähle deine Proteine",
                "subtitle": 'Wenn du fertig bist klicke auf "Weiter"'

            }

        }

        dispatcher.utter_message(
            text="Wähle deine Lieblingsproteine:", buttons=prot_buttons,
            json_message=label_protein
        )
        return []
