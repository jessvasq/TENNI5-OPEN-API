import models
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required

#blueprints record operations to execute when registered on an app 
match = Blueprint('matches', 'match')


'''POST ROUTE - CREATE '''

'''Route handler for a POST request at the root path ("/") of the app. When accessed, it retrieves the JSON payload from the request, creates a new match object in the database with the provided data, prints information about the created match object, converts it to a dictionary, and returns a JSON response containing the match's data and a success message'''


# @match.route('/', methods=['POST'])
# def create_match():
#     payload=request.get_json()
#     print(type(payload), 'payload')
#     new_match = models.Match.create(**payload)
#     #print object
#     print(new_match.__dict__)
#     print(dir(new_match)) #prints all the methods and attributes of the match object
#     #change model to dictionary
#     print(model_to_dict(new_match), 'dictionary')
#     match_dict = model_to_dict(new_match) #assigns the converted dictionary of the match object to the match_dict variable.
#     return jsonify(
#         data=match_dict,
#         message="Successfully created",
#         status=201
#         ), 201
  
@match.route('/', methods=['POST'])
@login_required
def create_match():
    payload = request.get_json() #retrieves the request as JSON format 
    new_match = models.Match.create(
        image=payload['image'],
        description=payload['description'],
        location=payload['location'],
        date=payload['date'],
        host_name=current_user.id,
        players=payload['players'],
        skill_level=payload['skill_level'],
        price=payload['price']
        )
    match_dict = model_to_dict(new_match)#converts object to dictionary and assigns to match_dict variable 
    
    return jsonify(
        data=match_dict, 
        message= "Match has been succesfully created", 
        status=201, 
    ), 201
  
  
    

'''GET ROUTE - INDEX all "matches"'''

'''route handler for a GET request at the root path ("/") of the app. When accessed, it retrieves all the matches from the database, converts them to dictionaries, prints them to the console, and returns a JSON response containing the matches' data and a success message. If there are no matches in the database, it returns an error response.'''

@match.route('/')
def get_all_matches():
    try:
        matches=[model_to_dict(match) for match in models.Match.select()] #.select() finds/retrieves all the matches on our model. It iterates over the 
       #result and converts each match object to a dictionary and the result is stored in the 'matches' variable as a list of dictionaries
        print(matches)
        return jsonify(data=matches, status={
            "code":200, 
            "message": f"Success! All matches have been retrieved. Total matches: {len(matches)}"
        })
    except models.DoesNotExist: # #if there are no matches in the database, it returns a JSON response with: 
        return jsonify(
            data={}, # an empty data object
            status={
                "code": 401, #an error mssg
                "message": "Error pulling the data"
            }
        )


# @match.route('/')
# def get_all_matches():
#     match_dict = [model_to_dict(match) for match in current_user.my_matches]
#     return jsonify({
#         "data":match_dict, 
#         "message": f"Successfully found {len(match_dict)} matches", 
#         "status": 200
#     }), 200





'''SHOW ROUTE - show a specific "match"''' 

'''Route handler for a GET request at the '/<id>' route of the app. When accessed, it captures the id value from the URL, retrieves the corresponding match' object from the database, prints information about the retrieved match' object, converts it to a dictionary, and returns a JSON response containing the matches's data, along with a success message and a status code of 200.'''


@match.route('/<id>', methods=['GET'])
def get_match(id): #accepts "id" as param
    print(id, "id") 
    match = models.Match.get_by_id(id) #fetches a 'match' object with the corresponding id from the database
    print(match.__dict__) #prints "match" dictionary
    return jsonify(
        data=model_to_dict(match), #converts "match" object to a dictionary
        status=200,
        message='Sucess'
    ), 200    



'''UPDATE ROUTE'''

''' Route handler for a PUT request at the '/<id>' route of the app. When accessed, it captures the id value from the URL, retrieves the corresponding match object from the database, updates it with the data provided in the request payload, and returns a JSON response containing the updated match's data, along with a success message and a status code of 200.'''


@match.route('/<id>', methods=['PUT'])
@login_required
def update_match(id): #accepts id parameter 
    payload = request.get_json() #retieves the JSON from the request
    query = models.Match.update(**payload).where((models.Match.id==id) & (models.Match.host_name == current_user))#update method is applied to the "match" object with the same id & username. This object is then assigned to the query variable
    query.execute() #executes the updates 
    return jsonify( #returns a JSON response 
        data=model_to_dict(models.Match.get_by_id(id)),
        status=200, 
        message='match updated successfully'
    ), 200
    
'''DELETE ROUTE'''

'''Route handler for a DELETE request at the '/<id>' route of the app. When accessed, it captures the id value from the URL, constructs a delete query to remove the corresponding match object from the database, and returns a JSON response indicating the success of the deletion, along with a success message and a status code of 200.'''


# @match.route('/<id>', methods=['Delete'])
# @login_required
# def delete_match(id):
#     query = models.Match.delete().where(models.Match.id==id)
#     query.execute()
#     return jsonify(
#         data="match successfully deleted",
#         status=200, 
#         message='match deleted successfully'
#     ), 200
    
#need to figure out how to delete 

@match.route('/<id>', methods=['Delete'])
@login_required
def delete_match(id):
    query = models.Match.delete().where((models.Match.id==id) & (models.Match.host_name == current_user))
    query.execute()
    return jsonify(
        data="match successfully deleted",
        status=200, 
        message='match deleted successfully'
    ), 200