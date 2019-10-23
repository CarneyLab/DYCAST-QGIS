import sys
import traceback
from qgis.core import Qgis
from dycast_qgis.services.logging_service import log_message, log_exception


def enable_remote_debugging():
    try:
        import ptvsd
        if ptvsd.is_attached():
            log_message("Remote Debug for Visual Studio is already active", Qgis.Info)
            return
        ptvsd.enable_attach(address=('localhost', 5678))
        log_message("Attached remote Debug for Visual Studio", Qgis.Info)
    except Exception as e:
        log_exception(e)
