import sys
from contextlib import contextmanager
from qgis.core import QgsMessageLog, Qgis


MESSAGE_CATEGORY = 'Messages'

class StdOutLogger:

    def write(self, msg):
        QgsMessageLog.logMessage(msg, MESSAGE_CATEGORY, Qgis.Info)

@contextmanager
def redirect_stdout():
    oldout = sys.stdout
    sys.stdout = StdOutLogger()
    try:
        yield
    finally:
        sys.stdout = oldout