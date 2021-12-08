# DYCAST plugin for QGIS

* For additional information see www.DYCAST.org
* This is a plugin for the [DYCAST](https://github.com/CarneyLab/DYCAST) application
<br>

## Installation steps

1). Install **PostgreSQL** and **PostGIS**

* Plugin supports at least PostgreSQL 9.6: https://www.postgresql.org/download/
* Plugin supports at least PostGIS 2.3*-3.01: http://postgis.net/install/, http://download.osgeo.org/postgis/windows/pg96/archive/

(*Note: if PostGIS 2.3 yields <i>"ERROR: could not load library "C:/Program Files/PostgreSQL/9.6/lib/rtpostgis-2.3.dll": The specified module could not be found"</i>, then copy-paste files "libeay32.dll" and "ssleay32.dll" from the folder "bin/postgisgui" to "bin")

2). Install the latest stable version 3 (_3.16 was used during development_)  of **QGIS** (https://qgis.org), the open-source cross-platform GIS software

3). Install the **DYCAST plugin**  
From the main screen of QGIS, click Plugins > Manage and Install Plugins... > Install from ZIP > select the plugin .zip file

For troubleshooting, here are the plugins folders of QGIS (this is where the above zip will be automatically unzipped):  
* Mac: /home/<your username> /.local/share/QGIS/QGIS3/profiles/default/python/plugins
* Windows: C:\Users\<your username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins
https://docs.qgis.org/3.16/en/docs/user_manual/plugins/plugins.html  
  
4). Run the plugin  
From the QGIS menu bar, click on Plugins > Dycast > Open Dycast  

5). Setup DYCAST  
From the DYCAST plugin window, run the setup by clicking Setup > Enter your PostgreSQL credentials (the defaults are already filled in) > Create database
  
## Work in progress  
The DYCAST QGIS plugin is a proof of concept, a work in progress and therefore not a finished product. Some pointers for current concern and future development efforts:
  - Several packages are outdated and require security updates (in particular SQL Alchemy)
  - This plugin contains a copy of the [DYCAST app](https://github.com/CarneyLab/DYCAST) itself and is therefore not automatically updated when a new release of DYCAST arrives. 
  
