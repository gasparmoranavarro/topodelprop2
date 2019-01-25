# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/_Gaspar12/_Tesis/UPVUsuarios/UPVDelPropUsu/forms_ui/frmPPalUsuarios.ui'
#
# Created: Fri Nov 09 13:05:39 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmPPalUsuarios(object):
    def setupUi(self, frmPPalUsuarios):
        frmPPalUsuarios.setObjectName(_fromUtf8("frmPPalUsuarios"))
        frmPPalUsuarios.resize(317, 169)
        frmPPalUsuarios.setWindowTitle(QtGui.QApplication.translate("frmPPalUsuarios", "TopoDelProp-Usuarios", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(frmPPalUsuarios)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        frmPPalUsuarios.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(frmPPalUsuarios)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 317, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuCrear_usuario = QtGui.QMenu(self.menubar)
        self.menuCrear_usuario.setTitle(QtGui.QApplication.translate("frmPPalUsuarios", "Gestión de usuarios", None, QtGui.QApplication.UnicodeUTF8))
        self.menuCrear_usuario.setObjectName(_fromUtf8("menuCrear_usuario"))
        self.menuAcerca_de = QtGui.QMenu(self.menubar)
        self.menuAcerca_de.setTitle(QtGui.QApplication.translate("frmPPalUsuarios", "Acerca de", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAcerca_de.setObjectName(_fromUtf8("menuAcerca_de"))
        frmPPalUsuarios.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(frmPPalUsuarios)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frmPPalUsuarios.setStatusBar(self.statusbar)
        self.opCrearUsuario = QtGui.QAction(frmPPalUsuarios)
        self.opCrearUsuario.setText(QtGui.QApplication.translate("frmPPalUsuarios", "Crear usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.opCrearUsuario.setObjectName(_fromUtf8("opCrearUsuario"))
        self.opBuscarEditar = QtGui.QAction(frmPPalUsuarios)
        self.opBuscarEditar.setText(QtGui.QApplication.translate("frmPPalUsuarios", "Buscar-Editar usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.opBuscarEditar.setObjectName(_fromUtf8("opBuscarEditar"))
        self.opDesactivarEditores = QtGui.QAction(frmPPalUsuarios)
        self.opDesactivarEditores.setText(QtGui.QApplication.translate("frmPPalUsuarios", "Desactivar todos los editores", None, QtGui.QApplication.UnicodeUTF8))
        self.opDesactivarEditores.setObjectName(_fromUtf8("opDesactivarEditores"))
        self.opActivarEditores = QtGui.QAction(frmPPalUsuarios)
        self.opActivarEditores.setText(QtGui.QApplication.translate("frmPPalUsuarios", "Activar todos los editores", None, QtGui.QApplication.UnicodeUTF8))
        self.opActivarEditores.setObjectName(_fromUtf8("opActivarEditores"))
        self.opAcercaDe = QtGui.QAction(frmPPalUsuarios)
        self.opAcercaDe.setText(QtGui.QApplication.translate("frmPPalUsuarios", "Acerca de ...", None, QtGui.QApplication.UnicodeUTF8))
        self.opAcercaDe.setObjectName(_fromUtf8("opAcercaDe"))
        self.menuCrear_usuario.addAction(self.opCrearUsuario)
        self.menuCrear_usuario.addAction(self.opBuscarEditar)
        self.menuCrear_usuario.addAction(self.opDesactivarEditores)
        self.menuCrear_usuario.addAction(self.opActivarEditores)
        self.menuAcerca_de.addAction(self.opAcercaDe)
        self.menubar.addAction(self.menuCrear_usuario.menuAction())
        self.menubar.addAction(self.menuAcerca_de.menuAction())

        self.retranslateUi(frmPPalUsuarios)
        QtCore.QMetaObject.connectSlotsByName(frmPPalUsuarios)

    def retranslateUi(self, frmPPalUsuarios):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frmPPalUsuarios = QtGui.QMainWindow()
    ui = Ui_frmPPalUsuarios()
    ui.setupUi(frmPPalUsuarios)
    frmPPalUsuarios.show()
    sys.exit(app.exec_())

