# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pyUPVBib
                                 A QGIS plugin
 Documented library for Postgis work. Necesary for TopoDelPropPlugin
                             -------------------
        begin                : 2013-12-10
        copyright            : (C) 2013 by Joaquin Gaspar Mora Navarro. Universidad Politécnica de Valencia
        email                : topodelprop@gmail.com
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

def classFactory(iface):
    # load pyUPVBib class from file pyUPVBib
    from pyupvbib import pyUPVBib
    return pyUPVBib(iface)
