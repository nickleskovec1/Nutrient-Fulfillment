import pandas as pd;
import json;
import os;
from enum import Enum, auto;
import csv;


# https://ods.od.nih.gov/HealthInformation/Dietary_Reference_Intakes.aspx

os.environ['PYTHONIOENCODING'] = 'UTF-8';

# recommended daily allowance vs adequate intake
class Recommend_Type(Enum):
    RDA = auto()
    AI = auto()


def read_nutrient_code_to_nutrient_file(filename: str):
    file_data = [];

    # opening the CSV file
    with open(filename, mode ='r') as file:
    
        # reading the CSV file
        csvFile = csv.reader(file)
        
        attr_id_to_index = {};
        index = 0;
        # displaying the contents of the CSV file
        for line in csvFile:
            file_data.append(line);
            attr_id_to_index[line[0]] = index;
            index += 1;
        return [file_data, attr_id_to_index];

def get_age_range(age_mo: float):
    age_yr_ranges = [1, 4, 9, 14, 19, 31, 51, 70];

    # find age range
    age_str = '';

    #infant - months for age
    if age_mo < 12:
        if age_mo < 7:
            age_str = '0-6 mo';
        else:
            age_str = '7-12 mo';
        return age_str;
    
    # older than infant - years for age
    index = 1;
    while index < len(age_yr_ranges):
        if age_mo < age_yr_ranges[index]*12:
            break;
        index += 1;

    if index == len(age_yr_ranges):
        age_str = '> 70 y';
    else:
        age_str = str(age_yr_ranges[index-1]) + '-' + str(age_yr_ranges[index]-1) + ' y';
    return age_str;

# assume no inconsistencies amongst types for now
def get_rdi_data(rdi_data, life_stage: str, age_range: str):
    return rdi_data[life_stage][age_range];


def load_and_format_data(path):

    table_docs = ['elements', 'vitamins', 'macronutrients'];
    rdi_data = {};
    for doc in table_docs:

        # get full name of file
        pathname = path + 'DRI_' + doc + '2021.xls';

        # read in file as dataframe
        nutrient_table= pd.read_excel(pathname);

        # get the names of each nutrient - need to edit some
        nutrient_keys = nutrient_table.keys().to_list();

        # editting nutrient keys - remove newlines
        for i in range(0, len(nutrient_keys)):
            nutrient_keys[i] = nutrient_keys[i].replace("\n", " ");

        # for all numeric values in table remove '*' at end of 
        # value and indicate that this is an adequate intake vs
        # an RDI
        #nutrient_table.replace(to_replace=r'(.+)\*$', value=)

        # replace the nutrient keys with editted versions
        nutrient_table.set_axis(nutrient_keys, axis='columns', inplace=True);


        # reorganize the data and make it readable
        rdi_data[doc] = {};
        life_stage = "";
        for row in nutrient_table.itertuples(True, None):
            index = row[0];
            # new life stage
            if pd.isnull(row[2]):
                life_stage = row[1];
                rdi_data[doc][life_stage] = {};
            # data for each age group for each life stage
            else:
                age = row[1];
                rdi_data[doc][life_stage][age] = nutrient_table.iloc[index, 2:].to_dict();
    
    # Pretty Print JSON
    json_formatted_str = json.dumps(rdi_data, indent=4)
    #print(json_formatted_str)



path = "~/Documents/";
rdi_data = load_and_format_data(path);