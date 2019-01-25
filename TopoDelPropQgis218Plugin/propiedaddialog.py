# -*- coding: utf-8 -*-
"""
/***************************************************************************
 propiedadDialog
                                 A QGIS plugin
 Delimitación de propiedades por topografia clasica
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
"""

from PyQt4 import QtCore, QtGui
from ui_propiedad import Ui_propiedad
# create the dialog for zoom to point


class propiedadDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_propiedad()
        self.ui.setupUi(self)
