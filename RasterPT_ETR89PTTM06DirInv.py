# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterPT_ETR89PTTM06DirInv.py
    ---------------------
    Date                 : March 2015
    Copyright            : (C) 2015 by Giovanni Manghi
                           (C) 2015 by Fernando Ribeiro aka The Geocrafter
    Email                : giovanni dot manghi at naturalgis dot pt
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Giovanni Manghi'
__date__ = 'March 2015'
__copyright__ = '(C) 2015, Giovanni Manghi'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from urllib.request import urlretrieve

from qgis.PyQt.QtGui import QIcon

from qgis.core import (QgsRasterFileWriter,
                       QgsProcessingException,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterDestination
                      )

from processing.algs.gdal.GdalAlgorithm import GdalAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils

from ntv2_transformations.transformations import pt_transformation

pluginPath = os.path.dirname(__file__)


class RasterPT_ETR89PTTM06DirInv(GdalAlgorithm):

    INPUT = 'INPUT'
    TRANSF = 'TRANSF'
    CRS = 'CRS'
    GRID = 'GRID'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'ptrastertransform'

    def displayName(self):
        return '[PT] Direct and inverse Raster Tranformation'

    def group(self):
        return '[PT] Portugal (mainland)'

    def groupId(self):
        return 'portugal'

    def tags(self):
        return 'raster,grid,ntv2,direct,inverse,portugal'.split(',')

    def shortHelpString(self):
        return 'Direct and inverse raster tranformations using Portugal (mainland) NTv2 grids.'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'pt.png'))

    def initAlgorithm(self, config=None):
        self.directions = ['Direct: Old Data -> PT-TM06/ETRS89 [EPSG:3763]',
                           'Inverse: PT-TM06/ETRS89 [EPSG:3763] -> Old Data'
                          ]

        self.datums = (('Datum Lisboa [EPSG:20791/EPSG:5018/ESRI:102165]', 20791),
                       ('Datum Lisboa Militar [EPSG:20790/ESRI:102164]', 20790),
                       ('Datum 73 [EPSG:27493/ESRI:102161]', 27493),
                       ('Datum 73 Militar [ESRI:102160]', 102160),
                       ('ED50 UTM 29N [EPSG:23029] (Only grid from José Alberto Gonçalves)', 23029),
                      )

        self.grids = (('José Alberto Gonçalves', 'pt_e89'),
                      ('Direção-Geral do Territorio', 'PT_ETRS89_geo')
                     )

        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT,
                                                            'Input raster'))
        self.addParameter(QgsProcessingParameterEnum(self.TRANSF,
                                                     'Transformation',
                                                     options=self.directions,
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.CRS,
                                                     'Old Datum',
                                                     options=[i[0] for i in self.datums],
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.GRID,
                                                     'NTv2 Grid',
                                                     options=[i[0] for i in self.grids],
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterRasterDestination(self.OUTPUT,
                                                                  'Output'))

    def getConsoleCommands(self, parameters, context, feedback, executing=True):
        inLayer = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        if inLayer is None:
            raise QgsProcessingException(self.invalidRasterError(parameters, self.INPUT))

        outFile = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        self.setOutputValue(self.OUTPUT, outFile)

        direction = self.parameterAsEnum(parameters, self.TRANSF, context)
        epsg = self.datums[self.parameterAsEnum(parameters, self.CRS, context)][1]
        grid = self.grids[self.parameterAsEnum(parameters, self.GRID, context)][1]

        found, text = pt_transformation(epsg, grid)
        if not found:
           raise QgsProcessingException(text)

        arguments = []

        if direction == 0:
            # Direct transformation
            arguments.append('-s_srs')
            arguments.append(text)
            arguments.append('-t_srs')
            arguments.append('EPSG:4258')
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:4258')
            arguments.append('-t_srs')
            arguments.append(text)

        arguments.append('-multi')
        arguments.append('-of')
        arguments.append(QgsRasterFileWriter.driverForExtension(os.path.splitext(outFile)[1]))
        arguments.append(inLayer.source())
        arguments.append(outFile)

        if not os.path.isfile(os.path.join(pluginPath, 'grids', 'pt73_e89.gsb')):
            urlretrieve ('http://www.naturalgis.pt/downloads/ntv2grids/pt/pt73_e89.gsb', os.path.join(pluginPath, 'grids', 'pt73_e89.gsb'))
            urlretrieve ('http://www.naturalgis.pt/downloads/ntv2grids/pt/ptED_e89.gsb', os.path.join(pluginPath, 'grids', 'ptED_e89.gsb'))
            urlretrieve ('http://www.naturalgis.pt/downloads/ntv2grids/pt/ptLB_e89.gsb', os.path.join(pluginPath, 'grids', 'ptLB_e89.gsb'))
            urlretrieve ('http://www.naturalgis.pt/downloads/ntv2grids/pt/ptLX_e89.gsb', os.path.join(pluginPath, 'grids', 'ptLX_e89.gsb'))
            urlretrieve ('http://www.naturalgis.pt/downloads/ntv2grids/pt/D73_ETRS89_geo.gsb', os.path.join(pluginPath, 'grids', 'D73_ETRS89_geo.gsb'))
            urlretrieve ('http://www.naturalgis.pt/downloads/ntv2grids/pt/DLX_ETRS89_geo.gsb', os.path.join(pluginPath, 'grids', 'DLX_ETRS89_geo.gsb'))

        return ['gdalwarp', GdalUtils.escapeAndJoin(arguments)]
