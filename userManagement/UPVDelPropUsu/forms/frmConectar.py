# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Qgs18/apps/qgis/python/plugins/TopoDelProp/forms_ui/frmConectar.ui'
#
# Created: Fri Nov 09 12:37:52 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmConectar(object):
    def setupUi(self, frmConectar):
        frmConectar.setObjectName(_fromUtf8("frmConectar"))
        frmConectar.resize(371, 251)
        frmConectar.setWindowTitle(QtGui.QApplication.translate("frmConectar", "TopoDelProp-Conectar", None, QtGui.QApplication.UnicodeUTF8))
        self.tbHost = QtGui.QLineEdit(frmConectar)
        self.tbHost.setGeometry(QtCore.QRect(100, 30, 251, 20))
        self.tbHost.setText(QtGui.QApplication.translate("frmConectar", "localhost", None, QtGui.QApplication.UnicodeUTF8))
        self.tbHost.setObjectName(_fromUtf8("tbHost"))
        self.tbBda = QtGui.QLineEdit(frmConectar)
        self.tbBda.setGeometry(QtCore.QRect(100, 100, 251, 20))
        self.tbBda.setText(QtGui.QApplication.translate("frmConectar", "propiedad", None, QtGui.QApplication.UnicodeUTF8))
        self.tbBda.setObjectName(_fromUtf8("tbBda"))
        self.tbNumCol = QtGui.QLineEdit(frmConectar)
        self.tbNumCol.setGeometry(QtCore.QRect(100, 130, 251, 20))
        self.tbNumCol.setText(_fromUtf8(""))
        self.tbNumCol.setObjectName(_fromUtf8("tbNumCol"))
        self.label = QtGui.QLabel(frmConectar)
        self.label.setGeometry(QtCore.QRect(20, 30, 46, 13))
        self.label.setText(QtGui.QApplication.translate("frmConectar", "Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(frmConectar)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 81, 16))
        self.label_2.setText(QtGui.QApplication.translate("frmConectar", "Base de datos:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_4 = QtGui.QLabel(frmConectar)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 121, 16))
        self.label_4.setText(QtGui.QApplication.translate("frmConectar", "Usuario:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(frmConectar)
        self.label_5.setGeometry(QtCore.QRect(20, 170, 121, 16))
        self.label_5.setText(QtGui.QApplication.translate("frmConectar", "Contraseña:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.tbContr = QtGui.QLineEdit(frmConectar)
        self.tbContr.setGeometry(QtCore.QRect(100, 170, 251, 20))
        self.tbContr.setInputMask(_fromUtf8(""))
        self.tbContr.setText(_fromUtf8(""))
        self.tbContr.setEchoMode(QtGui.QLineEdit.Password)
        self.tbContr.setPlaceholderText(_fromUtf8(""))
        self.tbContr.setObjectName(_fromUtf8("tbContr"))
        self.bttConectar = QtGui.QPushButton(frmConectar)
        self.bttConectar.setGeometry(QtCore.QRect(150, 200, 75, 23))
        self.bttConectar.setText(QtGui.QApplication.translate("frmConectar", "Conectar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttConectar.setObjectName(_fromUtf8("bttConectar"))
        self.lbEstado = QtGui.QLabel(frmConectar)
        self.lbEstado.setGeometry(QtCore.QRect(10, 230, 341, 16))
        self.lbEstado.setText(_fromUtf8(""))
        self.lbEstado.setObjectName(_fromUtf8("lbEstado"))
        self.tbPort = QtGui.QLineEdit(frmConectar)
        self.tbPort.setGeometry(QtCore.QRect(100, 60, 251, 20))
        self.tbPort.setText(QtGui.QApplication.translate("frmConectar", "5432", None, QtGui.QApplication.UnicodeUTF8))
        self.tbPort.setObjectName(_fromUtf8("tbPort"))
        self.label_6 = QtGui.QLabel(frmConectar)
        self.label_6.setGeometry(QtCore.QRect(20, 70, 46, 13))
        self.label_6.setText(QtGui.QApplication.translate("frmConectar", "Puerto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))

        self.retranslateUi(frmConectar)
        QtCore.QMetaObject.connectSlotsByName(frmConectar)

    def retranslateUi(self, frmConectar):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmConectar = QtGui.QDialog()
    ui = Ui_frmConectar()
    ui.setupUi(frmConectar)
    frmConectar.show()
    sys.exit(app.exec_())

