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
    Formulario para seleccionar el src y el municipio con el que se va a trabajar.
    No se hace ninguna comprobación de si el municipio pertenece al src o no.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para seleccionar el src y el municipio con el que se va a trabajar.
        No se hace ninguna comprobación de si el municipio pertenece al src o no.
"""
import sys
from PyQt4 import QtCore, QtGui

import pyUPVBib.pyPgGas

from TopoDelProp.forms.frmMunicipio import Ui_frmMunicipio
"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""
class ctrMunicipio(QtGui.QDialog):

    #constructor
    def __init__(self, oUtiles):
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self)
        #Inicializa el formulario
        self.ui=Ui_frmMunicipio() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.oUtiles=oUtiles
        self.municipio=None
        self.listaValoresQlist=None
        self.src=None
        #inicializa las variables de la clase
        self.connect(self.ui.bttAceptar, QtCore.SIGNAL("clicked()"),self.aceptar)
        self.connect(self.ui.listWidget, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.lwMuniClick)
        self.connect(self.ui.txtMunicipio, QtCore.SIGNAL("textChanged(const QString &)"),self.filtrar)
        self.connect(self.ui.listWidgetSrc, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.lwSrcClick)
        self.carga_municipios()
        self.carga_src()

    def lwSrcClick(self, elemClicado):
        """
        Establece la propiedad src
        """
        self.src=elemClicado.text()
        
    def lwMuniClick(self, elemClicado):
        """
        Establece la propiedad municipio
        """
        self.municipio=elemClicado.text()
        
    def aceptar(self):
        self.close()

    def get_municipio(self):
        return self.municipio

    def get_src(self):
        return self.src
    
    def filtrar(self):
        if self.listaValoresQlist==None:
            return
        cad=self.ui.txtMunicipio.text()
        cad=cad.lower()
        if cad=="" or cad==None:
            return
        self.ui.listWidget.clear()
        for valor in self.listaValoresQlist:
            valor2=valor.lower()
            if cad in valor2:
                self.ui.listWidget.addItem(valor) 

    def carga_municipios(self):
        listaValores = self.oUtiles.oDicDominios.get("municipio")
        self.listaValoresQlist=listaValores
        if listaValores==None:#el campo no tiene posibles valores
            return
        for valor in listaValores:
            self.ui.listWidget.addItem(valor)
    
    def carga_src(self):
        listaValores = self.oUtiles.oDicDominios.get("src_trabajo")
        if listaValores==None:#el campo no tiene posibles valores
            return
        for valor in listaValores:
            self.ui.listWidgetSrc.addItem(valor)

    def closeEvent(self, event):
        if self.src==None:
            reply = QtGui.QMessageBox.question(self, 'Mensaje', unicode("No ha seleccionado src. ¿Seguro que desea salir?","utf-8"), QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            #Si se selecciona Si se acepta el evento, si se selecciona
            #no se ignora el evento
            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()           
        elif self.municipio==None:
            reply = QtGui.QMessageBox.question(self, 'Mensaje', unicode("No ha seleccionado el municipio. ¿Seguro que desea salir?","utf-8"), QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            #Si se selecciona Si se acepta el evento, si se selecciona
            #no se ignora el evento
            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

        