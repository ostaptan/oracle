import sys
import re
import subprocess
import wikipedia
import logging
import peewee

from datetime import date
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from features.speaker import Speaker
from db.models import Definitions

class Searcher:
  def __init__(self):
    self.speaker = Speaker()

  def __speak(self, text, app_name='searcher'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.speaker.text2speech(text)

  def local_news(self):
    try:
      news_url = "https://news.google.com/news/rss/headlines/section/geo/Lviv"
      client = urlopen(news_url)
      xml_page = client.read()
      client.close()
      soup_page = soup(xml_page, "xml")
      news_list = soup_page.findAll("item")
      for news in news_list[:3]:
        self.__speak(str(news.title.text.encode('utf-8'))[1:])
    except Exception as e:
      print(e)
      return False

  def topic_news(self, topic):
    try:
      news_url = "https://news.google.com/rss/search?q={topic}+when:7d"
      client = urlopen(news_url)
      xml_page = client.read()
      client.close()
      soup_page = soup(xml_page, "xml")
      news_list = soup_page.findAll("item")
      for news in news_list[:3]:
        self.__speak(str(news.title.text.encode('utf-8'))[1:])
    except Exception as e:
      print(e)
      return False

  def wiki(self, topic):
    try:
      ex_def = Definitions.get(topic == topic)
    except peewee.DoesNotExist:
      ex_def = None
    if ex_def:
      self.__speak(f'Already told you about {topic}')
      self.__speak(ex_def.text)
    else:
      self.__speak(f'Searching in wikipedia about {topic}')
      try:
        wiki_resp = wikipedia.page(topic)
        res = str(wiki_resp.content[:500].encode('utf-8'))
        resp = re.sub('[^a-zA-Z.\d\s]', '', res)[1:]
        Definitions.create(topic=topic, text=resp, created_at=date.today())
        self.__speak(resp)
      except wikipedia.exceptions.PageError:
        Definitions.create(topic=topic, text='Cannot find anything', created_at=date.today())
        self.__speak(f'Cannot find anything about {topic}')

