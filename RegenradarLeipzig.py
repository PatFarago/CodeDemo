import requests
from twilio.rest import Client

#Little API-Call from twilio to get weather information at certain latitude & longitude (here Leipzig, Germany)
#to tell you, if you should take an umbrella with you or not
#Enjoy


api_key = "c881524b83d41f7952f7253834655949"

params = {
    "lat": 51.34,
    "lon": 12.37,
    "appid": api_key,
    "cnt": 1,
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=params)
response.raise_for_status()
data = response.json()

for hour_data in data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        print("Nimm einen Regenschirm mit!")
    else:
        print("Du brauchst keinen Regenschirm :)")
