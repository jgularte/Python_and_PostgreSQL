import oauth2
import json
from classes.database import ConnectionFromPool
from utility.oauth import consumer


class UserScreenName:

    @classmethod
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id=None):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    @classmethod
    def __repr__(self):
        return "<User: {0}>".format(self.screen_name)

    @classmethod
    def save_to_db(self):
        # get connection from  connection_pool

        with ConnectionFromPool() as cursor:
            # build code to execute
            cursor.execute('insert into public.screen_name (screen_name, oauth_token, oauth_token_secret)'
                           ' values (%s, %s, %s)', (self.screen_name, self.oauth_token, self.oauth_token_secret))

    @classmethod
    def twitter_request(self, uri, verb='GET'):
        # Use valid oauth tokens to make query
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        response, content = authorized_client.request(uri, verb)
        return json.loads(content.decode('utf-8'))

    @classmethod
    def load_db_screen_name(cls, screen_name: str):
        with ConnectionFromPool() as cursor:
            # make sure second arg is a tuple by adding a 'unnecessary' comma
            cursor.execute('select * from public.screen_name where screen_name=%s', (screen_name,))
            user_data = cursor.fetchone()

            if user_data:
                return cls(screen_name=user_data[1], oauth_token=user_data[2],
                           oauth_token_secret=user_data[3], id=user_data[0])
