import sys
import os
import re

from features.writer import Writer
from features.conductor import Conductor

class BasicCommander:
  # speaker
  def __init__(self, speaker):
    self.conductor = Conductor(speaker)
    self.writer = Writer(speaker)

  def do(self, speech):
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
