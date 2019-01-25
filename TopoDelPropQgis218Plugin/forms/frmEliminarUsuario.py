# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms_ui/frmEliminarUsuario.ui'
#
# Created: Sat Sep 08 15:51:14 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmEliminarUsuario(object):
    def setupUi(self, frmEliminarUsuario):
        frmEliminarUsuario.setObjectName(_fromUtf8("frmEliminarUsuario"))
        frmEliminarUsuario.resize(332, 126)
        frmEliminarUsuario.setWindowTitle(QtGui.QApplication.translate("frmEliminarUsuario", "UPV-DelProp: eliminar usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.label = QtGui.QLabel(frmEliminarUsuario)
        self.label.setGeometry(QtCore.QRect(20, 20, 351, 16))
        self.label.setText(QtGui.QApplication.translate("frmEliminarUsuario", "Usuario a eliminar:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtUsuario = QtGui.QLineEdit(frmEliminarUsuario)
        self.txtUsuario.setGeometry(QtCore.QRect(20, 50, 291, 22))
        self.txtUsuario.setObjectName(_fromUtf8("txtUsuario"))
        self.bttEiminar = QtGui.QPushButton(frmEliminarUsuario)
        self.bttEiminar.setGeometry(QtCore.QRect(60, 80, 93, 28))
        self.bttEiminar.setText(QtGui.QApplication.translate("frmEliminarUsuario", "Eliminar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttEiminar.setObjectName(_fromUtf8("bttEiminar"))
        self.bttCancelar = QtGui.QPushButton(frmEliminarUsuario)
        self.bttCancelar.setGeometry(QtCore.QRect(170, 80, 93, 28))
        self.bttCancelar.setText(QtGui.QApplication.translate("frmEliminarUsuario", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttCancelar.setObjectName(_fromUtf8("bttCancelar"))

        self.retranslateUi(frmEliminarUsuario)
        QtCore.QMetaObject.connectSlotsByName(frmEliminarUsuario)

    def retranslateUi(self, frmEliminarUsuario):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmEliminarUsuario = QtGui.QDialog()
    ui = Ui_frmEliminarUsuario()
    ui.setupUi(frmEliminarUsuario)
    frmEliminarUsuario.show()
    sys.exit(app.exec_())

