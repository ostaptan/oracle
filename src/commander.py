#
# will be replaced by neural net
#
import sys
import os
import re
import time
import logging

from features.listener import Listener
from features.radio import Radio
from features.searcher import Searcher
from features.writer import Writer
from features.conductor import Conductor

class Commander:
  def __init__(self, speaker):
    self.listener = Listener()
    self.speaker = speaker
    self.radio = Radio(speaker)
    self.conductor = Conductor(speaker)
    self.writer = Writer(speaker)
    self.searcher = Searcher(speaker)

  def do(self, speech):
    if re.search('greeting', speech):
      self.radio.greeting()

    # ---
    # radio section
    #
    if re.search('radio', speech):
      self.radio.scenario()

    if re.search('joke', speech):
      self.radio.joke()

    if re.search('spen', speech):
      phrase = ''.join(speech.split('spen')[1:]).strip()
      self.speaker.tell(phrase)

    if re.search('spua', speech):
      phrase = ''.join(speech.split('spua')[1:]).strip()
      self.speaker.tell_ua(phrase)

    if re.search('time', speech):
      self.radio.datetime_now()

    if re.search('aphorism|quote', speech):
      self.radio.aphorism()

    if re.search('poem', speech):
      self.radio.poem()

    if re.search('weather', speech):
      self.radio.weather()

    if re.search('dialectica', speech):
      self.radio.read_dial()

    # ---
    # searcher section
    #
    if re.search('wiki', speech):
      topic = ' '.join(speech.split('wiki')[1:]).strip()
      self.searcher.wiki(topic)

    if re.search('local news', speech):
      self.searcher.local_news()

    # WORLD NATION BUSINESS TECHNOLOGY ENTERTAINMENT SPORTS SCIENCE HEALTH
    if re.search('news about', speech):
      topic = speech.split('about')[-1].strip()
      self.searcher.topic_news(topic.upper())

    # ---
    # writer section
    #
    if re.search('fix todo', speech):
      todo = ''.join(speech.split('todo')[1:]).strip()
      self.writer.mustdo(todo)

    if re.search('show fixed|todos', speech):
      self.writer.show_mustdo()

    recent_rec = self.writer.recent_file()
    if recent_rec and recent_rec.opened:
      f = open(recent_rec.path, 'a+')
      f.write(f, speech + "\n")

      if re.search('end', speech):
        self.writer.wclose(f)

    # ---
    # conductor section
    #
    if re.search('open|launch|start application', speech):
      app_name = speech.split('application')[-1].strip()
      self.conductor.launch(app_name)

    if re.search('unlock', speech):
      self.conductor.unlock('MUSTDO')

    if re.search('lock', speech):
      self.conductor.lock('MUSTDO')

    if re.search('stop|finish|shutdown|exit', speech):
      self.conductor.exit()

    if re.search('sleep', speech):
      self.conductor.sleep()


