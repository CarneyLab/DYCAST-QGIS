from qgis.core import QgsTask, QgsMessageLog

MESSAGE_CATEGORY = 'Messages'

class LoadCasesTask(QgsTask):
    """Runs the load_cases command in Dycast"""

    def __init__(self):
        super().__init__("Test load cases")
        self.expection = None

    def run(self):
        QgsMessageLog.logMessage("Started load_cases task", MESSAGE_CATEGORY, QgsMessageLog.INFO)
        try:
            from .dycast_app.dycast import main as dycast_main
            return True
        except Exception as e:
            self.exception = e
            return False
    
    def finished(self, result):
        if result:
            QgsMessageLog.logMessage("Succesfully finished the load_cases task", MESSAGE_CATEGORY, QgsMessageLog.SUCCESS)
        else:
            if self.exception:
                QgsMessageLog.logMessage("Failed to run the load_cases task. \
                 Exception: {exception}".format(exception=self.exception), \
                 MESSAGE_CATEGORY, QgsMessageLog.CRITICAL)
                raise self.exception
            else:
                QgsMessageLog.logMessage("Failed to run the load_cases task. \
                 No exception was raised", \
                 MESSAGE_CATEGORY, QgsMessageLog.WARNING)

