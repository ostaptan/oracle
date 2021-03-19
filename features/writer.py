import re
import sys
import logging
from features.speaker import Speaker

class Writer:
  def __init__(self):
    self.speaker = Speaker()
    self.recent_file = open(f'./sandbox/default.txt', 'a+')

  def speak(self, text, app_name='writer'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.speaker.text2speech(text)

  def file_open(self, fname):
    self.speak(f'Opening file {fname} in a sandbox.')
    f = open(f'./sandbox/{fname}.txt', 'a+')
    self.recent_file = f

  def file_write(self, speech):
    self.recent_file.write(speech + "\n")

  def close_file(self):
    self.speak(f'Closing file.')
    self.recent_file.close()
