# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pyUPVBibDialog
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
"""

from PyQt4 import QtCore, QtGui
from ui_pyupvbib import Ui_pyUPVBib
# create the dialog for zoom to point


class pyUPVBibDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_pyUPVBib()
        self.ui.setupUi(self)
