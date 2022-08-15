import requests, json, re
from difflib import get_close_matches

# ○○市××区 → id
def get_point_id(address):
    url = "https://zutool.jp/api/getweatherpoint/"+address

    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestsException as e:
        print("HTTP Error: ", e)

    else:
        response_data = response.json()
        result_data = json.loads(response_data['result'])
        if not result_data:
            return None
        else:
            city_code = result_data[0]['city_code']
            return city_code


def get_prefecture_from_location(location):
    # location から 郵便番号を抽出
    post_number = re.search(r"\d{3}-\d{4}", location).group()

    url = "http://geoapi.heartrails.com/api/json?method=searchByPostal&postal=" + post_number

    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print("HTTP Error: ", e)

    else:
        response_data = response.json()
        prefecture = response_data["response"]["location"][0]["prefecture"]
        return prefecture


def get_location_info(user_location):
    prefecture = get_prefecture_from_location(user_location)

    url = "https://zutool.jp/api/getweatherpoint/"+prefecture

    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestsException as e:
        print("HTTP Error: ", e)

    else:
        response_data = json.loads(response.json()["result"])

        name_list = []
        for location_info in response_data:
            name_list.append(location_info["name"])

        user_location_name = get_close_matches(user_location, name_list, n=1, cutoff=0.1)[0]

        for location_info in response_data:
            if location_info["name"] == user_location_name: return {"city_code":location_info["city_code"], "name":location_info["name"]}


def get_weather_status(city_code):
    url = "https://zutool.jp/api/getweatherstatus/" + city_code

    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestsException as e:
        print("HTTP Error: ", e)

    else:
        response_data = response.json()
        return response_data

def get_pressure_status(city_code, date):
    pressure_level = [
        "通常😐",
        "通常😐",
        "やや注意😨",
        "注意😵",
        "警戒😱"
    ]
    pressure_info = ""
    date_weather_status = get_weather_status(city_code)[date]
    for i in range(24):
        pressure_info = pressure_info + f"{i}時 : {date_weather_status[i]['pressure']} hPa, {pressure_level[int(date_weather_status[i]['pressure_level'])]}\n"
    return pressure_info
