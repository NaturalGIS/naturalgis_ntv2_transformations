A plugin for the QGIS Processing toolbox to allow users do Datum transformations with NTv2 grids
--------------------------------------

![](/icons/naturalgis.png)

Developed by NaturalGIS 

web: http://www.naturalgis.pt/ 

email: giovanni.manghi@naturalgis.pt

This plugin allows QGIS user to do easily direct/inverse Datum transformations (for vectors and rasters) using NTv2 grids. Available transformations will be the ones that are supported by NTv2 grids that will be possible to redistribute legally with the plugin itself.

The plugin needs QGIS 2.8 to work.

Supported transformations:

![](/icons/de.png)

-  Germany: Gauss-Krüger zone 3 <--> ETRS89/UTM Zone 32N [BETA2007.gsb]

Source for [BETA2007.gsb]: 
http://crs.bkg.bund.de/crseu/crs/descrtrans/BeTA/de_dhdn2etrs_beta.php

![](/icons/pt.png)

-  Portugal: Datum 73 <--> ETRS89/PT-TM06 [pt73_e89.gsb]
-  Portugal: Datum 73 <--> ETRS89/PT-TM06 [D73_ETRS89_geo.gsb]
-  Portugal: Datum Lisboa <--> ETRS89/PT-TM06 [ptLX_e89.gsb]
-  Portugal: Datum Lisboa <--> ETRS89/PT-TM06 [DLX_ETRS89_geo.gsb]
-  Portugal: Datum Europeu 1950 <--> ETRS89/PT-TM06 [ptED_e89.gsb]

Source for [pt73_e89.gsb], [ptED_e89.gsb] and [ptLX_e89.gsb], Prof. José Alberto Gonçalves:
http://www.fc.up.pt/pessoas/jagoncal/coordenadas/

Source for [D73_ETRS89_geo.gsb] and [DLX_ETRS89_geo.gsb], Direção-Geral do Território:
http://www.dgterritorio.pt/cartografia_e_geodesia/geodesia/transformacao_de_coordenadas/grelhas_em_ntv2/