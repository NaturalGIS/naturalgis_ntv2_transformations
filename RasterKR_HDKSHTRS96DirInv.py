# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterKR_HDKSHTRS96DirInv.py
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

from ntv2_transformations.transformations import hr_transformation

pluginPath = os.path.dirname(__file__)


class RasterKR_HDKSHTRS96DirInv(GdalAlgorithm):

    INPUT = 'INPUT'
    TRANSF = 'TRANSF'
    CRS = 'CRS'
    GRID = 'GRID'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'hrrastertransform'

    def displayName(self):
        return '[HR] Direct and inverse Raster Transformation'

    def group(self):
        return '[HR] Croatia'

    def groupId(self):
        return 'croatia'

    def tags(self):
        return 'raster,grid,ntv2,direct,inverse,croatia'.split(',')

    def shortHelpString(self):
        return 'Direct and inverse raster transformations using Croatia NTv2 grids.'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'hr.png'))

    def initAlgorithm(self, config=None):
        self.directions = ['Direct: Old Data -> HTRS96/Croatia TM [EPSG:3765]',
                           'Inverse: HTRS96/Croatia TM [EPSG:3765] -> Old Data'
                          ]

        self.datums = (('HDKS5 [Custom]', 5),
                       ('HDKS6 [Custom]', 6),
                      )

        self.grids = (('HRNTv2', 'HRNTv2'),
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

        found, text = hr_transformation(epsg, grid)
        if not found:
           raise QgsProcessingException(text)

        arguments = []

        if direction == 0:
            # Direct transformation
            arguments.append('-s_srs')
            arguments.append(text)
            arguments.append('-t_srs')
            arguments.append('EPSG:3765')
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:3765')
            arguments.append('-t_srs')
            arguments.append(text)

        arguments.append('-multi')
        arguments.append('-of')
        arguments.append(QgsRasterFileWriter.driverForExtension(os.path.splitext(outFile)[1]))
        arguments.append(inLayer.source())
        arguments.append(outFile)

        gridFile = os.path.join(pluginPath, 'grids', 'HRNTv2.gsb')
        if not os.path.isfile(gridFile):
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/hr/HRNTv2.gsb', gridFile)

        return ['gdalwarp', GdalUtils.escapeAndJoin(arguments)]
