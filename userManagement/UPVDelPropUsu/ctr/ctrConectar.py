# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UPVDelProp
                                 A QGIS plugin
 UPVDelProp
                              -------------------
        begin                : 2011-12-19
        copyright            : (C) 2011 by J. Gaspar Mora Navarro
        email                : upvdelprop@gmail.com
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
    Formulario para conectar con PostgreSQL.
    @author: J. Gaspar Mora navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: upvdelprop@gmail.com
    @version: 0.1
    @summary: Formulario para conectar con PostgreSQL.
             Necesita psycopg2"""
import sys
from PyQt4 import QtCore, QtGui

import pyUPVBib.pyPgGas

from forms.frmConectar import Ui_frmConectar

#sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
#from pydevd import *

class ctrConectar(QtGui.QDialog):
    """
    Presenta un cuadro de dialogo para conectar con la base de datos
    Una vez se pulsa el botón Conectar, se conecta con Postgres, 
    almacenándose la conexión en la variable de clase oConectaPg,
    cerrandose el cuadro de dialogo.
    Esta variable se puede recuperar utilizando el metodo getOConectaPG()
    de este controlador.
    Si no se puede conectar, se muestra un mensaje con el error y
    el método getOConectaPG() devuelve None.
    Si el usuario presiona la X para cerrar el cuadro de dialogo,
    aparece un mensaje indicando si quiere o no abandonar.
    """
    #constructor
    def __init__(self, iface):
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self)
        #Inicializa el formulario
        self.ui=Ui_frmConectar() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.iface=iface
        self.conectado=False
        self.oConectaPg=None
        #inicializa las variables de la clase
        self.connect(self.ui.bttConectar, QtCore.SIGNAL("clicked()"),self.arrancar)
        
    def arrancar(self):
        """
        Metodo que se ejecuta con el evento clic del boton conectar
        Inicializa la variable de la clase oConectaPg si puede conectar,
        en caso contrario oConectaPg=None
        """
        bda=str(self.ui.tbBda.text())
        host2=str(self.ui.tbHost.text())
        port=str(self.ui.tbPort.text())
        usuario=str(self.ui.tbNumCol.text())
        psw=str(self.ui.tbContr.text())
        self.oConectaPg=pyUPVBib.pyPgGas.ConectaPg(bda, usuario, psw,host2, port, connection_timeout=10)
        if self.oConectaPg.conectado==False:
            QtGui.QMessageBox.information(self,"Error", self.oConectaPg.descripcion_error,1)
            return
        self.conectado=True
        self.close()
    def getOConectaPg(self):
        """
        Devuelve la variable de la clase oConectaPg, que puede vales
        un objeto de la clase oConectaPg o None.
        @return: La variable de la clase oConectaPg, que puede valer
            un objeto de la clase oConectaPg o None.
        """
        return self.oConectaPg #puede ser un objeto ConectaPg o None
    def closeEvent(self, event):
        """
        Se ejecuta en el caso de de el usuario pulse la X del formulario
        Se muestra un cuadro de dialogo para permitir al usuario volver
        al cuadro de dialogo o salir. Si sale, self.oConectaPg se establece
        a None.
        """
        if self.conectado==False:
            reply = QtGui.QMessageBox.question(self, 'Mensaje', "Seguro que desea salir?", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            #Si se selecciona Si se acepta el evento, si se selecciona
            #no se ignora el evento
            if reply == QtGui.QMessageBox.Yes:
                self.oConectaPg=None
                event.accept()
            else:
                event.ignore()