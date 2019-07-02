from classes.user import User
from classes.database import Database
from utility import oauth

# Initialize the database and set up the consumer object.
Database.initialize(user='postgres', password='francis24$', database='learning', host='localhost')

# check for a user in the database
email = input('Email: ')
user = User.load_db_email(email)

# if not found, authenticate and create user
if not user:

    # oauth verification process
    request_token = oauth.get_request_token()
    oauth_verifier = oauth.get_oauth_verifier(request_token)
    access_token = oauth.get_access_token(request_token, oauth_verifier)

    # create a new user and save them to the database
    user = User(email, input('first_name: '), input('last_name: '),
                access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

# Use user info to make a GET request to the twitter API
text = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')
for tweet in text['statuses']:
    print(tweet['text'])
