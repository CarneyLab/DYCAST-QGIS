import sys
from qgis.core import Qgis, QgsTask

from dycast_qgis.models.risk_generation_parameters import RiskGenerationParameters
from dycast_qgis.services.logging_service import log_message, log_exception
from dycast_qgis.util.redirect_stdout import redirect_stdout


class GenerateRiskTask(QgsTask):

    def __init__(self, description, parameters: RiskGenerationParameters):
        super().__init__(description, QgsTask.CanCancel)
        self.parameters = parameters

    def run(self):
        log_message("Started generate_risk task", Qgis.Info)

        if not hasattr(sys, 'argv'):
            sys.argv  = ['']
            
        command = ["generate_risk","--spatial-domain", self.parameters.spatialDomain,"--temporal-domain", self.parameters.temporalDomain,"--close-in-space", self.parameters.closeInSpace,"--close-in-time", self.parameters.closeInTime,"--case-threshold", self.parameters.caseThreshold,"--startdate", self.parameters.startDate,"--enddate", self.parameters.endDate,"--srid-extent", self.parameters.sridOfExtent,"--extent-min-x", self.parameters.extentMinX,"--extent-min-y", self.parameters.extentMinY,"--extent-max-x", self.parameters.extentMaxX,"--extent-max-y", self.parameters.extentMaxY]
        log_message(f"Running command: {command}", Qgis.Info)

        from dycast_app.dycast import main as dycast_main
        with redirect_stdout():
            try:
                dycast_main(command)
            except Exception as ex:
                log_exception(ex)
                return False

        return True

    def finished(self, result=None):
        if result:
            log_message("Succesfully finished the generate_risk task", Qgis.Success)
        else:
            log_message("Failed to run the generate_risk task", Qgis.Warning)

            if self.exception:
                log_exception(self.exception)
            else:
                log_message("No exception was raised", Qgis.Warning)
