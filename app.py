import pathlib
import requests
from flask import Flask, render_template,Response
from flask_opencv_streamer import streamer
import cv2
import mediapipe as mp
import numpy as np
app = Flask(__name__)

camera = cv2.VideoCapture(0 )
# @app.route('/', endpoint='index_endpoint')
# def index():
#     return render_template('index.html')


# @app.route('/login',endpoint='login_endpoint')
# def login():
#     return render_template("login.html")


def generate_frames():
    while True:
        success,frame=camera.read()
        if not success:
            break
        else:
            
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type:image/jpeg\r\n\r\n'+frame+b'\r\n')


@app.route('/',endpoint='workoutplanner_endpoint')
def workout_planner():
    name="Shubh Vora"
    photourl="www.gmail.com"
    email="shubhvora03@gmail.com"
    firstname="Shubh"
    return render_template('workout.html',name=name,photourl=photourl,email=email,firstname=firstname)

@app.route('/recipeai',endpoint='getkhana_endpoint')
def get_khana():
    print("got request")
    name="Shubh Vora"
    photourl="www.gmail.com"
    email="shubhvora03@gmail.com"
    firstname="Shubh"
    return render_template('getkhana.html',name=name,photourl=photourl,email=email,firstname=firstname)

@app.route('/monitoring',endpoint='monitoring_endpoint')
def stream_page():
    return render_template('video_stream.html')

@app.route('/video')
def video():

    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
