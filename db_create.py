from app import db
from models import User

#create the database and the db tables
db.create_all()

#insert 
db.session.add(User("Peter", "peteroo@gmail.com","bcdefg","1.2.1994"))
db.session.add(User("Penina", "penina@gmail.com","123456","1.12.1994"))
#commit the changes
db.session.commit()