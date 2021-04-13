import os
import sys
import requests
import cryptography
import justext
import time
import logging
import subprocess

from cryptography.fernet import Fernet

class Conductor:
  APPSTORE = {
    'brave': "/Applications/'Brave Browser.app'",
    'sublime': "/Applications/'Sublime Text.app'",
    'steam': '/Applications/Steam.app',
    'skype': '/Applications/Skype.app',
    'telegram': '/Applications/Telegram.app',
  }

  def __init__(self, speaker):
    self.speaker = speaker

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

  def exit(self):
    self.speaker.tell('Exiting. Good bye.')
    sys.exit()

  def sleep(self):
    tn = time.strftime("%H:%M", time.localtime())
    self.speaker.tell(f'Sleeping at {tn}')
    time.sleep(float(60*60*3)) # 60 secs in 60 mins 3 times
    self.speaker.tell('Awaken!')

  def launch(self, app_name):
    self.speaker.tell(f'Opening {app_name}')
    app_path = self.APPSTORE.get(app_name)
    subprocess.call(["/bin/bash","-c",f'open {app_path}'])

  def unlock(self, fname):
    try:
      key = self.__get_key()
      fernet = Fernet(key)

      with open(f'sandbox/{fname}.txt', 'rb') as enc_file:
        encrypted = enc_file.read()

      decrypted = fernet.decrypt(encrypted)
    except cryptography.fernet.InvalidToken:
      decrypted = encrypted

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


