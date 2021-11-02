# DYCAST plugin for QGIS

* For additional information see www.DYCAST.org and https://github.com/CarneyLab/DYCAST

## Installation steps

1). Install **PostgreSQL** and **PostGIS**<br>
In pgAdmin, create a new database "dycast"<br>

Supports at least PostgreSQL 9.6: https://www.postgresql.org/download/<br>
Supports at least PostGIS 2.3-3.01: http://postgis.net/install/, http://download.osgeo.org/postgis/windows/pg96/archive/<br>
(Note: if PostGIS 2.3 yields <i>"ERROR: could not load library "C:/Program Files/PostgreSQL/9.6/lib/rtpostgis-2.3.dll": The specified module could not be found"</i>, then copy-paste files "libeay32.dll" and "ssleay32.dll" from the folder "bin/postgisgui" to "bin")

2). Install the latest version of **QGIS** (https://qgis.org), the open-source cross-platform GIS software<br>

3). Install **DYCAST plugin**<br>
From the main screen of QGIS, click Plugins > Manage and Install Plugins... > Install from ZIP > select the plugin .zip file

For troubleshooting, here are the plugins folders of QGIS (this is where the above zip will be automatically unzipped):<br>
On Mac: /home/<your username> /.local/share/QGIS/QGIS3/profiles/default/python/plugins<br>
On Windows: C:\Users\<your username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins<br>
https://docs.qgis.org/3.16/en/docs/user_manual/plugins/plugins.html
