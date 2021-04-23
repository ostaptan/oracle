import os
import re
import uuid
import json
import peewee
import datetime
import requests
import urllib
import socket

from db.models import Weathers
from src.weather_puller import WeatherPuller

def datetime_now():
  tdate = datetime.datetime.now().strftime("%b %d %Y")
  ttime = datetime.datetime.now().strftime("%H:%M")

  try:
    today_w = Weathers.select().where(Weathers.created_at >= datetime.date.today()).order_by(Weathers.id.desc()).get()
  except peewee.DoesNotExist:
    today_w = None

  if today_w:
    return(f"It's {ttime} o'clock")
  else:
    return(f'Today is {tdate}\n' + f"It's {ttime} o'clock")

def pull_weather():
  try:
    today_w = Weathers.select().where(Weathers.created_at >= datetime.date.today()).order_by(Weathers.id.desc()).get()
  except peewee.DoesNotExist:
    today_w = None

  weather_speech = fetch_data()
  w_data = re.findall(r"[-+]?\d*\.\d+|\d+", weather_speech)

  if today_w:
    # self.speaker.write(f'Last recorded temp: {today_w.temperature} and wind: {today_w.wind}')
    if today_w.temperature == float(w_data[0]) and today_w.wind == float(w_data[1]):
      return "Weather haven't changed."
    else:
      Weathers.create(temperature=float(w_data[0]), wind=float(w_data[1]), created_at=datetime.date.today())
      return('The weather has changed.' + '\n' + weather_speech)
  else:
    try:
      Weathers.create(temperature=float(w_data[0]), wind=float(w_data[1]), created_at=datetime.date.today())
    except IndexError:
      pass
    return weather_speech

def fetch_data():
  city = InfoProducer().city()
  url = 'https://api.openweathermap.org/data/2.5/weather?appid=a10fd8a212e47edf8d946f26fb4cdef8'
  final_url = url + '&q=' + city + "&units=metric"
  json_data = requests.get(final_url).json()
  wp = WeatherPuller(json_data)
  return wp.format_speech(city)

def debugger():
  import pdb; pdb.set_trace()

class InfoProducer:
  def __init__(self):
    url = 'http://ipinfo.io/json'
    response = urllib.request.urlopen(url)
    self.data = json.load(response)

  def city(self):
    return self.data['city']

  def ip(self):
    return self.data['ip']

  def sysn(self):
    return os.getcwd().split('/')[2]

  def mac(self):
    return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
