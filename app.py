from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy
#models
import models
from resources.match import match
from flask_cors import CORS

DEBUG=True
PORT=8000

#initialize instance of the Flask class
app = Flask(__name__)

#set up a database connection before a request
#g global access to our database 
@app.before_request
def before_request():
    #assign the values of models.DATABASE to 'g.db'
    g.db=models.DATABASE
    #opens a connection when a request starts
    g.db.connect()

#close the db connection after the response is returned
@app.after_request
def after_request(response): 
    g.db.close()
    return response 

'''SET UP CORS: MATCH'''
#CORS - let us communicate with our frontend, frontend can send HTTP requests
CORS(match, origins=['http://localhost:3000'], supports_credentials=True) #allow cookies to be sent to the server
#set up the prefix for every route in our match resource 
app.register_blueprint(match, url_prefix='/tenni5open')





@app.route('/')
def hello():
    return 'Hello Mundo!'



if __name__ == '__main__':
    models.initialize()
    #runs our app
    app.run(debug=DEBUG, port=PORT)