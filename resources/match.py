import models
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

#blueprints record operations to execute when registered on an app 
match = Blueprint('matches', 'match')


'''POST ROUTE - CREATE '''

'''Route handler for a POST request at the root path ("/") of the web application. When accessed, it retrieves the JSON payload from the request, creates a new dog object in the database with the provided data, prints information about the created dog object, converts it to a dictionary, and returns a JSON response containing the dog's data and a success message'''


@match.route('/', methods=['POST'])
def create_match():
    payload=request.get_json()
    print(type(payload), 'payload')
    new_match = models.Match.create(**payload)
    #print object
    print(new_match.__dict__)
    print(dir(new_match)) #prints all the methods and attributes of the match object
    #change model to dictionary
    print(model_to_dict(new_match), 'dictionary')
    match_dict = model_to_dict(new_match) #assigns the converted dictionary of the match object to the match_dict variable.
    return jsonify(
        data=match_dict,
        message="Successfully created",
        status=201
        ), 201