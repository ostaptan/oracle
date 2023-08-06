import random
import os
import time
import logging
import sys
import platform

from gtts import gTTS
import subprocess

class Speaker:
  def __init__(self, app_name):
    self.app_name = app_name

  def write(self, text):
    print(text)
    logging.basicConfig(filename=f'logs/{self.app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)

  def tell_ua(self, text):
    logging.basicConfig(filename=f'logs/{self.app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.__text2speech(text, lang='uk')

  def tell(self, text):
    logging.basicConfig(filename=f'logs/{self.app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.__text2speech(text)

  def __play_on_platforms(self, text, lang):
    myobj = gTTS(text=text, lang=lang, slow=False)
    filename_str = '-'.join(text.split(' ')[:3])
    print(text)
    filename_ascii = time.strftime("%H%M%S%d%m%Y") + '_' + '-'.join(str(ord(word)) for word in filename_str)
    myobj.save(f'sounds/{filename_ascii}.mp3')
    if 'ubuntu' in platform.version().lower():
      os.system('play ' + f'sounds/{filename_ascii}.mp3 --no-show-progress')
    else:
      os.system('afplay ' + f'sounds/{filename_ascii}.mp3')

  def __text2speech(self, text, lang='en'):
    """
    Convert any text to speech
    :param text: str
        text (String)
    :param lang: str
        default 'en'
    :return: Bool
        True / False (Play sound if True otherwise write exception to log and return False)
    """
    try:
      self.__play_on_platforms(text, lang)
      return True
    except Exception as e:
      mytext = "Sorry I couldn't understand."
      self.__play_on_platforms(mytext, lang)
      # os.system("""
      #         osascript -e 'display notification "{}" with title "{}"' with timeout of 86400 seconds end timeout
      #         """.format("Sorry I couldn't understand.", 'Oracle'))
      return False
