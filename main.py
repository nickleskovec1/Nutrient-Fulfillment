import requests
import json
import ndjson
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont


class Nutrition:

    def __init__(self, nutrients, daily_values):
        self.nutrients = nutrients
        self.daily = daily_values

    def __str__(self):
        ret_str = ""
        for key, value in self.nutrients.items():
            nutrient = key[3::].replace("_", " ")
            ret_str += ("{:<18}" + ": " + "{:<8.2f}" + "{:<4} -> {:<5.2%}" + "\n")\
                .format(nutrient, value, self.daily[key], value/self.daily[key])
        return ret_str


def initialize_secrets(path_app_id: str, path_key: str):
    """
    Initializes the api key and api id
    :param path_app_id: Path to app id
    :param path_key: Path to key
    :return: dictionary of headers required for api get request
    """
    with open(path_app_id, "r") as f:
        ret_app_id = f.readline()
    with open(path_key, "r") as f:
        ret_key = f.readline()
    ret_headers = {"x-app-id": ret_app_id, "x-app-key": ret_key, "x-remote-user-id": "0"}
    return ret_headers


def init_nutrition(flag=0):
    strings = ["nf_calories", "nf_total_fat", "nf_saturated_fat", "nf_cholesterol", "nf_sodium", "nf_total_carbohydrate",
               "nf_dietary_fiber", "nf_sugars", "nf_protein", "nf_potassium"]
    daily_values = [2000, 78, 20, 300, 2400, 275, 28, 50, 50, 275]
    ret_dict = dict()
    if not flag:
        for nutrient in strings:
            ret_dict[nutrient] = 0
    else:
        for i in range(len(strings)):
            ret_dict[strings[i]] = daily_values[i]
    return ret_dict


def make_request(user_input: str):
    """
    Makes request to api
    :param user_input: item to be queried
    :return: response from query
    """
    res = requests.get("https://trackapi.nutritionix.com/v2/search/instant?query=" + user_input, headers=header)
    res = res.json()
    return res


def make_request1(event=None):
    daily_nutrition = init_nutrition()
    query = dict()
    query["query"] = w.get()
    res = requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients", data=query, headers=header).json()
    foods = res["foods"]
    for food in foods:
        for key in daily_nutrition:
            if food[key]:  # Check for null value
                daily_nutrition[key] += food[key]
    today_nutrition = Nutrition(daily_nutrition, fda_nut_values)
    sti = today_nutrition.__str__()
    change_text(sti)
    headline.config(text="{}".format(w.get()))
    table_headers.config(text="{:<18} {:<8} {:<8} {:<5}".format("Nutrient", "Consumed", "DV", "%DV"), justify=LEFT)
    w.delete(0, END)
    del today_nutrition

    # with open("test.json", "w") as f:
    #     json.dump(res, f, sort_keys=True, indent=4, separators=(',', ': '))


def change_text(new_string):
    lab.config(text=new_string)


header = initialize_secrets("app_id.txt", "key.txt")
fda_nut_values = init_nutrition(flag=1)


m = tk.Tk()
fontStyle = tkFont.Font(family="TkFixedFont", size=30)
default_font = tkFont.nametofont("TkFixedFont")
default_font.configure(size=21)
w = Entry(m, font="TkFixedFont 45")
w.bind("<Return>", make_request1)
w.grid(row=0, column=0)
lab = tk.Label(m,text="Enter in food items and hit Enter", font="TkFixedFont", justify=LEFT)
headline = tk.Label(m,text="", font="TkFixedFont")
headline.grid(row=1, column=0)
table_headers = tk.Label(m, text="", font="TkFixedFont", justify=LEFT, anchor="w")
table_headers.grid()
lab.grid()
m.mainloop()

