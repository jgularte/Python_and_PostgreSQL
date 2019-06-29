from database import ConnectionFromPool


class User:

    def __init__(self, email, first_name, last_name, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

    def __repr__(self):
        return "<User: {0}>".format(self.email)

    def save_to_db(self):
        # get connection from  connection_pool

        with ConnectionFromPool() as cursor:
            # build code to execute
            cursor.execute('insert into users (email, first_name, last_name) values (%s, %s, %s)',
                           (self.email, self.first_name, self.last_name))

    @classmethod
    def load_db_email(cls, email):
        with ConnectionFromPool() as cursor:
            # make sure second arg is a tuple by adding second comma
            cursor.execute('select * from users where email=%s', (email,))
            user_data = cursor.fetchone()

            return cls(email=user_data[1], first_name=user_data[2],
                       last_name=user_data[3], id=user_data[0])
