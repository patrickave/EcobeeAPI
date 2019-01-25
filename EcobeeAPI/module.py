
import requests
import json
import logging
import logging
logging.basicConfig(level=logging.DEBUG)

def load_config(config_file):
    with open(config_file) as json_data_file:
        data = json.load(json_data_file)
    return data

def get_thermostat(access_token):
    access_token = access_token
    url = 'https://api.ecobee.com/1/thermostat'
    header = {'Content-Type': 'application/json;charset=UTF-8',
              'Authorization': 'Bearer ' + access_token}
    params = {'json': ('{"selection":{"selectionType":"registered",'
                        '"includeRuntime":"true",'
                        '"includeSensors":"true",'
                        '"includeProgram":"true",'
                        '"includeEquipmentStatus":"true",'
                        '"includeEvents":"true",'
                        '"includeWeather":"true",'
                        '"includeSettings":"true"}}')}

    request = requests.get(url, headers=header, params=params)
    reqcode = request.status_code
    logging.debug('HTTP Status Code: %s', reqcode)
    return request

def convert_fahrenheit(temp):
    celcius = (temp - 320.0) * (5.0 / 90.0) 
    fahrenheit = 9.0/5.0 * celcius + 32.0
    return fahrenheit

def refresh_token():
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)

    url = 'https://api.ecobee.com/token'
    params = {'grant_type': 'refresh_token',
              'refresh_token': (data['ecobee_api']['refresh_token']),
              'client_id': (data['ecobee_api']['api_key'])}
    request = requests.post(url, params=params)
    reqcode = request.status_code

    if reqcode != 200:
        print(request.status_code)
        print('some type of debug logic and config here')

    if reqcode == 200:
        access_token = request.json()['access_token']
        print('DEBUG ACCESS TOKEN: ', access_token)
        refresh_token = request.json()['refresh_token']
        print('DEBUG REFRESH TOKEN: ', refresh_token)

        with open('config.json', 'r+') as f:
            data = json.load(f)
            data['ecobee_api']['access_token'] = access_token
            data['ecobee_api']['refresh_token'] = refresh_token
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()     # remove remaining part
    return

