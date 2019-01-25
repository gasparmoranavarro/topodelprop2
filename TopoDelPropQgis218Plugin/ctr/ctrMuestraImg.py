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
    Formulario para descargar y mostrar las imágenes de los elementos interiores.
    @author: J. Gaspar Mora navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para descargar y mostrar las imágenes de los elementos interiores.
"""
import sys
import os
from PyQt4 import QtCore, QtGui
from TopoDelProp.forms.frmMuestraImg import Ui_frmMuestraImg

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

 
"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""

class ctrMuestraImg(QtGui.QDialog):
    """
    Formulario que muestra las imagenes de los elementos interiores 
    (tablas ed_img_elem_int o img_elem_int).
    Se necesita que la capa exista, que sea de tipo multipolygon y que 
    haya un elemento seleccionado.
    """
    #constructor
    def __init__(self,oUtiles):
        """
        @type oUtiles:  UilsPropiedad.Utils.Utiles
        @param oUtiles: Clase con las utilidades necesarias para esta aplicacion
        """
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self, oUtiles.iface.mainWindow())
        
        #Inicializa el formulario
        self.ui=Ui_frmMuestraImg() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.tblDatos=self.ui.tblDatos #tabla con los datos del punto
        self.oUtiles=oUtiles
        
        #self.oUtiles.ntrabajo=self.oUtiles.id_trabajo
        self.ui.bttAnterior.setVisible(False)
        self.ui.bttSiguiente.setVisible(False)
       
    def muestraImagen(self,nomImagen):
        """
        Muestra la imagen en el formulario.
        """       
        #primero comprueba que la imagen no haya sido descargada ya,
        #en tal caso no hace falta que vuelva a descargarse del servidor

        if os.path.exists(nomImagen):
            try:
                self.ui.lbImg.setPixmap(QtGui.QPixmap(_fromUtf8(nomImagen)))
                self.ui.lbEstado.setText("Imagen encontrada en: " + nomImagen)
                return
            except Exception, e:
                QtGui.QMessageBox.information(self,"Error al cargar la imagen" , e.message + ". Imagen: " + nomImagen,1)
                self.ok=False
                return
            
    def muestraValores(self,dic):
        """
        Muestra los valores de los campos en el formulario.
        """
        listaNombreCampos=dic.keys()#devuelve todas las claves del diccionario
        self.tblDatos.setRowCount(len(listaNombreCampos))
        self.tblDatos.setColumnCount(1)
        self.tblDatos.setHorizontalHeaderLabels(['Valor del campo'])
        self.tblDatos.setVerticalHeaderLabels(listaNombreCampos)

        listaValores=dic.values()
        i=0
        for valor in listaValores:
            newitem = QtGui.QTableWidgetItem(str(valor))
            self.tblDatos.setItem(i, 0, newitem)
            i=i+1
        
