from flask import request,jsonify,make_response
from functools import wraps
from validate_email import validate_email
import datetime
from app import app

#Route for registering a user.This route takes the users details and assigns them a unique id 
@app.route("/register",methods=["POST"])
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

    
