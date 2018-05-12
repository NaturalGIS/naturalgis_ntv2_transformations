# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterPT_ETR89PTTM06DirInv.py
    ---------------------
    Date                 : March 2015
    Copyright            : (C) 2015 by Giovanni Manghi
    Email                : giovanni dot manghi at naturalgis dot pt
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
    Code refactor - epsg strings as list
    ------------------------------------
    Date                 : August 2015
    Copyright            : (C) 2015 by Fernando Ribeiro aka The Geocrafter
    Email                : fernandinand at gmail dot com
***************************************************************************
"""

__author__ = 'Giovanni Manghi'
__date__ = 'March 2015'
__copyright__ = '(C) 2015, Giovanni Manghi'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import inspect
import os

from PyQt4.QtGui import *

from qgis.core import *

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


class RasterPT_ETR89PTTM06DirInv(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: Old Data -> PT-TM06/ETRS89 [EPSG:3763]',
                      'Inverse: PT-TM06/ETRS89 [EPSG:3763] -> Old Data']
    CRS = 'CRS'
    CRS_OPTIONS = ['Datum Lisboa [EPSG:20791/EPSG:5018/ESRI:102165]',
                   'Datum Lisboa Militar [EPSG:20790/ESRI:102164]',
                   'Datum 73 [EPSG:27493/ESRI:102161]',
                   'Datum 73 Militar [ESRI:102160]',
                   u'ED50 UTM 29N [EPSG:23029] (Only grid from José Alberto Gonçalves)']
    GRID = 'GRID'
    GRID_OPTIONS = [u'José Alberto Gonçalves',
                    u'Direção-Geral do Territorio']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/pt.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[PT] Direct and inverse Raster Tranformation'
        self.group = '[PT] Portugal (mainland)'
        self.addParameter(ParameterRaster(self.INPUT, 'Input raster', False))
        self.addParameter(ParameterSelection(self.TRANSF, 'Transformation',
                          self.TRANSF_OPTIONS))
        self.addParameter(ParameterSelection(self.CRS, 'Old Datum',
                          self.CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.GRID, 'NTv2 Grid',
                          self.GRID_OPTIONS))
        self.addOutput(OutputRaster(self.OUTPUT, 'Output'))

    def transfList(self):
        return [
            [
                # Datum Lisboa
                ['+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=0 +y_0=0 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/ptLX_e89.gsb +wktext +pm=lisbon +units=m +no_defs'],
                ['+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=0 +y_0=0 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/DLX_ETRS89_geo.gsb +wktext +pm=lisbon +units=m +no_defs']
            ],
            [
                # Datum Lisboa Militar
                ['+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=200000 +y_0=300000 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/ptLX_e89.gsb +wktext +pm=lisbon +units=m +no_defs'],
                ['+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=200000 +y_0=300000 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/DLX_ETRS89_geo.gsb +wktext +pm=lisbon +units=m +no_defs']
            ],
            [
                # Datum 73
                ['+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=180.598 +y_0=-86.99 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/pt73_e89.gsb +wktext +units=m +no_defs'],
                ['+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=180.598 +y_0=-86.99 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/D73_ETRS89_geo.gsb +wktext +units=m +no_defs']
            ],
            [
                # Datum 73 Militar
                ['+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=200180.598 +y_0=299913.01 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/pt73_e89.gsb +wktext +units=m +no_defs'],
                ['+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=200180.598 +y_0=299913.01 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/D73_ETRS89_geo.gsb +wktext +units=m +no_defs']
            ],
            [
                # ED50 UTM 29N - Jose Alberto Goncalves
                ['+proj=utm +zone=29 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/ptED_e89.gsb +wktext +units=m +no_defs'],
                # Duplicate here...GUI not safe!
                ['+proj=utm +zone=29 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/ptED_e89.gsb +wktext +units=m +no_defs']
            ]
        ]

    def processAlgorithm(self, progress):

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            arguments.append(str(self.transfList()[self.getParameterValue(self.CRS)][self.getParameterValue(self.GRID)])[2:-2])
            arguments.append('-t_srs')
            arguments.append('EPSG:3763')
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:3763')
            arguments.append('-t_srs')
            arguments.append(str(self.transfList()[self.getParameterValue(self.CRS)][self.getParameterValue(self.GRID)])[2:-2])

        arguments.append('-multi')
        arguments.append('-of')
        out = self.getOutputValue(self.OUTPUT)
        arguments.append(GdalUtils.getFormatShortNameFromFilename(out))
        arguments.append(self.getParameterValue(self.INPUT))
        arguments.append(out)

        if os.path.isfile(os.path.dirname(__file__) + '/grids/pt73_e89.gsb') is False:
           import urllib
           urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/pt/pt73_e89.gsb", os.path.dirname(__file__) + "/grids/pt73_e89.gsb")
           urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/pt/ptED_e89.gsb", os.path.dirname(__file__) + "/grids/ptED_e89.gsb")
           urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/pt/ptLB_e89.gsb", os.path.dirname(__file__) + "/grids/ptLB_e89.gsb")
           urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/pt/ptLX_e89.gsb", os.path.dirname(__file__) + "/grids/ptLX_e89.gsb")
           urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/pt/D73_ETRS89_geo.gsb", os.path.dirname(__file__) + "/grids/D73_ETRS89_geo.gsb")
           urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/pt/DLX_ETRS89_geo.gsb", os.path.dirname(__file__) + "/grids/DLX_ETRS89_geo.gsb")

        GdalUtils.runGdal(['gdalwarp', GdalUtils.escapeAndJoin(arguments)],
                          progress)
