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

from au_crs_definitions import (GDA2020CONF, GDA2020CONF_DIST, NEW_CRS_STRINGS_2020,
                                OLD_CRS_STRINGS_2020)
from processing.algs.gdal.GdalUtils import GdalUtils
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.gui.Help2Html import getHtmlFromRstFile
from PyQt4.QtGui import QIcon
from transform_utilities import update_local_file, log

try:
    from processing.parameters.ParameterRaster import ParameterRaster
    from processing.parameters.ParameterSelection import ParameterSelection
    from processing.outputs.OutputRaster import OutputRaster
except:
    from processing.core.parameters import ParameterRaster
    from processing.core.parameters import ParameterSelection
    from processing.core.outputs import OutputRaster


class RasterAU_GDA94_2020DirInv(GeoAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    OLD_CRS = 'OLD_CRS'
    NEW_CRS = 'NEW_CRS'
    ZONE = 'ZONE'

    TRANSF_OPTIONS = ['Direct: Old CRS -> New CRS',
                      'Inverse: New CRS -> Old CRS']

    OLD_CRS_OPTIONS = OLD_CRS_STRINGS_2020.keys()
    NEW_CRS_OPTIONS = NEW_CRS_STRINGS_2020.keys()
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
        self.name = '[AU] GDA94 to GDA2020 Raster Direct and inverse'
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

        old_crs_epsg = OLD_CRS_STRINGS_2020[old_crs][1].format(zone=zone)
        new_crs_epsg = NEW_CRS_STRINGS_2020[new_crs][1].format(zone=zone)

        old_crs_string = OLD_CRS_STRINGS_2020[old_crs][0].format(zone=zone)
        new_crs_string = NEW_CRS_STRINGS_2020[new_crs][0].format(zone=zone)

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            arguments.append(old_crs_string)
            arguments.append('-t_srs')
            arguments.append(new_crs_string)
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append(new_crs_string)
            arguments.append('-t_srs')
            arguments.append(old_crs_string)

        arguments.append('-multi')
        arguments.append('-of')
        out = self.getOutputValue(self.OUTPUT)
        arguments.append(GdalUtils.getFormatShortNameFromFilename(out))
        arguments.append(self.getParameterValue(self.INPUT))
        arguments.append(out)

        # Set the EPSG code
        arguments.append('&&')
        arguments.append('gdal_edit.py')
        arguments.append('-a_srs')
        if self.getParameterValue(self.TRANSF) == 0:
            # Direct
            arguments.append(new_crs_epsg)
        else:
            # Inverse
            arguments.append(old_crs_epsg)
        arguments.append(out)

        if not os.path.isfile(GDA2020CONF_DIST) or not os.path.isfile(GDA2020CONF):
            log("Downloading files")
            update_local_file("https://s3-ap-southeast-2.amazonaws.com/transformation-grids/GDA94_GDA2020_conformal.gsb", GDA2020CONF)
            update_local_file("https://s3-ap-southeast-2.amazonaws.com/transformation-grids/GDA94_GDA2020_conformal_and_distortion.gsb", GDA2020CONF_DIST)

        commands = ['gdalwarp', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
