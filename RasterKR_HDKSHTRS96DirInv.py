# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterKR_HDKSHTRS96DirInv.py
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


class RasterKR_HDKSHTRS96DirInv(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: Old Data -> HTRS96/Croatia TM [EPSG:3765]',
                      'Inverse: HTRS96/Croatia TM [EPSG:3765] -> Old Data']
    CRS = 'CRS'
    CRS_OPTIONS = ['HDKS5 [Custom]','HDKS6 [Custom]']

    GRID = 'GRID'
    GRID_OPTIONS = ['HRNTv2']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/hr.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[HR] Direct and inverse Raster Tranformation'
        self.group = '[HR] Croatia'
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
                # HDKS5
                if self.getParameterValue(self.GRID) == 0:
                    # HR_NTv2
                    arguments.append('+proj=tmerc +pm=greenwich +lat_0=0 +lon_0=15 +k=0.9999 +x_0=5500000 +y_0=0 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/HRNTv2.gsb +wktext +units=m')
            else:
                # HDKS6
                if self.getParameterValue(self.GRID) == 0:
                    # HR_NTv2
                    arguments.append('+proj=tmerc +pm=greenwich +lat_0=0 +lon_0=18 +k=0.9999 +x_0=6500000 +y_0=0 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/HRNTv2.gsb +wktext +units=m')
            arguments.append('-t_srs')
            arguments.append('EPSG:3765')
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:3765')
            arguments.append('-t_srs')
            if self.getParameterValue(self.CRS) == 0:
                # HDKS5
                if self.getParameterValue(self.GRID) == 0:
                    # HR_NTv2
                    arguments.append('+proj=tmerc +pm=greenwich +lat_0=0 +lon_0=15 +k=0.9999 +x_0=5500000 +y_0=0 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/HRNTv2.gsb +wktext +units=m')
            else:
                # HDKS6
                if self.getParameterValue(self.GRID) == 0:
                    # HR_NTv2
                    arguments.append('+proj=tmerc +pm=greenwich +lat_0=0 +lon_0=18 +k=0.9999 +x_0=6500000 +y_0=0 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/HRNTv2.gsb +wktext +units=m')

        arguments.append('-multi')
        arguments.append('-of')
        out = self.getOutputValue(self.OUTPUT)
        arguments.append(GdalUtils.getFormatShortNameFromFilename(out))
        arguments.append(self.getParameterValue(self.INPUT))
        arguments.append(out)

        if os.path.isfile(os.path.dirname(__file__) + '/grids/HRNTv2.gsb') is False:
            try:
                from urllib import urlretrieve
            except ImportError:
                from urllib.request import urlretrieve
            urlretrieve ("https://github.com/NaturalGIS/ntv2_transformations_grids_and_sample_data/raw/master/hr/HRNTv2.gsb", os.path.dirname(__file__) + "/grids/HRNTv2.gsb")

        GdalUtils.runGdal(['gdalwarp', GdalUtils.escapeAndJoin(arguments)],
                          progress)
