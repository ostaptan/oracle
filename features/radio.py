import random
import csv
import os
import re
import schedule
import logging
import time
import pyjokes
import peewee
from datetime import date
from features.speaker import Speaker
from db.models import Weathers

import src.weather_m as wea
import src.clock_m as clock

class Radio:
  def __init__(self):
    self.speaker = Speaker()

  # def speak_ua(self, text, app_name='radio'):
  #   logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
  #   logging.info(text)
  #   self.speaker.text2speech(text, lang='uk')

  def write(self, text, app_name='radio'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)

  def speak(self, text, app_name='radio'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.speaker.text2speech(text)

  def greeting(self):
    sys_name = os.getcwd().split('/')[2]
    self.speak(f'Welcome, {sys_name}!')

  def aphorism(self):
    with open('/Users/ostaptan/Datasets/quotes_dataset.csv', 'r') as file:
      reader = csv.reader(file)
      chosen_row = random.choice(list(reader))
      quote, author, tokens = chosen_row[0], chosen_row[1], chosen_row[2]
      self.speak(quote)
      self.speak(f'Author {author}.')

  def joke(self):
    joke = pyjokes.get_joke(language='en', category='all')
    self.speak(joke)

  def weather(self):
    try:
      today_w = Weathers.select().where(Weathers.created_at >= date.today()).order_by(Weathers.id.desc()).get()
    except peewee.DoesNotExist:
      today_w = None

    weather_res = wea.get_data(city='Lviv')
    w_data = re.findall("[+-]?\d+\.\d+", weather_res)
    if today_w:
      self.write(f'Last recorded temp: {today_w.temperature} and wind: {today_w.wind}')
      if today_w.temperature == float(w_data[0]) and today_w.wind == float(w_data[1]):
        self.write('Weather havent changed.')
        return
      else:
        Weathers.create(temperature=float(w_data[0]), wind=float(w_data[1]), created_at=date.today())
        self.speak('The weather has changed.')
        weather = ', temperature'.join(weather_res.split('temperature'))
        self.speak(weather)
    else:
      Weathers.create(temperature=float(w_data[0]), wind=float(w_data[1]), created_at=date.today())
      weather = ', temperature'.join(weather_res.split('temperature'))
      self.speak(weather)

  def datetime_now(self):
    tdate = clock.date()
    ttime = clock.time()

    try:
      today_w = Weathers.select().where(Weathers.created_at >= date.today()).order_by(Weathers.id.desc()).get()
    except peewee.DoesNotExist:
      today_w = None

    if today_w:
      self.speak(f"It's {ttime} o'clock")
    else:
      self.speak(f'Today is {tdate}')
      self.speak(f"It's {ttime} o'clock")


  def scenario(self):
    self.greeting()
    self.datetime_now()
    self.weather()
    self.speak('Aphorism:')
    self.aphorism()
    self.speak('A joke:')
    self.joke()

if __name__ == "__main__":
  disc = Radio()
  disc.scenario()
