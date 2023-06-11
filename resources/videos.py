import models
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

#blueprints record operations to execute when registered on an app 
video = Blueprint('videos', 'video')


'''POST ROUTE - CREATE '''

'''Route handler for a POST request at the root path ("/") of the app. When accessed, it retrieves the JSON payload from the request, creates a new video object in the database with the provided data, prints information about the created video object, converts it to a dictionary, and returns a JSON response containing the video's data and a success message'''

@video.route('/', methods=['POST'])
def create_video():
    payload = request.get_json() #retrieves the request as JSON format 
    new_video = models.Video.create(
        video = payload['video'],
        description = payload['description'],
        title = payload['title'],
    )
    video_dict = model_to_dict(new_video)#converts object to dictionary and assigns to video_dict variable 
    
    return jsonify(
        data=video_dict, 
        message= "video has been succesfully created", 
        status=201, 
    ), 201
  

'''GET ROUTE - INDEX all "videos"'''

'''route handler for a GET request at the root path ("/") of the app. When accessed, it retrieves all the videos from the database, converts them to dictionaries, prints them to the console, and returns a JSON response containing the videos' data and a success message. If there are no videos in the database, it returns an error response.'''

@video.route('/')
def get_all_videos():
    try:                                                 #testing......where(models.video.host_name != current_user)
        videos=[model_to_dict(video) for video in models.Video.select()] #.select() finds/retrieves all the videos on our model. It iterates over the 
       #result and converts each video object to a dictionary and the result is stored in the 'videos' variable as a list of dictionaries
        print(videos)
        return jsonify(data=videos, status={
            "code":200, 
            "message": f"Success! All videos have been retrieved. Total videos: {len(videos)}"
        })
    except models.DoesNotExist: # #if there are no videos in the database, it returns a JSON response with: 
        return jsonify(
            data={}, # an empty data object
            status={
                "code": 401, #an error mssg
                "message": "Error pulling the data"
            }
        )



'''SHOW ROUTE - show a specific "video"''' 

'''Route handler for a GET request at the '/<id>' route of the app. When accessed, it captures the id value from the URL, retrieves the corresponding video' object from the database, prints information about the retrieved video' object, converts it to a dictionary, and returns a JSON response containing the videos's data, along with a success message and a status code of 200.'''


@video.route('/<id>', methods=['GET'])
def get_video(id): #accepts "id" as param
    print(id, "id") 
    video = models.Video.get_by_id(id) #fetches a 'video' object with the corresponding id from the database
    print(video.__dict__) #prints "video" dictionary
    return jsonify(
        data=model_to_dict(video), #converts "video" object to a dictionary
        status=200,
        message='Sucess'
    ), 200    



