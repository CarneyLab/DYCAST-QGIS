import sys
import traceback
from qgis.core import QgsMessageLog, Qgis


MESSAGE_CATEGORY = 'Messages'


def log_message(message, category: Qgis.MessageLevel = Qgis.Info):
    QgsMessageLog.logMessage(message, MESSAGE_CATEGORY, category)


def log_exception(exception: Exception):
    QgsMessageLog.logMessage("An error occurred", MESSAGE_CATEGORY, Qgis.Critical)
    QgsMessageLog.logMessage("Type: {type}".format(type=type(exception).__name__), MESSAGE_CATEGORY, Qgis.Critical)
    QgsMessageLog.logMessage("Message: {message}".format(message=str(exception)), MESSAGE_CATEGORY, Qgis.Critical)
    _log_formatted_traceback()


def _log_formatted_traceback():
    _, _, exc_traceback = sys.exc_info()

    if exc_traceback:
        format_traceback = traceback.format_tb(exc_traceback)
        for line in format_traceback:
            QgsMessageLog.logMessage(repr(line), MESSAGE_CATEGORY, Qgis.Critical)
