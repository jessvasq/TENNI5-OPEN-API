#import all from peewee
from peewee import *
import datetime


#need to update this and connect to our production database postgres
DATABASE = SqliteDatabase('tenni5.sqlite')


class Match(Model):
    id = AutoField(primary_key=True)
    image = CharField()
    description = CharField()
    location = CharField()
    date = DateField()
    host_name = CharField()
    players=CharField()
    skill_level=CharField()
    price = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        
#initialize, set our datatables

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Match], safe=True)
    print('Tables created')
    DATABASE.close()

