import json
from baseTest import BaseTestCase

from API.models import User,Category,business
from API import  app
from API.models import db


class Create_business(BaseTestCase):
    #----------------------- CREATE_business ENDPOINT--------------------------------

    def test_post_at_create_business_endpoint(self):      
        #Testing the create_business end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post('/api/v1/businesses')
        assert response.status=="401 UNAUTHORIZED"
    
    def test_post_at_create_business_endpoint(self):      
        #Testing the create_business end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_business/1",
            headers = self.headers, 
            content_type='application/json',
            data=json.dumps(self.business)
               )
        self.assertIn(
            "business created!",
            str(response.data)
               )
        assert response.status=="201 CREATED"

    def test_post_at_create_business_endpoint_with_invalid_data(self):      
        #Testing the create_business end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_business/1",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.invalid_data)
            )
        self.assertIn(
            "Invalid Data Submitted",
            str(response.data)
            )
        assert response.status=="400 BAD REQUEST"

    def test_post_at_create_business_endpoint_with_poor_spelling(self):      
        #Testing the create_business end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post('/api/v1/businesses')
        assert response.status=="404 NOT FOUND"

    def test_get_at_create_endpoint_endpoint(self):
        #Testing the create_business end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.get('/api/v1/businesses')
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_put_at_create_business_endpoint(self):
        #Testing the create_business end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put('/api/v1/businesses')
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_delete_at_create_business_endpoint(self):
        #Testing the create_business end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete('/api/v1/businesses')
        assert response.status=="405 METHOD NOT ALLOWED"