A plugin for the QGIS Processing toolbox to allow users do Datum transformations with NTv2 grids
--------------------------------------

![](/icons/naturalgis.png)

Developed by NaturalGIS 

web: http://www.naturalgis.pt/ 

email: giovanni.manghi@naturalgis.pt

This plugin allows QGIS user to do easily direct/inverse Datum transformations (for vectors and rasters) using NTv2 grids. Available transformations are the ones supported by NTv2 grids that will be possible to redistribute legally with the plugin itself.

The plugin needs QGIS >= 2.8 to work.

This plugin is directly derived from https://github.com/qgispt/processing_pttransform originally developed by Alexander Bruy, Pedro Venâncio and NaturalGIS (http://www.naturalgis.pt/), with the support of the Portuguese QGIS user group (http://www.qgis.pt/).

If you have a NTv2 grid that can be legally redistributed and you would like to have it added to this plugin please file a feature request here:

https://github.com/NaturalGIS/ntv2_transformations/issues

Contributors:

- Alexander Bruy
- Carlos López Quintanilla (carlos.lopez@psig.es)
- Fernando Ribeiro aka The Geocrafter (fernandinand@gmail.com)
- Pedro Venâncio (pedrongvenancio@gmail.com)

Supported transformations:

![](/icons/at.png)

-  Austria: MGI [EPSG:4312] <==> ETRS89 [EPSG:4258] [AT_GIS_GRID.gsb]
-  MGI/Austria GK west [EPSG:31254] <==> ETRS89 [EPSG:4258] [AT_GIS_GRID.gsb]
-  MGI/Austria GK central [EPSG:31255] <==> ETRS89 [EPSG:4258] [AT_GIS_GRID.gsb]
-  MGI/Austria GK east [EPSG:31256] <==> ETRS89 [EPSG:4258] [AT_GIS_GRID.gsb]
-  MGI/Austria GK M28 [EPSG:31257] <==> ETRS89 [EPSG:4258] [AT_GIS_GRID.gsb]
-  MGI/Austria GK M31 [EPSG:31258] <==> ETRS89 [EPSG:4258] [AT_GIS_GRID.gsb]
-  MGI/Austria GK M34 [EPSG:31259] <==> ETRS89 [EPSG:4258] [AT_GIS_GRID.gsb]

Source for [AT_GIS_GRID.gsb], Bundesministerium für Wissenschaft, Forschung und Wirtschaft nachgeordnete Bundesbehörde mit den Aufgabenbereichen Vermessung und Geoinformation und Mess- und Eichwesen: 
http://www.bev.gv.at/portal/page?_pageid=713,2103845&_dad=portal&_schema=PORTAL

![](/icons/cat.png)

-  Catalonia: ED50/UTM 31N [EPSG:23031] <==> ETRS89/UTM zone 31N [EPSG:25831] [100800401.gsb]

Source for [100800401.gsb], Institut Cartogràfic i Geològic de Catalunya: 
http://www.icc.cat/eng/Home-ICC/Geodesia/Recursos

![](/icons/hr.png)

-  Croatia: HDKS5/6 [Custom CRSs] <==> HTRS96/Croatia TM [EPSG:3765] [HRNTv2.gsb]

Source for [HRNTv2.gsb]: 
http://geosinjal.blogspot.pt/2012/12/kreiranje-ntv2-grid-datoteke-za.html

![](/icons/de.png)

-  Germany: Gauss-Krüger zone 3 [EPSG:31467] <==> ETRS89 [EPSG:4258] [BETA2007.gsb]

Source for [BETA2007.gsb]: 
http://crs.bkg.bund.de/crseu/crs/descrtrans/BeTA/de_dhdn2etrs_beta.php

![](/icons/it.png)

-  Italy (Emilia-Romagna): Monte Mario - GBO [EPSG:3003] <==> ETRS89 [EPSG:4258] [RER_AD400_MM_ETRS89_V1A.gsb]
-  Italy (Emilia-Romagna): UTM - ED50 [EPSG:23032] <==> ETRS89 [EPSG:4258] [RER_ED50_ETRS89_GPS7_K2.GSB]

