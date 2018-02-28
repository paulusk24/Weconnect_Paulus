from flask import request,jsonify,make_response
from functools import wraps
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
import datetime
import jwt 
import re
import uuid

from app import app
from models import User,Business,Review
from models import db

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

#Route to login and generate token 
@app.route('/api/auth/v1/login',methods=["POST"])
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


#Route for password reset
@app.route('/api/auth/v1/reset-password',methods=["POST"])
@token_required
def password_reset(current_user):
    login_user = request.get_json(force=True)
    username = login_user['username']
    password = login_user['password']

    new_pass = user_obj.password_reset(username, password)
    if new_pass == "Password reset successfully":
        return jsonify(response=new_pass), 201
    else:
        return jsonify(response=new_pass),400
    return jsonify(new_pass)

#Route to logout     
@app.route('/api/v1/auth/logout', methods=['POST'])
@token_required
def logout():
    response = jsonify({})
    result = auth_check()
    if isinstance(result, str):
        response = jsonify({'message': result})
        response.status_code = 401
    else:
        User.logout(result)
        response = jsonify({'message':'You are now logged out.'})      
        response.status_code = 200
    return response

    #Route for creating a business
@app.route('/api/v1/businesses',methods=["POST"])
@token_required
def create_business(current_user):
    #checking if its a json object
    if not request.json:
        return jsonify({
        "Status":"Fail",
        "message ":"Invalid Data Submitted"
        }),400
    #Obtaining data 
    data = request.get_json()
    business_title =data.get("business_title")
    business_description=data.get("business_description")
    category_id=data.get("category_id")
    location_id=data.get("location_id")
    #Checking to see if all fields are filled
    if  not (business and business_description):
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure you have all fields"
                }),400

    #Checking to make sure there is no empty string
    if  business_title == "" or business_description == "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input a business_title and business_description "
            }),400

    new_business = Business(
        business_id=str(uuid.uuid4()),
        business_title = data["business_title"],
        category_id=data["category_id"],
        business_description = data["business_description"],
        email=current_user.email,
        business_date_stamp = str(datetime.datetime.now()),
        location_id=data["location_id"]
        )   

    db.session.add(new_business)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "business created!"
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
    business_data['category_id']=business.category_id
    business_data['location_id']=business.location_id

        
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
        business_data['category_id']=business.category_id
        business_data['location_id']=business.location_id
        output.append(business_data)

    return jsonify({"businesses" : output})

#Endpoint to edit business using a specific id
@app.route("/edit_business/<business_id>", methods=["PUT"])
@token_required
def edit_business(current_user, business_id):
    #Checking to see if its a business and is in the database
    business = business.query.filter_by(business_id=business_id, email=current_user.email).first()

    if not  business:
        return jsonify({
            "Status":"Fail",
            "message" : "No business found!"
            }),404
    #Checking if its a json object
    if not request.json:
        return jsonify({
        "Status":"Fail",
        "message ":"Invalid Data Submitted"
        }),400
    #Obtaining data from user    
    data = request.get_json()
    business_title = data.get("business_title")
    business_description = data.get("business_description")

    #Checking to see if all fields are filled.
    if not (business_title and business_description):
        return jsonify({
        "Status":"Fail",
        "message" : "Please ensure all fields are filled!"
        }),400

    business.business_title =business_title
    business.business_description=business_description
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "business has been edited!"
        }),201

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


@app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['POST'])
def review(businessId):
    result = auth_check()
    if isinstance(result, str):
        response = jsonify({'message': result})
        response.status_code = 401
    else:
        business = Business.get_business(int(businessId))
        user = User.get_user(int(request.data['userId']))
        if business:
            review = Review(comment=str(request.data['comment']), business=business, user=user)
            review.create()
            response = jsonify(Review.get_review_details(review))      
            response.status_code = 201
        else:
            response = jsonify({'message': 'Specified business not found.'})
            response.status_code = 404
    return response

@app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['GET'])
def reviews(businessId):
    response = jsonify({'message': 'Business not found.'})
    response.status_code = 404
    business = Business.get_business(businessId)
    if business:
        reviews = business.reviews
        if len(reviews) > 0:
            reviews = [Review.get_review_details(r) for r in reviews]
            response = jsonify(reviews)      
            response.status_code = 200
        else:
            response = {'message': 'No reviews to show.'}
            response.status_code = 404
    return response

