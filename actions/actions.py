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

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        covid_resources = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "MBMC",
                    "subtitle": "FIND BED, SAVE LIFE.",
                    "image_url": "static/hospital-beds-application.jpg",
                    "buttons": [{
                        "title": "Hospital Beds Availability",
                        "url": "https://www.covidbedmbmc.in/",
                        "type": "web_url"
                    },
                        {
                            "title": "MBMC",
                            "type": "postback",
                            "payload": "/affirm"
                        }
                    ]
                },
                    {
                        "title": "COVID.ARMY",
                        "subtitle": "OUR NATION, SAVE NATION.",
                        "image_url": "static/oxygen-cylinder-55-cft-500x554-500x500.jpg",
                        "buttons": [{
                            "title": "RESOURCES AVAILABILITY",
                            "url": "https://covid.army/",
                            "type": "web_url"
                        },
                            {
                                "title": "COVID ARMY",
                                "type": "postback",
                                "payload": "/deny"
                            }
                        ]
                    },
                    {
                        "title": "Innovate Youself",
                        "subtitle": "Get It, Make it.",
                        "image_url": "static/test.jpg",
                        "buttons": [{
                            "title": "Innovate Yourself",
                            "url": "https://www.innovationyourself.com/",
                            "type": "web_url"
                        },
                            {
                                "title": "Innovate Yourself",
                                "type": "postback",
                                "payload": "/greet"
                            }
                        ]
                    },
                    {
                        "title": "RASA CHATBOT",
                        "subtitle": "Conversational AI",
                        "image_url": "static/rasa.png",
                        "buttons": [{
                            "title": "Rasa",
                            "url": "https://www.rasa.com",
                            "type": "web_url"
                        },
                            {
                                "title": "Rasa Chatbot",
                                "type": "postback",
                                "payload": "/greet"
                            }
                        ]
                    }
                ]
            }
        }

        dispatcher.utter_message(attachment=covid_resources)
        return []
