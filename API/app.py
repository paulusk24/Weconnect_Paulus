#import flask class from the flask module
from flask import (Flask,redirect,
                url_for,request,make_response,session,flash,jsonify)
from flask_sqlalchemy import SQLAlchemy
from functools import wraps


#create application object
app = Flask(__name__)
#set a secret key
app.config['SECRET_KEY'] = 'Johnny Depp'
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresl://postgres:c0m9k#tWxF@localhost/weconnect.db'

db = SQLAlchemy(app)

from API import views
from API import models

if __name__ == '__main__':
  app.run(debug=True)