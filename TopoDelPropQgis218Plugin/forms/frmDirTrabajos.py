# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms_ui/frmDirTrabajos.ui'
#
# Created: Sat May 26 17:06:20 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmDirTrabajos(object):
    def setupUi(self, frmDirTrabajos):
        frmDirTrabajos.setObjectName(_fromUtf8("frmDirTrabajos"))
        frmDirTrabajos.resize(568, 300)
        frmDirTrabajos.setWindowTitle(QtGui.QApplication.translate("frmDirTrabajos", "Seleccione un directorio para almacenar los trabajos", None, QtGui.QApplication.UnicodeUTF8))
        self.label = QtGui.QLabel(frmDirTrabajos)
        self.label.setGeometry(QtCore.QRect(20, 10, 441, 21))
        self.label.setText(QtGui.QApplication.translate("frmDirTrabajos", "Seleccione un directorio para almacenar datos de los trabajos.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(frmDirTrabajos)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 431, 16))
        self.label_2.setText(QtGui.QApplication.translate("frmDirTrabajos", "Debe ser un directorio donde tenga permiso de escritura.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(frmDirTrabajos)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 531, 16))
        self.label_3.setText(QtGui.QApplication.translate("frmDirTrabajos", "La ruta al directorio se almacenará en el archivo dirTrabajos.txt", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(frmDirTrabajos)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 541, 16))
        self.label_4.setText(QtGui.QApplication.translate("frmDirTrabajos", "Se intentará guardar este archivo en el directorio base donde se guarda este programa,", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(frmDirTrabajos)
        self.label_5.setGeometry(QtCore.QRect(50, 90, 511, 20))
        self.label_5.setText(QtGui.QApplication.translate("frmDirTrabajos", "si no se consigue, se intentará guardar en c:/, y si esto también falla, si no desea", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(frmDirTrabajos)
        self.label_6.setGeometry(QtCore.QRect(50, 110, 491, 16))
        self.label_6.setText(QtGui.QApplication.translate("frmDirTrabajos", "que aparezca este cuadro siempre que ejecute el programa,", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(frmDirTrabajos)
        self.label_7.setGeometry(QtCore.QRect(50, 130, 501, 16))
        self.label_7.setText(QtGui.QApplication.translate("frmDirTrabajos", ", tendrá que crear el archivo c:/dirTrabajos.txt e introducir la ruta usted mismo.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(frmDirTrabajos)
        self.label_8.setGeometry(QtCore.QRect(20, 150, 531, 16))
        self.label_8.setText(QtGui.QApplication.translate("frmDirTrabajos", "La ruta a los trabajos no debe contener acentos, ni eñes, ni espacios, y debe tener", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(frmDirTrabajos)
        self.label_9.setGeometry(QtCore.QRect(20, 170, 531, 16))
        self.label_9.setText(QtGui.QApplication.translate("frmDirTrabajos", "la barra de dividir para separar las carpetas. Por ejemplo c:/Trabajos/delProp", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(frmDirTrabajos)
        self.label_10.setGeometry(QtCore.QRect(20, 210, 181, 16))
        self.label_10.setText(QtGui.QApplication.translate("frmDirTrabajos", "Directorio para los trabajos:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.tbDirTrabajos = QtGui.QLineEdit(frmDirTrabajos)
        self.tbDirTrabajos.setGeometry(QtCore.QRect(20, 230, 381, 20))
        self.tbDirTrabajos.setObjectName(_fromUtf8("tbDirTrabajos"))
        self.bttSeleccionar = QtGui.QPushButton(frmDirTrabajos)
        self.bttSeleccionar.setGeometry(QtCore.QRect(410, 230, 91, 23))
        self.bttSeleccionar.setText(QtGui.QApplication.translate("frmDirTrabajos", "Seleccionar ...", None, QtGui.QApplication.UnicodeUTF8))
        self.bttSeleccionar.setObjectName(_fromUtf8("bttSeleccionar"))
        self.bttAceptar = QtGui.QPushButton(frmDirTrabajos)
        self.bttAceptar.setGeometry(QtCore.QRect(190, 260, 75, 23))
        self.bttAceptar.setText(QtGui.QApplication.translate("frmDirTrabajos", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAceptar.setObjectName(_fromUtf8("bttAceptar"))

        self.retranslateUi(frmDirTrabajos)
        QtCore.QMetaObject.connectSlotsByName(frmDirTrabajos)

    def retranslateUi(self, frmDirTrabajos):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmDirTrabajos = QtGui.QDialog()
    ui = Ui_frmDirTrabajos()
    ui.setupUi(frmDirTrabajos)
    frmDirTrabajos.show()
    sys.exit(app.exec_())

