# -*- coding: utf-8 -*-
"""
/***************************************************************************
 propiedad
                                 A QGIS plugin
 Delimitacion de propiedades por topografia clasica
                             -------------------
        begin                : 2013-10-04
        copyright            : (C) 2013 by Joaquin Gaspar Mora Navarro
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


def name():
    return "propiedad"


def description():
    return "Delimitacion de propiedades por topografia clasica. Gestion de geometrias y metadatos"


def version():
    return "Version 0.5"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "2.0"

def author():
    return "Joaquin Gaspar Mora Navarro"

def email():
    return "topodelprop@gmail.com"

def classFactory(iface):
    # load propiedad class from file propiedad
    from propiedad import clsPropiedad
    return clsPropiedad(iface)
