import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.core import QgsMessageLog, Qgis

from dycast_qgis.services.configuration_service import ConfigurationService
from dycast_qgis.services.database_service import DatabaseService
from dycast_qgis.models.configuration import Configuration


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings_dialog.ui'))

MESSAGE_CATEGORY = 'Messages'


class SettingsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, config: Configuration, config_service: ConfigurationService, database_service: DatabaseService, parent=None):
        """Constructor."""
        super(SettingsDialog, self).__init__(parent)
        self.config = config
        self.configuration_service = config_service
        self.database_service = database_service

        self.setupUi(self)
        self.initialize_fields()

        self.settingsDialogButtonBox.accepted.connect(self.on_save)
        self.settingsDialogButtonBox.rejected.connect(self.on_cancel)
        self.testConnectionPushButton.clicked.connect(self.on_test_connection)

        self.export_environment_variables(config)

    def on_cancel(self):
        self.initialize_fields()

    def on_save(self):
        config_from_form = self.read_config_from_form()
        self.export_environment_variables(config_from_form)
        try:
            self.config_service.persist_config(config_from_form)
            self.config = config_from_form
        except Exception as e:
            QgsMessageLog.logMessage("Failed to save settings, rolling back to previous configuration. \
                Exception: {exception}".format(exception=e),
                                     MESSAGE_CATEGORY, Qgis.Critical)
            self.export_environment_variables(self.config)

    def read_config_from_form(self) -> Configuration:
        config = Configuration()

        config.db_host = self.dbHostLineEdit.text()
        config.db_port = self.dbPortLineEdit.text()
        config.db_name = self.dbNameLineEdit.text()
        config.db_user = self.dbUserLineEdit.text()
        config.db_password = self.dbPasswordLineEdit.text()

        return config

    def initialize_fields(self):
        self.dbHostLineEdit.setText(self.config.db_host)
        self.dbPortLineEdit.setText(self.config.db_port)
        self.dbNameLineEdit.setText(self.config.db_name)
        self.dbUserLineEdit.setText(self.config.db_user)
        self.dbPasswordLineEdit.setText(self.config.db_password)

    def on_test_connection(self):
        self.databaseServerStatusLabel.setText("Testing...")
        config = self.read_config_from_form()
        can_connect = self.can_connect(config)
        self.databaseServerStatusLabel.setText(str(can_connect))

    def can_connect(self, config: Configuration):
        database_service = DatabaseService(config)
        return database_service.check_can_connect_db()

    def export_environment_variables(self, config: Configuration):
        os.environ["DBHOST"] = config.db_host
        os.environ["DBPORT"] = config.db_port
        os.environ["DBNAME"] = config.db_name
        os.environ["DBUSER"] = config.db_user
        os.environ["DBPASSWORD"] = config.db_password
