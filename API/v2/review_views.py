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
from models import Review,db


class Review_views():
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