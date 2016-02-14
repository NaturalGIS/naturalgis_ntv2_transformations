# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorCAT_ED50ETRS89DirInv.py
    ---------------------
    Date                 : July 2015
    Copyright            : (C) 2015 by Carlos López (PSIG)
    Email                : carlos dot lopez at psig dot es
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Carlos López (PSIG)'
__date__ = 'July 2015'
__copyright__ = '(C) 2015, Carlos López (PSIG)'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import inspect
import os

from PyQt4.QtGui import *

from qgis.core import *

from processing.gui.Help2Html import getHtmlFromRstFile

try:
    from processing.parameters.ParameterVector import ParameterVector
    from processing.parameters.ParameterSelection import ParameterSelection
    from processing.outputs.OutputVector import OutputVector
except:
    from processing.core.parameters import ParameterVector
    from processing.core.parameters import ParameterSelection
    from processing.core.outputs import OutputVector

from processing.tools.system import *

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils
from processing.tools.vector import ogrConnectionString, ogrLayerName


class VectorCAT_ED50ETRS89DirInv(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: Old Data -> ETRS89 UTM 31N [EPSG:25831]',
                      'Inverse: ETRS89 UTM 31N [EPSG:25831] -> Old Data']
    CRS = 'CRS'
    CRS_OPTIONS = ['ED50/UTM 31N [EPSG:23031]']

    GRID = 'GRID'
    GRID_OPTIONS = ['100800401']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/cat.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[CAT] Direct and inverse Vector tranformation'
        self.group = '[CAT] Catalonia'
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
                # ED50/UTM 31N [EPSG:23031]
                if self.getParameterValue(self.GRID) == 0:
                    # 100800401
                    arguments.append('+proj=utm +zone=31 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/100800401.gsb +wktext +units=m +no_defs')
            arguments.append('-t_srs')
            arguments.append('EPSG:25831')

            arguments.append('-f')
            arguments.append('ESRI Shapefile')

            arguments.append(outFile)
            arguments.append(conn)
            arguments.append(ogrLayerName(inLayer))

        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:25831')
            arguments.append('-t_srs')
            if self.getParameterValue(self.CRS) == 0:
                # ED50/UTM 31N [EPSG:23031]
                if self.getParameterValue(self.GRID) == 0:
                    # 100800401
                    arguments.append('+proj=utm +zone=31 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/100800401.gsb +wktext +units=m +no_defs')
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
            arguments.append('EPSG:23031') 
            arguments.append(outFile)    
            arguments.append('/vsistdin/')

        arguments.append('-lco') 
        arguments.append('ENCODING=UTF-8')

        if os.path.isfile(os.path.dirname(__file__) + '/grids/100800401.gsb') is False:
           import urllib
           urllib.urlretrieve ("https://github.com/NaturalGIS/ntv2_transformations_grids_and_sample_data/raw/master/cat/100800401.gsb", os.path.dirname(__file__) + "/grids/100800401.gsb")

        commands = ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
