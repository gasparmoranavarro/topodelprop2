# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Qgs18/apps/qgis/python/plugins/TopoDelProp/forms_ui/frmPassword.ui'
#
# Created: Fri Nov 09 12:38:57 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmPassword(object):
    def setupUi(self, frmPassword):
        frmPassword.setObjectName(_fromUtf8("frmPassword"))
        frmPassword.resize(386, 414)
        frmPassword.setWindowTitle(QtGui.QApplication.translate("frmPassword", "TopoDelProp: Usuarios.", None, QtGui.QApplication.UnicodeUTF8))
        self.label = QtGui.QLabel(frmPassword)
        self.label.setGeometry(QtCore.QRect(10, 220, 381, 16))
        self.label.setText(QtGui.QApplication.translate("frmPassword", "Usuario:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtUsuario = QtGui.QLineEdit(frmPassword)
        self.txtUsuario.setGeometry(QtCore.QRect(10, 240, 361, 22))
        self.txtUsuario.setObjectName(_fromUtf8("txtUsuario"))
        self.txtPsw1 = QtGui.QLineEdit(frmPassword)
        self.txtPsw1.setGeometry(QtCore.QRect(10, 290, 361, 22))
        self.txtPsw1.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPsw1.setObjectName(_fromUtf8("txtPsw1"))
        self.txtPsw2 = QtGui.QLineEdit(frmPassword)
        self.txtPsw2.setGeometry(QtCore.QRect(10, 340, 361, 22))
        self.txtPsw2.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPsw2.setObjectName(_fromUtf8("txtPsw2"))
        self.label_2 = QtGui.QLabel(frmPassword)
        self.label_2.setGeometry(QtCore.QRect(10, 270, 101, 16))
        self.label_2.setText(QtGui.QApplication.translate("frmPassword", "Contraseña:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(frmPassword)
        self.label_3.setGeometry(QtCore.QRect(10, 320, 131, 16))
        self.label_3.setText(QtGui.QApplication.translate("frmPassword", "Confirme contraseña:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.bttAceptar = QtGui.QPushButton(frmPassword)
        self.bttAceptar.setGeometry(QtCore.QRect(100, 370, 93, 28))
        self.bttAceptar.setText(QtGui.QApplication.translate("frmPassword", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAceptar.setObjectName(_fromUtf8("bttAceptar"))
        self.bttCancelar = QtGui.QPushButton(frmPassword)
        self.bttCancelar.setGeometry(QtCore.QRect(200, 370, 93, 28))
        self.bttCancelar.setText(QtGui.QApplication.translate("frmPassword", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttCancelar.setObjectName(_fromUtf8("bttCancelar"))
        self.plainTextEdit = QtGui.QPlainTextEdit(frmPassword)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 20, 361, 191))
        self.plainTextEdit.setToolTip(QtGui.QApplication.translate("frmPassword", "Condiciones para crear usuarios", None, QtGui.QApplication.UnicodeUTF8))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlainText(QtGui.QApplication.translate("frmPassword", "Asegúrese de:\n"
"       - Que la longitud del nombre de usuario está entre 10 y 25 caractéres.\n"
"        - Que comienza por una letra del abecedario. Esto es necesario para los\n"
"            usuarios de postgres.\n"
"        - Que la contraseña tiene una longitud mínima de 15 caractéres y:\n"
"            - Tiene algún número.\n"
"            - Tiene alguno de los siguientes caractéres =,<,>,@,#,%,$", None, QtGui.QApplication.UnicodeUTF8))
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))

        self.retranslateUi(frmPassword)
        QtCore.QMetaObject.connectSlotsByName(frmPassword)

    def retranslateUi(self, frmPassword):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmPassword = QtGui.QDialog()
    ui = Ui_frmPassword()
    ui.setupUi(frmPassword)
    frmPassword.show()
    sys.exit(app.exec_())

