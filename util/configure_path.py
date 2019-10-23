import os
import sys
from qgis.core import Qgis
from dycast_qgis.services.logging_service import log_message, log_exception


def configure_path():
    current_directory = get_root_directory()
    add_plugin_to_path(current_directory)
    add_dycast_to_path(current_directory)


def get_root_directory():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(
        os.path.join(current_directory, ".."))


def add_plugin_to_path(current_directory):
    add_to_path(current_directory)


def add_dycast_to_path(current_directory):
    dycast_path = os.path.join(current_directory, 'dycast_app')
    add_to_path(dycast_path)


def add_to_path(path):
    if path not in sys.path:
        log_message("Adding [{path}] to path".format(path=path), Qgis.Info)
        sys.path.append(path)
    else:
        log_message("Directory [{path}] is present in path".format(
            path=path), Qgis.Info)
