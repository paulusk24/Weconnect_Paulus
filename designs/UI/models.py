#User Models
class Users(object):
       
    def __init__(self,username,email, password,user_date_stamp):
        #initiliazing User class constructor
        self.username=username
        self.email = email
        self.password = password
        self.user_date_stamp = user_date_stamp

    

class Businesses(object):
    
    def __init__(self, business_id, business_title,business_description,category_id,email,business_date_stamp):
        #initiliazing business class constructor
        self.business_id= business_id
        self.business_title = business_title
        self.business_description= business_description
        self.category_id =category_id
        self.email= email
        self.business_date_stamp = business_date_stamp

class Reviews(object):

    def __init__(self,username,review_id,review_description,business_id):
     #initiliazing business reviews constructor
     self.username=username
     self.review_id= review_id
     self.review_description= review_description
     self.business_id= business_id
