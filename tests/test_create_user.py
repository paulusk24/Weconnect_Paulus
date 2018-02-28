import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Create_user(BaseTestCase):
    
    #-----------------------REGISTER ENDPOINT--------------------------------
    def test_get_at_register_endpoint(self):
        #Testing the register end point
        #If the method is an GET Method Should not be allowed
        
        result=self.client.get("/register")
        assert result.status =="405 METHOD NOT ALLOWED" #Change to 400
    
    def test_put_at_register_endpoint(self):
        #Testing the register end point
        #If the method is an PUT Method Should not be allowed
        result=self.client.put("/register")
        assert result.status =="405 METHOD NOT ALLOWED"

    def test_delete_at_register_endpoint(self):
        #Testing the register end point
        #If the method is an DELETE Method Should not be allowed
        result=self.client.delete("/register")
        assert result.status =="405 METHOD NOT ALLOWED"
        
    def test_post_at_register_endpoint(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        response = self.client.post("/register")
        assert response.status=="400 BAD REQUEST" 

    def test_post_with_user_info_at_register_user(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        #If Data posted through this method,it should allow and have a positve response
        #Should also give New user  has been created! message
        self.user={
            "username":"Jonas",
            "email":"jonas123@gmail.com",
            "password":"*****"
            }
        response = self.client.post(
            "/register",
            data=json.dumps(self.user),
            headers={"Content-Type":"application/json"}
            )
        self.assertIn(
            "New user  has been created!",
            str(response.data)
            )
        assert response.status=="201 CREATED"
    
    def test_post_with_invalid_data_at_register_user(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        #If Data posted through this method,it should allow and have a positce response
        response = self.client.post(
            "/register",
            data=json.dumps(self.invalid_data),
            headers={"Content-Type":"application/json"}
            )
        self.assertIn(
            "Invalid Data Submitted",
            str(response.data)
            )
        assert response.status=="400 BAD REQUEST"

    def test_post_register_endpoint_with_poor_spelling(self):
        #Testing the register end point if method is get but endpoint spelt poorly
        self.user={
            "username":"Jonas",
            "email":"jonas123@gmail.com",
            "password":"*****"
            }
        response = self.client.post(
            "/registar",
            data=json.dumps(self.user),
            headers={"Content-Type":"application/json"}
            )
        assert response.status=="404 NOT FOUND"