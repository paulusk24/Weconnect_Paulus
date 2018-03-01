from flask import (Flask,render_template,redirect,
                url_for,request,make_response,session,jsonify,flash,g)
from functools import wraps
from validate_email import validate_email
import datetime
from app import app

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

    #Checking to see if the email is valid
    if  not validate_email(email):
        return jsonify({
            "Status":"Fail",
            "message":"Please input correct email"
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
#login requred decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for ('/api/auth/v1/login'))
    return wrap

#user logs in
@app.route('/api/auth/v1/login', methods=['GET', 'POST'])
def login():
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
@login_required
def logout():
    session.pop('logged_in', None)
    response = jsonify({'message':'Logged out'})
    response.status_code = 405


@app.route('/api/auth/v1/reset-password', methods=['GET', 'POST'])
def password_reset():
    if request.method == "GET":
        user = User.get_user(id(request.data.get('userId', 0)))
        response = jsonify(User.get_user_details(user))       
        response.status_code = 200
    elif request.method == "POST":
        user1 = User.get_user((request.data.get('userId', 0)))
        user = User.get_user_details(user1)
        user["password"] = str(request.data.get('password', user1.password))
        response = jsonify({'message':'Password Reset.'})       
        response.status_code = 200
    return response




@app.route('/api/v1/businesses/<int:business_id>', methods=['DELETE'])
def delete_business(business_id):
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
    review = Review(comment=str(request.data.get('review_description', '')))
    review.business_id = int(request.data.get('business_id', 0))
    review.user_id = int(request.data.get('userId', 0))
    response = jsonify(Review.get_review(review))       
    response.status_code = 200
    return response

@app.route('/api/v1/businesses/<int:business_id>/reviews', methods=['GET'])
def reviews(business_id):
    reviews = []
    reviews_list = Review.get_review()
    for review in reviews_list:
        if review.business_id == business_id:
            reviews.append(Review.get_review(review))
    response = jsonify(reviews)       
    response.status_code = 200
    return response


    
