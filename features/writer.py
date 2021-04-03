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
    self.speaker = Speaker('writer')

  def recent_file(self):
    try:
      ActiveFiles \
        .select() \
        .where(ActiveFiles.created_at >= date.today()) \
        .order_by(ActiveFiles.id.desc()) \
        .get()
    except peewee.DoesNotExist:
      return None

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

  def wclose(self, f):
    self.speaker.tell('Text fixed in files.')
    f.close()
    Conductor().lock('MUSTDO')
    recent_rec = self.recent_file()
    if recent_rec:
      recent_rec.opened = False
      recent_rec.save()

