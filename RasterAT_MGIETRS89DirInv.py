# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterAT_MGIETRS89DirInv.py
    ---------------------
    Date                 : October 2015
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
__date__ = 'October 2015'
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


class RasterAT_MGIETRS89DirInv(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: Old Data -> ETRS89 [EPSG:4258]',
                      'Inverse: ETRS89 [EPSG:4258] -> Old Data']
    CRS = 'CRS'
    CRS_OPTIONS = ['MGI [EPSG:4312]',
                   'MGI/Austria GK west [EPSG:31254]',
                   'MGI/Austria GK central [EPSG:31255]',
                   'MGI/Austria GK east [EPSG:31256]',
                   'MGI/Austria GK M28 [EPSG:31257]',
                   'MGI/Austria GK M31 [EPSG:31258]',
                   'MGI/Austria GK M34 [EPSG:31259]']

    GRID = 'GRID'
    GRID_OPTIONS = ['AT_GIS_GRID']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/at.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[AT] Direct and inverse Raster Tranformation'
        self.group = '[AT] Austria'
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
                # MGI
                ['+proj=longlat +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/AT_GIS_GRID.gsb +wktext +no_defs']
            ],
            [
                # MGI/Austria GK west
                ['+proj=tmerc +lat_0=0 +lon_0=10.33333333333333 +k=1 +x_0=0 +y_0=-5000000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/AT_GIS_GRID.gsb +wktext +units=m +no_defs']
            ],
            [
                # MGI/Austria GK central
                ['+proj=tmerc +lat_0=0 +lon_0=13.33333333333333 +k=1 +x_0=0 +y_0=-5000000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/AT_GIS_GRID.gsb +wktext +units=m +no_defs']
            ],
            [
                # MGI/Austria GK east
                ['+proj=tmerc +lat_0=0 +lon_0=16.33333333333333 +k=1 +x_0=0 +y_0=-5000000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/AT_GIS_GRID.gsb +wktext +units=m +no_defs']
            ],
            [
                # MGI/Austria GK M28
                ['+proj=tmerc +lat_0=0 +lon_0=10.33333333333333 +k=1 +x_0=150000 +y_0=-5000000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/AT_GIS_GRID.gsb +wktext +units=m +no_defs']
            ],
            [
                # MGI/Austria GK M31
                ['+proj=tmerc +lat_0=0 +lon_0=13.33333333333333 +k=1 +x_0=450000 +y_0=-5000000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/AT_GIS_GRID.gsb +wktext +units=m +no_defs']
            ],
            [
                # MGI/Austria GK M34
                ['+proj=tmerc +lat_0=0 +lon_0=16.33333333333333 +k=1 +x_0=750000 +y_0=-5000000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/AT_GIS_GRID.gsb +wktext +units=m +no_defs']
            ]
        ]         

    def processAlgorithm(self, progress):
      
        doTransf = self.transfList()      

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            arguments.append(str(doTransf[self.getParameterValue(self.CRS)][self.getParameterValue(self.GRID)])[2:-2])
            arguments.append('-t_srs')
            arguments.append('EPSG:4258')
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:4258')
            arguments.append('-t_srs')
            arguments.append(str(doTransf[self.getParameterValue(self.CRS)][self.getParameterValue(self.GRID)])[2:-2])

        arguments.append('-multi')
        arguments.append('-of')
        out = self.getOutputValue(self.OUTPUT)
        arguments.append(GdalUtils.getFormatShortNameFromFilename(out))
        arguments.append(self.getParameterValue(self.INPUT))
        arguments.append(out)

        if os.path.isfile(os.path.dirname(__file__) + '/grids/AT_GIS_GRID.gsb') is False:
           import urllib
           urllib.urlretrieve ("https://github.com/NaturalGIS/ntv2_transformations_grids_and_sample_data/raw/master/at/AT_GIS_GRID.gsb", os.path.dirname(__file__) + "/grids/AT_GIS_GRID.gsb")

        GdalUtils.runGdal(['gdalwarp', GdalUtils.escapeAndJoin(arguments)],
                          progress)
