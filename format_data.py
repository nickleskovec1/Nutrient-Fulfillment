import pandas as pd;

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
        pathname = path + 'DRI_' + doc + '2021.xls';
        nutrient_table= pd.read_excel(pathname);
        #print(nutrient_table);
        tmp = nutrient_table.keys();
        #print(tmp);

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
                print(age);
                rdi_data[doc][life_stage][age] = nutrient_table.iloc[index, 2:].to_dict();
    print(rdi_data[doc]);


        
    #print(row);
