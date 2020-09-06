import os
import pickle

from dycast_qgis.models.configuration import Configuration
from dycast_qgis.models.risk_generation_parameters import RiskGenerationParameters
from dycast_qgis.services.logging_service import log_message


class ConfigurationService():
    def __init__(self, config_file_path=None):
        self.config_file_path = config_file_path or self._get_default_config_path()

    def _get_default_config_path(self):
        return self._get_absolute_path("dycast_qgis.config")

    def _get_risk_generation_parameters_path(self):
        return self._get_absolute_path("risk_generation_parameters.config")

    def _get_absolute_path(self, relative_path: str):
        return os.path.join(self._get_root_directory(), relative_path)

    def _get_root_directory(self):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        return os.path.abspath(
            os.path.join(current_directory, ".."))

    def persist_config(self, config: Configuration):
        return self._persist_instance_to_file(config, self.config_file_path)

    def persist_risk_generation_parameters(self, risk_generation_parameters: RiskGenerationParameters):
        return self._persist_instance_to_file(risk_generation_parameters, self._get_risk_generation_parameters_path())

    def _persist_instance_to_file(self, instance, file_path: str):
        try:
            file = open(file_path, "wb")
            pickle.dump(instance, file)
        finally:
            if (file):
                file.close()

    def load_config(self):
        file_type = "configuration"
        empty_instance = Configuration()
        return self._try_load_file(file_type, self.config_file_path, empty_instance)

    def load_risk_generation_parameters(self):
        file_type = "risk generation parameters"
        empty_instance = RiskGenerationParameters()
        return self._try_load_file(file_type, self._get_risk_generation_parameters_path(), empty_instance)

    def _try_load_file(self, file_type: str, file_path: str, empty_instance):
        try:
            return self._load_file(file_path)
        except (FileNotFoundError, EOFError, TypeError):
            log_message("No {file_type} found on disk, initializing default settings...".format(file_type=file_type))
            return empty_instance

    def _load_file(self, file_path):
        file = None
        try:
            file = open(file_path, "rb")
            return pickle.load(file)
        finally:
            if (file):
                file.close()

    def export_environment_variables(self, config: Configuration):
        os.environ["DBHOST"] = config.db_host
        os.environ["DBPORT"] = config.db_port
        os.environ["DBNAME"] = config.db_name
        os.environ["DBUSER"] = config.db_user
        os.environ["DBPASSWORD"] = config.db_password
