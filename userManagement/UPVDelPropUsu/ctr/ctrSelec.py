# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
from forms.frmSelec import Ui_frmSelec

import sys
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
#from pydevd import *

class ctrSelec(QtGui.QDialog):
    """
    Muestra un cuadro de dialgogo con una tabla donde se introducen los valores de los
    campos que existen en el cursor psycopg2.
    Si el se usa el metodo exec_() para mostrar el formulario, el forulario retorna un entero.
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