from qgis.core import Qgis

from dycast_qgis.models.configuration import Configuration
from dycast_qgis.services.database_service import DatabaseService
from dycast_qgis.services.logging_service import log_message, log_exception


def run_db_checks(config: Configuration):
    database_service = DatabaseService(config)
    can_connect = check_can_connect_db(database_service)
    db_exists = check_db_exists(database_service)

    return {'can_connect': can_connect, 'db_exists': db_exists}


def check_can_connect_db(database_service: DatabaseService) -> bool:
    return database_service.check_can_connect_db()


def check_db_exists(database_service: DatabaseService) -> bool:
    return database_service.check_if_db_exists()


def run(task, config: Configuration) -> bool:
    return run_db_checks(config)


def finished(exception, result=None):
    if result is not None:
        log_message("Succesfully tested database connection. Result: {result}".format(result=result['can_connect']), Qgis.Info)
    else:
        if exception:
            log_message("Failed to run the test_connection task", Qgis.Critical)
            log_exception(exception)
            raise exception

        log_message(
            "Failed to run the test_connection task. No exception was raised", Qgis.Warning)
