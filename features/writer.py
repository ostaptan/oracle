import re
import sys
import logging
import peewee
from datetime import date
from db.models import ActiveFiles

from features.conductor import Conductor

class Writer:
  def __init__(self, speaker):
    self.speaker = speaker
    self.conductor = Conductor(speaker)

  def recent_file(self):
    try:
      ActiveFiles \
        .select() \
        .where(ActiveFiles.created_at >= date.today()) \
        .order_by(ActiveFiles.id.desc()) \
        .get()
    except peewee.DoesNotExist:
      return None

  def show_mustdo(self):
    fname = 'MUSTDO'
    self.conductor.unlock(fname)
    fpath = f'./sandbox/{fname}.txt'
    with open(fpath, 'r') as file:
      print(file.read())
    self.conductor.lock(fname)

  def mustdo(self, speech):
    file = self.wopen('MUSTDO')
    file.write(speech + "\n")
    self.speaker.tell('Text fixed in files.')
    self.wclose(file)

  def wopen(self, fname):
    self.conductor.unlock(fname)
    fpath = f'./sandbox/{fname}.txt'
    f = open(fpath, 'a+')
    ActiveFiles.create(
      path=fpath,
      opened=True,
      created_at=date.today()
    )
    return f

  def wclose(self, f):
    f.close()
    self.conductor.lock('MUSTDO')
    recent_rec = self.recent_file()
    if recent_rec:
      recent_rec.opened = False
      recent_rec.save()

