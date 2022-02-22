import requests
from twilio.rest import Client


api_key = "ad098dc91d0eba488c4f0982578e8004"

account_sid = 'AC4c525788499cf21ebc1db315cfb429dc'
auth_token = 'fb9e8a8322d74aedf3ef66f95448c657'

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

for i in range(12):
    weather_id = data["hourly"][i]["weather"][0]["id"] 
    weather_data_record.append(weather_id)

while not rain:    
    if weather_id in weather_data_record and weather_id < 700:
        rain = True
        client = Client(account_sid, auth_token)

        message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an Umbrella",
        from_='+19034378260',
        to='+66614385165'
        )

    print(message.status)
