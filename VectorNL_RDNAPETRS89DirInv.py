# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorNL_RDNAPETRS89DirInv.py
    ---------------------
    Date                 : August 2015
    Copyright            : (C) 2015 by Fernando Ribeiro aka The Geocrafter
    Email                : fernandinand at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Fernando Ribeiro aka The Geocrafter'
__date__ = 'August 2015'
__copyright__ = '(C) 2015, Fernando Ribeiro aka The Geocrafter'

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


class VectorNL_RDNAPETRS89DirInv(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    TRANSF = 'TRANSF'
    TRANSF_OPTIONS = ['Direct: Old Data -> ETRS89 [EPSG:4258]',
                      'Inverse: ETRS89 [EPSG:4258] -> Old Data']
    CRS = 'CRS'
    CRS_OPTIONS = ['Amersfoort/RD [EPSG:28992]']
    GRID = 'GRID'
    GRID_OPTIONS = ['RDNAPTRANS [NTv2 + VDatum]', 'RDNAPTRANS [NTv2 only]']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/nl.png')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = '[NL] Direct and inverse Vector tranformation'
        self.group = '[NL] Netherlands'
        self.addParameter(ParameterVector(self.INPUT, 'Input vector',
                          [ParameterVector.VECTOR_TYPE_ANY]))
        self.addParameter(ParameterSelection(self.TRANSF, 'Transformation',
                          self.TRANSF_OPTIONS))
        self.addParameter(ParameterSelection(self.CRS, 'Old Datum',
                          self.CRS_OPTIONS))
        self.addParameter(ParameterSelection(self.GRID, 'NTv2 Grid',
                          self.GRID_OPTIONS))
        self.addOutput(OutputVector(self.OUTPUT, 'Output'))

    def transfList(self):
        return [
            [
                # RDNAPTRANS NTv2 + VDatum
                ['+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/rdtrans2008.gsb +geoidgrids=' + os.path.dirname(__file__) + '/grids/naptrans2008.gtx +wktext +units=m +no_defs'],
                # RDNAPTRANS NTv2 Only
                ['+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +nadgrids=' + os.path.dirname(__file__) + '/grids/rdtrans2008.gsb +wktext +units=m +no_defs']
            ]
        ]

    def processAlgorithm(self, progress):

        inLayer = self.getParameterValue(self.INPUT)
        conn = ogrConnectionString(inLayer)[1:-1]

        output = self.getOutputFromName(self.OUTPUT)
        outFile = output.value

        if self.getParameterValue(self.TRANSF) == 0:
            # Direct transformation
            arguments = ['-s_srs']
            arguments.append(str(self.transfList()[self.getParameterValue(self.CRS)][self.getParameterValue(self.GRID)])[2:-2])
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
            arguments.append(str(self.transfList()[self.getParameterValue(self.CRS)][self.getParameterValue(self.GRID)])[2:-2])
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
            arguments.append('EPSG:28992')
            arguments.append(outFile)    
            arguments.append('/vsistdin/')

        arguments.append('-lco') 
        arguments.append('ENCODING=UTF-8')

        if os.path.isfile(os.path.dirname(__file__) + '/grids/rdtrans2008.gsb') is False:
            import urllib
            urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/nl/rdtrans2008.gsb", os.path.dirname(__file__) + "/grids/rdtrans2008.gsb")
            urllib.urlretrieve ("http://www.naturalgis.pt/downloads/ntv2grids/nl/naptrans2008.gtx", os.path.dirname(__file__) + "/grids/naptrans2008.gtx")

        commands = ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
