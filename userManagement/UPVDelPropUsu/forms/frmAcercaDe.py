# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Qgs18/apps/qgis/python/plugins/TopoDelProp/forms_ui/frmAcercaDe.ui'
#
# Created: Fri Nov 09 12:37:26 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmAcercaDe(object):
    def setupUi(self, frmAcercaDe):
        frmAcercaDe.setObjectName(_fromUtf8("frmAcercaDe"))
        frmAcercaDe.resize(566, 320)
        frmAcercaDe.setWindowTitle(QtGui.QApplication.translate("frmAcercaDe", "TopoDelProp", None, QtGui.QApplication.UnicodeUTF8))
        self.label = QtGui.QLabel(frmAcercaDe)
        self.label.setGeometry(QtCore.QRect(190, 10, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setText(QtGui.QApplication.translate("frmAcercaDe", "TopoDelProp", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(frmAcercaDe)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 471, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setText(QtGui.QApplication.translate("frmAcercaDe", "Programa para la gestión de los datos topográficos", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(frmAcercaDe)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 531, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setText(QtGui.QApplication.translate("frmAcercaDe", "generados al delimitar una finca registral sobre el terreno", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(frmAcercaDe)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setText(QtGui.QApplication.translate("frmAcercaDe", "Autor:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(frmAcercaDe)
        self.label_5.setGeometry(QtCore.QRect(70, 260, 461, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setText(QtGui.QApplication.translate("frmAcercaDe", "Dep. de Ingeniería Cartográfica, Geodesia y Fotogrametría", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(frmAcercaDe)
        self.label_6.setGeometry(QtCore.QRect(70, 230, 301, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setText(QtGui.QApplication.translate("frmAcercaDe", "Universidad Politécnica de Valencia", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(frmAcercaDe)
        self.label_7.setGeometry(QtCore.QRect(70, 200, 421, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setText(QtGui.QApplication.translate("frmAcercaDe", "J. Gaspar Mora Navarro", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(frmAcercaDe)
        self.label_8.setGeometry(QtCore.QRect(70, 290, 461, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setText(QtGui.QApplication.translate("frmAcercaDe", "topodelprop@gmail.com", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(frmAcercaDe)
        self.label_9.setGeometry(QtCore.QRect(20, 60, 521, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setText(QtGui.QApplication.translate("frmAcercaDe", "Delimitación de la propiedad por topografía clásica", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))

        self.retranslateUi(frmAcercaDe)
        QtCore.QMetaObject.connectSlotsByName(frmAcercaDe)

    def retranslateUi(self, frmAcercaDe):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmAcercaDe = QtGui.QDialog()
    ui = Ui_frmAcercaDe()
    ui.setupUi(frmAcercaDe)
    frmAcercaDe.show()
    sys.exit(app.exec_())

