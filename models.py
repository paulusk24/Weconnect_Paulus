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
         
    def __init__(self,username,email, password,business,reviews):
        #initiliazing User class constructor
        self.username=username
        self.email = email
        self.password = password
        self.business = business
        self.reviews = reviews
        
   
   
    def get_user_details(self):
        return {"username": self.username, "email": self.email,"password":self.password}
    
    @staticmethod
    def get_user(id):
        users = User.get_users()
        user = User(username='', email='',password='',business='',reviews='')
        for u in users:
            if u.id == id:
                user = u
        return user

    @staticmethod
    def get_users():
        user1 = User(username='pooh', email='pooh@cats.com',password='1234',business='Decorators',reviews='reviews_comments')
        user1.id=1
        user1. password='123456'
        user2 = User(username='bool', email='bool@cats.com',password='5432',business='confectionary',reviews='reviews_comments')
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
    
    def __init__(self, business_title,business_description,category_id,email,location_id):
        #initiliazing business class constructor
        self.business_title = business_title
        self.business_description= business_description
        self.category_id =category_id
        self.location_id =location_id
        self.email= email
            
    @staticmethod
    def get_business(id):
        businesses = Business.get_businesses()
        business = Business(business_title='', business_description='',location_id='',category_id='',email='')
        for b in businesses:
            if b.id == id:
                business = b
        return business

    @staticmethod
    def get_business_details(business):
        return {'business_id': business.business_id, 'business_title':business.business_title, 'business_description': business.business_description, 'category_id':business.category_id, \
            'location_id ':business.location_id , 'email':business.email}
    
    @staticmethod
    def get_businesses():
        business1 = Business(business_title='CakeAlbum', business_description='confectionary',location_id='Kololo',category_id='B',email='jk@gmail.com')
        business1.id=1
        businesses= [business1]
        return businesses

class Review(object):
    review_id=0
    review_description=''
    username=''
    business_id=0
    
    def __init__(self,username,review_description):
     #initiliazing business reviews constructor
     self.username=username  
     self.review_description= review_description
   
    @staticmethod
    def get_review(review):
        return {'review_description':Review.review_description, 'review_id':Review.review_id, 'business_id':Review.business_id,'username':Review.username}

    @staticmethod
    def get_reviews():
        review1 = Review(username='Peter',review_description='great!!')
        review2 = Review(username='Paul',review_description='Good staff!!')
        review1.id = 1
        review1.business_id = 1
        review2.id = 2
        review2.business_id = 2
        reviews = [ review1, review2 ]
        return reviews

