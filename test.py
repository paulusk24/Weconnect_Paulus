from  app import  app
import unittest

class FlaskTestCase(unittest.TestCase):

  
    #Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/api/auth/v1/login',content_type='jsonify')
        self.assertEqual(response.status_code, 500)
    
    #Ensure that login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/api/auth/v1/login',content_type='jsonify')
        self.assertEqual(response.status_code, 500)

    #Ensure login behaves correctly given the correct credentials
    def test_corect_login(self):
        tester = app.test_client(self)
        response = tester.post('/api/auth/v1/login',content_type='jsonify')
        self.assertEqual(response.status_code, 400)

#Ensure login behaves correctly given the incorrect credentials
def test_incorect_login(self):
        tester = app.test_client(self)
        response = tester.post('/api/auth/v1/login',content_type='jsonify')
        self.Equal(response.status_code, 405)

#Ensure logout behaves correctly and is not accessible with a GET Request
def test_logout(self):
        tester = app.test_client(self)
        tester.post('/api/auth/v1/login',content_type='jsonify')
        response = tester.get('/api/auth/v1/logout')
        self.Equal(response.status_code, 405)


#Test register_user is accessible without login
def test_register_user_endpoint(self):
        tester = app.test_client(self)
        response = tester.get('/api/auth/v1/register')
        self.assertEqual(response.status_code, 200)

#Test password reset endpoint is accessible without login
def test_password_reset_endpoint(self):
        response = self.client().get('/api/v1/auth/reset-password')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

