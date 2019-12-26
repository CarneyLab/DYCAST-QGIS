import sys
import os
import subprocess

from qgis.core import Qgis, QgsApplication
from qgis.PyQt.QtCore import Qt

from dycast_qgis.util.redirect_stdout import redirect_stdout
from dycast_qgis.models.configuration import Configuration
from dycast_qgis.services.database_service import DatabaseService
from dycast_qgis.services.logging_service import log_message, log_exception

def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def check_if_db_exists(config: Configuration) -> bool:
    database_service = DatabaseService(config)
    return database_service.check_if_db_exists()


def run(task, config: Configuration, force: bool):
    log_message("Started create_database task", Qgis.Info)

    if check_if_db_exists(config):
        log_message("Database already exists, skipping...", Qgis.Info)
    else:
        with redirect_stdout():
            log_message("Database does not exists yet, setting up...", Qgis.Info)

            from dycast_app.dycast import main as dycast_main

            command = ["setup_dycast", "--monte-carlo-file",
                       "Dengue_max_100_40000.csv"]

            if force:
                command.append("--force-db-init")

            log_message(f"Running command: {command}", Qgis.Info)
            dycast_main(command)

    return {"db_exists": check_if_db_exists(config)}


def finished(exception, result=None):
    if result:
        log_message("Succesfully finished the create_database task", Qgis.Success)
    else:
        log_message("Failed to run the create_database task", Qgis.Warning)
        log_message("You may need to manually remove the (partly created) database", Qgis.Warning)

        if exception:
            log_exception(exception)
        else:
            log_message("No exception was raised", Qgis.Warning)

        return {"db_exists": "Error"}
