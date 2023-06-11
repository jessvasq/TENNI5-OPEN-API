import models
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

#blueprints record operations to execute when registered on an app 
equipment = Blueprint('equipments', 'equipment')


'''POST ROUTE - CREATE '''

'''Route handler for a POST request at the root path ("/") of the app. When accessed, it retrieves the JSON payload from the request, creates a new video object in the database with the provided data, prints information about the created video object, converts it to a dictionary, and returns a JSON response containing the video's data and a success message'''

@equipment.route('/', methods=['POST'])
def create_equipment():
    payload = request.get_json() #retrieves the request as JSON format 
    new_equipment = models.Equipment.create(
        category = payload['category'],
        description = payload['description'],
        store = payload['store'],
        image = payload['image'],
    )
    equipment_dict = model_to_dict(new_equipment)#converts object to dictionary and assigns to equipment_dict variable 
    
    return jsonify(
        data=equipment_dict, 
        message= "equipment has been succesfully created", 
        status=201, 
    ), 201
  

'''GET ROUTE - INDEX all "equipments"'''

'''route handler for a GET request at the root path ("/") of the app. When accessed, it retrieves all the equipments from the database, converts them to dictionaries, prints them to the console, and returns a JSON response containing the equipments' data and a success message. If there are no equipments in the database, it returns an error response.'''

@equipment.route('/')
def get_all_equipments():
    try:                                                 #testing......where(models.equipment.host_name != current_user)
        equipments=[model_to_dict(equipment) for equipment in models.Equipment.select()] #.select() finds/retrieves all the equipments on our model. It iterates over the 
       #result and converts each equipment object to a dictionary and the result is stored in the 'equipments' variable as a list of dictionaries
        print(equipments)
        return jsonify(data=equipments, status={
            "code":200, 
            "message": f"Success! All equipments have been retrieved. Total equipments: {len(equipments)}"
        })
    except models.DoesNotExist: # #if there are no equipments in the database, it returns a JSON response with: 
        return jsonify(
            data={}, # an empty data object
            status={
                "code": 401, #an error mssg
                "message": "Error pulling the data"
            }
        )



'''SHOW ROUTE - show a specific "equipment"''' 

'''Route handler for a GET request at the '/<id>' route of the app. When accessed, it captures the id value from the URL, retrieves the corresponding equipment' object from the database, prints information about the retrieved equipment' object, converts it to a dictionary, and returns a JSON response containing the equipments's data, along with a success message and a status code of 200.'''


@equipment.route('/<id>', methods=['GET'])
def get_equipment(id): #accepts "id" as param
    print(id, "id") 
    equipment = models.Equipment.get_by_id(id) #fetches a 'equipment' object with the corresponding id from the database
    print(equipment.__dict__) #prints "equipment" dictionary
    return jsonify(
        data=model_to_dict(equipment), #converts "equipment" object to a dictionary
        status=200,
        message='Sucess'
    ), 200    



