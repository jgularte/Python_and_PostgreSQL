from psycopg2 import pool
from utility import constants


# todo: currently each class has its own file. Look into splitting this into two files
class Database:
    __connection_pool = None

    @staticmethod
    def initialize(**kwargs):
        Database.__connection_pool = pool.SimpleConnectionPool(constants.MIN_INIT_CONN,
                                                               constants.MAX_CONN_POOL,
                                                               **kwargs)

    @staticmethod
    def get_connection():
        return Database.__connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        Database.__connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database.__connection_pool.closeall()


class ConnectionFromPool:

    def __init__(self):
        self.connection = None
        self.cursor = None

    # called when the 'with' keyword is called on our object
    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    # called when exiting the 'with' keyword call
    # exception_type, exception_val, exception_traceback
    def __exit__(self, exc_type, exc_val, exc_tb):

        # if an error, rollback connection
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()

        # no matter what, put back connection
        Database.return_connection(self.connection)
