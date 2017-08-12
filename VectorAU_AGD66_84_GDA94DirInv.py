# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorAU_AGD66_84_GDA94_2020DirInv.py
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

import inspect
import os

from PyQt4.QtGui import QIcon

from processing.gui.Help2Html import getHtmlFromRstFile

try:
    from processing.parameters.ParameterVector import ParameterVector
    from processing.parameters.ParameterSelection import ParameterSelection
    from processing.outputs.OutputVector import OutputVector
except:
    from processing.core.parameters import ParameterVector
    from processing.core.parameters import ParameterSelection
    from processing.core.outputs import OutputVector

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils
from processing.tools.vector import ogrConnectionString, ogrLayerName

from transform_utilities import update_local_file

class VectorAU_AGD66_84_GDA94DirInv(GeoAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    OLD_CRS = 'OLD_CRS'
    NEW_CRS = 'NEW_CRS'
    ZONE = 'ZONE'

    AGD66GRID = os.path.dirname(__file__) + '/grids/A66_National_13_09_01.gsb'
    AGD84GRID = os.path.dirname(__file__) + '/grids/National_84_02_07_01.gsb'

    TRANSF_OPTIONS = ['Direct: Old CRS -> New CRS',
                      'Inverse: New CRS -> Old CRS']

    OLD_CRS_OPTIONS = [
        'AGD66 AMG [EPSG:202XX]',
        'AGD84 AMG [EPSG:203XX]',
        'AGD66 Latitude and Longitude [EPSG:4202]',
        'AGD84 Latitude and Longitude [EPSG:4203]',
    ]
    NEW_CRS_OPTIONS = [
        'GDA94 MGA [EPSG:283XX]',
        'GDA94 Latitude and Longitude [EPSG:4283]'
    ]
    ZONE_OPTIONS = [
        'n/a',
        '49',
        '50',
        '51',
        '52',
        '53',
        '54',
        '55',
        '56',
    ]

    OLD_CRS_STRINGS = {
        'AGD66 AMG [EPSG:202XX]': [
            '+proj=utm +zone=<ZONE> +south +ellps=aust_SA +units=m +no_defs +nadgrids=' + AGD66GRID + ' +wktext',
            'EPSG:202<ZONE>'
        ],
        'AGD84 AMG [EPSG:203XX]': [
            '+proj=utm +zone=<ZONE> +south +ellps=aust_SA +units=m +no_defs +nadgrids=' + AGD84GRID + ' +wktext',
            'EPSG:203<ZONE>'
        ],
        'AGD66 Latitude and Longitude [EPSG:4202]': [
            '+proj=longlat +ellps=aust_SA +no_defs +nadgrids=' + AGD66GRID + ' +wktext',
            'EPSG:4202'
        ],
        'AGD84 Latitude and Longitude [EPSG:4203]': [
            '+proj=longlat +ellps=aust_SA +no_defs +nadgrids=' + AGD84GRID + ' +wktext'
            'EPSG:4203'
        ]
    }
    NEW_CRS_STRINGS = {
        'GDA94 MGA [EPSG:283XX]': 'EPSG:283<ZONE>',
        'GDA94 Latitude and Longitude [EPSG:4283]': 'EPSG:4238'
    }

    def getIcon(self):
        return QIcon(os.path.dirname(__file__) + '/icons/au.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
            html = getHtmlFromRstFile(filename)
            return True, html
        except:
            return False, None

    def defineCharacteristics(self):
        self.name = '[AU] AGD66/84 to GDA94 Vector Direct and inverse'
        self.group = '[AU] Australia'
        self.addParameter(ParameterVector(self.INPUT, 'Input vector', [ParameterVector.VECTOR_TYPE_ANY]))
        self.addParameter(ParameterSelection(self.TRANSF, 'Transformation', self.TRANSF_OPTIONS))
        self.addParameter(ParameterSelection(self.OLD_CRS, 'Old CRS', self.OLD_CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.NEW_CRS, 'New CRS', self.NEW_CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.ZONE, 'UTM Zone', self.ZONE_OPTIONS))
        self.addOutput(OutputVector(self.OUTPUT, 'Output'))

    def processAlgorithm(self, progress):
        inLayer = self.getParameterValue(self.INPUT)
        conn = ogrConnectionString(inLayer)[1:-1]

        output = self.getOutputFromName(self.OUTPUT)
        outFile = output.value

        zone = self.ZONE_OPTIONS[self.getParameterValue(self.ZONE)]

        if zone == 'n/a':
            # Check we're doing lat/lon, or bail
            pass

        old_crs = self.OLD_CRS_OPTIONS[self.getParameterValue(self.OLD_CRS)]
        new_crs = self.NEW_CRS_OPTIONS[self.getParameterValue(self.NEW_CRS)]

        old_crs_epsg = self.OLD_CRS_STRINGS[old_crs][1].replace('<ZONE>', zone)
        new_crs_epsg = self.NEW_CRS_STRINGS[new_crs].replace('<ZONE>', zone)

        old_crs_string = self.OLD_CRS_STRINGS[old_crs][0].replace('<ZONE>', zone)

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            arguments.append(old_crs_string)
            arguments.append('-t_srs')
            arguments.append(new_crs_epsg)
            arguments.append('-f')
            arguments.append('ESRI Shapefile')
            arguments.append('-lco')
            arguments.append('ENCODING=UTF-8')
            arguments.append(outFile)
            arguments.append(conn)
            arguments.append(ogrLayerName(inLayer))
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append(new_crs_epsg)
            arguments.append('-t_srs')
            arguments.append(old_crs_string)
            arguments.append('-f')
            arguments.append('\"Geojson\"')
            arguments.append('/vsistdout/')
            arguments.append(conn)
            arguments.append(ogrLayerName(inLayer))
            arguments.append('|')
            arguments.append('ogr2ogr')
            arguments.append('-f')
            arguments.append('ESRI Shapefile')
            arguments.append('-a_srs')
            arguments.append(old_crs_epsg)
            arguments.append(outFile)
            arguments.append('/vsistdin/')
            arguments.append('-lco')
            arguments.append('ENCODING=UTF-8')

        if not os.path.isfile(self.AGD66GRID) or not os.path.isfile(self.AGD84GRID):
            print("DOWNLOADING GSB FILES")
            update_local_file("https://s3-ap-southeast-2.amazonaws.com/transformationgrids/A66_National_13_09_01.gsb", self.AGD66GRID)
            update_local_file("https://s3-ap-southeast-2.amazonaws.com/transformationgrids/National_84_02_07_01.gsb", self.AGD84GRID)

        commands = ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
