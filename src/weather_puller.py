import time
import re
import requests
import json
import peewee

from datetime import date

from db.models import Weathers
from urllib.request import urlopen

class WeatherPuller:
  def __init__(self, json_data):
    self.json_data = json_data

  def __temperature(self):
    return self.json_data['main']['temp']

  def __weather_type(self):
    return self.json_data['weather'][0]['description']

  def __wind_speed(self):
    return self.json_data['wind']['speed']

  def __pressure(self):
    return self.json_data['main']['pressure']

  def __humidity(self):
    return self.json_data['main']['humidity']

  def __sunset(self):
    timestamp = self.json_data['sys']['sunset']
    return time.strftime('%H:%M', time.gmtime(timestamp))

  def format_speech(self, city):
    return "The weather in {} is currently {} with: a temperature {} degrees and wind speeds reaching {} km/ph. Pressure is {} millibars and humidity {} %. A Sun is going down at {}." \
      .format(
        city,
        self.__weather_type(),
        self.__temperature(),
        self.__wind_speed(),
        self.__pressure(),
        self.__humidity(),
        self.__sunset()
      )

def get_city():
  url = 'http://ipinfo.io/json'
  response = urlopen(url)
  data = json.load(response)
  print(f'Current location: {data}')
  return data['city']

def main():
  try:
    today_w = Weathers.select().where(Weathers.created_at >= date.today()).order_by(Weathers.id.desc()).get()
  except peewee.DoesNotExist:
    today_w = None

  weather_speech = fetch_data()
  w_data = re.findall(r"[-+]?\d*\.\d+|\d+", weather_speech)

  if today_w:
    # self.speaker.write(f'Last recorded temp: {today_w.temperature} and wind: {today_w.wind}')
    if today_w.temperature == float(w_data[0]) and today_w.wind == float(w_data[1]):
      return "Weather haven't changed."
    else:
      Weathers.create(temperature=float(w_data[0]), wind=float(w_data[1]), created_at=date.today())
      return('The weather has changed.' + '\n' + weather_speech)
  else:
    try:
      Weathers.create(temperature=float(w_data[0]), wind=float(w_data[1]), created_at=date.today())
    except IndexError:
      pass
    return weather_speech

def fetch_data():
  city = get_city()
  url = 'https://api.openweathermap.org/data/2.5/weather?appid=a10fd8a212e47edf8d946f26fb4cdef8'
  final_url = url + '&q=' + city + "&units=metric"
  json_data = requests.get(final_url).json()
  wp = WeatherPuller(json_data)
  return wp.format_speech(city)

