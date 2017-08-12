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

from PyQt4.QtGui import QIcon

from processing.gui.Help2Html import getHtmlFromRstFile

try:
    from processing.parameters.ParameterRaster import ParameterRaster
    from processing.parameters.ParameterSelection import ParameterSelection
    from processing.outputs.OutputRaster import OutputRaster
except:
    from processing.core.parameters import ParameterRaster
    from processing.core.parameters import ParameterSelection
    from processing.core.outputs import OutputRaster

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils

from transform_utilities import update_local_file

from qgis.core import (QgsCoordinateReferenceSystem, QgsMessageLog)


class RasterAU_GDA94_2020DirInv(GeoAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    OLD_CRS = 'OLD_CRS'
    NEW_CRS = 'NEW_CRS'
    ZONE = 'ZONE'

    GDA2020CONF_DIST = os.path.dirname(__file__) + '/grids/GDA94_GDA2020_conformal_and_distortion.gsb'

    TRANSF_OPTIONS = ['Direct: Old CRS -> New CRS',
                      'Inverse: New CRS -> Old CRS']

    OLD_CRS_OPTIONS = [
        'GDA94 MGA [EPSG:283XX]',
        'GDA94 Latitude and Longitude [EPSG:4283]',
    ]
    NEW_CRS_OPTIONS = [
        'GDA2020 MGA [EPSG:327XX]',
        'GDA2020 Latitude and Longitude [EPSG:7844]'
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

    # Replace EPSGs are used to revert to WGS if the GDA2020 codes are unavailable
    REPLACE_EPSGS = {
        '78': '327',
        '7844': '4326'
    }

    OLD_CRS_STRINGS = {
        'GDA94 MGA [EPSG:283XX]': [
            '+proj=utm +zone=<ZONE> +south +ellps=GRS80 +units=m +no_defs +nadgrids=' + GDA2020CONF_DIST + ' +wktext',
            'EPSG:283<ZONE>'
        ],
        'GDA94 Latitude and Longitude [EPSG:4283]': [
            '+proj=longlat +ellps=GRS80 +no_defs +nadgrids=' + GDA2020CONF_DIST + ' +wktext',
            'EPSG:4283'
        ],
    }
    NEW_CRS_STRINGS = {
        'GDA2020 MGA [EPSG:327XX]': 'EPSG:78<ZONE>',  # 327 is the WGS alternative...
        'GDA2020 Latitude and Longitude [EPSG:7844]': 'EPSG:7844'
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

        old_crs_epsg = self.OLD_CRS_STRINGS[old_crs][1].replace('<ZONE>', zone)
        new_crs_epsg = self.NEW_CRS_STRINGS[new_crs].replace('<ZONE>', zone)

        old_crs_string = self.OLD_CRS_STRINGS[old_crs][0].replace('<ZONE>', zone)

        check_srs = QgsCoordinateReferenceSystem()
        new_epsg_int = int(new_crs_epsg.split(":")[1])

        if not check_srs.createFromId(new_epsg_int):
            # This means the new SRS is not available, and we should use a WGS based one
            if zone == 'n/a':
                zone = ''
            new_crs_epsg = new_crs_epsg.replace(str(new_epsg_int), self.REPLACE_EPSGS[str(new_epsg_int).replace(zone, '')] + zone)
            QgsMessageLog.logMessage(
                ("Couldn't find EPSG:{} in the list of available CRSs, update to a newer version of QGIS to enable it.\n"
                 "For now, the CRS is being set to a WGS alternative: {}".format(new_epsg_int, new_crs_epsg)),
                'Processing',
                QgsMessageLog.INFO
            )

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

        if not os.path.isfile(self.GDA2020CONF_DIST):
            print("DOWNLOADING GSB FILES")
            update_local_file("https://s3-ap-southeast-2.amazonaws.com/transformationgrids/GDA94_GDA2020_conformal_and_distortion.gsb", self.GDA2020CONF_DIST)

        commands = ['gdalwarp', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
