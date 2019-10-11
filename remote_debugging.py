import sys
import traceback
from qgis.core import QgsMessageLog, Qgis


MESSAGE_CATEGORY = 'Messages'


def enable_remote_debugging():
    try:
        import ptvsd
        if ptvsd.is_attached():
            QgsMessageLog.logMessage("Remote Debug for Visual Studio is already active", MESSAGE_CATEGORY, Qgis.Info)
            return
        ptvsd.enable_attach(address=('localhost', 5678))
        QgsMessageLog.logMessage("Attached remote Debug for Visual Studio", MESSAGE_CATEGORY, Qgis.Info)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        format_exception = traceback.format_exception(exc_type, exc_value, exc_traceback)
        QgsMessageLog.logMessage(repr(format_exception[0]), MESSAGE_CATEGORY, Qgis.Critical)
        QgsMessageLog.logMessage(repr(format_exception[1]), MESSAGE_CATEGORY, Qgis.Critical)
        QgsMessageLog.logMessage(repr(format_exception[2]), MESSAGE_CATEGORY, Qgis.Critical)

        # Make generic exception logger method ^
