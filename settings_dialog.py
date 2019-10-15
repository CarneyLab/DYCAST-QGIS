import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.core import QgsMessageLog, Qgis

from dycast_qgis.services.configuration_service import ConfigurationService
from dycast_qgis.models.configuration import Configuration


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings_dialog.ui'))

MESSAGE_CATEGORY = 'Messages'


class SettingsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, config: Configuration, config_service: ConfigurationService, parent=None):
        """Constructor."""
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.initialize_fields(config)
        self.settingsDialogButtonBox.accepted.connect(lambda: self.on_save(config, config_service))
        self.settingsDialogButtonBox.rejected.connect(lambda: self.on_cancel(config))
        self.export_environment_variables(config)

    def on_cancel(self, config: Configuration):
        self.initialize_fields(config)

    def on_save(self, config: Configuration, config_service: ConfigurationService):
        previous_config = config
        try:
            config.db_host = self.dbHostLineEdit.text()
            config.db_port = self.dbPortLineEdit.text()
            config.db_name = self.dbNameLineEdit.text()
            config.db_user = self.dbUserLineEdit.text()
            config.db_password = self.dbPasswordLineEdit.text()

            self.export_environment_variables(config)
            config_service.persist_config(config)

        except Exception as e:
            QgsMessageLog.logMessage("Failed to save settings, rolling back to previous configuration. \
                Exception: {exception}".format(exception=e),
                                     MESSAGE_CATEGORY, Qgis.Critical)
            config = previous_config

    def initialize_fields(self, config: Configuration):
        self.dbHostLineEdit.setText(config.db_host)
        self.dbPortLineEdit.setText(config.db_port)
        self.dbNameLineEdit.setText(config.db_name)
        self.dbUserLineEdit.setText(config.db_user)
        self.dbPasswordLineEdit.setText(config.db_password)

    def export_environment_variables(self, config: Configuration):
        os.environ["DBHOST"] = config.db_host
        os.environ["DBPORT"] = config.db_port
        os.environ["DBNAME"] = config.db_name
        os.environ["DBUSER"] = config.db_user
        os.environ["DBPASSWORD"] = config.db_password
