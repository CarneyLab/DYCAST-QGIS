from qgis.core import QgsProject
from qgis.core import Qgis

from dycast_qgis.services.logging_service import log_message, log_exception

class LayerService():

    def __init__(self):
        self.expected_layers = ['cases', 'risk']

    def get_all_layers(self):
        return QgsProject.instance().layerTreeRoot().children()

    def initialize_layers(self):
        layers = self.get_all_layers()

        for expected_layer in self.expected_layers:
            if expected_layer not in layers:
                log_message("Initializing layer {expected_layer}".format(expected_layer=expected_layer), Qgis.Info)
                pass
            else:
                log_message("Layer {expected_layer} already exists".format(expected_layer=expected_layer))
