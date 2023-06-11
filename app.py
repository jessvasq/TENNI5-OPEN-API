from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
#models
import models
from resources.match import match
from resources.user import user
#chat
from resources.chat import chat
#videos
from resources.videos import video
#equipment 
from resources.equipment import equipment

DEBUG=True
PORT=8000


#initialize instance of the Flask class
app = Flask(__name__)

'''USER SESSION'''

#Login manager to set up the session 
login_manager = LoginManager()

#SECRET KEY to encode the session 
app.secret_key = 'R00NDMDNK8200B42'
#set up the session in the app 
login_manager.init_app(app)

@login_manager.user_loader #load the user object whenever we access the session. It takes the unicode ID of a user, and return the corresponding user object.
def load_user(user_id):
    try: 
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

''''''

#set up a database connection before a request
#g global access to our database 
@app.before_request
def before_request():
    #assign the values of models.DATABASE to 'g.db'
    g.db=models.DATABASE
     #assign the values of models.DATABASE to 'g.db'
    g.db_1=models.DATABASE1
    #opens a connection when a request starts
    g.db.connect()
    g.db_1.connect()

#close the db connection after the response is returned
@app.after_request
def after_request(response): 
    g.db.close()
    g.db_1.close()
    return response 

'''SET UP CORS: TENNIS MATCH'''
#CORS - let us communicate with our frontend, frontend can send HTTP requests
CORS(match, origins=['http://localhost:3000'], supports_credentials=True) #allow cookies to be sent to the server
#set up the prefix for every route in our match resource 
app.register_blueprint(match, url_prefix='/tenni5open')

'''SET UP CORS: USER'''
#setting up cors to allow react to connect to the API
CORS(user, origins=['http://localhost:3000'], supports_credentials=True) #support_credentials=True, let us send cookies back and forth 
app.register_blueprint(user, url_prefix='/user')


#####CHAT 

'''SET UP CORS: CHAT'''
#setting up cors to allow react to connect to the API
CORS(chat, origins=['http://localhost:3000'], supports_credentials=True) #support_credentials=True, let us send cookies back and forth 
app.register_blueprint(chat, url_prefix='/chat')

#####################################

'''SET UP CORS: VIDEOS'''
CORS(video, origins=['http://localhost:3000'], supports_credentials=True) #support_credentials=True, let us send cookies back and forth 
app.register_blueprint(video, url_prefix='/tutorials')

'''SET UP CORS: EQUIPMENT'''
CORS(equipment, origins=['http://localhost:3000'], supports_credentials=True) #support_credentials=True, let us send cookies back and forth 
app.register_blueprint(equipment, url_prefix='/equipment')

@app.route('/')
def hello():
    return 'Hello Mundo!'



if __name__ == '__main__':
    models.initialize()
    #runs our app
    app.run(debug=DEBUG, port=PORT)