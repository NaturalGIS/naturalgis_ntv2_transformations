A plugin for the QGIS Processing toolbox to allow users do Datum transformations with NTv2 grids
--------------------------------------

![](/icons/naturalgis.png)

Developed by NaturalGIS 

web: http://www.naturalgis.pt/ 

email: giovanni.manghi@naturalgis.pt

This plugin allows QGIS user to do easily direct/inverse Datum transformations (for vectors and rasters) using NTv2 grids. Available transformations will be the ones that are supported by NTv2 grids that will be possible to redistribute legally with the plugin itself.

The plugin needs QGIS 2.8 to work.

This plugin is directly derived from https://github.com/qgispt/processing_pttransform originally developed by Alexander Bruy, Pedro Venâncio and NaturalGIS (http://www.naturalgis.pt/), with the support of the Portuguese QGIS user group (http://www.qgis.pt/).

If you have a NTv2 grid that can be legally redistributed and you would like to have it added to this plugin please file a feature request here:

https://github.com/NaturalGIS/ntv2_transformations/issues

Supported transformations:

![](/icons/de.png)

-  Germany: Gauss-Krüger zone 3 <==> ETRS89/UTM Zone 32N [BETA2007.gsb]

Source for [BETA2007.gsb]: 
http://crs.bkg.bund.de/crseu/crs/descrtrans/BeTA/de_dhdn2etrs_beta.php

![](/icons/it.png)

-  Italy (Emilia-Romagna): Monte Mario - GBO [EPSG:3003] <==> ETRS89/UTM zone 32N [EPSG:25832] [RER_AD400_MM_ETRS89_V1A.gsb]
-  Italy (Emilia-Romagna): UTM - ED50 [EPSG:23032] <==> ETRS89/UTM zone 32N [EPSG:25832] [RER_ED50_ETRS89_GPS7_K2.GSB]

Source for [RER_ED50_ETRS89_GPS7_K2.gsb] and [RER_AD400_MM_ETRS89_V1A.gsb]:
http://geoportale.regione.emilia-romagna.it/it/services/servizi%20tecnici/servizio-di-conversione/grigliati-ntv2-rer-2013-la-trasformazione-di-coordinate-in-emilia-romagna

![](/icons/pt.png)

-  Portugal (mainland): Datum 73 <==> ETRS89/PT-TM06 [pt73_e89.gsb]
-  Portugal (mainland): Datum 73 <==> ETRS89/PT-TM06 [D73_ETRS89_geo.gsb]
-  Portugal (mainland): Datum Lisboa <==> ETRS89/PT-TM06 [ptLX_e89.gsb]
-  Portugal (mainland): Datum Lisboa <==> ETRS89/PT-TM06 [DLX_ETRS89_geo.gsb]
-  Portugal (mainland): Datum Europeu 1950 (ED50) <==> ETRS89/PT-TM06 [ptED_e89.gsb]

Source for [pt73_e89.gsb], [ptED_e89.gsb] and [ptLX_e89.gsb], Prof. José Alberto Gonçalves:
http://www.fc.up.pt/pessoas/jagoncal/coordenadas/

Source for [D73_ETRS89_geo.gsb] and [DLX_ETRS89_geo.gsb], Direção-Geral do Território:
http://www.dgterritorio.pt/cartografia_e_geodesia/geodesia/transformacao_de_coordenadas/grelhas_em_ntv2/

![](/icons/es.png)

-  Spain (mainland): ED50/UTM 29N <==> ETRS89/UTM 29N [PENR2009.gsb]
-  Spain (mainland): ED50/UTM 30N <==> ETRS89/UTM 30N [PENR2009.gsb]
-  Spain (mainland): ED50/UTM 31N <==> ETRS89/UTM 31N [PENR2009.gsb]

Source for [PENR2009.gsb]:
http://www.ign.es/ign/layoutIn/herramientas.do