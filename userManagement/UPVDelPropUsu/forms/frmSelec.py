# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms_ui/frmSelec.ui'
#
# Created: Wed Jul 18 12:50:20 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmSelec(object):
    def setupUi(self, frmSelec):
        frmSelec.setObjectName(_fromUtf8("frmSelec"))
        frmSelec.resize(972, 310)
        frmSelec.setWindowTitle(QtGui.QApplication.translate("frmSelec", "Seleccionar trabajo", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget = QtGui.QTableWidget(frmSelec)
        self.tableWidget.setGeometry(QtCore.QRect(10, 30, 951, 231))
        self.tableWidget.setToolTip(QtGui.QApplication.translate("frmSelec", "Seleccione una fila y pulse aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.bttAceptar = QtGui.QPushButton(frmSelec)
        self.bttAceptar.setGeometry(QtCore.QRect(440, 270, 111, 31))
        self.bttAceptar.setText(QtGui.QApplication.translate("frmSelec", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAceptar.setObjectName(_fromUtf8("bttAceptar"))
        self.bttCancelar = QtGui.QPushButton(frmSelec)
        self.bttCancelar.setGeometry(QtCore.QRect(570, 270, 91, 31))
        self.bttCancelar.setText(QtGui.QApplication.translate("frmSelec", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttCancelar.setObjectName(_fromUtf8("bttCancelar"))
        self.label = QtGui.QLabel(frmSelec)
        self.label.setGeometry(QtCore.QRect(20, 10, 331, 16))
        self.label.setText(QtGui.QApplication.translate("frmSelec", "Selecciones el trabajo que desea consultar:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(frmSelec)
        QtCore.QMetaObject.connectSlotsByName(frmSelec)

    def retranslateUi(self, frmSelec):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmSelec = QtGui.QDialog()
    ui = Ui_frmSelec()
    ui.setupUi(frmSelec)
    frmSelec.show()
    sys.exit(app.exec_())

