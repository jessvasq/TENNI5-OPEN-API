import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict
from datetime import datetime, timedelta

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
        

'''LOGIN ROUTE'''  
'''Route handler for a POST request at the '/login' route of the User model. When accessed, it retrieves the login data from the request payload, checks if a user with the provided email exists, checks the password, logs in the user if the credentials are correct, and returns a JSON response indicating the success or failure of the login process.'''


@user.route('/login', methods=["POST"])
def login():
    #retrieve the json from the route
    payload = request.get_json()

    #check if all required fields are present in the payload
    if 'email' not in payload or 'password' not in payload:
        return jsonify(data={}, status={"code": 400, "message": "Missing email or password in request"})

    #Query to search by email 
    try: 
        user = models.User.get(models.User.email == payload['email']) 
        user_dict = model_to_dict(user) #user found --> convert the user models to a dictionary 
        
        #use bcrypt to check if the input password matches the pw stored in the database. Returns True or False depending on whther our hash's match
        if(check_password_hash(user_dict['password'], payload['password'])):
            #starts the session and securely log in the user
            login_user(user) 
            #remove any sensitive data from the user dictionary 
            del user_dict['password'] #deletes the pw
      
            return jsonify(data=user_dict, 
                           status={
                               "code":200,
                               "message": "You have successfully logged in!"
                               })
        else: 
            return jsonify(data={}, status={"code": 401, "message":"Try again! Username or password is incorrect" })
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username does not exist. Please create an account"})


'''LOGOUT ROUTE'''
@user.route('/logout')
#login_required decorator, requires users to be logged in to access a certain route
@login_required
def logout():
    logout_user()
    return jsonify(
        data={}, 
        status=200, 
        message='Successful logout'
    ), 200
