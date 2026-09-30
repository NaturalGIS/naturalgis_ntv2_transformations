"""Compatibilidad de la API GDAL de Processing entre QGIS 3.x y QGIS 4.x.

En QGIS 4 GdalAlgorithm.getOgrCompatibleSource devuelve un GdalConnectionDetails
y GdalUtils.ogrConnectionStringAndFormat ya no existe; en 3.x devolvían tuplas.
"""
from processing.algs.gdal.GdalUtils import GdalUtils


def ogr_input(alg, name, parameters, context, feedback, executing):
    """Devuelve (connection_string, layer_name) de una entrada vectorial."""
    res = alg.getOgrCompatibleSource(name, parameters, context, feedback, executing)
    if hasattr(res, 'connection_string'):
        return res.connection_string, res.layer_name
    return res


def ogr_output(out_file, context):
    """Devuelve (connection_string, format) de una salida vectorial."""
    if hasattr(GdalUtils, 'gdal_connection_details_from_uri'):
        res = GdalUtils.gdal_connection_details_from_uri(out_file, context)
        return res.connection_string, res.format
    return GdalUtils.ogrConnectionStringAndFormat(out_file, context)
