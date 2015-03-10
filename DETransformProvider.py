# -*- coding: utf-8 -*-

"""
***************************************************************************
    DETransformProvider.py
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

import os

from PyQt4.QtGui import *

from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingConfig import Setting, ProcessingConfig
from processing.tools import system

from ntv2_transformations.VectorDE_GK3ETRS8932NDirInv import VectorDE_GK3ETRS8932NDirInv
from ntv2_transformations.RasterDE_GK3ETRS8932NDirInv import RasterDE_GK3ETRS8932NDirInv
from ntv2_transformations.VectorPT_ETR89PTTM06DirInv import VectorPT_ETR89PTTM06DirInv
from ntv2_transformations.RasterPT_ETR89PTTM06DirInv import RasterPT_ETR89PTTM06DirInv
from ntv2_transformations.VectorES_ED50ERTS89DirInv import VectorES_ED50ERTS89DirInv
from ntv2_transformations.RasterES_ED50ERTS89DirInv import RasterES_ED50ERTS89DirInv
from ntv2_transformations.VectorIT_RER_ETRS89DirInv import VectorIT_RER_ETRS89DirInv
from ntv2_transformations.RasterIT_RER_ETRS89DirInv import RasterIT_RER_ETRS89DirInv
from ntv2_transformations.VectorCH_LV95ETRS89DirInv import VectorCH_LV95ETRS89DirInv
from ntv2_transformations.RasterCH_LV95ETRS89DirInv import RasterCH_LV95ETRS89DirInv
from ntv2_transformations.VectorUK_OSGB36ETRS89DirInv import VectorUK_OSGB36ETRS89DirInv
from ntv2_transformations.RasterUK_OSGB36ETRS89DirInv import RasterUK_OSGB36ETRS89DirInv


class DETransformProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)

        self.activate = False

        self.alglist = [VectorPT_ETR89PTTM06DirInv(),RasterDE_GK3ETRS8932NDirInv(),RasterPT_ETR89PTTM06DirInv(),VectorDE_GK3ETRS8932NDirInv(),
			VectorES_ED50ERTS89DirInv(),RasterES_ED50ERTS89DirInv(),VectorIT_RER_ETRS89DirInv(),RasterIT_RER_ETRS89DirInv()
			,VectorCH_LV95ETRS89DirInv(), RasterCH_LV95ETRS89DirInv(),VectorUK_OSGB36ETRS89DirInv(),RasterUK_OSGB36ETRS89DirInv()
			]
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)

    def unload(self):
        AlgorithmProvider.unload(self)

    def getName(self):
        return 'ntv2_transformations'

    def getDescription(self):
        return u'NTV2 Datum Transformations'

    def getIcon(self):
        return QIcon(os.path.dirname(__file__) + '/icons/naturalgis_32.png')

    def _loadAlgorithms(self):
        self.algs = self.alglist
