# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms_ui/frmMuestraImg.ui'
#
# Created: Mon May 28 13:55:58 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmMuestraImg(object):
    def setupUi(self, frmMuestraImg):
        frmMuestraImg.setObjectName(_fromUtf8("frmMuestraImg"))
        frmMuestraImg.resize(902, 484)
        frmMuestraImg.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        frmMuestraImg.setAcceptDrops(False)
        frmMuestraImg.setWindowTitle(QtGui.QApplication.translate("frmMuestraImg", "Imagen del linde", None, QtGui.QApplication.UnicodeUTF8))
        frmMuestraImg.setToolTip(QtGui.QApplication.translate("frmMuestraImg", "Muestra la imagens del linde", None, QtGui.QApplication.UnicodeUTF8))
        frmMuestraImg.setInputMethodHints(QtCore.Qt.ImhNone)
        frmMuestraImg.setSizeGripEnabled(False)
        self.lbImg = QtGui.QLabel(frmMuestraImg)
        self.lbImg.setGeometry(QtCore.QRect(10, 40, 611, 401))
        self.lbImg.setToolTip(QtGui.QApplication.translate("frmMuestraImg", "Imagen del linde", None, QtGui.QApplication.UnicodeUTF8))
        self.lbImg.setText(_fromUtf8(""))
        self.lbImg.setScaledContents(True)
        self.lbImg.setObjectName(_fromUtf8("lbImg"))
        self.bttAnterior = QtGui.QPushButton(frmMuestraImg)
        self.bttAnterior.setGeometry(QtCore.QRect(630, 450, 131, 23))
        self.bttAnterior.setToolTip(QtGui.QApplication.translate("frmMuestraImg", "Anterior imagen seleccionada", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAnterior.setText(QtGui.QApplication.translate("frmMuestraImg", "Anterior imagen", None, QtGui.QApplication.UnicodeUTF8))
        self.bttAnterior.setObjectName(_fromUtf8("bttAnterior"))
        self.bttSiguiente = QtGui.QPushButton(frmMuestraImg)
        self.bttSiguiente.setGeometry(QtCore.QRect(770, 450, 121, 23))
        self.bttSiguiente.setToolTip(QtGui.QApplication.translate("frmMuestraImg", "Siguiente imagem seleccionada", None, QtGui.QApplication.UnicodeUTF8))
        self.bttSiguiente.setText(QtGui.QApplication.translate("frmMuestraImg", "Siguiente imagen", None, QtGui.QApplication.UnicodeUTF8))
        self.bttSiguiente.setObjectName(_fromUtf8("bttSiguiente"))
        self.tblDatos = QtGui.QTableWidget(frmMuestraImg)
        self.tblDatos.setGeometry(QtCore.QRect(630, 40, 261, 401))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblDatos.sizePolicy().hasHeightForWidth())
        self.tblDatos.setSizePolicy(sizePolicy)
        self.tblDatos.setToolTip(QtGui.QApplication.translate("frmMuestraImg", "Datos del punto", None, QtGui.QApplication.UnicodeUTF8))
        self.tblDatos.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tblDatos.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblDatos.setAlternatingRowColors(True)
        self.tblDatos.setTextElideMode(QtCore.Qt.ElideNone)
        self.tblDatos.setRowCount(1)
        self.tblDatos.setColumnCount(1)
        self.tblDatos.setObjectName(_fromUtf8("tblDatos"))
        self.tblDatos.horizontalHeader().setCascadingSectionResizes(True)
        self.tblDatos.horizontalHeader().setStretchLastSection(True)
        self.lbMensaje = QtGui.QLabel(frmMuestraImg)
        self.lbMensaje.setGeometry(QtCore.QRect(10, 10, 831, 16))
        self.lbMensaje.setText(QtGui.QApplication.translate("frmMuestraImg", "Imagen del linde", None, QtGui.QApplication.UnicodeUTF8))
        self.lbMensaje.setObjectName(_fromUtf8("lbMensaje"))
        self.label_3 = QtGui.QLabel(frmMuestraImg)
        self.label_3.setGeometry(QtCore.QRect(630, 20, 101, 16))
        self.label_3.setText(QtGui.QApplication.translate("frmMuestraImg", "Datos del punto:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lbEstado = QtGui.QLabel(frmMuestraImg)
        self.lbEstado.setGeometry(QtCore.QRect(10, 450, 611, 16))
        self.lbEstado.setText(_fromUtf8(""))
        self.lbEstado.setObjectName(_fromUtf8("lbEstado"))

        self.retranslateUi(frmMuestraImg)
        QtCore.QMetaObject.connectSlotsByName(frmMuestraImg)

    def retranslateUi(self, frmMuestraImg):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmMuestraImg = QtGui.QDialog()
    ui = Ui_frmMuestraImg()
    ui.setupUi(frmMuestraImg)
    frmMuestraImg.show()
    sys.exit(app.exec_())

