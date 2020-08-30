import sys
from qgis.core import Qgis

from dycast_qgis.models.risk_generation_parameters import RiskGenerationParameters
from dycast_qgis.services.logging_service import log_message, log_exception
from dycast_qgis.util.redirect_stdout import redirect_stdout


def run(task, parameters: RiskGenerationParameters):
    log_message("Started generate_risk task", Qgis.Info)

    if not hasattr(sys, 'argv'):
        sys.argv  = ['']
        
    from dycast_app.dycast import main as dycast_main
    
    with redirect_stdout():
        command = [
            "generate_risk",
            "--monte-carlo-file", "Dengue_max_100_40000.csv",
            "--spatial-domain", parameters.spatialDomain,
            "--temporal-domain", parameters.temporalDomain,
            "--close-in-space", parameters.closeInSpace,
            "--close-in-time", parameters.closeInTime,
            "--case-threshold", parameters.caseThreshold,
            "--startdate", parameters.startDate,
            "--enddate", parameters.endDate,
            "--srid-extent", parameters.sridOfExtent,
            "--extent-min-x", parameters.extentMinX,
            "--extent-min-y", parameters.extentMinY,
            "--extent-max-x", parameters.extentMaxX,
            "--extent-max-y", parameters.extentMaxY
            ]

        log_message(f"Running command: {command}", Qgis.Info)
        try:
            dycast_main(command)
        except Exception as ex:
            log_exception(ex)

def finished(exception, result=None):
    if result:
        log_message("Succesfully finished the generate_risk task", Qgis.Success)
    else:
        log_message("Failed to run the generate_risk task", Qgis.Warning)

        if exception:
            log_exception(exception)
        else:
            log_message("No exception was raised", Qgis.Warning)
