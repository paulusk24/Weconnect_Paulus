import json
from baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Edit_Recipe(BaseTestCase):
        #----------------------- EDIT RECIPE ENDPOINT--------------------------------
    
    def test_post_at_edit_recipe_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/edit_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"
    
    def test_get_at_edit_recipe_endpoint_(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/edit_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_put_at_edit_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/edit_recipe/<recipe_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_put_at_edit_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_recipe/1",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.recipe)
            )
        response2 = self.client.put(
            "/edit_recipe/1",
            headers = self.headers, 
            content_type='application/json',
            data=json.dumps(self.recipe)
            )
        self.assertIn(
            "Recipe has been edited!",
            str(response2.data)
            )
        assert response.status=="201 CREATED"

    def test_put_at_edit_recipe_endpoint_with_invalid_data(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_recipe/1",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.recipe)
            )
        response2 = self.client.put(
            "/edit_recipe/1",
            headers = self.headers, 
            content_type='application/json',
            data=json.dumps(self.invalid_data)
            )
        self.assertIn(
            "Invalid Data Submitted",
            str(response2.data)
            )