from qgis.core import QgsTask, QgsMessageLog, Qgis

# from settings_dialog import SettingsDialog
from dycast_qgis.models.configuration import Configuration
from dycast_qgis.services.database_service import DatabaseService

MESSAGE_CATEGORY = 'Messages'


class TestConnectionTask(QgsTask):

    def __init__(self, settings_dialog):
        super().__init__("TestConnection")
        self.settings_dialog = settings_dialog
        self.can_connect = False
        self.exception = None

    def read_config_from_form(self) -> Configuration:
        config = Configuration()

        config.db_host = self.settings_dialog.dbHostLineEdit.text()
        config.db_port = self.settings_dialog.dbPortLineEdit.text()
        config.db_name = self.settings_dialog.dbNameLineEdit.text()
        config.db_user = self.settings_dialog.dbUserLineEdit.text()
        config.db_password = self.settings_dialog.dbPasswordLineEdit.text()

        return config

    def check_can_connect_db(self, config: Configuration) -> bool:
        database_service = DatabaseService(config)
        return database_service.check_can_connect_db()

    def run(self):
        import ptvsd
        ptvsd.debug_this_thread()
        self.settings_dialog.databaseServerStatusLabel.setText("Testing...")

        try:
            config = self.read_config_from_form()
            self.can_connect = self.check_can_connect_db(config)
            return True
        except Exception as e:
            self.exception = e
            return False

    def finished(self, result):
        if result:
            self.settings_dialog.databaseServerStatusLabel.setText(
                str(self.can_connect))
        else:
            self.settings_dialog.databaseServerStatusLabel.setText("False")

            if self.exception is None:
                QgsMessageLog.logMessage(
                    'Task "{name}" not successful but without exception'.format(
                        name=self.description()),
                    MESSAGE_CATEGORY, Qgis.Warning)
            else:
                QgsMessageLog.logMessage(
                    'Task "{name}" Exception: {exception}'.format(
                        name=self.description(),
                        exception=self.exception),
                    MESSAGE_CATEGORY, Qgis.Critical)
                raise self.exception
