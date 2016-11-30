# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorUK_OSGB36ETRS89DirInv.py
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


class VectorUK_OSGB36ETRS89DirInv(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: Old Data -> ETRS89 [EPSG:4258]',
                      'Inverse: ETRS89 [EPSG:4258] -> Old Data']
    CRS = 'CRS'
    CRS_OPTIONS = ['OSGB 1936/British National Grid [EPSG:27700]']

    GRID = 'GRID'
    GRID_OPTIONS = ['OSTN02_NTv2']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/uk.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[UK] Direct and inverse Vector tranformation'
        self.group = '[UK] United Kingdom'
        self.addParameter(ParameterVector(self.INPUT, 'Input vector',
                          [ParameterVector.VECTOR_TYPE_ANY]))
        self.addParameter(ParameterSelection(self.TRANSF, 'Transformation',
                          self.TRANSF_OPTIONS))
        self.addParameter(ParameterSelection(self.CRS, 'Old Datum',
                          self.CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.GRID, 'Ntv2 Grid',
                          self.GRID_OPTIONS))
        self.addOutput(OutputVector(self.OUTPUT, 'Output'))

    def processAlgorithm(self, progress):
        inLayer = self.getParameterValue(self.INPUT)
        conn = ogrConnectionString(inLayer)[1:-1]

        output = self.getOutputFromName(self.OUTPUT)
        outFile = output.value

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            if self.getParameterValue(self.CRS) == 0:
                # GOSGB 1936/British National Grid
                if self.getParameterValue(self.GRID) == 0:
                    # OSTN02_NTv2
                    arguments.append('+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +nadgrids=' + os.path.dirname(__file__) + '/grids/OSTN02_NTv2.gsb +wktext +units=m +no_defs')
            arguments.append('-t_srs')
            arguments.append('EPSG:4258')

            arguments.append('-f')
            arguments.append('ESRI Shapefile')

            arguments.append(outFile)
            arguments.append(conn)
            arguments.append(ogrLayerName(inLayer))

        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:4258')
            arguments.append('-t_srs')
            if self.getParameterValue(self.CRS) == 0:
                # OSGB 1936/British National Grid
                if self.getParameterValue(self.GRID) == 0:
                    # OSTN02_NTv2
                    arguments.append('+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +nadgrids=' + os.path.dirname(__file__) + '/grids/OSTN02_NTv2.gsb +wktext +units=m +no_defs')
            arguments.append('-f')
            arguments.append('\"Geojson\"')
            arguments.append('/vsistdout/')
            arguments.append(conn)
            arguments.append(ogrLayerName(inLayer))
            arguments.append('-lco')
            arguments.append('ENCODING=UTF-8')
            arguments.append('|')
            arguments.append('ogr2ogr')
            arguments.append('-f')
            arguments.append('ESRI Shapefile')
            arguments.append('-a_srs')
            arguments.append('EPSG:27700')
            arguments.append(outFile)
            arguments.append('/vsistdin/')

        arguments.append('-lco')
        arguments.append('ENCODING=UTF-8')

        if os.path.isfile(os.path.dirname(__file__) + '/grids/OSTN02_NTv2.gsb') is False:
            try:
                from urllib import urlretrieve
            except ImportError:
                from urllib.request import urlretrieve
            urlretrieve ("https://github.com/NaturalGIS/ntv2_transformations_grids_and_sample_data/raw/master/uk/OSTN02_NTv2.gsb", os.path.dirname(__file__) + "/grids/OSTN02_NTv2.gsb")

        commands = ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
