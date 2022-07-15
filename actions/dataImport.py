# import of restaurant data via pandas

import pandas as pd

github_link = 'https://github.com/schmcklr/rasa_chatbot_master/blob/master/restaurantData/Restaurant_DB.xlsx?raw=true'

# import of tabs
restaurants = pd.read_excel(
    github_link,
    sheet_name="Restaurants")
dishes = pd.read_excel(
    github_link,
    sheet_name="Gerichte")
drinks = pd.read_excel(
    github_link,
    sheet_name="Getränke")
particularities = pd.read_excel(
    github_link,
    sheet_name="Besonderheiten")
allergens = pd.read_excel(
    github_link,
    sheet_name="Allergene")
categories = pd.read_excel(
    github_link,
    sheet_name="Speiserichtungen")
ingredients = pd.read_excel(
    github_link,
    sheet_name="Zutaten")
sub_cats = pd.read_excel(
    github_link,
    sheet_name="Unterkategorien"
)

# needed to display all columns
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)
