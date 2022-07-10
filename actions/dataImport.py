# import of restaurant data
# from datetime import datetime
import pandas as pd


# import calendar

# Load workbook and print sheet names
# wb = load_workbook('https://github.com/schmcklr/rasa_chatbot_master/blob/kevin/restaurantData/DB_Restaurant.xlsx')
# sheet_list = wb.sheetnames
# print(wb.sheetnames)

github_link = 'https://github.com/schmcklr/rasa_chatbot_master/blob/master/restaurantData/Restaurant_DB.xlsx?raw=true'

# import of tables
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


# get current time, needed for enquiry if restaurant open
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time is :", current_time)
# print(datetime.today().weekday())

# get weekday, needed for enquiry if restaurant open
# curr_date = datetime.today()
# print(calendar.day_name[curr_date.weekday()])

# needed to display all columns
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)



