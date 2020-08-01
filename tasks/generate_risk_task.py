from qgis.core import Qgis

from dycast_qgis.services.logging_service import log_message, log_exception
from dycast_qgis.util.redirect_stdout import redirect_stdout


def run(task):
    log_message("Started generate_risk task", Qgis.Info)
    from dycast_app.dycast import main as dycast_main
    with redirect_stdout():
        command = ["generate_risk", "--monte-carlo-file", "Dengue_max_100_40000.csv"]
        log_message(f"Running command: {command}", Qgis.Info)
        dycast_main(command)

def finished(exception, result=None):
    if result:
        log_message("Succesfully finished the generate_risk task", Qgis.Success)
    else:
        log_message("Failed to run the generate_risk task", Qgis.Warning)

        if exception:
            log_exception(exception)
        else:
            log_message("No exception was raised", Qgis.Warning)
