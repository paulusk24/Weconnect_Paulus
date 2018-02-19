import json

from flask import (Flask,render_template,redirect,
                url_for,request,make_response)

app = Flask(__name__)

@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/home')
def home():
        return render_template('home.html')

@app.route('/register')
def register():
        return render_template('register.html')

@app.route('/business')
def business():
        return render_template('business.html')



if __name__ == '__main__':
  app.run(debug=True)