Source for [RER_ED50_ETRS89_GPS7_K2.gsb] and [RER_AD400_MM_ETRS89_V1A.gsb]:
http://geoportale.regione.emilia-romagna.it/it/services/servizi%20tecnici/servizio-di-conversione/grigliati-ntv2-rer-2013-la-trasformazione-di-coordinate-in-emilia-romagna

![](/icons/nl.png)

-  Netherlands: Amersfoort/RD [EPSG:28992] <==> ETRS89 [EPSG:4258] [rdtrans2008.gsb] and [naptrans2008.gtx]

Source for [rdtrans2008.gsb] and [naptrans2008.gtx]:
http://www.kadaster.nl/web/Themas/Registraties/Rijksdriehoeksmeting/Transformatie-van-coordinaten.htm

![](/icons/pt.png)

-  Portugal (mainland): Datum 73 [EPSG:27493/ESRI:102161] <==> ETRS89/PT-TM06 [EPSG:3763] [pt73_e89.gsb] or [D73_ETRS89_geo.gsb]
-  Portugal (mainland): Datum 73 Militar [ESRI:102160] <==> ETRS89/PT-TM06 [EPSG:3763] [pt73_e89.gsb] or [D73_ETRS89_geo.gsb]
-  Portugal (mainland): Datum Lisboa [EPSG:20791/EPSG:5018/ESRI:102165] <==> ETRS89/PT-TM06 [EPSG:3763] [ptLX_e89.gsb] or [DLX_ETRS89_geo.gsb]
-  Portugal (mainland): Datum Lisboa Militar [EPSG:20790/ESRI:102164] <==> ETRS89/PT-TM06 [EPSG:3763] [ptLX_e89.gsb] or [DLX_ETRS89_geo.gsb]
-  Portugal (mainland): Datum Europeu 1950 (ED50) [EPSG:23029] <==> ETRS89/PT-TM06 [EPSG:3763] [ptED_e89.gsb]

Source for [pt73_e89.gsb], [ptED_e89.gsb] and [ptLX_e89.gsb], Prof. José Alberto Gonçalves:
http://www.fc.up.pt/pessoas/jagoncal/coordenadas/

Source for [D73_ETRS89_geo.gsb] and [DLX_ETRS89_geo.gsb], Direção-Geral do Território:
http://www.dgterritorio.pt/cartografia_e_geodesia/geodesia/transformacao_de_coordenadas/grelhas_em_ntv2/

![](/icons/es.png)

-  Spain (mainland): ED50/UTM 29N [EPSG:23029] <==> ETRS89 [EPSG:4258] [PENR2009.gsb]
-  Spain (mainland): ED50/UTM 30N [EPSG:23030] <==> ETRS89 [EPSG:4258] [PENR2009.gsb]
-  Spain (mainland): ED50/UTM 31N [EPSG:23031] <==> ETRS89 [EPSG:4258] [PENR2009.gsb]

Source for [PENR2009.gsb]:
http://www.ign.es/ign/layoutIn/herramientas.do

![](/icons/ch.png)

- Switzerland: CH1903 [EPSG:21781] <==> ETRS89 [EPSG:4258] [chenyx06etrs.gsb]
- Switzerland: CH1903 [EPSG:21781] <==> CH1903+ [EPSG:2056] [CHENYX06a.gsb]

Source for [chenyx06etrs.gsb] and [CHENYX06a.gsb]:

http://www.swisstopo.admin.ch/internet/swisstopo/en/home/products/software/products/chenyx06.html

![](/icons/uk.png)

- UK: OSGB 1936/British National Grid [EPSG:27700] <==> ETRS89 [EPSG:4258] [OSTN02_NTv2.gsb]

Source for [OSTN02_NTv2.gsb]:

http://www.ordnancesurvey.co.uk/business-and-government/help-and-support/navigation-technology/os-net/ostn02-ntv2-format.html