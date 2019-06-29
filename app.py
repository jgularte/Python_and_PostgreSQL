from user import User
from database import Database

database = Database()
database.initialize(user='postgres', password='francis24$', database='learning', host='localhost')

