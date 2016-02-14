# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorCH_LV95ETRS89DirInv.py
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

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils
from processing.tools.vector import ogrConnectionString, ogrLayerName


class VectorCH_LV95ETRS89DirInv(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: CH1903 [EPSG:21781] -> New Data',
                      'Inverse: New Data -> CH1903 [EPSG:21781]']
    CRS = 'CRS'
    CRS_OPTIONS = ['ETRS89 [EPSG:4258]',
		   'CH1903+ [EPSG:2056]']

    GRID = 'GRID'
    GRID_OPTIONS = ['CHENyx06']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/ch.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[CH] Direct and inverse Vector transformation'
        self.group = '[CH] Switzerland'
        self.addParameter(ParameterVector(self.INPUT, 'Input vector',
                          [ParameterVector.VECTOR_TYPE_ANY]))
        self.addParameter(ParameterSelection(self.TRANSF, 'Transformation',
                          self.TRANSF_OPTIONS))
        self.addParameter(ParameterSelection(self.CRS, 'New Datum',
                          self.CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.GRID, 'NTv2 Grid',
                          self.GRID_OPTIONS))
        self.addOutput(OutputVector(self.OUTPUT, 'Output'))

    def processAlgorithm(self, progress):
        inLayer = self.getParameterValue(self.INPUT)
        conn = ogrConnectionString(inLayer)[1:-1]

        output = self.getOutputFromName(self.OUTPUT)
        outFile = output.value

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-t_srs']
            if self.getParameterValue(self.CRS) == 0:
               #untested
               arguments.append('EPSG:4258')
               gridname = 'chenyx06etrs.gsb' 
               arguments.append('-s_srs')
               arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/' + gridname + ' +wktext +units=m +no_defs')
               arguments.append('-f')
               arguments.append('ESRI Shapefile')
               arguments.append(outFile)
               arguments.append(conn)
               arguments.append(ogrLayerName(inLayer))
            else:
               arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +nadgrids=@null +wktext +units=m')
               gridname = 'CHENYX06a.gsb'                   
               arguments.append('-s_srs')
               arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/' + gridname + ' +wktext +units=m +no_defs')
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
               arguments.append('EPSG:2056') 
               arguments.append(outFile)    
               arguments.append('/vsistdin/') 
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            if self.getParameterValue(self.CRS) == 0:
               #untested
               arguments.append('EPSG:4258')
               gridname = 'chenyx06etrs.gsb' 
               arguments.append('-t_srs')
               arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/' + gridname + ' +wktext +units=m +no_defs')
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
               arguments.append('EPSG:21781') 
               arguments.append(outFile)    
               arguments.append('/vsistdin/')
            else:
               gridname = 'CHENYX06a.gsb' 
               arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +nadgrids=@null +wktext +units=m')
               arguments.append('-t_srs')
               arguments.append('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/' + gridname + ' +wktext +units=m +no_defs')                  
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
               arguments.append('EPSG:21781') 
               arguments.append(outFile)    
               arguments.append('/vsistdin/')

        arguments.append('-lco') 
        arguments.append('ENCODING=UTF-8')
               
        if os.path.isfile(os.path.dirname(__file__) + '/grids/CHENYX06a.gsb') is False:
           import urllib
           urllib.urlretrieve ("https://github.com/NaturalGIS/ntv2_transformations_grids_and_sample_data/raw/master/ch/CHENYX06a.gsb", os.path.dirname(__file__) + "/grids/CHENYX06a.gsb")
           urllib.urlretrieve ("https://github.com/NaturalGIS/ntv2_transformations_grids_and_sample_data/raw/master/ch/chenyx06etrs.gsb", os.path.dirname(__file__) + "/grids/chenyx06etrs.gsb")

        commands = ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
