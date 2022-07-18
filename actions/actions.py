# This files contains our custom actions which can be used to run
# custom Python code.
#
# See code comments or our documentation for more information

# import of json for using json.dumps() to convert obj into json str
import json

# Rasa SDK Imports # collectingDispatcher allows sending messages back to the user
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType

# imports from dataImport (DB-Excel)
from actions import dataImport

sc = dataImport.sub_cats
cb = dataImport.categories.Bezeichnung
dt = dataImport.dishes
rl = dataImport.restaurants


# function which gets triggered if user choose no advice
class ActionNoAdvice(Action):
    def name(self) -> Text:
        return "action_no_advice"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Text]:
        dispatcher.utter_message(
            text=f"Was du brauchst meine Hilfe gar nicht? Dann vielleicht beim nächsten Mal! Au Revoir 🥖",
            image='https://img.freepik.com/vektoren-kostenlos/nettes-laechelndes-glueckliches-paket-lieferkasten-zeigen-muskel-flache-zeichentrickfigur-abbildung-isolated-auf-weissem-hintergrund-lieferung-box-charakter-konzept_92289-1418.jpg?w=2000')
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
        user_name = tracker.get_slot('name_slot')
        dispatcher.utter_message(
            text=f"{user_name}, bist du vegetarisch, vegan oder isst du alles?",
            buttons=[{"payload": "/choose{\"veg_ent\": \"eat_all\"}", "title": "Allesesser"},
                     {"payload": "/choose{\"veg_ent\": \"vegan\"}", "title": "Vegan"},
                     {"payload": "/choose{\"veg_ent\": \"vegetarian\"}", "title": "Vegetarier"}]

        )
        return []


# function which access above veg_slot and confirms the user selection
class ActionReplyToVegetarian(Action):

    def name(self) -> Text:
        return "reply_to_veg"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> List[EventType]:
        user_name = tracker.get_slot('name_slot')
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
            text=f"Gut {user_name}, ich merke mir, dass du {reply} bist! In nur 4 Schritten gelangst du nun zu deinem Wunschgericht 😊"
        )
        return []


