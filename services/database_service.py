from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists

from models.configuration import Configuration


class DatabaseService():

    def __init__(self, config: Configuration):
        self.config = config

    def check_can_connect_db(self) -> bool:
        engine = self.db_connect()
        try:
            engine.connect()
            return True
        except OperationalError:
            return False

    def check_if_db_exists(self) -> bool:
        return database_exists(self.get_sqlalchemy_conn_string())

    def db_connect(self):
        """
        Connect to database.
        Returns sqlalchemy engine instance
        """
        return create_engine(self.get_sqlalchemy_conn_string())

    def get_sqlalchemy_conn_string(self):
        return URL(drivername="postgres",
                   host=self.config.db_host,
                   port=self.config.db_port,
                   username=self.config.db_user,
                   password=self.config.db_password,
                   database=self.config.db_name)
