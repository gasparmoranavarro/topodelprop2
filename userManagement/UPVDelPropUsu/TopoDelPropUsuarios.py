#!/usr/lib/python27
#/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Gaspar
#
# Created:     14/09/2012
# Copyright:   (c) Gaspar 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
from ctr.ctrPPalUsuarios  import ctrPPalUsuarios
import sys
from utilidadesUsu.utils import InicializaUtiles


def main():

    ut=InicializaUtiles()
    try:
        ut.inicializa()
        oUtiles=ut.getUtiles()
    except Exception,e:
        QtGui.QMessageBox.information(None,"Mensaje" , e.message,1)
        sys.exit(0)
    app = QtGui.QApplication(sys.argv)#requerido por todas las aplicaciones Qt antes de inicicializar el formulario
    dlg = ctrPPalUsuarios(oUtiles)
    dlg.show()
    sys.exit(app.exec_())#requerido por todas las aplicaciones Qt despues de inicializar el formulario


if __name__ == '__main__':
    main()
