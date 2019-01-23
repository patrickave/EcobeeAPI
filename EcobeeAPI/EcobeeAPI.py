import requests
import json
import datetime
from module import *
import logging
from database import *
logging.basicConfig(level=logging.DEBUG)
with open("config.json") as json_data_file:
    data = json.load(json_data_file)
now = datetime.datetime.now()
db = Database('10.0.0.7', dbname='copper', username='copper_user', password='copper')
token = data['ecobee_api']['access_token']
request = get_thermostat(access_token=token)


if request.status_code != 200:
   refresh_token()
   logging.debug('Access Token Expired: Requesting New Tokens')
   request = get_thermostat(access_token=token)

if request.status_code == 200:
    thermostats = request.json()['thermostatList']
    weather = request.json()['thermostatList'][0]['weather']
    forecast = weather['forecasts']
    outside_temp = forecast[0]['temperature']
    outside_temp_int = convert_fahrenheit(float(outside_temp))

    for eachsensor in thermostats[0]['remoteSensors']:
        name = eachsensor.get('name')
        for temp in eachsensor['capability']:
            id = temp.get('id')
            if id == '1':
                temp_value = temp.get('value')
                inside_temp_int = convert_fahrenheit(float(temp_value))
                db.add_temperature('ecobee', now.strftime("%Y-%m-%d %H:%M"), name, inside_temp_int, outside_temp_int)



