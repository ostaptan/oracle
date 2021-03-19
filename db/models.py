from peewee import *

db = SqliteDatabase('db/oracle_dev.sqlite')

class BaseModel(Model):
  class Meta:
    database = db

class Weathers(BaseModel):
  temperature = FloatField(unique=False)
  wind = FloatField(unique=False)
  created_at = DateField(unique=False)

class Definitions(BaseModel):
  topic = CharField(unique=True)
  text = TextField(unique=False)
  created_at = DateField(unique=False)

db.connect()
db.create_tables([Weathers, Definitions])
