from qgis.core import Qgis, QgsProject, QgsMapLayer, QgsVectorLayer, QgsRasterLayer, QgsDataSourceUri, QgsLayerTreeLayer
from qgis.gui import QgisInterface, QgsMapCanvas

from dycast_qgis.models.configuration import Configuration
from dycast_qgis.services.logging_service import log_message, log_exception

class LayerService():
    def __init__(self, config: Configuration):
        self.config = config

        self.expected_raster_layers = [
            ('OpenStreetMap',
             'type=xyz&url=http://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857',
             'wms')]

        self.expected_database_layers = {
            'cases': 'location'
            }

    def get_qgs_instance(self):
        return QgsProject.instance()

    def get_project_instance_layers(self):
        return self.get_qgs_instance().mapLayers().values()

    def get_project_instance_layer_names(self):
        layers = self.get_project_instance_layers()
        return [layer.name() for layer in layers]

    def get_tree_root_layers(self):
        return self.get_qgs_instance().layerTreeRoot().children()

    def initialize_layers(self):
        self.add_database_layers_to_project_instance()
        self.add_raster_layers_to_project_instance()
        self.add_project_instance_layers_to_root()

    def add_raster_layers_to_project_instance(self):
        layer_names = self.get_project_instance_layer_names()

        for (layer_name, layer_url, service_type) in self.expected_raster_layers:
            if layer_name not in layer_names:
                log_message("Adding [{layer_name}] raster layer".format(layer_name=layer_name), Qgis.Info)
                rlayer = QgsRasterLayer(layer_url, layer_name, service_type)
                self.add_layer_to_map(rlayer)

    def add_project_instance_layers_to_root(self):
        project_instance_layers = self.get_project_instance_layers()
        root = self.get_qgs_instance().layerTreeRoot()

        log_message("Layer count 2: {layer_count}".format(layer_count=len(project_instance_layers)))
        for layer in project_instance_layers:
            log_message(layer.name())
            root.insertChildNode(-1, QgsLayerTreeLayer(layer))

        layer_tree_root = self.get_tree_root_layers()

        log_message("Layer count 1: {layer_count}".format(layer_count=len(layer_tree_root)))
        for layer in layer_tree_root:
            log_message(layer.name())

    def add_database_layers_to_project_instance(self):
        layer_names = self.get_project_instance_layer_names()

        for layer_name, geometry_column in self.expected_database_layers.items():
            if layer_name not in layer_names:
                log_message("Adding [{layer_name}] database layer".format(layer_name=layer_name), Qgis.Info)
                self.initialize_database_layer(layer_name, geometry_column)
            else:
                log_message("Layer {layer_name} already exists".format(layer_name=layer_name))

    def initialize_database_layer(self, layer_name, geometry_column):
        layer = self.create_layer_from_table(layer_name, geometry_column)

        if not layer.isValid():
            log_exception("Layer not valid: {layer_name}".format(layer_name=layer_name))
            return

        self.add_layer_to_map(layer)

    def create_layer_from_table(self, table_name, geometry_column):
        uri = self.get_uri()
        uri.setDataSource(self.config.db_schema, table_name, geometry_column, "")

        return QgsVectorLayer(uri.uri(), table_name, "postgres")

    def get_uri(self):
        uri = QgsDataSourceUri()
        uri.setConnection(self.config.db_host, self.config.db_port, self.config.db_name, self.config.db_user, self.config.db_password)
        return uri

    def add_layer_to_map(self, layer: QgsMapLayer):
        if layer.isValid():
            self.get_qgs_instance().addMapLayer(layer)
        else:
            log_message("Raster layer [{layer_name}] was invalid, skipping...".format(layer_name=layer.name()), Qgis.Warning)        
