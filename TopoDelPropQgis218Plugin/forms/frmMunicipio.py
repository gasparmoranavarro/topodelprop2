# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Qgs18/apps/qgis/python/plugins/TopoDelProp/forms_ui/frmMunicipio.ui'
#
# Created: Fri Nov 09 12:38:35 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmMunicipio(object):
    def setupUi(self, frmMunicipio):
        frmMunicipio.setObjectName(_fromUtf8("frmMunicipio"))
        frmMunicipio.resize(338, 346)
        frmMunicipio.setWindowTitle(QtGui.QApplication.translate("frmMunicipio", "TopoDelProp-Municipio", None, QtGui.QApplication.UnicodeUTF8))
        self.label = QtGui.QLabel(frmMunicipio)
        self.label.setGeometry(QtCore.QRect(20, 120, 361, 16))
        self.label.setText(QtGui.QApplication.translate("frmMunicipio", "Seleccione el municipio:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.listWidget = QtGui.QListWidget(frmMunicipio)
        self.listWidget.setGeometry(QtCore.QRect(20, 170, 301, 131))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.txtMunicipio = QtGui.QLineEdit(frmMunicipio)
        self.txtMunicipio.setGeometry(QtCore.QRect(20, 140, 301, 22))
        self.txtMunicipio.setObjectName(_fromUtf8("txtMunicipio"))
        self.bttAceptar = QtGui.QPushButton(frmMunicipio)
        self.bttAceptar.setGeometry(QtCore.QRect(120, 310, 93, 28))
        self.bttAceptar.setText(QtGui.QApplication.translate("frmMunicipio", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAceptar.setObjectName(_fromUtf8("bttAceptar"))
        self.listWidgetSrc = QtGui.QListWidget(frmMunicipio)
        self.listWidgetSrc.setGeometry(QtCore.QRect(20, 30, 301, 71))
        self.listWidgetSrc.setObjectName(_fromUtf8("listWidgetSrc"))
        self.label_2 = QtGui.QLabel(frmMunicipio)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 361, 16))
        self.label_2.setText(QtGui.QApplication.translate("frmMunicipio", "Seleccione el SRC del municipio:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(frmMunicipio)
        QtCore.QMetaObject.connectSlotsByName(frmMunicipio)

    def retranslateUi(self, frmMunicipio):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmMunicipio = QtGui.QDialog()
    ui = Ui_frmMunicipio()
    ui.setupUi(frmMunicipio)
    frmMunicipio.show()
    sys.exit(app.exec_())

