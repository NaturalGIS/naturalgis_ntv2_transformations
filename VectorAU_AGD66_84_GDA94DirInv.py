# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorAU_AGD66_84_GDA94DirInv.py
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

from qgis.core import (QgsProcessingException,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterVectorDestination
                      )

from processing.algs.gdal.GdalAlgorithm import GdalAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils

from ntv2_transformations.transformations import au_transformation_agd

pluginPath = os.path.dirname(__file__)


class VectorAU_AGD66_84_GDA94DirInv(GdalAlgorithm):

    INPUT = 'INPUT'
    TRANSF = 'TRANSF'
    SRC_CRS = 'SRC_CRS'
    DST_CRS = 'DST_CRS'
    ZONE = 'ZONE'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'auvectortransformagd'

    def displayName(self):
        return '[AU] AGD66/84 to GDA94 Direct and inverse Vector Transformation'

    def group(self):
        return '[AU] Australia'

    def groupId(self):
        return 'australia'

    def tags(self):
        return 'vector,grid,ntv2,direct,inverse,australia'.split(',')

    def shortHelpString(self):
        return 'Direct and inverse vector transformations using Australia NTv2 grids.'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'au.png'))

    def initAlgorithm(self, config=None):
        self.directions = ['Direct: Old CRS -> New CRS',
                           'Inverse: New CRS -> Old CRS'
                          ]

        self.src_datums = (('AGD66 AMG [EPSG:202XX]', 202),
                           ('AGD66 Latitude and Longitude [EPSG:4202]', 4202),
                           ('AGD84 AMG [EPSG:203XX]', 203),
                           ('AGD84 Latitude and Longitude [EPSG:4203]', 4203),
                           ('GDA94 MGA [EPSG:283XX]', 283),
                           ('GDA94 Latitude and Longitude [EPSG:4283]', 4283),
                          )

        self.dst_datums = (('GDA94 MGA [EPSG:283XX]', 283),
                           ('GDA94 Latitude and Longitude [EPSG:4283]', 4283),
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

        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              'Input vector'))
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
        self.addParameter(QgsProcessingParameterVectorDestination(self.OUTPUT,
                                                                  'Output'))

    def getConsoleCommands(self, parameters, context, feedback, executing=True):
        ogrLayer, layerName = self.getOgrCompatibleSource(self.INPUT, parameters, context, feedback, executing)
        outFile = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        self.setOutputValue(self.OUTPUT, outFile)

        output, outputFormat = GdalUtils.ogrConnectionStringAndFormat(outFile, context)
        if outputFormat in ('SQLite', 'GPKG') and os.path.isfile(output):
            raise QgsProcessingException('Output file "{}" already exists.'.format(output))

        direction = self.parameterAsEnum(parameters, self.TRANSF, context)
        src_crs = self.src_datums[self.parameterAsEnum(parameters, self.SRC_CRS, context)][1]
        dst_crs = self.dst_datums[self.parameterAsEnum(parameters, self.DST_CRS, context)][1]

        v = self.parameterAsEnum(parameters, self.ZONE, context)
        zone = '' if v == 0  else self.zones[v]

        found, text = au_transformation_agd(src_crs, zone)
        if not found:
           raise QgsProcessingException(text)

        arguments = []

        if direction == 0:
            # Direct transformation
            arguments = ['-s_srs']
            arguments.append(text)
            arguments.append('-t_srs')
            arguments.append('EPSG:{}{}'.format(dst_crs, zone))
            arguments.append('-f {}'.format(outputFormat))
            arguments.append('-lco')
            arguments.append('ENCODING=UTF-8')
            arguments.append(output)
            arguments.append(ogrLayer)
            arguments.append(layerName)
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:{}{}'.format(dst_crs, zone))
            arguments.append('-t_srs')
            arguments.append(text)
            arguments.append('-f')
            arguments.append('Geojson')
            arguments.append('/vsistdout/')
            arguments.append(ogrLayer)
            arguments.append(layerName)
            arguments.append('|')
            arguments.append('ogr2ogr')
            arguments.append('-f {}'.format(outputFormat))
            arguments.append('-a_srs')
            arguments.append('EPSG:{}{}'.format(src_crs, zone))
            arguments.append(output)
            arguments.append('/vsistdin/')
            arguments.append('-lco')
            arguments.append('ENCODING=UTF-8')

        if not os.path.isfile(os.path.join(pluginPath, 'grids', 'A66_National_13_09_01.gsb')):
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/au/A66_National_13_09_01.gsb', os.path.join(pluginPath, 'grids', 'A66_National_13_09_01.gsb'))
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/au/National_84_02_07_01.gsb', os.path.join(pluginPath, 'grids', 'National_84_02_07_01.gsb'))

        return ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
