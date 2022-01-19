#
# must be replaced by network
#
import sys
import os
import re
import time
import json
import logging

from features.listener import Listener
from features.radio import Radio
from features.searcher import Searcher
from features.writer import Writer
from features.conductor import Conductor
from features.emailer import Emailer
from features.data_forest import DataForest

class Commander:
  def __init__(self, speaker):
    self.listener = Listener()
    self.speaker = speaker
    self.radio = Radio(speaker)
    self.conductor = Conductor(speaker)
    self.writer = Writer(speaker)
    self.searcher = Searcher(speaker)
    self.emailer = Emailer(speaker)
    self.data_forest = DataForest(speaker)

  def do(self, speech):
    if re.search('greeting', speech):
      self.radio.greeting()

    # ---
    # static radio section
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
    # data forest section
    #
    if re.search('df.map', speech):
      sys_name = os.getcwd().split('/')[2]
      default_path = f'/Users/{sys_name}/Downloads'
      working_dir = speech.split(':')[-1].strip() or default_path
      fmap, stats = self.data_forest.rec_map({}, working_dir)
      print(f'Files Map: ({len(fmap)})')
      print(stats)
      # print(json.dumps(fmap, indent=4, sort_keys=False))

    if re.search('df.classify', speech):
      sys_name = os.getcwd().split('/')[2]
      default_path = f'/Users/{sys_name}/Downloads'
      working_dir = speech.split(':')[-1].strip() or default_path
      self.data_forest.classify(working_dir)

    # must focus/saver/notetaker action to save latest speech/text/output
    # reminder about it later
    #

    # ---
    # research section
    #
    # WIP
    # if re.search('emailer', speech):
    #   self.emailer.map()

    if re.search('google', speech):
      question = speech.split(':')[-1].strip()
      self.searcher.google(question)

    if re.search('wiki', speech):
      topic = speech.split(':')[-1].strip()
      self.searcher.wiki(topic)

    if re.search('local news', speech):
      self.searcher.local_news()

    # WORLD NATION BUSINESS TECHNOLOGY ENTERTAINMENT SPORTS SCIENCE HEALTH
    if re.search('news', speech):
      topic = speech.split(':')[-1].strip()
      self.searcher.topic_news(topic.upper())

    # ---
    # files management section
    #
    if re.search('todo', speech):
      todo = speech.split(':')[-1].strip()
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
    # settings & apps section
    #
    if re.search('open|launch|start app', speech):
      app_name = speech.split('app')[-1].strip()
      self.conductor.launch(app_name)

    if re.search('unlock', speech):
      self.conductor.unlock('MUSTDO')

    if re.search('lock', speech):
      self.conductor.lock('MUSTDO')

    if re.search('stop|finish|shutdown|exit', speech):
      self.conductor.exit()

    # if re.search('sleep', speech):
      # cannot interrupt this one
      # self.conductor.sleep()


