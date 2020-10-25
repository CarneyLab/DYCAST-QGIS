import os
import subprocess
from subprocess import Popen, PIPE
from pathlib import Path
from qgis.core import Qgis
from dycast_qgis.services.logging_service import log_message, log_exception
from dycast_qgis.services.subprocess_service import SubprocessService

class DependencyService():

    def __init__(self):
        pass

    def install_dependencies(self):
        
        subprocess_service = SubprocessService()

        if (self.installation_is_required()):
            log_message("Installing dependencies...", Qgis.Info)

            requirements_file = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt' )
            requirements_file_dycast = os.path.join(os.path.dirname(__file__), '..', 'dycast_app', 'init', 'requirements.txt' )
            
            python_home = os.environ['PYTHONHOME']
            python_binary = 'python'

            command_base = [ python_binary, '-m', 'pip', 'install' ]
            upgrade_command = ['--upgrade', 'pip', '--user', '--no-warn-script-location']
            installation_command = ['--requirement', requirements_file, '--user']
            installation_command_dycast = ['--requirement', requirements_file_dycast, '--user']
            
            log_message("Upgrading PIP...", Qgis.Info)
            subprocess_service.run_subprocess(command_base + upgrade_command)
            log_message("Installing QGIS plugin dependencies...", Qgis.Info)
            subprocess_service.run_subprocess(command_base + installation_command)
            log_message("Installing Dycast app dependencies...", Qgis.Info)
            subprocess_service.run_subprocess(command_base + installation_command_dycast)
            
            if self.can_import_all_modules:
                log_message("All dependencies could be loaded. Installation successful.", Qgis.Info)
                log_message("!! !! ", Qgis.Warning)
                log_message("Important: A restart of QGIS is required ", Qgis.Warning)
                log_message("!! !! ", Qgis.Warning)
            else: 
                log_message("Dependencies could not be loaded after installation. Try restartin QGIS" ,Qgis.Critical)


    def debug_info(self, subprocess_service: SubprocessService):
        log_message("PYTHONHOME:", Qgis.Info)
        python_home = os.environ['PYTHONHOME']
        log_message(python_home, Qgis.Info)
        python_binary = os.path.join(python_home, 'python')
        pip3_binary = os.path.join(python_home, 'Scripts', 'pip3')

        log_message("Test 1", Qgis.Info)
        subprocess_service.run_subprocess(['python', '--version'])

        log_message("Test 2", Qgis.Info)
        if os.name == 'nt':
            subprocess_service.run_subprocess(['where', 'python'])
        else:
            subprocess_service.run_subprocess(['which', 'python'])
        
        log_message("Test 4", Qgis.Info)
        subprocess_service.run_subprocess([python_binary, '--version'])

        log_message("Test 5", Qgis.Info)
        subprocess_service.run_subprocess([python_binary, '-m', 'pip', '--version'])

        log_message("Test 6", Qgis.Info)
        subprocess_service.run_subprocess([os.path.join(python_home, 'Scripts', 'pip3'), '--version'])

        log_message("Test 7", Qgis.Info)
        subprocess_service.run_subprocess(['pip3', '--version'])

        # log_message("Test 8", Qgis.Info)
        # subprocess_service.run_subprocess([python_binary, '-m', 'pip', 'install', '--upgrade', 'pip'])

        # log_message("Test 9", Qgis.Info)
        # subprocess_service.run_subprocess(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])

        # log_message("Test 10", Qgis.Info)
        # subprocess_service.run_subprocess([pip3_binary, 'install', '--upgrade', 'pip'])

    def installation_is_required(self):
        log_message("Checking if dependencies are installed", Qgis.Info)
        
        if self.can_import_all_modules():
            log_message("Dependencies are installed", Qgis.Info)
            return False
        else:
            log_message("Dependencies are not installed", Qgis.Info)
            return True

    def can_import_all_modules(self):
        current_directory = Path(__file__).parent
        task_directory = Path(os.path.join(current_directory, '..', 'tasks'))
        if self.can_import_modules(current_directory) and self.can_import_modules(task_directory, 'dycast_qgis.tasks'):
            log_message("Dependencies could be imported", Qgis.Info)
            return True
        else:
            log_message("Dependencies could not be imported", Qgis.Info)
            return False

    def can_import_modules(self, path: Path, module_prefix: str = ''):
        try:
            from importlib import import_module

            for f in path.glob("*.py"):
                if not f.stem.startswith("_"):
                    import_module(f"{module_prefix}.{f.stem}", __package__)
            
            return True

        except ImportError:
            return False
        except FileNotFoundError as e:
            log_exception(e)
            return False


    def log_message(self, message, log_level: Qgis.MessageLevel):
        if message:
            log_message(message, log_level)
