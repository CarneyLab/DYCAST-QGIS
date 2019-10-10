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
    except ptvsd.AttachAlreadyEnabledError:
        QgsMessageLog.logMessage("Remote Debug for Visual Studio is already active", MESSAGE_CATEGORY, Qgis.Info)
        pass
    except Exception as e:
        QgsMessageLog.logMessage(type(e.__name__), MESSAGE_CATEGORY, Qgis.Critical)
        QgsMessageLog.logMessage(e.args, MESSAGE_CATEGORY, Qgis.Critical)
        QgsMessageLog.logMessage(str(e), MESSAGE_CATEGORY, Qgis.Critical)
