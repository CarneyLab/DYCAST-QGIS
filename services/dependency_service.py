import sys
import os
from pathlib import Path
from qgis.core import Qgis
from dycast_qgis.services.logging_service import log_message, log_exception
from dycast_qgis.services.subprocess_service import SubprocessService

class DependencyService():

    def __init__(self):
        pass

    def install_dependencies(self):
        
        # self.debug_info(subprocess_service)

        if (self.installation_is_required()):
            log_message("Installing dependencies...", Qgis.Info)

            self.install_wheel_dependencies()
            self.install_pypi_dependencies()

            if self.can_import_all_modules:
                log_message("All dependencies could be loaded. Installation successful.", Qgis.Info)

            else: 
                log_message("Dependencies could not be loaded after installation. Try restartin QGIS" ,Qgis.Critical)

    def install_wheel_dependencies(self):
        current_directory = Path(__file__).parent
        wheels_directory = Path(os.path.join(current_directory, '..', 'dependencies', 'wheels'))

        for wheel in wheels_directory.glob('**/*.whl'):
            sys.path.insert(0, str(wheel))

    def install_pypi_dependencies(self):
        python_binary = 'python'
        command_base = [ python_binary, '-m', 'pip', 'install' ]

        log_message("Installing pyproj...", Qgis.Info)
        subprocess_service = SubprocessService()
        subprocess_service.run_subprocess(command_base + ['pyproj==1.9.6'])

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
