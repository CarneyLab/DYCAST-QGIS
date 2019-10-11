import sys
import os
import subprocess
import ptvsd

from qgis.core import QgsTask, QgsMessageLog, Qgis

from util.redirect_stdout import redirect_stdout

MESSAGE_CATEGORY = 'Messages'


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))

def run(task, file_path):
    ptvsd.debug_this_thread()
    QgsMessageLog.logMessage("Started load_cases task",
                             MESSAGE_CATEGORY, Qgis.Info)
    with redirect_stdout():
        from dycast_app.dycast import main as dycast_main
        from dycast_app.models.classes import dycast_parameters

        dycast_main(["load_cases", "--srid-cases",
                    "3857", "--file", file_path])
        return "Success!"


def finished(exception, result=None, ):
    if result:
        QgsMessageLog.logMessage(
            "Succesfully finished the load_cases task", MESSAGE_CATEGORY, Qgis.Success)
    else:
        if exception:
            QgsMessageLog.logMessage("Failed to run the load_cases task. \
                Exception: {exception}".format(exception=exception),
                                     MESSAGE_CATEGORY, Qgis.Critical)

            raise exception

        QgsMessageLog.logMessage("Failed to run the load_cases task. \
                No exception was raised",
                                 MESSAGE_CATEGORY, Qgis.Warning)
