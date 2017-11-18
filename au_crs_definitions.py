# This file holds definitions of the CRSs used in Australia.
import os

AGD66GRID = os.path.dirname(__file__) + '/grids/A66_National_13_09_01.gsb'
AGD84GRID = os.path.dirname(__file__) + '/grids/National_84_02_07_01.gsb'
GDA2020CONF_DIST = os.path.dirname(__file__) + '/grids/GDA94_GDA2020_conformal_and_distortion.gsb'

OLD_CRS_STRINGS = {
    'AGD66 AMG [EPSG:202XX]': [
        '+proj=utm +zone={zone} +south +ellps=aust_SA +towgs84=-117.808,-51.536,137.784,0.303,0.446,0.234,-0.29 +units=m +no_defs +nadgrids=' + AGD66GRID + ' +wktext',
        'EPSG:202{zone}'
    ],
    'AGD66 Latitude and Longitude [EPSG:4202]': [
        '+proj=longlat +ellps=aust_SA +towgs84=-117.808,-51.536,137.784,0.303,0.446,0.234,-0.29 +no_defs +nadgrids=' + AGD66GRID + ' +wktext',
        'EPSG:4202'
    ],
    'AGD84 AMG [EPSG:203XX]': [
        '+proj=utm +zone={zone} +south +ellps=aust_SA +towgs84=-134,-48,149,0,0,0,0 +units=m +no_defs +nadgrids=' + AGD84GRID + ' +wktext',
        'EPSG:203{zone}'
    ],
    'AGD84 Latitude and Longitude [EPSG:4203]': [
        '+proj=longlat +ellps=aust_SA +towgs84=-134,-48,149,0,0,0,0 +no_defs +nadgrids=' + AGD84GRID + ' +wktext'
        'EPSG:4203'
    ],
    'GDA94 MGA [EPSG:283XX]': [
        '+proj=utm +zone={zone} +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +nadgrids=' + GDA2020CONF_DIST + ' +wktext',
        'EPSG:283{zone}'
    ],
    'GDA94 Latitude and Longitude [EPSG:4283]': [
        '+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs +nadgrids=' + GDA2020CONF_DIST + ' +wktext',
        'EPSG:4283'
    ],
}

NEW_CRS_STRINGS = {
    'GDA94 MGA [EPSG:283XX]': 'EPSG:283{zone}',
    'GDA94 Latitude and Longitude [EPSG:4283]': 'EPSG:4238'
}

# These are handled differently, because the transform needs to be done using the proj string
# otherwise, it seems to ignore the grid.
NEW_CRS_STRINGS_2020 = {
    'GDA2020 MGA [EPSG:78XX]': [
        '+proj=utm +zone={zone} +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +wktext',
        'EPSG:78{zone}'
    ],
    'GDA2020 Latitude and Longitude [EPSG:7844]': [
        '+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs +wktext'
        'EPSG:7844'
    ]
}
