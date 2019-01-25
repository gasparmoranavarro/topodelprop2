# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms_ui/frmSelEsquema.ui'
#
# Created: Mon Jul 30 16:57:07 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmSelEsquema(object):
    def setupUi(self, frmSelEsquema):
        frmSelEsquema.setObjectName(_fromUtf8("frmSelEsquema"))
        frmSelEsquema.resize(293, 302)
        frmSelEsquema.setWindowTitle(QtGui.QApplication.translate("frmSelEsquema", "Seleccione dónde buscar", None, QtGui.QApplication.UnicodeUTF8))
        self.lwTipoTrabajo = QtGui.QListWidget(frmSelEsquema)
        self.lwTipoTrabajo.setGeometry(QtCore.QRect(10, 30, 271, 81))
        self.lwTipoTrabajo.setObjectName(_fromUtf8("lwTipoTrabajo"))
        self.lwSrc = QtGui.QListWidget(frmSelEsquema)
        self.lwSrc.setGeometry(QtCore.QRect(10, 140, 271, 121))
        self.lwSrc.setObjectName(_fromUtf8("lwSrc"))
        self.label = QtGui.QLabel(frmSelEsquema)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 16))
        self.label.setText(QtGui.QApplication.translate("frmSelEsquema", "Seleccione el tipo de trabajo:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(frmSelEsquema)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 251, 16))
        self.label_2.setText(QtGui.QApplication.translate("frmSelEsquema", "Seleccione el sistema de coordenadas:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.bttAceptar = QtGui.QPushButton(frmSelEsquema)
        self.bttAceptar.setGeometry(QtCore.QRect(90, 270, 93, 28))
        self.bttAceptar.setText(QtGui.QApplication.translate("frmSelEsquema", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAceptar.setObjectName(_fromUtf8("bttAceptar"))

        self.retranslateUi(frmSelEsquema)
        QtCore.QMetaObject.connectSlotsByName(frmSelEsquema)

    def retranslateUi(self, frmSelEsquema):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmSelEsquema = QtGui.QDialog()
    ui = Ui_frmSelEsquema()
    ui.setupUi(frmSelEsquema)
    frmSelEsquema.show()
    sys.exit(app.exec_())

