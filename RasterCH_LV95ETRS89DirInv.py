# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterCH_LV95ETRS89DirInv.py
    ---------------------
    Date                 : August 2019
    Copyright            : (C) 2019 by Giovanni Manghi
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

__author__ = 'Alexander Bruy, Giovanni Manghi'
__date__ = 'August 2019'
__copyright__ = '(C) 2019, Giovanni Manghi'

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

pluginPath = os.path.dirname(__file__)


class RasterCH_LV95ETRS89DirInv(GdalAlgorithm):

    INPUT = 'INPUT'
    TRANSF = 'TRANSF'
    CRS = 'CRS'
    GRID = 'GRID'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'chrastertransform'

    def displayName(self):
        return '[CH] Direct and inverse Raster Tranformation'

    def group(self):
        return '[CH] Switzerland'

    def groupId(self):
        return 'switzerland'

    def tags(self):
        return 'raster,grid,ntv2,direct,inverse,switzerland'.split(',')

    def shortHelpString(self):
        return 'Direct and inverse raster tranformations using Switzerland NTv2 grids.'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'ch.png'))

    def initAlgorithm(self, config=None):
        self.directions = ['Direct: CH1903/LV03 [EPSG:21781] -> New Data',
                           'Inverse: New Data -> CH1903/LV03 [EPSG:21781]'
                          ]

        self.datums = ['ETRS89 [EPSG:4258]',
                       'CH1903+ [EPSG:2056]'
                      ]

        self.grids = ['CHENyx06']

        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT,
                                                            'Input raster'))
        self.addParameter(QgsProcessingParameterEnum(self.TRANSF,
                                                     'Transformation',
                                                     options=self.directions,
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.CRS,
                                                     'New Datum',
                                                     options=[i[0] for i in self.datums],
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.GRID,
                                                     'NTv2 Grid',
                                                     options=self.grids,
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
        crs = self.parameterAsEnum(parameters, self.CRS, context)
        grid = self.parameterAsEnum(parameters, self.GRID, context)

        arguments = []

        if direction == 0:
            # Direct transformation
            arguments.append('-t_srs')
            if crs == 0:
                gridFile = os.path.join(pluginPath, 'grids', 'CHENYX06a.gsb')
                arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +nadgrids=@null +wktext +units=m')
            else:
                gridFile = os.path.join(pluginPath, 'grids', 'chenyx06etrs.gsb')
                arguments.append('EPSG:4258')

            arguments.append('-s_srs')
            arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile))
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            if crs == 0:
                gridFile = os.path.join(pluginPath, 'grids', 'CHENYX06a.gsb')
                arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +nadgrids=@null +wktext +units=m')
            else:
                gridFile = os.path.join(pluginPath, 'grids', 'chenyx06etrs.gsb')
                arguments.append('EPSG:4258')

            arguments.append('-t_srs')
            arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile))

        arguments.append('-multi')
        arguments.append('-of')
        arguments.append(QgsRasterFileWriter.driverForExtension(os.path.splitext(outFile)[1]))
        arguments.append(inLayer.source())
        arguments.append(outFile)

        if not os.path.isfile(os.path.join(pluginPath, 'grids', 'CHENYX06a.gsb')):
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/ch/CHENYX06a.gsb', os.path.join(pluginPath, 'grids', 'CHENYX06a.gsb'))
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/ch/chenyx06etrs.gsb', os.path.join(pluginPath, 'grids', 'chenyx06etrs.gsb'))

        return ['gdalwarp', GdalUtils.escapeAndJoin(arguments)]
