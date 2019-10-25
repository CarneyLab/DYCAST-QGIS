import sys
import traceback
from qgis.core import QgsMessageLog, Qgis


MESSAGE_CATEGORY = 'Messages'


def log_message(message, category: Qgis.MessageLevel = Qgis.Info):
    QgsMessageLog.logMessage(message, MESSAGE_CATEGORY, category)


def log_exception(exception: Exception):
    QgsMessageLog.logMessage(type(exception).__name__, MESSAGE_CATEGORY, Qgis.Critical)
    QgsMessageLog.logMessage(str(exception), MESSAGE_CATEGORY, Qgis.Critical)
    _log_formatted_traceback()


def _log_formatted_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_type:
        format_exception = traceback.format_exception(exc_type, exc_value, exc_traceback)
        QgsMessageLog.logMessage(repr(format_exception[0]), MESSAGE_CATEGORY, Qgis.Critical)
        QgsMessageLog.logMessage(repr(format_exception[1]), MESSAGE_CATEGORY, Qgis.Critical)
        QgsMessageLog.logMessage(repr(format_exception[2]), MESSAGE_CATEGORY, Qgis.Critical)
