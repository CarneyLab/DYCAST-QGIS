from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists

from dycast_qgis.models.configuration import Configuration


class DatabaseService():

    def __init__(self, config: Configuration):
        self.config = config

    def check_can_connect_db(self) -> bool:
        engine = self.db_connect("postgres")
        try:
            engine.connect()
            return True
        except OperationalError:
            return False
        finally:
            engine.dispose()

    def check_if_db_exists(self) -> bool:
        try:
            return database_exists(self.get_sqlalchemy_conn_string())
        except OperationalError:
            return False

    def db_connect(self, db_name=None):
        """
        Connect to database.
        Returns sqlalchemy engine instance
        """
        return create_engine(self.get_sqlalchemy_conn_string(db_name))

    def get_sqlalchemy_conn_string(self, db_name=None):
        return URL(drivername="postgresql",
                   host=self.config.db_host,
                   port=self.config.db_port,
                   username=self.config.db_user,
                   password=self.config.db_password,
                   database=db_name or self.config.db_name)
