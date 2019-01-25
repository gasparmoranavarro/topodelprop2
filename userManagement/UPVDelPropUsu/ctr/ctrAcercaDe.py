# This Python file uses the following encoding: utf-8
'''
Created on 11/05/2012
@author: J. Gaspar Mora Navarro
'''

import sys
from PyQt4 import QtCore, QtGui

import pyUPVBib.pyPgGas

from  forms.frmAcercaDe import Ui_frmAcercaDe

class ctrAcercaDe(QtGui.QDialog):

    #constructor
    def __init__(self):
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self)
        #Inicializa el formulario
        self.ui=Ui_frmAcercaDe() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
