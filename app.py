#from flask_api import FlaskAPI
from flask import jsonify
import json
#import flask class from the flask module
from flask import (Flask,render_template,redirect,
                url_for,request,make_response,session,flash,g)

from models import User,Business,Review
import views

#create application object
app = Flask(__name__)
#set a secret key
app.secret_key = "Johnny Depp" 

if __name__ == '__main__':
   app.run(debug=True)