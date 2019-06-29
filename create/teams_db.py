from database import ConnectionFromPool, Database
from utility import lists
from utility import db_login as db

Database.initialize(user=db.USER, password=db.PASSWORD, database=db.DATABASE, host=db.HOST)

for i in lists.NFL_TEAMS:
    with ConnectionFromPool() as cursor:
        print(i)