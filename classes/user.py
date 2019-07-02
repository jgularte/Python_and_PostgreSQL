import oauth2
import json
from classes.database import ConnectionFromPool
from utility.oauth import consumer


class User:

    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User: {0}>".format(self.email)

    def save_to_db(self):
        # get connection from  connection_pool

        with ConnectionFromPool() as cursor:
            # build code to execute
            cursor.execute('insert into users (email, first_name, last_name, oauth_token, oauth_token_secret)'
                           ' values (%s, %s, %s, %s, %s)', (self.email, self.first_name, self.last_name,
                                                            self.oauth_token, self.oauth_token_secret))

    def twitter_request(self, uri, verb='GET'):
        # Use valid oauth tokens to make query
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        response, content = authorized_client.request(uri, verb)
        return json.loads(content.decode('utf-8'))

    @classmethod
    def load_db_email(cls, email: str):
        with ConnectionFromPool() as cursor:
            # make sure second arg is a tuple by adding a 'unnecessary' comma
            cursor.execute('select * from users where email=%s', (email,))
            user_data = cursor.fetchone()

            if user_data:
                return cls(email=user_data[1], first_name=user_data[2], last_name=user_data[3],
                           oauth_token=user_data[4], oauth_token_secret=user_data[5], id=user_data[0])
