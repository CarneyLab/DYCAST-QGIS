import sys
import os
import subprocess

from qgis.core import Qgis, QgsApplication
from qgis.PyQt.QtCore import Qt

from dycast_qgis.models.configuration import Configuration
from dycast_qgis.services.database_service import DatabaseService
from dycast_qgis.services.layer_service import LayerService
from dycast_qgis.services.logging_service import log_message, log_exception


def run(task, layer_service: LayerService, config: Configuration, force: bool):
    log_message("Started initialize_layers task", Qgis.Info)
    existing_layers = layer_service.get_all_layers()

    if not existing_layers:
        try:
            layer_service.initialize_layers()
        except Exception as ex:
            log_exception(ex)
            raise
    else:
        log_message("Layers already initialized")
    return {"success": True}


def finished(exception, result=None):
    if result:
        log_message("Succesfully finished the initialize_layers task", Qgis.Success)
    else:
        log_message("Failed to run the initialize_layers task", Qgis.Warning)
        log_message("You may need to manually remove the (partly created) layers", Qgis.Warning)

        if exception:
            log_exception(exception)
        else:
            log_message("No exception was raised", Qgis.Warning)

        return {"success": False}
