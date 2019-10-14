class Configuration:
    def __init__(self, db_name=None, db_user=None, db_password=None, db_host=None, db_port=None):
        self.db_name = db_name if db_name is not None else "dycast"
        self.db_user = db_user if db_user is not None else "postgres"
        self.db_password = db_password if db_password is not None else "postgres"
        self.db_host = db_host if db_user is not None else "localhost"
        self.db_port = db_port if db_port is not None else "5432"
