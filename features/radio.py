import random
import requests
import justext
import csv
import os
import re
import schedule
import logging
import time
import pyjokes
import peewee
import datetime
from datetime import date
from features.speaker import Speaker
from db.models import Weathers

import src.weather_puller as wp

class Radio:
  def __init__(self):
    self.speaker = Speaker('mainframe')

  def __notify(self, title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"' with timeout of 86400 seconds end timeout
              """.format(text, title))

  def greeting(self):
    sys_name = os.getcwd().split('/')[2]
    text = f'Welcome, {sys_name}!'
    self.__notify('Oracle', 'γνῶθι σεαυτόν! '+text)
    self.speaker.tell(text)

  def aphorism(self):
    with open('./data/quotes_dataset.csv', 'r') as file:
      reader = csv.reader(file)
      chosen_row = random.choice(list(reader))
      quote, author, tokens = chosen_row[0], chosen_row[1], chosen_row[2]
      self.speaker.tell(quote)
      self.speaker.tell(f'Author {author}.')

  def poem(self):
    with open('./data/poem_dataset.csv', 'r') as file:
      reader = csv.reader(file)
      chosen_row = random.choice(list(reader))
      poem, author, title = chosen_row[4], chosen_row[1], chosen_row[2]
      self.speaker.tell(title)
      self.speaker.tell(poem)
      self.speaker.tell(f'Author {author}.')

  def joke(self):
    joke = pyjokes.get_joke(language='en', category='all')
    self.speaker.tell(joke)

  def weather(self):
    try:
      today_w = Weathers.select().where(Weathers.created_at >= date.today()).order_by(Weathers.id.desc()).get()
    except peewee.DoesNotExist:
      today_w = None

    weather_speech = wp.main(city='Lviv')
    w_data = re.findall(r"[-+]?\d*\.\d+|\d+", weather_speech)

    if today_w:
      self.speaker.write(f'Last recorded temp: {today_w.temperature} and wind: {today_w.wind}')
      if today_w.temperature == float(w_data[0]) and today_w.wind == float(w_data[1]):
        self.speaker.write('Weather havent changed.')
        return
      else:
        Weathers.create(temperature=float(w_data[0]), wind=float(w_data[1]), created_at=date.today())
        self.speaker.tell('The weather has changed.')
        self.speaker.tell(weather_speech)
    else:
      try:
        Weathers.create(temperature=float(w_data[0]), wind=float(w_data[1]), created_at=date.today())
      except IndexError:
        pass
      self.speaker.tell(weather_speech)

  def datetime_now(self):
    tdate = datetime.datetime.now().strftime("%b %d %Y")
    ttime = datetime.datetime.now().strftime("%H:%M")

    try:
      today_w = Weathers.select().where(Weathers.created_at >= date.today()).order_by(Weathers.id.desc()).get()
    except peewee.DoesNotExist:
      today_w = None

    if today_w:
      self.speaker.tell(f"It's {ttime} o'clock")
    else:
      self.speaker.tell(f'Today is {tdate}')
      self.speaker.tell(f"It's {ttime} o'clock")

  def read_dial(self):
    response = requests.get(f'https://pidru4niki.com/15780506/filosofiya/osnovni_zakoni_dialektiki_svitoglyadne_metodologichne_znachennya')
    paragraphs = justext.justext(response.content, justext.get_stoplist("Ukrainian"))
    prs = [pp for pp in paragraphs if not pp.is_boilerplate]
    chosen_p = random.choice(list(prs))
    self.speaker.tell_ua(chosen_p.text)

  def scenario(self):
    self.greeting()
    self.datetime_now()
    self.weather()

    self.speaker.tell('Aphorism:')
    self.aphorism()
    self.speaker.tell('A joke:')
    self.joke()
    self.speaker.tell('A poem:')
    self.poem()
    self.speaker.tell_ua('Елемент діалектики:')
    self.read_dial()

if __name__ == "__main__":
  disc = Radio()
  disc.scenario()
