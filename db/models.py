from peewee import *

db = SqliteDatabase('db/oracle_dev.sqlite')

class BaseModel(Model):
  class Meta:
    database = db

class ActiveFiles(BaseModel):
  path = CharField()
  opened = BooleanField()
  created_at = DateField()

class Weathers(BaseModel):
  temperature = FloatField()
  wind = FloatField()
  created_at = DateField()

class Definitions(BaseModel):
  topic = CharField(unique=True)
  text = TextField()
  created_at = DateField()

db.connect()
db.create_tables([Weathers, Definitions, ActiveFiles])
