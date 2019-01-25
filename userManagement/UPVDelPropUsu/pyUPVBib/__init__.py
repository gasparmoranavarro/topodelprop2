"""

 Este plugin esta vacio. No hace nada. Se utiliza como biblioteca comun para otros
 plugins
 
/***************************************************************************
 propiedad
                                 A QGIS plugin
 delimitacion propiedad
                             -------------------
        begin                : 2011-12-19
        copyright            : (C) 2011 by gaspar mora
        email                : gaspar.mora.navarro@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "Proyecto vacio"
def description():
    return "Proyecto vacio"
def version():
    return "Version 0.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def classFactory(iface):
    # load propiedad class from file propiedad
    from pyQgsBibGas.vacio import clsVacio
    return clsVacio(iface)
