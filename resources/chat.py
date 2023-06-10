import models
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required

#blueprints record operations to execute when registered on an app 
chat = Blueprint('chats', 'chat')


'''GET ROUTE -- retrieves mssgs'''
'''Selects and retrieves all messages where the conversation_id matches the specific convo'''
@chat.route('/<conversation_id>', methods=['GET'])
def get_mssg(conversation_id): 
    try:                                                 
        messages=[model_to_dict(chat) for chat in models.Message.select().where((models.Message.conversation == conversation_id))]
       #Selects all 'Message' objects from the 'Message' models where the 'converstation' matches the provided 'conversation_id' parameter
        print(messages)
        return jsonify(data=messages, status={ #converts list of dictionaries into a JSON response 
            "code":200, 
            "message": f"Success! All messages have been retrieved. Total matches: {len(messages)}"
        })
    except models.DoesNotExist: # #if there are no matches in the database, it returns a JSON response with: 
        return jsonify(
            data={}, # an empty data object
            status={
                "code": 401, #an error mssg
                "message": "Error pulling the data"
            }
        )

'''POST ROUTE - CREATES A NEW MESSGE'''

@chat.route('/newmessage', methods=['POST'])
def create_mssg(): 
    payload = request.get_json()
    new_convo = models.Conversation.create(
        name = payload['name']
    )
    convo_dict = model_to_dict(new_convo)
    return jsonify(
            data=convo_dict, 
            message= "New conversation succesfully created", 
            status=201, 
        ), 201
    


'''POST ROUTE - SENDS A MSSG'''

@chat.route('/', methods=['POST'])
def send_mssg():
    payload = request.get_json() #retrieves the request as JSON format, data should be sent as JSON so we can parses to the payload variable 
    new_msgg = models.Message.create(
        conversation=payload['conversation'], #assign values to the fields below to then create a new model 
        user=current_user.id,
        message=payload['message']
        )
    mssg_dict = model_to_dict(new_msgg)#converts object to dictionary and assigns to match_dict variable 
    
    return jsonify(
        data=mssg_dict, 
        message= "Message sent succesfully created", 
        status=201, 
    ), 201
  
  
