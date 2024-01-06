import requests


def get_daily_horoscope(sign, day):
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params=params)

    return response.json()


# print(get_daily_horoscope("Ari","Today"))