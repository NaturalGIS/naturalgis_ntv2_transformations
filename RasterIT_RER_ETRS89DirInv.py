# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterIT_RER_ETRS89DirInv.py
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


class RasterIT_RER_ETRS89DirInv(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: Old Data -> ETRS89 [EPSG:4258]',
                      'Inverse: ETRS89 [EPSG:4258] -> Old Data']
    CRS = 'CRS'
    CRS_OPTIONS = ['Monte Mario - GBO [EPSG:3003]',
                  'UTM - ED50 [EPSG:23032]']

    GRID = 'GRID'
    GRID_OPTIONS = ['Grigliati NTv2 RER 2013 la trasformazione di coordinate in Emilia-Romagna']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/it.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[IT] Direct and inverse Raster transformation'
        self.group = '[IT] Italy (Emilia-Romagna)'
        self.addParameter(ParameterRaster(self.INPUT, 'Input raster', False))
        self.addParameter(ParameterSelection(self.TRANSF, 'Transformation',
                          self.TRANSF_OPTIONS))
        self.addParameter(ParameterSelection(self.CRS, 'Old Datum',
                          self.CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.GRID, 'NTv2 Grid',
                          self.GRID_OPTIONS))
        self.addOutput(OutputRaster(self.OUTPUT, 'Output'))

    def processAlgorithm(self, progress):

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            if self.getParameterValue(self.CRS) == 0:
                # Monte Mario - GBO
                if self.getParameterValue(self.GRID) == 0:
                    # Grigliati NTv2 RER 2013 la trasformazione di coordinate in Emilia-Romagna
                    arguments.append('+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=1500000 +y_0=0 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/RER_AD400_MM_ETRS89_V1A.gsb +wktext +units=m +no_defs')
            else:
                # UTM - ED50
                if self.getParameterValue(self.GRID) == 0:
                    # Grigliati NTv2 RER 2013 la trasformazione di coordinate in Emilia-Romagna
                    arguments.append('+proj=utm +zone=32 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/RER_ED50_ETRS89_GPS7_K2.gsb +wktext +units=m +no_defs')
            arguments.append('-t_srs')
            arguments.append('EPSG:4258')
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:4258')
            arguments.append('-t_srs')
            if self.getParameterValue(self.CRS) == 0:
                # Monte Mario - GBO
                if self.getParameterValue(self.GRID) == 0:
                    # Grigliati NTv2 RER 2013 la trasformazione di coordinate in Emilia-Romagna
                    arguments.append('+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=1500000 +y_0=0 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/RER_AD400_MM_ETRS89_V1A.gsb +wktext +units=m +no_defs')
            else:
                # UTM - ED50
                if self.getParameterValue(self.GRID) == 0:
                    # Grigliati NTv2 RER 2013 la trasformazione di coordinate in Emilia-Romagna
                    arguments.append('+proj=utm +zone=32 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/RER_ED50_ETRS89_GPS7_K2.gsb +wktext +units=m +no_defs')

        arguments.append('-multi')
        arguments.append('-of')
        out = self.getOutputValue(self.OUTPUT)
        arguments.append(GdalUtils.getFormatShortNameFromFilename(out))
        arguments.append(self.getParameterValue(self.INPUT))
        arguments.append(out)

        if os.path.isfile(os.path.dirname(__file__) + '/grids/RER_AD400_MM_ETRS89_V1A.gsb') is False:
           import urllib
           urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/it_rer/RER_AD400_MM_ETRS89_V1A.gsb", os.path.dirname(__file__) + "/grids/RER_AD400_MM_ETRS89_V1A.gsb")
           urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/it_rer/RER_ED50_ETRS89_GPS7_K2.GSB", os.path.dirname(__file__) + "/grids/RER_ED50_ETRS89_GPS7_K2.GSB")

        GdalUtils.runGdal(['gdalwarp', GdalUtils.escapeAndJoin(arguments)],
                          progress)
