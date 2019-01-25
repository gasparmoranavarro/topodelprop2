# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmAtribFinca.ui'
#
# Created: Tue Dec 20 13:08:44 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmAtribFinca(object):
    def setupUi(self, frmAtribFinca):
        frmAtribFinca.setObjectName(_fromUtf8("frmAtribFinca"))
        frmAtribFinca.resize(480, 283)
        frmAtribFinca.setWindowTitle(QtGui.QApplication.translate("frmAtribFinca", "Atributos de la finca", None, QtGui.QApplication.UnicodeUTF8))
        self.bttCalcular = QtGui.QPushButton(frmAtribFinca)
        self.bttCalcular.setGeometry(QtCore.QRect(270, 230, 75, 23))
        self.bttCalcular.setToolTip(QtGui.QApplication.translate("frmAtribFinca", "Pulse para calcular", None, QtGui.QApplication.UnicodeUTF8))
        self.bttCalcular.setText(QtGui.QApplication.translate("frmAtribFinca", "Calcular", None, QtGui.QApplication.UnicodeUTF8))
        self.bttCalcular.setObjectName(_fromUtf8("bttCalcular"))
        self.txtA = QtGui.QLineEdit(frmAtribFinca)
        self.txtA.setGeometry(QtCore.QRect(150, 40, 231, 20))
        self.txtA.setObjectName(_fromUtf8("txtA"))
        self.txtB = QtGui.QLineEdit(frmAtribFinca)
        self.txtB.setGeometry(QtCore.QRect(150, 80, 231, 20))
        self.txtB.setObjectName(_fromUtf8("txtB"))
        self.txtResultado = QtGui.QLineEdit(frmAtribFinca)
        self.txtResultado.setGeometry(QtCore.QRect(150, 120, 231, 20))
        self.txtResultado.setText(_fromUtf8(""))
        self.txtResultado.setReadOnly(True)
        self.txtResultado.setObjectName(_fromUtf8("txtResultado"))

        self.retranslateUi(frmAtribFinca)
        QtCore.QMetaObject.connectSlotsByName(frmAtribFinca)

    def retranslateUi(self, frmAtribFinca):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmAtribFinca = QtGui.QDialog()
    ui = Ui_frmAtribFinca()
    ui.setupUi(frmAtribFinca)
    frmAtribFinca.show()
    sys.exit(app.exec_())

