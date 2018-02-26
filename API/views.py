from flask import request,jsonify,make_response
from functools import wraps
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
import datetime
import jwt 
import re
import uuid

from API import app
from API.models import User,Business,Review
from API.models import db


#Method to assign token to function
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({
                "message" : "1.Token is missing!"
                }), 401
        try: 
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(email=data["email"]).first()
        except:
            return jsonify({
                "Status":"Fail",
                "message" : "2.Token is invalid!"
                }), 401

        return f(current_user, *args, **kwargs)
    return decorated


#Route for creating a user.This route takes the users details and assigns them a unique id 
@app.route("/api/auth/v1/register",methods=["POST"])
def create_user(current_user):
    
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
    
    #Checking for Special character in the name and email
    if  not re.match(
        "^[A-Za-z0-9_-]*$", 
        username) or  not re.match(
        "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", 
        email):
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure you have not input special characters"
        }),400

    #Checking if email already exists   
    email_already_exists = db.session.query(db.exists().where(User.email == email)).scalar()
    if email_already_exists:
        return jsonify({
            "Status":"Fail",
            "message":"This email has already been used to register"
            }),400
    #Checking to make sure no empty strings are sent
    if username == "" or email == "" or password== "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure you have input all your details"
            }),400
            
    hashed_password = generate_password_hash(password, method="sha256")
    new_user = User(
            username=username, 
            email=email, 
            password=hashed_password,
            user_date_stamp = str(datetime.datetime.now()),
            )
    #Saving new user
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "New user  has been created!"
        }),201

    #Route for retrieving a business
    @app.route('/api/v1/businesses/<businessId>',methods=["GET"])
    @token_required
    def get_a_business(current_user,business_id):
        business = Business.query.filter_by(business_id=business_id).first()
        
        if not business:
            return jsonify({'message':'No user found'})

        business_data = {}
        business_data['business_id'] = business.business_id
        business_data['username']=business.username
        business_data['review_description']=business.review_description
        business_data['review_id']=business.review_id
            
        return jsonify({"businesses" : business_data})

    #Route for retrieving all businesses
    @app.route('/api/api/v1/businesses',methods=["GET"])
    @token_required
    def get_all_businesses(current_user):
        businesses = Business.query.all()

        output = []

        for business in businesses:
            business_data = {}
            business_data['business_id'] = business.business_id
            business_data['username']=business.username
            business_data['review_description']=business.review_description
            business_data['review_id']=business.review_id
            output.append(business_data)

        return jsonify({"businesses" : output})

    #Route for removing a business
    @app.route('/api/v1/businesses/<businessId>',methods=["DELETE"]) 
    @token_required
    def delete_a_business(current_user,business_id):
        business = Business.query.filter_by(business_id=business_id).first()
        
        if not business:
            return jsonify({'message':'No user found'})

        #Deleting a user
        db.session.delete(new_user)
        db.session.commit()
        return jsonify({'message':'The user has been deleted'})

    #Route to login and generate token 
    @app.route('/api/auth/v1/login',methods=["POST","GET"])
    def login():
    #Obtain user details in Json Format
        auth = request.get_json()
        if not auth or not auth["username"] or not auth["password"]:
            return  make_response(
            "1.Could not verify"
            ),400

        #Check Database to see if username provided is there
        user = User.query.filter_by(username=auth["username"]).first()

        if not user:
            return make_response(
            "2.Could not verify because provided details are not for user"
            ),400
        #Check the provided password and if true provide token
        if check_password_hash(user.password, auth["password"]):
            token = jwt.encode({
               "email" : user.email, 
               "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
               app.config["SECRET_KEY"])
            return jsonify({"token" : token.decode("UTF-8")}),201
        return make_response("1.Could not verify" ),400


        @app.route('/api/auth/v1/logout')
        @login
        @token_required
        def logout():
              session.pop('logged_in', None)
              return jsonify({'message':'You were just logged out!'})


