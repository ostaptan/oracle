import os
import sys
import requests
import justext
import logging
import subprocess
from features.speaker import Speaker
from cryptography.fernet import Fernet

class Conductor:
  APPSTORE = {
    'brave': "/Applications/'Brave Browser.app'",
    'sublime': "/Applications/'Sublime Text.app'",
    'steam': '/Applications/Steam.app',
    'skype': '/Applications/Skype.app',
    'telegram': '/Applications/Telegram.app',
  }

  def __init__(self):
    self.speaker = Speaker()

  def speak(self, text, app_name='conductor'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.speaker.text2speech(text)

  def launch(self, app_name):
    self.speak(f'Opening {app_name}')
    app_path = self.APPSTORE.get(app_name)
    subprocess.call(["/bin/bash","-c",f'open {app_path}'])

  def unlock(self, fname):
    key = self.__get_key()
    fernet = Fernet(key)

    with open(f'sandbox/{fname}.txt', 'rb') as enc_file:
      encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)
    print(decrypted)
    with open(f'sandbox/{fname}.txt', 'wb') as dec_file:
      dec_file.write(decrypted)

  def lock(self, fname):
    key = self.__get_key()
    fernet = Fernet(key)

    with open(f'sandbox/{fname}.txt', 'rb') as file:
      original = file.read()

    encrypted = fernet.encrypt(original)

    with open(f'sandbox/{fname}.txt', 'wb') as encrypted_file:
      encrypted_file.write(encrypted)

  def __get_key(self):
    key_path = 'db/fernet.key'

    if os.path.exists(key_path):
      with open(key_path, 'rb') as filekey:
        return filekey.read()
    else:
      with open(key_path, 'wb') as filekey:
        key = Fernet.generate_key()
        filekey.write(key)
        return key

