﻿# -*- coding: utf-8 -*-
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
    Formulario para seleccionar el archivo con la ruta al directorio que almacena los trabajos.
    @author: J. Gaspar Mora navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para seleccionar el archivo con la ruta al directorio que almacena los trabajos..
"""

import sys
import os
from PyQt4 import QtCore, QtGui

from TopoDelProp.forms.frmDirTrabajos import Ui_frmDirTrabajos

#sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
#from pydevd import *

class ctrDirTrabajos(QtGui.QDialog):
    """
    Presenta un cuadro de dialogo para seleccionar la ruta donde
    se quieren guardar los trabajos. Intenta guardar la ruta en el 
    directorio del plugin, en el archivo dirTrabajos.txt, o en c:/dirTrabajos.txt
    El archivo debe estar guardado en codificacion ANSI y no tener espacios ni acentos
    ni enyes.
    Si no puede crear el archivo, se da un mensaje, pero no se genera
    ninguna excepción. La excepcion se generara despues, cuando se comprueba
    que el archivo dirtrabajos.txt no existe, en Utils.InicializaUtiles,
    que es donde se hace la llamada a este cuadro de dialogo.
    """
    #constructor
    def __init__(self, iface):
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self, iface.mainWindow())
        #Inicializa el formulario
        self.ui=Ui_frmDirTrabajos() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.iface=iface
        self.introducido=False

        #inicializa las variables de la clase
        self.connect(self.ui.bttAceptar, QtCore.SIGNAL("clicked()"),self.aceptar)
        self.connect(self.ui.bttSeleccionar, QtCore.SIGNAL("clicked()"),self.seleccionar)
    def seleccionar(self):
        dirTrab=QtGui.QFileDialog.getExistingDirectory(self.iface.mainWindow(), "Seleccione el directorio para los trabajos")
        self.ui.tbDirTrabajos.setText(str(dirTrab))
        
    def aceptar(self):
        """
        Metodo que se ejecuta con el evento clic del boton Aceptar
        Intenta guardar la ruta que el usuario ha puesto en la caja de texto
        del cuadro de dialogo en el archivo dirtrabajos.txt
        """
        dirTra=str(self.ui.tbDirTrabajos.text())
        if not(os.path.isdir(dirTra)):
            QtGui.QMessageBox.information(self.iface.mainWindow(),"Hubo un problema", "La ruta de los trabajos " + dirTra + " No es valida. Intentelo de nuevo",1)
            return
        #la ruta ya es valida
        dirBase=sys.path[2]#directorio base de la aplicación c:/users/.../.qgis/python/plugins
        ruta=dirBase + "/UPV-DelProp/dirTrabajos.txt"
        try:
            f=open(ruta,"w")
            f.write(dirTra)
            f.close()
            self.introducido=True
            self.close()
        except Exception,e:
            #la primera ruta ha fallado
            ruta2="c:/dirTrabajos.txt"
            try:
                f=open(ruta2,"w")
                f.write(dirTra)
                f.close()
                self.introducido=True
                self.close()
            except Exception,e:
                QtGui.QMessageBox.information(self.iface.mainWindow(),"Hubo un problema", "No se puede escribir el archivo " + ruta + " ni en " + ruta2 + ". La aplicacion no tiene permiso de escritura. Por favor cree el archivo y guarde la ruta Ud. mismo",1)

    def closeEvent(self, event):
        """
        Se ejecuta en el caso de de el usuario pulse la X del formulario
        Se muestra un cuadro de dialogo para permitir al usuario volver
        al cuadro de dialogo o salir. 
        """
        if self.introducido==False:
            reply = QtGui.QMessageBox.question(self, 'Mensaje', "Seguro que desea salir?", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            #Si se selecciona Si se acepta el evento, si se selecciona
            #no se ignora el evento
            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
    