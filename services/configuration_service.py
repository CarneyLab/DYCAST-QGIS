import os
import pickle

from dycast_qgis.models.configuration import Configuration
from dycast_qgis.services.logging_service import log_message


class ConfigurationService():
    def __init__(self, config_file_path=None):
        self.config_file_path = config_file_path or self._get_default_config_path()

    def _get_default_config_path(self):
        return os.path.join(self._get_root_directory(), "dycast_qgis.config")

    def _get_root_directory(self):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        return os.path.abspath(
            os.path.join(current_directory, ".."))

    def persist_config(self, config: Configuration):
        try:
            config_file = open(self.config_file_path, "wb")
            pickle.dump(config, config_file)
        finally:
            config_file.close()

    def load_config(self):
        config_file = None
        try:
            config_file = open(self.config_file_path, "rb")
            return pickle.load(config_file)
        except (FileNotFoundError, EOFError, TypeError):
            log_message("No configuration found on disk, initializing default settings...")
            return Configuration()
        finally:
            if (config_file):
                config_file.close()

    def export_environment_variables(self, config: Configuration):
        os.environ["DBHOST"] = config.db_host
        os.environ["DBPORT"] = config.db_port
        os.environ["DBNAME"] = config.db_name
        os.environ["DBUSER"] = config.db_user
        os.environ["DBPASSWORD"] = config.db_password
