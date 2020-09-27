import subprocess
from subprocess import Popen, PIPE
from qgis.core import Qgis
from dycast_qgis.services.logging_service import log_message, log_exception

class SubprocessService():    
    def run_subprocess(self, command):
        process = subprocess.Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

        while True:
            output = process.stdout.readline()

            if self.is_done(process, output):
                break

            self.log_message(output.strip(), Qgis.Info)

        while True:
            error = process.stderr.readline()
            
            if self.is_done(process, error):
                break

            self.log_message(error.strip(), Qgis.Critical)

    def is_done(self, process, output):
        return output == '' and process.poll() is not None

    def log_message(self, message, log_level: Qgis.MessageLevel):
        if message:
            log_message(message, log_level)