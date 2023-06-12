import models
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

#blueprints record operations to execute when registered on an app 
lesson = Blueprint('lessons', 'lesson')


'''POST ROUTE - CREATE '''

'''Route handler for a POST request at the root path ("/") of the app. When accessed, it retrieves the JSON payload from the request, creates a new lesson object in the database with the provided data, prints information about the created lesson object, converts it to a dictionary, and returns a JSON response containing the lesson's data and a success message'''

@lesson.route('/', methods=['POST'])
def create_lesson():
    payload = request.get_json() #retrieves the request as JSON format 
    new_lesson = models.Lesson.create(
        video = payload['video'],
        title = payload['title'],
    )
    lesson_dict = model_to_dict(new_lesson)#converts object to dictionary and assigns to lesson_dict variable 
    
    return jsonify(
        data=lesson_dict, 
        message= "lesson has been succesfully created", 
        status=201, 
    ), 201
  

'''GET ROUTE - INDEX all "lessons"'''

'''route handler for a GET request at the root path ("/") of the app. When accessed, it retrieves all the lessons from the database, converts them to dictionaries, prints them to the console, and returns a JSON response containing the lessons' data and a success message. If there are no lessons in the database, it returns an error response.'''

@lesson.route('/')
def get_all_lessons():
    try:                                                
        lessons=[model_to_dict(lesson) for lesson in models.Lesson.select()] #.select() finds/retrieves all the lessons on our model. It iterates over the 
       #result and converts each lesson object to a dictionary and the result is stored in the 'lessons' variable as a list of dictionaries
        print(lessons)
        return jsonify(data=lessons, status={
            "code":200, 
            "message": f"Success! All lessons have been retrieved. Total lessons: {len(lessons)}"
        })
    except models.DoesNotExist: # #if there are no lessons in the database, it returns a JSON response with: 
        return jsonify(
            data={}, # an empty data object
            status={
                "code": 401, #an error mssg
                "message": "Error pulling the data"
            }
        )



'''SHOW ROUTE - show a specific "lesson"''' 

'''Route handler for a GET request at the '/<id>' route of the app. When accessed, it captures the id value from the URL, retrieves the corresponding lesson' object from the database, prints information about the retrieved lesson' object, converts it to a dictionary, and returns a JSON response containing the lessons's data, along with a success message and a status code of 200.'''


@lesson.route('/<id>', methods=['GET'])
def get_lesson(id): #accepts "id" as param
    print(id, "id") 
    lesson = models.Lesson.get_by_id(id) #fetches a 'lesson' object with the corresponding id from the database
    print(lesson.__dict__) #prints "lesson" dictionary
    return jsonify(
        data=model_to_dict(lesson), #converts "lesson" object to a dictionary
        status=200,
        message='Sucess'
    ), 200    



