import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

#User blueprint 
user = Blueprint('users', 'user', url_prefix='/user')



'''REGISTER ROUTE'''

'''Route handler for a POST request at the '/register' route of the User model. When accessed, it retrieves the registration data from the request payload, checks if a user with the same email already exists. If the user doesn't exit, it creates a new user with the provided data, hashes the password, logs in the user, and returns a JSON response indicating the success of the registration process.'''

            #user/register
@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json() #This has all the data like username, email, password. Simiar to req.body
    
    payload['email'] = payload['email'].lower()
    try: 
        #check if the user already exist by querying by their email 
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={
            "code": 401, 
            "message": 'Try Again! A user with that email already exists'
        })
        
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) #hashes the password which replaces the plain-text password with its hashed representation 
        user = models.User.create(**payload) #creates a new user object in the database using the 'create' method. The '**payload" passes its contents as keyword arguments to the create method 
        
        login_user(user) #logs in the newly registered user. initiates the session
        user_dict = model_to_dict(user) #converts the 'user' object to a dictionary
        print(user_dict)
        print(type(user_dict))
        del user_dict['password'] #removes the password key from the 'user_dict' dictionary. Used as a security measure to prevent exposing the hashed password in the response
        
        
        #returns a JSON response 
        return jsonify(data=user_dict, status={
            "code": 201, 
            "message": 'Success, user successfully created '
        })
        
        