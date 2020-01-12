class Configuration:
    def __init__(self, db_name=None, db_user=None, db_password=None, db_host=None, db_port=None):
        self.db_name = db_name or "dycast"
        self.db_user = db_user or "postgres"
        self.db_password = db_password or "postgres"
        self.db_host = db_host or "localhost"
        self.db_port = db_port or "5432"
        self.db_schema = "public"
