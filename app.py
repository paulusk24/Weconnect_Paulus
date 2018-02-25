import json
#import flask class from the flask module
from flask import (Flask,render_template,redirect,
                url_for,request,make_response,session,flash,g)
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

#create application object
app = Flask(__name__)
#set a secret key
app.config['SECRET_KEY'] = 'Johnny Depp'
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresl://postgres:c0m9k#tWxF@localhost/weconnect.db'

#create SQLAlchemy object
db = SQLAlchemy(app)

from models import User

#login requred decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for ('login'))
    return wrap

@app.route('/api/auth/v1/login',methods=['GET', 'POST'])

def login():
  error = None
  if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
          error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True 
            flash('You were just logged in!')
            return redirect(url_for('home'))
  return render_template('login.html',error=error)

#use decorators t link the function to the url
@app.route('/api/v1/home')
@login_required
def home():
     #return "WE, CONNECT" #return a string
    clients= db.session.query(User).all()
    return render_template('home.html',clients=clients)

#user creates an account
@app.route('/api/auth/v1/register')
def register():
        return render_template('register.html')

@app.route('/api/v1/businesses')
@login_required
def business():
        return render_template('business.html')

@app.route('/api/auth/v1/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('login'))



if __name__ == '__main__':
  app.run(debug=True)