# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmCompilar.ui'
#
# Created: Tue Mar 06 00:19:03 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmCompilar(object):
    def setupUi(self, frmCompilar):
        frmCompilar.setObjectName(_fromUtf8("frmCompilar"))
        frmCompilar.resize(618, 275)
        frmCompilar.setWindowTitle(QtGui.QApplication.translate("frmCompilar", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.txtArchEntrada = QtGui.QLineEdit(frmCompilar)
        self.txtArchEntrada.setGeometry(QtCore.QRect(30, 110, 401, 31))
        self.txtArchEntrada.setText(QtGui.QApplication.translate("frmCompilar", "C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms_ui", None, QtGui.QApplication.UnicodeUTF8))
        self.txtArchEntrada.setObjectName(_fromUtf8("txtArchEntrada"))
        self.label = QtGui.QLabel(frmCompilar)
        self.label.setGeometry(QtCore.QRect(40, 90, 181, 16))
        self.label.setText(QtGui.QApplication.translate("frmCompilar", "Archivo de entrada:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtArchSalida = QtGui.QLineEdit(frmCompilar)
        self.txtArchSalida.setGeometry(QtCore.QRect(30, 170, 401, 31))
        self.txtArchSalida.setText(QtGui.QApplication.translate("frmCompilar", "C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms", None, QtGui.QApplication.UnicodeUTF8))
        self.txtArchSalida.setObjectName(_fromUtf8("txtArchSalida"))
        self.label_2 = QtGui.QLabel(frmCompilar)
        self.label_2.setGeometry(QtCore.QRect(30, 150, 401, 16))
        self.label_2.setText(QtGui.QApplication.translate("frmCompilar", "Archivo de salida (machaca archivos existentes):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.bttArchEntrada = QtGui.QPushButton(frmCompilar)
        self.bttArchEntrada.setGeometry(QtCore.QRect(450, 110, 151, 31))
        self.bttArchEntrada.setText(QtGui.QApplication.translate("frmCompilar", "Archivo entrada ...", None, QtGui.QApplication.UnicodeUTF8))
        self.bttArchEntrada.setObjectName(_fromUtf8("bttArchEntrada"))
        self.bttArchSalida = QtGui.QPushButton(frmCompilar)
        self.bttArchSalida.setGeometry(QtCore.QRect(450, 170, 151, 31))
        self.bttArchSalida.setText(QtGui.QApplication.translate("frmCompilar", "Archivo salida ...", None, QtGui.QApplication.UnicodeUTF8))
        self.bttArchSalida.setObjectName(_fromUtf8("bttArchSalida"))
        self.bttGenerar = QtGui.QPushButton(frmCompilar)
        self.bttGenerar.setGeometry(QtCore.QRect(120, 230, 111, 31))
        self.bttGenerar.setText(QtGui.QApplication.translate("frmCompilar", "Generar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttGenerar.setObjectName(_fromUtf8("bttGenerar"))
        self.bttTerminar = QtGui.QPushButton(frmCompilar)
        self.bttTerminar.setGeometry(QtCore.QRect(250, 230, 101, 31))
        self.bttTerminar.setText(QtGui.QApplication.translate("frmCompilar", "Terminar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttTerminar.setObjectName(_fromUtf8("bttTerminar"))
        self.bttMismo = QtGui.QPushButton(frmCompilar)
        self.bttMismo.setGeometry(QtCore.QRect(450, 200, 151, 31))
        self.bttMismo.setText(QtGui.QApplication.translate("frmCompilar", "Salida en el mismo directorio", None, QtGui.QApplication.UnicodeUTF8))
        self.bttMismo.setObjectName(_fromUtf8("bttMismo"))
        self.bttRutaPyuic4 = QtGui.QPushButton(frmCompilar)
        self.bttRutaPyuic4.setGeometry(QtCore.QRect(450, 52, 151, 31))
        self.bttRutaPyuic4.setText(QtGui.QApplication.translate("frmCompilar", "Ruta ...", None, QtGui.QApplication.UnicodeUTF8))
        self.bttRutaPyuic4.setObjectName(_fromUtf8("bttRutaPyuic4"))
        self.txtRutaPyuic4 = QtGui.QLineEdit(frmCompilar)
        self.txtRutaPyuic4.setGeometry(QtCore.QRect(30, 50, 401, 31))
        self.txtRutaPyuic4.setText(QtGui.QApplication.translate("frmCompilar", "C:/Python27/Lib/site-packages/PyQt4/pyuic4.bat", None, QtGui.QApplication.UnicodeUTF8))
        self.txtRutaPyuic4.setObjectName(_fromUtf8("txtRutaPyuic4"))
        self.label_3 = QtGui.QLabel(frmCompilar)
        self.label_3.setGeometry(QtCore.QRect(30, 30, 151, 16))
        self.label_3.setText(QtGui.QApplication.translate("frmCompilar", "Ruta al archivo pyuic4.bat", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(frmCompilar)
        QtCore.QMetaObject.connectSlotsByName(frmCompilar)

    def retranslateUi(self, frmCompilar):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmCompilar = QtGui.QDialog()
    ui = Ui_frmCompilar()
    ui.setupUi(frmCompilar)
    frmCompilar.show()
    sys.exit(app.exec_())

