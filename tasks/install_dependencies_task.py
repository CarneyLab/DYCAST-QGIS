import sys
import os
import subprocess

from qgis.core import Qgis, QgsApplication
from qgis.PyQt.QtCore import Qt

from dycast_qgis.services.dependency_service import DependencyService
from dycast_qgis.services.logging_service import log_message, log_exception


def run(task):
    log_message("Started install_dependencies task", Qgis.Info)

    try:
        dependency_service = DependencyService()
        dependency_service.install_dependencies()
        return True
    except Exception as ex:
        task.exception = ex
        return False

def finished(exception, result=None):
    if result:
        log_message("Succesfully finished the install_dependencies task", Qgis.Success)
    else:
        log_message("Failed to run the install_dependencies task", Qgis.Warning)

        if exception:
            log_exception(exception)
        else:
            log_message("No exception was raised", Qgis.Warning)
