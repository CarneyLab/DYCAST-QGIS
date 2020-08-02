import os
import subprocess
from subprocess import Popen, PIPE
from pathlib import Path
from qgis.core import Qgis
from dycast_qgis.services.logging_service import log_message, log_exception

class DependencyService():

    def __init__(self):
        pass

    def install_dependencies(self):
        
        self.debug_info()

        if (self.installation_is_required()):
            log_message("Installing dependencies...", Qgis.Info)

            requirements_file = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt' )
            requirements_file_dycast = os.path.join(os.path.dirname(__file__), '..', 'dycast_app', 'init', 'requirements.txt' )
            
            python_home = os.environ['PYTHONHOME']
            python_binary = os.path.join(python_home, 'python')
            pip3_binary = os.path.join(python_home, 'Scripts', 'pip3')

            upgrade_command = [python_binary, '-m', 'pip', 'install', '--upgrade', 'pip', '--user', '--no-warn-script-location']
            installation_command = [python_binary, '-m', 'pip', 'install', '--requirement', requirements_file, '--user']
            installation_command_dycast = [python_binary, '-m', 'pip', 'install', '--requirement', requirements_file_dycast, '--user']
            
            log_message("Upgrading PIP...", Qgis.Info)
            self.run_subprocess(upgrade_command)
            log_message("Installing QGIS plugin dependencies...", Qgis.Info)
            self.run_subprocess(installation_command)
            log_message("Installing Dycast app dependencies...", Qgis.Info)
            self.run_subprocess(installation_command_dycast)
            
            log_message("Done installing dependencies.", Qgis.Info)


    def debug_info(self):
        log_message("PYTHONHOME:", Qgis.Info)
        python_home = os.environ['PYTHONHOME']
        log_message(python_home, Qgis.Info)
        python_binary = os.path.join(python_home, 'python')
        pip3_binary = os.path.join(python_home, 'Scripts', 'pip3')

        log_message("Test 1", Qgis.Info)
        self.run_subprocess(['python', '--version'])

        log_message("Test 2", Qgis.Info)
        if os.name == 'nt':
            self.run_subprocess(['where', 'python'])
        else:
            self.run_subprocess(['which', 'python'])
        
        log_message("Test 4", Qgis.Info)
        self.run_subprocess([python_binary, '--version'])

        log_message("Test 5", Qgis.Info)
        self.run_subprocess([python_binary, '-m', 'pip', '--version'])

        log_message("Test 6", Qgis.Info)
        self.run_subprocess([os.path.join(python_home, 'Scripts', 'pip3'), '--version'])

        log_message("Test 7", Qgis.Info)
        self.run_subprocess(['pip3', '--version'])

        log_message("Test 8", Qgis.Info)
        self.run_subprocess([python_binary, '-m', 'pip', 'install', '--upgrade', 'pip'])

        log_message("Test 9", Qgis.Info)
        self.run_subprocess(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])

        log_message("Test 10", Qgis.Info)
        self.run_subprocess([pip3_binary, 'install', '--upgrade', 'pip'])

    def installation_is_required(self):
        log_message("Checking if dependencies are installed", Qgis.Info)
        current_directory = Path(__file__).parent
        task_directory = Path(os.path.join(current_directory, '..', 'tasks'))
        if self.can_import_modules(current_directory) and self.can_import_modules(task_directory, 'dycast_qgis.tasks'):
            log_message("Dependencies are installed", Qgis.Info)
            return False
        else:
            return True

    def can_import_modules(self, path: Path, module_prefix: str = ''):
        try:
            from importlib import import_module

            for f in path.glob("*.py"):
                if not f.stem.startswith("_"):
                    import_module(f"{module_prefix}.{f.stem}", __package__)
            
            return True

        except ImportError:
            return False

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
