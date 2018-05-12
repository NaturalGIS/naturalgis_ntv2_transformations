# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterAU_AGD66_84_GDA94_2020DirInv.py
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

from au_crs_definitions import (AGD66GRID, AGD84GRID, NEW_CRS_STRINGS,
                                OLD_CRS_STRINGS)
from processing.algs.gdal.GdalUtils import GdalUtils
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.gui.Help2Html import getHtmlFromRstFile
from PyQt4.QtGui import QIcon
from transform_utilities import update_local_file

try:
    from processing.parameters.ParameterRaster import ParameterRaster
    from processing.parameters.ParameterSelection import ParameterSelection
    from processing.outputs.OutputRaster import OutputRaster
except:
    from processing.core.parameters import ParameterRaster
    from processing.core.parameters import ParameterSelection
    from processing.core.outputs import OutputRaster


class RasterAU_AGD66_84_GDA94DirInv(GeoAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    OLD_CRS = 'OLD_CRS'
    NEW_CRS = 'NEW_CRS'
    ZONE = 'ZONE'

    TRANSF_OPTIONS = ['Direct: Old CRS -> New CRS',
                      'Inverse: New CRS -> Old CRS']

    OLD_CRS_OPTIONS = OLD_CRS_STRINGS.keys()
    NEW_CRS_OPTIONS = NEW_CRS_STRINGS.keys()
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
        self.name = '[AU] AGD66/84 to GDA94 Raster Direct and inverse'
        self.group = '[AU] Australia'
        self.addParameter(ParameterRaster(self.INPUT, 'Input raster', False))
        self.addParameter(ParameterSelection(self.TRANSF, 'Transformation', self.TRANSF_OPTIONS))
        self.addParameter(ParameterSelection(self.OLD_CRS, 'Old CRS', self.OLD_CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.NEW_CRS, 'New CRS', self.NEW_CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.ZONE, 'UTM Zone', self.ZONE_OPTIONS))
        self.addOutput(OutputRaster(self.OUTPUT, 'Output'))

    def processAlgorithm(self, progress):

        zone = self.ZONE_OPTIONS[self.getParameterValue(self.ZONE)]

        if zone == 'n/a':
            # Check we're doing lat/lon, or bail
            pass

        old_crs = self.OLD_CRS_OPTIONS[self.getParameterValue(self.OLD_CRS)]
        new_crs = self.NEW_CRS_OPTIONS[self.getParameterValue(self.NEW_CRS)]

        old_crs_epsg = OLD_CRS_STRINGS[old_crs][1].format(zone=zone)
        new_crs_epsg = NEW_CRS_STRINGS[new_crs].format(zone=zone)

        old_crs_string = OLD_CRS_STRINGS[old_crs][0].format(zone=zone)

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            arguments.append(old_crs_string)
            arguments.append('-t_srs')
            arguments.append(new_crs_epsg)
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append(new_crs_epsg)
            arguments.append('-t_srs')
            arguments.append(old_crs_string)

        arguments.append('-multi')
        arguments.append('-of')
        out = self.getOutputValue(self.OUTPUT)
        arguments.append(GdalUtils.getFormatShortNameFromFilename(out))
        arguments.append(self.getParameterValue(self.INPUT))
        arguments.append(out)

        # Set the EPSG string when we aren't using one to define the target
        if self.getParameterValue(self.TRANSF) == 1:
            arguments.append('&&')
            arguments.append('gdal_edit.py')
            arguments.append('-a_srs')
            arguments.append(old_crs_epsg)
            arguments.append(out)

        if not os.path.isfile(AGD66GRID) or not os.path.isfile(AGD84GRID):
            print("DOWNLOADING GSB FILES")
            update_local_file("http://www.naturalgis.pt/downloads/ntv2grids/au/A66_National_13_09_01.gsb", AGD66GRID)
            update_local_file("http://www.naturalgis.pt/downloads/ntv2grids/au/National_84_02_07_01.gsb", AGD84GRID)

        commands = ['gdalwarp', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