# this function sends categories from our database to the FE
class ActionAskForCategory(Action):
    # return the name of the action - pay attention to the spelling
    def name(self) -> Text:
        return "ask_for_category"

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
                "title": "Bitte wähle deine gewünschten Kategorien",
                "subtitle": 'Falls du dich noch nicht festlegen willst, klicke auf "Weiter"'

            }}

        dispatcher.utter_message(
            buttons=cat_buttons,
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

        orientation_slot = tracker.get_slot('veg_slot')
        # this function checks if the user is vegan or vegetarian and sends only buttons suitable for him to the frontend
        if orientation_slot == 'vegan':
            protein_array = sc[(sc['Kategorie_ID'] == 2) & (sc['Bezeichnung']) &
                               (sc['Essverhalten'] == 'vegan')]
        elif orientation_slot == 'vegetarian':
            protein_array = sc[(sc['Kategorie_ID'] == 2) & (sc['Bezeichnung']) &
                               (sc['Essverhalten'] == 'vegan') |
                               (sc['Kategorie_ID'] == 2) & (sc['Bezeichnung']) &
                               (sc['Essverhalten'] == 'vegetarian')]
        elif orientation_slot == 'eat_all':
            protein_array = sc[(sc['Kategorie_ID'] == 2) & (sc['Bezeichnung']) &
                               (sc['Essverhalten'])]

        prot_buttons = [{"title": i, "payload": i} for i in
                        protein_array.Bezeichnung]

        label_protein = {

            "payload": 'choose_protein',
            "buttons": prot_buttons,
            "meta_data": {
                "intent": '/keep_on_protein{"prot_ent": ',
                "Badge": "Schritt 2:",
                "title": "Bitte wähle deine Proteine",
                "subtitle": 'Wenn du fertig bist klicke auf "Weiter"'

            }

        }

        dispatcher.utter_message(
            buttons=prot_buttons,
            json_message=label_protein
        )
        return []


class ActionAskForCarbs(Action):

    def name(self) -> Text:
        return "ask_for_carbs"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        orientation_slot = tracker.get_slot('veg_slot')

        if orientation_slot == 'vegan':
            carbs_array = sc[(sc['Kategorie_ID'] == 1) & (sc['Bezeichnung']) &
                             (sc['Essverhalten'] == 'vegan')]
        elif orientation_slot == 'vegetarian':
            carbs_array = sc[(sc['Kategorie_ID'] == 1) & (sc['Bezeichnung']) &
                             (sc['Essverhalten'] == 'vegan') |
                             (sc['Kategorie_ID'] == 1) & (sc['Bezeichnung']) &
                             (sc['Essverhalten'] == 'vegetarian')]
        elif orientation_slot == 'eat_all':
            carbs_array = sc[(sc['Kategorie_ID'] == 1) & (sc['Bezeichnung']) &
                             (sc['Essverhalten'])]

        carbs_buttons = [{"title": i, "payload": i} for i in
                         carbs_array.Bezeichnung]

        label_carbs = {

            "payload": 'choose_carbs',
            "buttons": carbs_buttons,
            "meta_data": {
                "intent": '/keep_on_carbs{"carbs_ent": ',
                "Badge": "Schritt 3:",
                "title": "Bitte wähle deine Kohlenhydrate",
                "subtitle": 'Wenn du fertig bist klicke auf "Weiter"'

            }

        }

        dispatcher.utter_message(
            buttons=carbs_buttons,
            json_message=label_carbs
        )
        return []


class ActionAskForGreen(Action):

    def name(self) -> Text:
        return "ask_for_green"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        orientation_slot = tracker.get_slot('veg_slot')

        if orientation_slot == 'vegan':
            green_array = sc[(sc['Kategorie_ID'] == 3) & (sc['Bezeichnung']) &
                             (sc['Essverhalten'] == 'vegan')]
        elif orientation_slot == 'vegetarian':
            green_array = sc[(sc['Kategorie_ID'] == 3) & (sc['Bezeichnung']) &
                             (sc['Essverhalten'] == 'vegan') |
                             (sc['Kategorie_ID'] == 3) & (sc['Bezeichnung']) &
                             (sc['Essverhalten'] == 'vegetarian')]
        elif orientation_slot == 'eat_all':
            green_array = sc[(sc['Kategorie_ID'] == 3) & (sc['Bezeichnung']) &
                             (sc['Essverhalten'])]

        green_buttons = [{"title": i, "payload": i} for i in
                         green_array.Bezeichnung]

        label_green = {

            "payload": 'choose_green',
            "buttons": green_buttons,
            "meta_data": {
                "intent": '/keep_on_green{"green_ent": ',
                "Badge": "Schritt 4:",
                "title": "Bitte wähle deine Extras",
                "subtitle": 'Wenn du fertig bist klicke auf "Weiter"'

            }

        }

        dispatcher.utter_message(
            buttons=green_buttons,
            json_message=label_green
        )
        return []


class ActionReturnSlots(Action):

    def name(self) -> Text:
        return "action_return_slots"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict
    ) -> List[EventType]:

        # getting slots back
        user_name = tracker.get_slot('name_slot')
        orientation_slot = tracker.get_slot('veg_slot')
        categories_slot = tracker.get_slot('cat_slot')
        protein_slot = tracker.get_slot('prot_slot')
        carbs_slot = tracker.get_slot('carbs_slot')
        green_slot = tracker.get_slot('green_slot')

        # write all dishes from db(Excel) in a python list
        dishes_list = dt.values.tolist()

        # split subcategories in different str and delete empty spaces
        for i in range(len(dishes_list)):
            sub_category_list = dishes_list[i][11].split(",")
            scl = [x.strip() for x in sub_category_list]
            dishes_list[i][11] = scl

        # add points to dish which fit to the information from slots - food direction like spanish, bavarian etc
        for i in range(len(dishes_list)):
            for j in range(len(dishes_list[i])):
                for elem in range(len(categories_slot)):
                    if categories_slot[elem] == dishes_list[i][j]:
                        dishes_list[i].insert(len(dishes_list), 3.0)

        # add points for proteins on top of last points
        for i in range(len(dishes_list)):
            for prot in range(len(protein_slot)):
                if protein_slot[prot] in (dishes_list[i][11]):
                    # check if there is already a value for ranking the dish- if yes add score to this value,
                    # if not append new score on last position
                    if type(dishes_list[i][-1]) == float:
                        dishes_list[i][-1] += 1.5
                    else:
                        dishes_list[i].insert(len(dishes_list), 1.5)

        # add points for carbs on top of last points (in case of no ranking, append a float on the end of the list)
        for i in range(len(dishes_list)):
            for carb in range(len(carbs_slot)):
                if carbs_slot[carb] in (dishes_list[i][11]):
                    if type(dishes_list[i][-1]) == float:
                        dishes_list[i][-1] += 1.2
                    else:
                        dishes_list[i].insert(len(dishes_list), 1.2)

        # add points for extras on top of last points (in case of no ranking, append a float on the end of the list)
        for i in range(len(dishes_list)):
            for green in range(len(green_slot)):
                if green_slot[green] in (dishes_list[i][11]):
                    if type(dishes_list[i][-1]) == float:
                        dishes_list[i][-1] += 1.0
                    else:
                        dishes_list[i].insert(len(dishes_list), 1.0)

        # filtering the dish_list regarding to users choice about food orientation with list comprehension
        filtered_dish_list = []
        for i in range(len(dishes_list)):
            if orientation_slot == "vegan":
                filtered_dish_list = [x for x in dishes_list if 'vegan' in x]
            elif orientation_slot == "vegetarian":
                filtered_dish_list = [x for x in dishes_list if 'vegetarian' in x or 'vegan' in x]
            elif orientation_slot == "eat_all":
                filtered_dish_list = [x for x in dishes_list]

        # if a dish has a score (type=float) append it to a new list and sort it from highest to lowest score
        sorted_dish_list = []
        for i in range(len(filtered_dish_list)):
            if type(filtered_dish_list[i][-1]) == float:
                sorted_dish_list.append(filtered_dish_list[i])
                sorted_dish_list.sort(key=lambda x: x[-1], reverse=True)

        # this final list splits above list to key value pairs and is prepared to get send to FE
        # ensure ascii is false bc of german letters (ä,ö,ü,ß) - now json dumbs uses unicode
        final_dish_list = [{}]
        for i in range(len(sorted_dish_list)):
            final_dish_list.append({
                "title": json.dumps(sorted_dish_list[i][2], ensure_ascii=False).replace('"', ""),
                "picture": json.dumps(sorted_dish_list[i][9], ensure_ascii=False).replace('"', ""),
                "subtitle": json.dumps(sorted_dish_list[i][8], ensure_ascii=False).replace('"', ""),
                "orientation": json.dumps(sorted_dish_list[i][1], ensure_ascii=False).replace('"', ""),
                "dish_id": json.dumps(sorted_dish_list[i][0], ensure_ascii=False).replace('"', ""),
                "price": json.dumps(sorted_dish_list[i][3], ensure_ascii=False).replace('"', ""),
                "veg_label": json.dumps(sorted_dish_list[i][4], ensure_ascii=False).replace('"', "").replace('eat_all',
                                                                                                             ""),
                "specials": json.dumps(sorted_dish_list[i][5], ensure_ascii=False).replace('"', ""),
                "allergen": json.dumps(sorted_dish_list[i][6], ensure_ascii=False).replace('"', ""),
                "course": json.dumps(sorted_dish_list[i][7], ensure_ascii=False).replace('"', ""),
                "subcategory": json.dumps(sorted_dish_list[i][11], ensure_ascii=False).replace('"', ""),
                "restaurant_id": json.dumps(sorted_dish_list[i][12], ensure_ascii=False).replace('"', ""),
                "restaurant_name": json.dumps(sorted_dish_list[i][13], ensure_ascii=False).replace('"', ""),
                "restaurant_link": json.dumps(sorted_dish_list[i][14], ensure_ascii=False).replace('"', "")
            })

            return_dishes = {
                "payload": 'dishes_selection',
                "data": final_dish_list,

            }
        dispatcher.utter_message(
            text=f"{user_name} gemäß deiner Auswahl habe ich leckere Gerichte für dich gefunden, die ideal zu dir "
                 f"passen!😍 Bitte wähle dein Lieblingsgericht!",
            json_message=return_dishes
        )
        return []
