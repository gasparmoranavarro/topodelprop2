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
    Formulario para la selección del tipo de trabajo: definitivo o en edicion, y
    el sistema de coordenadas src del trabajo.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para la selección del tipo de trabajo: definitivo o en edicion, y
        el sistema de coordenadas src del trabajo.
"""
from PyQt4 import QtCore, QtGui
import sys
from TopoDelProp.forms.frmSelEsquema import Ui_frmSelEsquema

"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""

class ctrSelEsquema(QtGui.QDialog):
    """
    Se utiliza para seleccionar el tipo de trabajo: definitivo o en edicion, y
    el sistema de coordenadas src del trabajo.
    """
    #constructor
    def __init__(self, oUtiles,mostrarEsquema=True):
        """
        Inicializa el cuadro de dialogo.
        
        @type oUtiles: utils.Utiles
        @param oUtiles: Objeto de la clase utiles
        """
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self,oUtiles.iface.mainWindow())
#        QtGui.QDialog.init(self,dlgPadre)

        #Inicializa el formulario
        self.ui=Ui_frmSelEsquema() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)

        self.oUtiles=oUtiles
        self.mostrarEsquema=mostrarEsquema
        self.__tipoTrabajo=None
        self.__src=None
        self.__esquema=None
        self.rellenaListas()
        if mostrarEsquema==False:
            self.ui.lwSrc.setEnabled(False)
            
        self.connect(self.ui.lwTipoTrabajo, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.lwTipoTrabajoClick)
        self.connect(self.ui.lwSrc, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.lwSrcClick)
        self.connect(self.ui.bttAceptar, QtCore.SIGNAL('clicked()'), self.bttAceptar)

    def rellenaListas(self):
        if self.oUtiles.oDicDominios!=None:
            listaValores = self.oUtiles.oDicDominios.get("src_trabajo")
        else:
            #no los ha cargado. No es editor ni consultor
            listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla="dom.src_trabajo", listaCampos=["src_trabajo"], condicionWhere=None,listaValoresCondWhere=None,bytea_output_to_escape=False)
            if isinstance(listaDic,Exception):
                    QtGui.QMessageBox.information(self,"Error al cargar dom.src_trabajo",listaDic.message ,1)#self es la ventana pasdre que necesita qmessagebox
                    return
            if len(listaDic)>0:#cada fila es un diccionario campo:valor
                listaValores=[]
                for dic in listaDic:
                    listaValores.append(dic.get("src_trabajo"))
            else:
                QtGui.QMessageBox.information(self,"Error al cargar dom.src_trabajo","No se ha cargado ningún valor" ,1)#self es la ventana pasdre que necesita qmessagebox
                return

        if listaValores==None:#el campo no tiene posibles valores
            return
        for valor in listaValores:
            self.ui.lwSrc.addItem(valor)
            
        self.ui.lwTipoTrabajo.addItem("Edicion")
        self.ui.lwTipoTrabajo.addItem("Definitivo")
        self.ui.lwTipoTrabajo.addItem("Historico")
    def lwTipoTrabajoClick(self, elemClicado):
        """
        Establece la propiedad tipoTrabajo
        """
        self.__tipoTrabajo=elemClicado.text()
        if self.__tipoTrabajo=="Historico":
            mens=unicode("Opción todavía no programada. Elija otra.","utf-8")
            QtGui.QMessageBox.information(self,"Lo sentimos",mens ,1)#self es la ventana pasdre que necesita qmessagebox
            self.__tipoTrabajo=None
    def lwSrcClick(self, elemClicado):
        """
        Establece la propiedad src
        """
        src=elemClicado.text()
        self.__src=src
    def getEsquema(self):
        prefijo=self.getPrefijoTipoTrabajo()
        if prefijo==None:
            return None
        self.__esquema=prefijo + "src" + self.__src
        return self.__esquema
    def getSrc(self):
        return self.__src
    def getTipoTrabajo(self):
        if self.__tipoTrabajo==None or self.__tipoTrabajo=="Historico":
            return None
        return self.__tipoTrabajo
    def getPrefijoTipoTrabajo(self):
        if self.__tipoTrabajo==None:
            return None
        if self.__tipoTrabajo=="Edicion":
            prefijo="ed_"
        elif self.__tipoTrabajo=="Definitivo":
            prefijo=""
        else:
            prefijo="hist_"
        return prefijo
    def bttAceptar(self):
        self.close()

    def closeEvent(self, event):
        """
        Evento que permite abrir una
        ventana de dialogo para confirmar la salida del programa
        """
        #Se genera la respuesta de la confirmacion de salir

        if self.__tipoTrabajo==None:
            mens=unicode("No ha seleccionado el tipo de trabajo. ¿Seguro que desea salir?","utf-8")
            reply = QtGui.QMessageBox.question(self, "Mensaje", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                #event.accept()
                self.close()
            else:
                event.ignore()
        elif self.mostrarEsquema==True: 
            if self.__src==None:
                mens=unicode("No ha seleccionado el SRC del trabajo. ¿Seguro que desea salir?","utf-8")
                reply = QtGui.QMessageBox.question(self, "Mensaje", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    #event.accept()
                    self.close()
                else:
                    event.ignore()
