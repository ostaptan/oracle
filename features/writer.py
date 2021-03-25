import re
import sys
import logging
import peewee
from datetime import date
from db.models import ActiveFiles

from features.speaker import Speaker
from features.conductor import Conductor

class Writer:
  def __init__(self):
    self.speaker = Speaker()

  def speak(self, text, app_name='writer'):
    logging.basicConfig(
      filename=f'logs/{app_name}.log',
      encoding='utf-8',
      level=logging.INFO
    )
    logging.info(text)
    self.speaker.text2speech(text)

  def mustdo(self, speech):
    file = self.wopen('MUSTDO')
    file.write(speech + "\n")
    self.wclose(file)

  def wopen(self, fname):
    Conductor().unlock('MUSTDO')
    fpath = f'./sandbox/{fname}.txt'
    f = open(fpath, 'a+')
    ActiveFiles.create(
      path=fpath,
      opened=True,
      created_at=date.today()
    )
    return f

  def recent_file(self):
    try:
      ActiveFiles \
        .select() \
        .where(ActiveFiles.created_at >= date.today()) \
        .order_by(ActiveFiles.id.desc()) \
        .get()
    except peewee.DoesNotExist:
      return None

  def wclose(self, f):
    f.close()
    Conductor().lock('MUSTDO')
    recent_rec = self.recent_file()
    recent_rec.opened = False
    recent_rec.save()

