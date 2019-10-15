import pickle
from dycast_qgis.models.configuration import Configuration

class ConfigurationService():
    def __init__(self, config_file_path=None):
        self.config_file_path = config_file_path or "dycast_qgis.config"

    def persist_config(self, config: Configuration):
        config_file = open(self.config_file_path, "wb")
        pickle.dump(config, config_file)
        config_file.close()

    def load_config(self):
        try:
            return pickle.load(open(self.config_file_path, "rb"))
        except EOFError:
            return Configuration()
        except TypeError:
            return Configuration()
