from flask import request,jsonify,make_response
from functools import wraps
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
import datetime
import jwt 
import re
import uuid

import app
from models import Business,db


class Business_views():
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
    @token_needed
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
