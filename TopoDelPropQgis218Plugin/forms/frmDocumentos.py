# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms_ui/frmDocumentos.ui'
#
# Created: Sun May 20 11:02:31 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgDocumentos(object):
    def setupUi(self, dlgDocumentos):
        dlgDocumentos.setObjectName(_fromUtf8("dlgDocumentos"))
        dlgDocumentos.setWindowModality(QtCore.Qt.WindowModal)
        dlgDocumentos.resize(761, 272)
        dlgDocumentos.setWindowTitle(QtGui.QApplication.translate("dlgDocumentos", "Archivos asociados al trabajo", None, QtGui.QApplication.UnicodeUTF8))
        dlgDocumentos.setToolTip(QtGui.QApplication.translate("dlgDocumentos", "Añade archivos al trabajo", None, QtGui.QApplication.UnicodeUTF8))
        dlgDocumentos.setModal(True)
        self.tableWidget = QtGui.QTableWidget(dlgDocumentos)
        self.tableWidget.setGeometry(QtCore.QRect(20, 40, 721, 192))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.bttAadir = QtGui.QPushButton(dlgDocumentos)
        self.bttAadir.setGeometry(QtCore.QRect(20, 240, 131, 23))
        self.bttAadir.setToolTip(QtGui.QApplication.translate("dlgDocumentos", "Añade una fila a la tabla para añadir un documento", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAadir.setText(QtGui.QApplication.translate("dlgDocumentos", "Agregar documento", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAadir.setObjectName(_fromUtf8("bttAadir"))
        self.bttEliminar = QtGui.QPushButton(dlgDocumentos)
        self.bttEliminar.setGeometry(QtCore.QRect(160, 240, 131, 23))
        self.bttEliminar.setToolTip(QtGui.QApplication.translate("dlgDocumentos", "Elimina la fila actual", None, QtGui.QApplication.UnicodeUTF8))
        self.bttEliminar.setText(QtGui.QApplication.translate("dlgDocumentos", "Eliminar documento", None, QtGui.QApplication.UnicodeUTF8))
        self.bttEliminar.setObjectName(_fromUtf8("bttEliminar"))
        self.bttTerminar = QtGui.QPushButton(dlgDocumentos)
        self.bttTerminar.setGeometry(QtCore.QRect(660, 240, 81, 23))
        self.bttTerminar.setToolTip(QtGui.QApplication.translate("dlgDocumentos", "Sale de este cuadro de diálogo", None, QtGui.QApplication.UnicodeUTF8))
        self.bttTerminar.setText(QtGui.QApplication.translate("dlgDocumentos", "Terminar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttTerminar.setObjectName(_fromUtf8("bttTerminar"))
        self.bttGuardar = QtGui.QPushButton(dlgDocumentos)
        self.bttGuardar.setGeometry(QtCore.QRect(580, 240, 75, 23))
        self.bttGuardar.setToolTip(QtGui.QApplication.translate("dlgDocumentos", "Guarda los datos en el disco local", None, QtGui.QApplication.UnicodeUTF8))
        self.bttGuardar.setText(QtGui.QApplication.translate("dlgDocumentos", "Guardar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttGuardar.setObjectName(_fromUtf8("bttGuardar"))
        self.label = QtGui.QLabel(dlgDocumentos)
        self.label.setGeometry(QtCore.QRect(20, 20, 541, 16))
        self.label.setText(QtGui.QApplication.translate("dlgDocumentos", "Introduzca los datos de los archivos a almacenar:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(dlgDocumentos)
        QtCore.QMetaObject.connectSlotsByName(dlgDocumentos)

    def retranslateUi(self, dlgDocumentos):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlgDocumentos = QtGui.QDialog()
    ui = Ui_dlgDocumentos()
    ui.setupUi(dlgDocumentos)
    dlgDocumentos.show()
    sys.exit(app.exec_())

