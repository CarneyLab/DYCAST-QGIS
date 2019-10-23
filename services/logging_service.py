import sys
import traceback
from qgis.core import QgsMessageLog, Qgis


MESSAGE_CATEGORY = 'Messages'


def log_message(message, category: Qgis.MessageLevel = Qgis.Info):
    QgsMessageLog.logMessage(message, MESSAGE_CATEGORY, category)

def log_exception(exception: Exception):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    format_exception = traceback.format_exception(exc_type, exc_value, exc_traceback)
    QgsMessageLog.logMessage(str(exception), MESSAGE_CATEGORY, Qgis.Critical)
    QgsMessageLog.logMessage(repr(format_exception[0]), MESSAGE_CATEGORY, Qgis.Critical)
    QgsMessageLog.logMessage(repr(format_exception[1]), MESSAGE_CATEGORY, Qgis.Critical)
    QgsMessageLog.logMessage(repr(format_exception[2]), MESSAGE_CATEGORY, Qgis.Critical)
