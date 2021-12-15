import requests


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
    ret_headers = {"x-app-id": ret_app_id, "x-app-key": ret_key}
    return ret_headers


def make_request(user_input: str):
    """
    Makes request to api
    :param user_input: item to be queried
    :return: response from query
    """
    res = requests.get("https://trackapi.nutritionix.com/v2/search/instant?query=" + user_input, headers=headers)
    res = res.json()
    return res


headers = initialize_secrets("app_id.txt", "key.txt")

# Example
response = make_request("Grilled Cheese")
print(response)
