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
    Formulario para la selección de una fila de una tabla.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para la selección de una fila de una tabla.
"""
from PyQt4 import QtCore, QtGui
import sys
from TopoDelProp.forms.frmSelec import Ui_frmSelec

import sys
"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""
class ctrSelec(QtGui.QDialog):
    """
    Muestra un cuadro de dialgogo con una tabla donde se introducen los valores de los
    campos que existen en el cursor psycopg2.
    Si el se usa el metodo exec_() para mostrar el formulario, el formulario retorna un entero.
    Si se usa show(), se puede acceder a la fila seleccionada a traves de la propiedad
    del formulario filaSeleccionada, que valdra -1, en caso de que haya cancelado, o no 
    haya elegido ninguna.
    """
    #constructor
    def __init__(self, dlgPadre, listaDic, oUtilidadesFormularios):
        """
        @type dlgPadre: QtGui.Qdialog
        @param dlgPadre: Dialogo desde el que se muestra este formulario
        @type listaDic: lista
        @param listaDic: Lista con las filas a mostrar. Cada fila es un diccionario
        @type oUtilidadesFormularios: UtilidadesFormularios
        @param oUtilidadesFormularios: Est clase se encuentra en el archivo pyQgsBibGas.gen.general.py, y
            es el encargado de rellenar la tabla con los registros del cursor
        @return: -1 si el usuario no ha hecho click sobre alguna de las filas de la tabla, pulsa cancelar
            o cierra el cuadro de dialogo con la X. Devuelve el numero de fila seleccionada, si 
            pincha en la tabla y luego Aceptar.
        """
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self,dlgPadre)
        #Inicializa el formulario
        self.ui=Ui_frmSelec() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.__filaSeleccionada=-1    
            
        self.connect(self.ui.bttCancelar,QtCore.SIGNAL('clicked()'),self.bttCancelar)#si
        self.connect(self.ui.bttAceptar,QtCore.SIGNAL('clicked()'),self.bttAceptar)
        self.connect(self.ui.tableWidget, QtCore.SIGNAL("cellClicked(int,int)"), self.tabla_click)
        oUtilidadesFormularios.rellenaTableWidgetListaDicFilas(self.ui.tableWidget,listaDic)
    def bttCancelar(self):
        self.filaSeleccionada=None
        self.done(-1)
    def bttAceptar(self):
        self.filaSeleccionada=self.ui.tableWidget.currentRow()
        self.done(self.filaSeleccionada)
    def tabla_click(self,filaSeleccionada, columna):
        self.filaSeleccionada=filaSeleccionada
    def closeEvent(self, event):
        self.done(-1)
    def __set_filaSeleccionada(self,num_fila):
        self.__filaSeleccionada=num_fila
    def __get_filaSeleccionada(self):
        return self.__filaSeleccionada
    filaSeleccionada=property(__get_filaSeleccionada,__set_filaSeleccionada,"Fila seleccionada en la tabla del formulario")     