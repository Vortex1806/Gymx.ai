import pathlib
import requests
from flask import Flask, render_template


app = Flask(__name__)

# @app.route('/', endpoint='index_endpoint')
# def index():
#     return render_template('index.html')


# @app.route('/login',endpoint='login_endpoint')
# def login():
#     return render_template("login.html")

@app.route('/',endpoint='workoutplanner_endpoint')
def workout_planner():
    name="Shubh Vora"
    photourl="www.gmail.com"
    email="shubhvora03@gmail.com"
    firstname="Shubh"
    return render_template('workout.html',name=name,photourl=photourl,email=email,firstname=firstname)



if __name__ == '__main__':
    app.run()
