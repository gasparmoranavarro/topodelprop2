# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TopoDelProp
                                 A QGIS plugin
 TopoDelProp
                              -------------------
        begin                : 2011-12-19
        copyright            : (C) 2011 by J. Gaspar Mora Navarro
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
"""
    Formulario Acerca de.
    @author: Joaquin Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: formulario Acerca de.
    """
import sys
from PyQt4 import QtCore, QtGui

from  TopoDelProp.forms.frmAcercaDe import Ui_frmAcercaDe

class ctrAcercaDe(QtGui.QDialog):

    #constructor
    def __init__(self):
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self)
        #Inicializa el formulario
        self.ui=Ui_frmAcercaDe() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
