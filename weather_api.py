import requests, json

# ○○市××区 → id
def get_point_id(address):
    url = "https://zutool.jp/api/getweatherpoint/"+address

    try:
        response = requests.get("https://zutool.jp/api/getweatherpoint/"+address)
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
