from datetime import datetime
#User Models
class User(object):
    user_id = 0
    username = ''
    email = ''
    password = ''
    business = []
    reviews = []
    user_stamp_date = datetime.utcnow()
         
    def __init__(self,username,email, password,user_date_stamp,business,reviews):
        #initiliazing User class constructor
        self.username=username
        self.email = email
        self.password = password
        self.business = business
        self.reviews = reviews
        self.user_date_stamp = user_date_stamp
   
   
    def get_user_details(self):
        return {"username": self.username, "email": self.email,"password":self.password}
    
    @staticmethod
    def get_user(id):
        users = User.get_users()
        user = User(username='', email='')
        for u in users:
            if u.id == id:
                user = u
        return user

    @staticmethod
    def get_users():
        user1 = User(username='pooh', email='pooh@cats.com')
        user1.id=1
        user1. password='123456'
        user2 = User(username='bool', email='bool@cats.com')
        user2.id=2
        user2. password='123456'
        users = [user1, user2]
        return users


class Business(object):
     
    business_id = 0
    business_title =''
    business_description = ''
    category_id =''
    location_id=''
    email = ''
    business_date_stamp = datetime.utcnow()
    
    def __init__(self, business_id, business_title,business_description,category_id,email,business_date_stamp,location_id):
        #initiliazing business class constructor
        self.business_id= business_id
        self.business_title = business_title
        self.business_description= business_description
        self.category_id =category_id
        self.location_id =location_id
        self.email= email
        self.business_date_stamp = business_date_stamp
    
    @staticmethod
    def get_business(id):
        businesses = Business.get_businesses()
        business = Business(name='', description='', user_id=0,location_id='')
        for b in businesses:
            if b.id == id:
                business = b
        return business

    @staticmethod
    def get_business_details(business):
        return {'business_id': business.business_id, 'business_title':business.business_title, 'business_description': business.business_description, 'category_id':business.category_id, \
            'location_id ':business.location_id , 'email':business.email}

    
class Review(object):
    review_id=0
    review_description=''
    username=''
    business_id=0
    
    def __init__(self,username,review_id,review_description,business_id):
     #initiliazing business reviews constructor
     self.username=username
     self.review_id= review_id
     self.review_description= review_description
     self.business_id= business_id

    @staticmethod
    def get_review(review):
        return {'review_description':Review.review_description, 'review_id':Review.review_id, 'business_id':Review.business_id,'username':Review.username}
