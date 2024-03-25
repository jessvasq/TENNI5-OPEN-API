#import all from peewee
from peewee import *
import datetime
#flask_login allows us to set up user sessions
from flask_login import UserMixin
from config import DATABASE_URL, DATABASE_URL_1


#updated to postgres
DATABASE = PostgresqlDatabase(DATABASE_URL)
DATABASE1 = PostgresqlDatabase(DATABASE_URL_1)

    
'''USER MODEL'''    
#UserMixin gives our class some default features 
class User(UserMixin, Model):
    username = CharField(unique=True) #each username/email should be unique within the database
    email = CharField(unique=True)
    password = CharField()    
    
    #The Meta class is used to provide metadata or config options for the model class. In this case, it specifies the database to which the 'user' model is associated with 
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

########## MESSAGING FUNCTION ###########################

'''CONVERSATION MODEL'''
class Conversation(Model):
    name = CharField()
    
    class Meta:
        database = DATABASE

'''MESSAGE MODEL'''
class Message(Model):
    conversation = ForeignKeyField(Conversation, backref="mssgs") #establishes a relationship between this model and Conversation model 
    user = ForeignKeyField(User, backref="mssgs") #each message will be associated with a user 
    message = CharField() #store the message 

    class Meta: 
        database = DATABASE

###################### FEATURES ###########################


'''VIDEO MODEL'''
class Video(Model):
    id = AutoField(primary_key=True)
    video = CharField()
    description = CharField()
    title = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE1


'''EQUIPMENT MODEL'''
class Equipment(Model):
    id = AutoField(primary_key=True)
    category = CharField()
    store = CharField()
    image = CharField()
    description = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE1
        

'''LESSON MODEL'''
class Lesson(Model):
    id = AutoField(primary_key=True)
    video = CharField()
    title = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE1
        

#initialize, set our datatables
def initialize():
    #connect to the database before each request
    DATABASE.connect()
    DATABASE1.connect()
    #create db tables
    #safe=True --> prevent accidental data loss or corruption byt checking if any of the tables already exist in the database. If they do, Peewee will not recreate or make any changes to them, it will skip the created tables and move on to create the tables that do not exist yet 
    DATABASE.create_tables([User, Match, Conversation, Message, Video], safe=True)
    print('Tables created')
    DATABASE1.create_tables([Video, Equipment, Lesson], safe=True)
    print('Media tables created')
    #close the database connection after each request
    DATABASE.close()
    DATABASE1.close()

