import sys
import requests
import justext
import logging
from features.speaker import Speaker

# smth is wrong here with conception of naming
#
#
#
#
#
#
#

class Performer:
  APPSTORE = {
    'brave': "/Applications/'Brave Browser.app'",
    'sublime': "/Applications/'Sublime Text.app'",
    'steam': '/Applications/Steam.app',
    'skype': '/Applications/Skype.app',
    'telegram': '/Applications/Telegram.app',
  }

  def __init__(self):
    self.speaker = Speaker()

  def speak(self, text, app_name='performer'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.speaker.text2speech(text)

  def launch(self, app_name):
    self.speak(f'Opening {app_name}')
    app_path = self.APPSTORE.get(app_name)
    subprocess.call(["/bin/bash","-c",f'open {app_path}'])

  def read(self, url):
    response = requests.get(url)
    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    for paragraph in paragraphs[5:22]:
      self.speak(paragraph.text)

