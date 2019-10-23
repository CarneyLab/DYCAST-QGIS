from qgis.core import QgsTask, QgsMessageLog, Qgis

# from settings_dialog import SettingsDialog
from dycast_qgis.models.configuration import Configuration
from dycast_qgis.services.database_service import DatabaseService
from dycast_qgis.services.logging_service import log_message, log_exception
MESSAGE_CATEGORY = 'Messages'


def read_config_from_form(settings_dialog) -> Configuration:
    config = Configuration()

    config.db_host = settings_dialog.dbHostLineEdit.text()
    config.db_port = settings_dialog.dbPortLineEdit.text()
    config.db_name = settings_dialog.dbNameLineEdit.text()
    config.db_user = settings_dialog.dbUserLineEdit.text()
    config.db_password = settings_dialog.dbPasswordLineEdit.text()

    return config


def check_can_connect_db(config: Configuration) -> bool:
    database_service = DatabaseService(config)
    return database_service.check_can_connect_db()


def run(task, config: Configuration) -> bool:

    can_connect = check_can_connect_db(config)
    return {'can_connect': can_connect}


def finished(exception, result=None):
    import ptvsd
    ptvsd.debug_this_thread()

    if result is not None:
        log_message("Succesfully tested database connection. Result: {result}".format(result=result['can_connect']), Qgis.Info)
    else:
        if exception:
            log_message("Failed to run the test_connection task", Qgis.Critical)
            log_exception(exception)
            raise exception

        log_message(
            "Failed to run the test_connection task. No exception was raised", Qgis.Warning)
