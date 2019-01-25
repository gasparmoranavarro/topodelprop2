# This Python file uses the following encoding: utf-8
'''
Created on 11/05/2012
@author: J. Gaspar Mora Navarro
'''

import sys
from PyQt4 import QtCore, QtGui

from forms.frmPassword import Ui_frmPassword

class ctrFrmPassword(QtGui.QDialog):
    """
    Realiza las siguientes comprobaciones:
        - Que la longitud del nombre de usuario está entre 10 y 25 caractéres.
        - Pasa e usuario a minúsculas. Si no luego no se puede conectar
        - El usuario ni el password pueden tener acentos, eñes o los caractéres ;:
        - Que comienza por una letra del abecedario. Esto es necesario para los
            usuarios de postgres.
        - Que la contraseña tiene una longitud mínima de 15 caractéres y:
            - Tiene algún número.
            - Tiene alguno de los siguientes caractéres =,<,>,@,#,%,$
    Si se cumplen todas get_ok() vale True.
    Si se cierra el cuadro de diálgo con la X, get_ok() vale False
    @return: 1 si es todo correcto. 0 caso contrario.
    """

    #constructor
    def __init__(self, iface):
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self)
        #Inicializa el formulario
        self.ui=Ui_frmPassword() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.iface=iface
        self.ok=False
        self.usuario=None#ya esta en unicode
        self.password=None
        #inicializa las variables de la clase
        self.connect(self.ui.bttAceptar, QtCore.SIGNAL("clicked()"),self.bttAceptar)
        self.connect(self.ui.bttCancelar, QtCore.SIGNAL("clicked()"),self.bttCancelar)

    def bttAceptar(self):
        try:
            self.usuario=str(self.ui.txtUsuario.text()).lower()#se crean en minusculas. PG no admite mayusculas
            psw1=str(self.ui.txtPsw1.text())
            psw2=str(self.ui.txtPsw2.text())
        except Exception, e:
            QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("No se soportan acentos ni eñes. " + self.toUtf8(e.message)),1)
            return
        if not(len(self.usuario)>9 and len(self.usuario)<26):
            QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("El usuario debe tener una longitud entre 10 y 25 caractéres."),1)
            return
        abecedario="abcdefghijklmnñopqrstuvwxyz"
        if not(self.usuario[0].lower() in abecedario):
            mens=self.toUtf8("El primer carácter del usuario debe encontarse en el abecedario.")
            QtGui.QMessageBox.information(self, "Error",mens,1)
            return

        caracteresNO=" áéíóúñ:/\\@#4$%&?¿¡¿ºª=<>\"\';"
        tieneCar=False

        for car in caracteresNO:
            if car in self.usuario:
                tieneCar=True
                break
            
        if tieneCar==True:
            mens=self.toUtf8("Los usuarios no deben tener ninguno de los siguientes caractéres: " + caracteresNO)
            QtGui.QMessageBox.information(self, "Error",mens,1)
            return
        
        tieneCar=False
        caracteresNO="áéíóúñ:/\\\"\';"
        for car in caracteresNO:
            if car in psw1:
                tieneCar=True
                break
        if tieneCar==True:
            mens=self.toUtf8("Las contraseñas no deben tener ninguno de los siguientes caractéres: " + caracteresNO)
            QtGui.QMessageBox.information(self, "Error",mens,1)
            return

        if self.usuario==psw1:
            QtGui.QMessageBox.information(self, 'Error', self.toUtf8("El usuario y la contraseña no pueden ser iguales") ,1)
            return
        if psw1!=psw2:
            QtGui.QMessageBox.information(self, "Error", self.toUtf8("Las contraseñas no coinciden"),1)
            return
        if len(psw1)<15:
            mens=self.toUtf8("Las contraseñas deben tener, por lo menos, 15 caractéres.")
            QtGui.QMessageBox.information(self, "Error",mens,1)
            return
        
        numeros="0123456789"
        tieneNum=False
        for num in numeros:
            if num in psw1:
                tieneNum=True
                break
        if tieneNum==False:
            mens=self.toUtf8("Las contraseñas deben tener, por lo menos, un número.")
            QtGui.QMessageBox.information(self, "Error",mens,1)
            return
        caracteres="=<>@#%$"
        tieneCar=False
        for car in caracteres:
            if car in psw1:
                tieneCar=True
                break
        if tieneCar==False:
            mens=self.toUtf8("Las contraseñas deben tener, por lo menos, uno de los siguientes caractéres: =,<,>,@,#,%,$")
            QtGui.QMessageBox.information(self, "Error",mens,1)
            return
        self.password=psw1
        self.ok=True
        self.done(1)
    
    def bttCancelar(self):
        self.ok=False
        self.close()
    def toUtf8(self,mens):
        return unicode(mens,"utf-8")
    def get_ok(self):
        return self.ok
    def get_password(self):
        return self.password
    def get_usuario(self):
        return self.usuario
    def closeEvent(self, event):
        """
        Se ejecuta en el caso de de el usuario pulse la X del formulario
        Se muestra un cuadro de dialogo para permitir al usuario volver
        al cuadro de dialogo o salir.
        """
        self.ok=False
        self.done(0)