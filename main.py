import requests
import json
import format_data;
#import ndjson
import tkinter as tk
from tkinter import *

# run as 'python -m main' -> in order to include cwd in sys.path for module search

class Nutrition:

    def __init__(self, nutrients, daily_values):
        self.nutrients = nutrients
        self.daily = daily_values

    def __str__(self):
        ret_str = ""
        print(self.nutrients)
        for key, value in self.nutrients.items():
            ret_str += key[3::].replace("_", " ") + ": "
            ret_str += ("{:.2f}" + " compared with daily value of " + "{} -> {:.2%}" + "\n")\
                .format(value, self.daily[key], value/self.daily[key])
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
    
    
    # get nutrient codes to names

    # get nutrient codes to line number in nutrient file data
    [file_data, nutrient_id_mapping] = format_data.read_nutrient_code_to_nutrient_file("/home/mary/Documents/Nutritionix_API_v2_USDA_Nutrient_Mapping.csv");
    
    # nutrients that are in the requested query
    nutrient_id_value_pairs = res["foods"][0]["full_nutrients"];
    for nutrient_id_value_pair in nutrient_id_value_pairs:
        nutrient_id = nutrient_id_value_pair["attr_id"];
        index = nutrient_id_mapping[str(nutrient_id)];
        nutrient_name = file_data[index][3];



    foods = res["foods"];

    for food in foods:
        for key in daily_nutrition:
            if food[key]:  # Check for null value
                daily_nutrition[key] += food[key]
    today_nutrition = Nutrition(daily_nutrition, fda_nut_values)

    #for nutrient in nutrients:

    sti = today_nutrition.__str__()
    change_text(sti)
    del today_nutrition

    # with open("test.json", "w") as f:
    #     json.dump(res, f, sort_keys=True, indent=4, separators=(',', ': '))


def change_text(new_string):
    lab.config(text=new_string)


header = initialize_secrets("app_id.txt", "key.txt")
fda_nut_values = init_nutrition(flag=1)


m = tk.Tk()
w = Entry(m, font="Calibri 45")
w.bind("<Return>", make_request1)
w.grid(row=0, column=2)
lab = tk.Label(m,text="Enter in food items and hit Enter", font="Calibri 20")

lab.grid()
m.mainloop()

