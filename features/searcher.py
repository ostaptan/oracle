import sys
import re
import subprocess
import wikipedia
import logging
import peewee
import requests
import json
import lxml

from datetime import date
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from db.models import Definitions

class Searcher:
  def __init__(self, speaker):
    self.speaker = speaker

  def local_news(self):
    try:
      news_url = "https://news.google.com/news/rss/headlines/section/geo/Lviv"
      client = urlopen(news_url)
      xml_page = client.read()
      client.close()
      soup_page = soup(xml_page, "xml")
      news_list = soup_page.findAll("item")
      for news in news_list[:3]:
        self.speaker.tell(str(news.title.text.encode('utf-8'))[1:])
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
        self.speaker.tell(str(news.title.text.encode('utf-8'))[1:])
    except Exception as e:
      print(e)
      return False

  def wiki(self, topic):
    try:
      ex_def = Definitions.get(topic == topic)
    except peewee.DoesNotExist:
      ex_def = None
    if ex_def:
      self.speaker.tell(f'Already told you about {topic}')
      self.speaker.tell(ex_def.text)
    else:
      self.speaker.tell(f'Searching in wikipedia about {topic}')
      try:
        wiki_resp = wikipedia.page(topic)
        res = str(wiki_resp.content[:500].encode('utf-8'))
        resp = re.sub('[^a-zA-Z.\d\s]', '', res)[1:]
        Definitions.create(topic=topic, text=resp, created_at=date.today())
        self.speaker.tell(resp)
      except wikipedia.exceptions.PageError:
        Definitions.create(topic=topic, text='Cannot find anything', created_at=date.today())
        self.speaker.tell(f'Cannot find anything about {topic}')

  def google(self, q):
    headers = {
      'User-agent':
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    params = {
      'q': q,
      'source': 'web'
    }
    html = requests.get('https://search.brave.com/search', headers=headers, params=params)
    bs = soup(html.text, "lxml")
    data = []

    for result in bs.select('.snippet.fdb'):
      title = result.select_one('.snippet-title').text.strip()
      img = result.select_one('.favicon')['src']
      link = result.a['href']

      try:
        desc = result.select_one('.snippet-description').text.strip()
      except:
        desc = None

      data.append({
        'title': title,
        'desc': desc,
        'link': link,
        'img': img
      })

    #TODO: neural select
    print(json.dumps(data[:4], indent=2, ensure_ascii=False))
    self.speaker.tell(data[3]['desc'])
