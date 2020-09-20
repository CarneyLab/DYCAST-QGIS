import os
import sys
from qgis.core import Qgis

from dycast_qgis.models.risk_generation_parameters import RiskGenerationParameters
from dycast_qgis.services.logging_service import log_message, log_exception
from dycast_qgis.services.subprocess_service import SubprocessService
from dycast_qgis.util.redirect_stdout import redirect_stdout


def run(task, parameters: RiskGenerationParameters):
    log_message("Started generate_risk task", Qgis.Info)

    if not hasattr(sys, 'argv'):
        sys.argv  = ['']
        
    subprocess_service = SubprocessService()

    # from dycast_app.dycast import main as dycast_main
    #os.path.dirname(__file__), 
    dycast_script = os.path.join(os.path.dirname(__file__), '..', 'dycast_app', 'dycast.py' )
    # command = [ 'python', dycast_script]
    # command_arguments = ["generate_risk","--spatial-domain", parameters.spatialDomain,"--temporal-domain", parameters.temporalDomain,"--close-in-space", parameters.closeInSpace,"--close-in-time", parameters.closeInTime,"--case-threshold", parameters.caseThreshold,"--startdate", parameters.startDate,"--enddate", parameters.endDate,"--srid-extent", parameters.sridOfExtent,"--extent-min-x", parameters.extentMinX,"--extent-min-y", parameters.extentMinY,"--extent-max-x", parameters.extentMaxX,"--extent-max-y", parameters.extentMaxY]
    # command.append(command_arguments)
    python_home = os.environ['PYTHONHOME']
    python_binary = os.path.join(python_home, 'python')
    command = [ 'python', dycast_script, "generate_risk","--spatial-domain", parameters.spatialDomain,"--temporal-domain", parameters.temporalDomain,"--close-in-space", parameters.closeInSpace,"--close-in-time", parameters.closeInTime,"--case-threshold", parameters.caseThreshold,"--startdate", parameters.startDate,"--enddate", parameters.endDate,"--srid-extent", parameters.sridOfExtent,"--extent-min-x", parameters.extentMinX,"--extent-min-y", parameters.extentMinY,"--extent-max-x", parameters.extentMaxX,"--extent-max-y", parameters.extentMaxY]
    log_message(f"Running command: {command}", Qgis.Info)

    try:
        subprocess_service.run_subprocess(command)
    except Exception as ex:
        log_exception(ex)

    # with redirect_stdout():
    #     command = ["generate_risk","--spatial-domain", parameters.spatialDomain,"--temporal-domain", parameters.temporalDomain,"--close-in-space", parameters.closeInSpace,"--close-in-time", parameters.closeInTime,"--case-threshold", parameters.caseThreshold,"--startdate", parameters.startDate,"--enddate", parameters.endDate,"--srid-extent", parameters.sridOfExtent,"--extent-min-x", parameters.extentMinX,"--extent-min-y", parameters.extentMinY,"--extent-max-x", parameters.extentMaxX,"--extent-max-y", parameters.extentMaxY]
    #     log_message(f"Running command: {command}", Qgis.Info)
    #     try:
    #         # dycast_main(["-h"])
    #         # dycast_main(["load_cases", "--srid-cases", "3857", "--file", "C:\\Users\\meije\\Documents\\Repositories\\dycast\\application\\tests\\test_data\\import\\input_cases_geometry.tsv"])
    #         dycast_main(command)
    #     except Exception as ex:
    #         log_exception(ex)

def finished(exception, result=None):
    if result:
        log_message("Succesfully finished the generate_risk task", Qgis.Success)
    else:
        log_message("Failed to run the generate_risk task", Qgis.Warning)

        if exception:
            log_exception(exception)
        else:
            log_message("No exception was raised", Qgis.Warning)
