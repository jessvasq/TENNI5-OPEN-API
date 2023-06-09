#import all from peewee
from peewee import *
import datetime
from flask_login import UserMixin


#need to update this and connect to our production database postgres
DATABASE = SqliteDatabase('tenni5.sqlite')

    
'''USER MODEL'''    
class User(UserMixin, Model):
    username = CharField(unique=True) #each username/email should be unique within the database
    email = CharField(unique=True)
    password = CharField()    
    
    #user will use the same database as the match model 
    class Meta: 
        database = DATABASE 
     
     
     

'''TENNIS MATCH MODEL'''
           #the 'Model' in the Match class argument is a class from Peewee that gives the ability to talk to our sql database
class Match(Model):
    id = AutoField(primary_key=True)
    image = CharField()
    description = CharField()
    location = CharField()
    date = DateField()
    username = CharField()
    host_name = ForeignKeyField(User, backref='my_matches')#we use 'my_matches' on ana instance of a User to list all matches associated with a single user 
    players=CharField()
    skill_level=CharField()
    price = CharField()
    is_in_my_matches = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

        
#initialize, set our datatables
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Match], safe=True)
    print('Tables created')
    DATABASE.close()

