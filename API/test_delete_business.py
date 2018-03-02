import json
from baseTest import BaseTestCase

from models import User,Business,Review
import  app
from models import db


class Delete_business(BaseTestCase):
        #----------------------- DELETE business ENDPOINT--------------------------------
    
    def test_post_at_delete_business_endpoint(self): 
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post('/api/v1/businesses/<business_id>')
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_delete_business_endpoint_(self):
        #If the method is a get , Method Should not be allowed 
        response = self.client.get('/api/v1/businesses/<business_id>')
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_put_at_delete_business_endpoint(self):
        #If the method is a put , Method Should not be allowed 
        response = self.client.put('/api/v1/businesses/<business_id>')
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_delete_at_delete_business_endpoint(self):
        #If the method is a delete , Method Should  be allowed and receive a unauthorised status code
        response = self.client.delete('/api/v1/businesses/<business_id>')
        assert response.status=="401 UNAUTHORIZED"

    def test_delete_at_delete_business_endpoint(self):
        #If the method is a delete , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_business/1",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.business)
            )

        response = self.client.delete(
            "/delete_business/1",
            headers = self.headers,
            content_type='application/json',
            data=json.dumps(self.business)
            )
        assert response.status=="200 OK"

    def test_delete_at_delete_business_endpoint_with_poor_spelling(self):
        #If the method is a delete , Method Should not be allowed 
        response = self.client.delete('/api/v1/businesses/<business_id>')
        assert response.status=="404 NOT FOUND"