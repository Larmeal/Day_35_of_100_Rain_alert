import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


api_key = os.environ.get("MY_API_KEY")

account_sid = 'AC4c525788499cf21ebc1db315cfb429dc'
auth_token = os.environ.get("MY_TOKEN")

document = {
    "lat": 13.756550,
    "lon": 100.523253,
    "exclude": "current,minutely,daily",
    "appid": api_key
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=document)
response.raise_for_status()
data = response.json()

weather_data_record = []
rain = False

for i in range(18):
    weather_id = data["hourly"][i]["weather"][0]["id"]
    weather_data_record.append(weather_id)

while not rain:
    if weather_id in weather_data_record and weather_id < 700:
        rain = True
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https': os.environ['https_proxy']}

        client = Client(account_sid, auth_token, http_client=proxy_client)

        message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an Umbrella",
        from_='+19034378260',
        to='+66614385165'
        )

    print(message.status)

