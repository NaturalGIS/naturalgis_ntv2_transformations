# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterAU_GDA94_2020DirInv.py
    ---------------------
    Date                 : March 2017
    Copyright            : (C) 2017 by Alex Leith and Giovanni Manghi
    Email                : alex at auspatious dot  com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alex Leith'
__date__ = 'March 2017'
__copyright__ = '(C) 2017, Alex Leith and Giovanni Manghi'

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

from ntv2_transformations.transformations import au_transformation_gda

pluginPath = os.path.dirname(__file__)


class RasterAU_GDA94_2020DirInv(GdalAlgorithm):

    INPUT = 'INPUT'
    TRANSF = 'TRANSF'
    SRC_CRS = 'SRC_CRS'
    DST_CRS = 'DST_CRS'
    ZONE = 'ZONE'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'aurastertransformgda'

    def displayName(self):
        return '[AU] GDA94 to GDA2020 Direct and inverse Raster Tranformation'

    def group(self):
        return '[AU] Australia'

    def groupId(self):
        return 'australia'

    def tags(self):
        return 'raster,grid,ntv2,direct,inverse,australia'.split(',')

    def shortHelpString(self):
        return 'Direct and inverse raster tranformations using Australia NTv2 grids.'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'au.png'))

    def initAlgorithm(self, config=None):
        self.directions = ['Direct: Old CRS -> New CRS',
                           'Inverse: New CRS -> Old CRS'
                          ]

        self.src_datums = (('GDA94 MGA [EPSG:283XX] (Conformal only)', '283'),
                           ('GDA94 Latitude and Longitude [EPSG:4283] (Conformal only)', '4283'),
                           ('GDA94 MGA [EPSG:283XX] (Conformal and Distortion)', '283cd'),
                           ('GDA94 Latitude and Longitude [EPSG:4283] (Conformal and Distortion)', '4283cd'),
                          )

        self.dst_datums = (('GDA2020 MGA [EPSG:78XX]', 78),
                           ('GDA2020 Latitude and Longitude [EPSG:7844]', 7844),
                          )

        self.zones = ['n/a',
                      '49',
                      '50',
                      '51',
                      '52',
                      '53',
                      '54',
                      '55',
                      '56']

        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT,
                                                            'Input raster'))
        self.addParameter(QgsProcessingParameterEnum(self.TRANSF,
                                                     'Transformation',
                                                     options=self.directions,
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.SRC_CRS,
                                                     'Old CRS',
                                                     options=[i[0] for i in self.src_datums],
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.DST_CRS,
                                                     'New CRS',
                                                     options=[i[0] for i in self.dst_datums],
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.ZONE,
                                                     'UTM Zone',
                                                     options=self.zones,
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
        src_crs = self.src_datums[self.parameterAsEnum(parameters, self.SRC_CRS, context)][1]
        dst_crs = self.dst_datums[self.parameterAsEnum(parameters, self.DST_CRS, context)][1]

        v = self.parameterAsEnum(parameters, self.ZONE, context)
        zone = '' if v == 0  else self.zones[v]

        old, new = au_transformation_gda(src_crs, dst_crs, zone)

        arguments = []

        if direction == 0:
            # Direct transformation
            arguments.append('-s_srs')
            arguments.append(old[0])
            arguments.append('-t_srs')
            arguments.append(new[0])
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append(new[0])
            arguments.append('-t_srs')
            arguments.append(old[0])

        arguments.append('-multi')
        arguments.append('-of')
        arguments.append(QgsRasterFileWriter.driverForExtension(os.path.splitext(outFile)[1]))
        arguments.append(inLayer.source())
        arguments.append(outFile)

        arguments.append('&&')
        arguments.append('gdal_edit.py')
        arguments.append('-a_srs')
        if direction == 0:
            arguments.append(new[1])
        else:
            arguments.append(old[1])
        arguments.append(outFile)

        if not os.path.isfile(os.path.join(pluginPath, 'grids', 'GDA94_GDA2020_conformal.gsb')):
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/au/GDA94_GDA2020_conformal.gsb', os.path.join(pluginPath, 'grids', 'GDA94_GDA2020_conformal.gsb'))
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/au/GDA94_GDA2020_conformal_and_distortion.gsb', os.path.join(pluginPath, 'grids', 'GDA94_GDA2020_conformal_and_distortion.gsb'))

        return ['gdalwarp', GdalUtils.escapeAndJoin(arguments)]
