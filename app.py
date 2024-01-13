import pathlib
import requests
from flask import Flask, render_template


app = Flask("Code Ai app")

@app.route('/', endpoint='index_endpoint')
def index():
    return render_template('index.html')


# @app.route('/login',endpoint='login_endpoint')
# def login():
#     return render_template("login.html")






if __name__ == '__main__':
    app.run()
