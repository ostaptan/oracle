import sys
import os
import re

from features.writer import Writer
from features.conductor import Conductor
import src.weather_puller as wp

class BasicCommander:
  def __init__(self, speaker):
    self.speaker = speaker
    self.conductor = Conductor(speaker)
    self.writer = Writer(speaker)

  def __notify(self, title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"' with timeout of 86400 seconds end timeout
              """.format(text, title))

  def greeting(self):

    text = f'Welcome, master {sys_name}!'
    self.__notify('γνῶθι σεαυτόν!', text)
    self.speaker.tell(text)

  def do(self, speech):

    if re.search('spen', speech):
      self.speaker.tell(''.join(speech.split('spen')[1:]).strip())
      return True

    if re.search('spua', speech):
      self.speaker.tell_ua(''.join(speech.split('spua')[1:]).strip())
      return True

    if re.search('greeting', speech):
      self.greeting()
      return True

    if re.search('weather', speech):
      self.speaker.tell(wp.main())
      return True

    # ---
    # writer section
    #
    if re.search('fix todo', speech):
      todo = ''.join(speech.split('todo')[1:]).strip()
      self.writer.mustdo(todo)
      return True

    if re.search('show fixed|todos', speech):
      self.writer.show_mustdo()
      return True

    # ---
    # conductor section
    #
    if re.search('open|launch|start application', speech):
      app_name = speech.split('application')[-1].strip()
      self.conductor.launch(app_name)
      return True

    if re.search('unlock', speech):
      self.conductor.unlock('MUSTDO')
      return True

    if re.search('lock', speech):
      self.conductor.lock('MUSTDO')
      return True

    if re.search('stop|finish|shutdown|exit', speech):
      self.conductor.exit()
      return True

    if re.search('sleep', speech):
      self.conductor.sleep()
      return True

    return False
