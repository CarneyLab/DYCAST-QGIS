import os
import sys
from qgis.core import QgsMessageLog, Qgis

MESSAGE_CATEGORY = 'Messages'


def configure_path():
    current_directory = get_root_directory()
    add_plugin_to_path(current_directory)
    add_dycast_to_path(current_directory)

def get_root_directory():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(
        os.path.join(current_directory, ".."))

def add_plugin_to_path(current_directory):
    if current_directory not in sys.path:
        QgsMessageLog.logMessage("Adding [{current_directory}] to path"
                                 .format(current_directory=current_directory),
                                 MESSAGE_CATEGORY, Qgis.Info)

        sys.path.append(current_directory)
    else:
        QgsMessageLog.logMessage("Plugin directory [{current_directory}] is present in path"
                                 .format(current_directory=current_directory),
                                 MESSAGE_CATEGORY, Qgis.Info)


def add_dycast_to_path(current_directory):
    dycast_path = os.path.join(current_directory, 'dycast_app')
    if dycast_path not in sys.path:
        QgsMessageLog.logMessage("Adding [{dycast_path}] to path"
                                 .format(dycast_path=dycast_path),
                                 MESSAGE_CATEGORY, Qgis.Info)

        sys.path.append(dycast_path)
    else:
        QgsMessageLog.logMessage("Dycast directory [{dycast_path}] is present in path"
                                 .format(dycast_path=dycast_path),
                                 MESSAGE_CATEGORY, Qgis.Info)
