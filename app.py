from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy
#models
import models


#initialize instance of the Flask class
app = Flask(__name__)
DEBUG=True
PORT=8000


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




@app.route('/')
def hello():
    return 'Hello Mundo!'


if __name__ == '__main__':
    models.initialize()
    #runs our app
    app.run(debug=DEBUG, port=PORT)