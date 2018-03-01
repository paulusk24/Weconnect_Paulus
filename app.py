#from flask_api import FlaskAPI
from flask import jsonify
import json
#import flask class from the flask module
from flask import (Flask,render_template,redirect,
                url_for,request,make_response,session,flash)

from models import User,Business,Review
#import views

#create application object
app = Flask(__name__)
#set a secret key
app.secret_key = "Johnny Depp" 

#Route for registering a user.This route takes the users details and assigns them a unique id 
@app.route("/api/auth/v1/register",methods=["POST"])
def create_user():
    
    if not request.json:

        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400

    user_info = request.get_json()
    username =user_info.get("username")
    email =user_info.get("email")
    password =user_info.get("password")

    #Checking if all fields are filled.
    if   isinstance(username,int):
        return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have input String"
            }),400

    #Checking if all fields are filled.
    if  not (username and  email and  password):
            return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have input all the required fields"
            }),400
  
    #Checking to make sure no empty strings are sent
    if username == "" or email == "" or password== "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure you have input all your details"
            }),400
            
    return jsonify({
        "Status":"Success",
        "message" : "New user  has been created!"
        }),201


#user logs in
@app.route('/api/auth/v1/login', methods=['GET', 'POST'])
def login():
    response = jsonify({})
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
          error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True 
            flash('You were just logged in!')
            response = jsonify({'message':'Logged in'})
            response.status_code = 200
    return response

@app.route('/api/auth/v1/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    response = jsonify({'message':'Logged out'})
    response.status_code = 405


@app.route('/api/auth/v1/reset-password', methods=['POST'])
def password_reset():
    response = jsonify({})
    user1 = User.get_user((request.data.get('user_id', 0)))
    user = User.get_user_details(user1)
    user["password"] = str(request.data.get('password', user1.password))
    response = jsonify({'message':'Password Reset.'})       
    response.status_code = 200
    return response




@app.route('/api/v1/businesses/<int:business_id>', methods=['DELETE'])
def delete_business(business_id):
    response = jsonify({})
    businesses = Business.get_businesses()
    for bus in businesses:
        if bus.id == int(business_id):
            businesses.remove(bus)
    businesses_list = []
    for bus in businesses:
        businesses_list.append(Business.get_business_details(bus))
    response = jsonify(businesses_list)
    response.status_code = 200

    return response

@app.route('/api/v1/businesses/<int:business_id>', methods=['GET'])
def business_details(business_id):
    response = jsonify({})
    business = {}
    businesses_list = Business.get_businesses()
    for bus in businesses_list:
        if bus.id == int(business_id):
            business = Business.get_business_details(bus)
    response = jsonify(business) 
    response.status_code = 200
    return response

@app.route('/api/v1/businesses/<int:business_id>/reviews', methods=['POST'])
def review(business_id):
    response = jsonify({})
    review = Review(review_description=str(request.data.get('review_description', '')),username = int(request.data.get('username','')))
    response = jsonify(Review.get_review(review))       
    response.status_code = 200
    return response

@app.route('/api/v1/businesses/<int:business_id>/reviews', methods=['GET'])
def reviews(business_id):
    response = jsonify({})
    reviews = []
    reviews_list = Review.get_reviews()
    for review in reviews_list:
        if review.business_id == business_id:
            reviews.append(Review.get_review(review))
    response = jsonify(reviews)       
    response.status_code = 200
    return response


if __name__ == '__main__':
   app.run(debug=True)