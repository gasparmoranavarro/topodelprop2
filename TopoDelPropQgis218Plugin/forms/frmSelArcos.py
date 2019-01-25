# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms_ui/frmSelArcos.ui'
#
# Created: Sun May 20 11:03:07 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmSelArcos(object):
    def setupUi(self, frmSelArcos):
        frmSelArcos.setObjectName(_fromUtf8("frmSelArcos"))
        frmSelArcos.resize(452, 201)
        frmSelArcos.setWindowTitle(QtGui.QApplication.translate("frmSelArcos", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label = QtGui.QLabel(frmSelArcos)
        self.label.setGeometry(QtCore.QRect(30, 10, 381, 51))
        self.label.setText(QtGui.QApplication.translate("frmSelArcos", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Seleccione los arcos que conforman el perímetro de la finca y pulse Aceptar: </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.bttGrabarFinca = QtGui.QPushButton(frmSelArcos)
        self.bttGrabarFinca.setGeometry(QtCore.QRect(54, 70, 81, 23))
        self.bttGrabarFinca.setText(QtGui.QApplication.translate("frmSelArcos", "GrabarFinca", None, QtGui.QApplication.UnicodeUTF8))
        self.bttGrabarFinca.setObjectName(_fromUtf8("bttGrabarFinca"))
        self.lbNumEltos = QtGui.QLabel(frmSelArcos)
        self.lbNumEltos.setGeometry(QtCore.QRect(40, 130, 381, 16))
        self.lbNumEltos.setText(QtGui.QApplication.translate("frmSelArcos", "Numero de elementos seleccionados: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lbNumEltos.setObjectName(_fromUtf8("lbNumEltos"))
        self.lbCapa = QtGui.QLabel(frmSelArcos)
        self.lbCapa.setGeometry(QtCore.QRect(40, 160, 401, 16))
        self.lbCapa.setText(QtGui.QApplication.translate("frmSelArcos", "Capa del 1er elto:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbCapa.setObjectName(_fromUtf8("lbCapa"))
        self.bttGrabarLindes = QtGui.QPushButton(frmSelArcos)
        self.bttGrabarLindes.setGeometry(QtCore.QRect(150, 70, 91, 23))
        self.bttGrabarLindes.setText(QtGui.QApplication.translate("frmSelArcos", "GrabarLindes", None, QtGui.QApplication.UnicodeUTF8))
        self.bttGrabarLindes.setObjectName(_fromUtf8("bttGrabarLindes"))
        self.bttGrabarImagenes = QtGui.QPushButton(frmSelArcos)
        self.bttGrabarImagenes.setGeometry(QtCore.QRect(270, 70, 111, 23))
        self.bttGrabarImagenes.setText(QtGui.QApplication.translate("frmSelArcos", "GrabarImagenes", None, QtGui.QApplication.UnicodeUTF8))
        self.bttGrabarImagenes.setObjectName(_fromUtf8("bttGrabarImagenes"))
        self.bttCambiaImg = QtGui.QPushButton(frmSelArcos)
        self.bttCambiaImg.setGeometry(QtCore.QRect(270, 110, 111, 23))
        self.bttCambiaImg.setText(QtGui.QApplication.translate("frmSelArcos", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.bttCambiaImg.setObjectName(_fromUtf8("bttCambiaImg"))

        self.retranslateUi(frmSelArcos)
        QtCore.QMetaObject.connectSlotsByName(frmSelArcos)

    def retranslateUi(self, frmSelArcos):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmSelArcos = QtGui.QDialog()
    ui = Ui_frmSelArcos()
    ui.setupUi(frmSelArcos)
    frmSelArcos.show()
    sys.exit(app.exec_())

