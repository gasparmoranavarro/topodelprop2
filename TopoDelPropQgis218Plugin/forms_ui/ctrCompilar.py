import os
from PyQt4 import QtCore, QtGui
import sys
from frmCompilar import Ui_frmCompilar

class ctrCompilar(QtGui.QDialog):
    #constructor
    def __init__(self):
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self)

        #Inicializa el formulario
        self.ui=Ui_frmCompilar() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)

        #Conecta los botones con m??todos de esta clase
        self.connect(self.ui.bttArchEntrada, QtCore.SIGNAL("clicked()"),self.archEntrada)
        self.connect(self.ui.bttArchSalida, QtCore.SIGNAL("clicked()"),self.archSalida)
        self.connect(self.ui.bttTerminar,QtCore.SIGNAL('clicked()'),self.terminar)
        self.connect(self.ui.bttGenerar, QtCore.SIGNAL('clicked()'),self.generar)
        self.connect(self.ui.bttMismo, QtCore.SIGNAL('clicked()'),self.mismo)
        self.connect(self.ui.bttRutaPyuic4, QtCore.SIGNAL('clicked()'),self.rutaPyuic4)


        self.show()#muestra el formulario

    def archEntrada(self):
        nombreArchivoEntrada= QtGui.QFileDialog.getOpenFileName(self, "Seleccionar archivo entrada")
        self.ui.txtArchEntrada.setText(nombreArchivoEntrada)
        s=os.path.split(str(nombreArchivoEntrada))
        archivo=s[1]
        archivo2=archivo.split(".")
        archivo3=archivo2[0]
        nomArchSalida="C:/Users/Gaspar/.qgis/python/plugins/delPropiedad/forms/" + archivo3 + ".py"
        self.ui.txtArchSalida.setText(nomArchSalida)

    def archSalida(self):
        nombreArchivoSalida= QtGui.QFileDialog.getOpenFileName(self, "Seleccionar archivo salida")
        self.ui.txtArchSalida.setText(nombreArchivoSalida)

    def terminar(self):
        self.close()

    def mismo(self):
        nombreArchivoEntrada= str(self.ui.txtArchEntrada.text())
        s=os.path.split(str(nombreArchivoEntrada))
        archivo=s[1]
        archivo2=archivo.split(".")
        archivo3=archivo2[0]
        nomArchSalida=s[0] + "/" + archivo3 + ".py"
        self.ui.txtArchSalida.setText(nomArchSalida)

    def rutaPyuic4(self):
        ruta= QtGui.QFileDialog.getOpenFileName(self, "Seleccionar el archivo pyuic4.bat")
        self.ui.txtRutaPyuic4.setText(ruta)

    def generar(self):
#        programa="C:/Python27/Lib/site-packages/PyQt4/pyuic4.bat"

        programa=str(self.ui.txtRutaPyuic4.text())
        archivoEnt=str(self.ui.txtArchEntrada.text())
        archivoSal=str(self.ui.txtArchSalida.text())

        orden =programa + " -o " + archivoSal + " -x " + archivoEnt
        os.system(orden)

def main():

    app = QtGui.QApplication(sys.argv)#requerido por todas las aplicaciones Qt antes de inicicializar el formulario
    ui = ctrCompilar()
    sys.exit(app.exec_())#requerido por todas las aplicaciones Qt despues de inicializar el formulario
if __name__ == '__main__':
    main()



"""
def main():
    #-o ui_nombre.py -x ui_nombre.ui
    programa="C:/Python27/Lib/site-packages/PyQt4/pyuic4.bat"
    archivoEnt="c:/temp/frmCompilar.ui"
    archivoSal="c:/temp/frmCompilar.py"
    orden =programa + " -o " + archivoSal + " -x " + archivoEnt
    os.system(orden)
"""

