# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorES_ED50ERTS89DirInv.py
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
    from processing.parameters.ParameterVector import ParameterVector
    from processing.parameters.ParameterSelection import ParameterSelection
    from processing.outputs.OutputVector import OutputVector
except:
    from processing.core.parameters import ParameterVector
    from processing.core.parameters import ParameterSelection
    from processing.core.outputs import OutputVector

from processing.tools.system import *

from processing.algs.gdal.OgrAlgorithm import OgrAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils


class VectorES_ED50ERTS89DirInv(OgrAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: Old Data -> ETRS89 [EPSG:4258]',
                      'Inverse: ETRS89 [EPSG:4258] -> Old Data']
    CRS = 'CRS'
    CRS_OPTIONS = ['ED50/UTM 29N [EPSG:23029]',
                   'ED50/UTM 30N [EPSG:23030]',
                   'ED50/UTM 31N [EPSG:23031]']
    GRID = 'GRID'
    GRID_OPTIONS = ['PENR2009']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/es.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[ES] Direct and inverse Vector transformation'
        self.group = '[ES] Spain (mainland)'
        self.addParameter(ParameterVector(self.INPUT, 'Input vector',
                          [ParameterVector.VECTOR_TYPE_ANY]))
        self.addParameter(ParameterSelection(self.TRANSF, 'Transformation',
                          self.TRANSF_OPTIONS))
        self.addParameter(ParameterSelection(self.CRS, 'Old Datum',
                          self.CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.GRID, 'NTv2 Grid',
                          self.GRID_OPTIONS))
        self.addOutput(OutputVector(self.OUTPUT, 'Output'))

    def processAlgorithm(self, progress):
        inLayer = self.getParameterValue(self.INPUT)
        conn = self.ogrConnectionString(inLayer)

        output = self.getOutputFromName(self.OUTPUT)
        outFile = output.value

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            if self.getParameterValue(self.CRS) == 0:
                # ED50/UTM 29N [EPSG:23029]
                if self.getParameterValue(self.GRID) == 0:
                    # PENR2009
                    arguments.append('+proj=utm +zone=29 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/PENR2009.gsb +wktext +units=m +no_defs')
                    arguments.append('-t_srs')
                    arguments.append('EPSG:4258')
            elif self.getParameterValue(self.CRS) == 1:
                # ED50/UTM 30N [EPSG:23030]
                if self.getParameterValue(self.GRID) == 0:
                    # PENR2009
                    arguments.append('+proj=utm +zone=30 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/PENR2009.gsb +wktext +units=m +no_defs')
                    arguments.append('-t_srs')
                    arguments.append('EPSG:4258')
            elif self.getParameterValue(self.CRS) == 2:
                # ED50/UTM 31N [EPSG:23031]
                if self.getParameterValue(self.GRID) == 0:
                    # PENR2009
                    arguments.append('+proj=utm +zone=31 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/PENR2009.gsb +wktext +units=m +no_defs')
                    arguments.append('-t_srs')
                    arguments.append('EPSG:4258')
            arguments.append('-f')
            arguments.append('ESRI Shapefile')
     
            arguments.append(outFile)
            arguments.append(conn)

        else:
            # Inverse transformation
            arguments = ['-t_srs']
            if self.getParameterValue(self.CRS) == 0:
                # ED50/UTM 29N [EPSG:23029]
                if self.getParameterValue(self.GRID) == 0:
                    # PENR2009
                    arguments.append('+proj=utm +zone=29 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/PENR2009.gsb +wktext +units=m +no_defs')
                    arguments.append('-s_srs')
                    arguments.append('EPSG:4258')
                    arguments.append('-f')
                    arguments.append('\"Geojson\"')
                    arguments.append('/vsistdout/')
                    arguments.append(conn)
                    arguments.append('-lco') 
                    arguments.append('ENCODING=UTF-8')
                    arguments.append('|')
                    arguments.append('ogr2ogr')
                    arguments.append('-f')               
                    arguments.append('ESRI Shapefile') 
                    arguments.append('-a_srs') 
                    arguments.append('EPSG:23029') 
                    arguments.append(outFile)    
                    arguments.append('/vsistdin/')
            elif self.getParameterValue(self.CRS) == 1:
                # ED50/UTM 30N [EPSG:23030]
                if self.getParameterValue(self.GRID) == 0:
                    # PENR2009
                    arguments.append('+proj=utm +zone=30 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/PENR2009.gsb +wktext +units=m +no_defs')
                    arguments.append('-s_srs')
                    arguments.append('EPSG:4258')
                    arguments.append('-f')
                    arguments.append('\"Geojson\"')
                    arguments.append('/vsistdout/')
                    arguments.append(conn)
                    arguments.append('-lco') 
                    arguments.append('ENCODING=UTF-8')
                    arguments.append('|')
                    arguments.append('ogr2ogr')
                    arguments.append('-f')               
                    arguments.append('ESRI Shapefile') 
                    arguments.append('-a_srs') 
                    arguments.append('EPSG:23030') 
                    arguments.append(outFile)    
                    arguments.append('/vsistdin/')
            elif self.getParameterValue(self.CRS) == 2:
                # ED50/UTM 31N [EPSG:23031]
                if self.getParameterValue(self.GRID) == 0:
                    # PENR2009
                    arguments.append('+proj=utm +zone=31 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/PENR2009.gsb +wktext +units=m +no_defs')
                    arguments.append('-s_srs')
                    arguments.append('EPSG:4258')
                    arguments.append('-f')
                    arguments.append('\"Geojson\"')
                    arguments.append('/vsistdout/')
                    arguments.append(conn)
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
                    
        commands = ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
