from PyQt4 import QtCore, QtGui
"""
from forms.frmPPalUsuarios import Ui_frmPPalUsuarios #la ruta de improtacion
                #debe comenzar desde donde se encuentre el programa que ejecuta esta clase.
from forms.frmConectar import Ui_frmConectar
from forms.frmIntrodDatos import Ui_frmIntrodDatos
"""
import ctrAcercaDe
import ctrConectar
import ctrIntrodDatos
import ctrIntrodDatos_N
import ctrIntrodDatos_NUsuario
import ctrIntrodDatos_Buscar
import sys

from forms.frmPPalUsuarios import Ui_frmPPalUsuarios

class ctrPPalUsuarios(QtGui.QMainWindow):
    #constructor
    def __init__(self,oUtiles):
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QMainWindow.__init__(self)

        #Inicializa el formulario
        self.ui=Ui_frmPPalUsuarios() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.oUtiles=oUtiles

        #Conecta los botones con m??todos de esta clase
        self.connect(self.ui.opCrearUsuario, QtCore.SIGNAL("triggered()"),self.opCrearusuario)
        self.connect(self.ui.opBuscarEditar, QtCore.SIGNAL("triggered()"),self.opBuscarEditar)
        self.connect(self.ui.opDesactivarEditores,QtCore.SIGNAL("triggered()"),self.opDesactivarEditores)
        self.connect(self.ui.opActivarEditores, QtCore.SIGNAL("triggered()"),self.opActivarEditores)
        self.connect(self.ui.opAcercaDe, QtCore.SIGNAL("triggered()"),self.opAcercaDe)
        self.oUtiles=oUtiles
        self.oUtiles.iface=self

    def opCrearusuario(self):
        dlg=ctrIntrodDatos_NUsuario.ctrIntrodDatos_NUsuario(oUtiles=self.oUtiles,usuarioYaCreado=False)
        dlg.exec_()

    def opBuscarEditar(self):
        dlgBus=ctrIntrodDatos_Buscar.ctrIntrodDatos_Buscar(self.oUtiles,tablaBuscar="comun.usuarios",nomCampoClave="id")
        idUsuario=dlgBus.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
        if idUsuario==-1:
            #QtGui.QMessageBox.information(self,"Mensaje" , "No se ha elegido ningun trabajo",1)
            return
        dicCondiciones={}
        dicCondiciones["id"]=idUsuario
        dlg=ctrIntrodDatos_NUsuario.ctrIntrodDatos_NUsuario(self.oUtiles,usuarioYaCreado=True)
        dlg.setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones=dicCondiciones)
        dlg.exec_()

    def opDesactivarEditores(self):
        resp=self.oUtiles.oConsultasPg.updateDatos(nombreTabla="comun.usuarios",listaCampos=["activado"], listaValores=["False"],nombreCampoBytea=None, esMulti=False, nombreCampoGeom=None, epsg=None, condicionWhere="tipo_usuario=%s", listaValoresCondWhere=["editor"])
        if isinstance(resp,Exception):
            QtGui.QMessageBox.information(self,"Error" , resp.message,1)
        elif resp==True:
            QtGui.QMessageBox.information(self,"Mensaje" , "Todos los editores fueron desactivados.",1)
        else:
            QtGui.QMessageBox.information(self,"Error" , self.toUtf8("Verifique que la operación se ha realizado correctamente."),1)            
    def opActivarEditores(self):
        resp=self.oUtiles.oConsultasPg.updateDatos(nombreTabla="comun.usuarios",listaCampos=["activado"], listaValores=["True"],nombreCampoBytea=None, esMulti=False, nombreCampoGeom=None, epsg=None, condicionWhere="tipo_usuario=%s", listaValoresCondWhere=["editor"])
        if isinstance(resp,Exception):
            QtGui.QMessageBox.information(self,"Error" , resp.message,1)
        elif resp==True:
            QtGui.QMessageBox.information(self,"Mensaje" , "Todos los editores fueron activados.",1)
        else:
            QtGui.QMessageBox.information(self,"Error" , self.toUtf8("Verifique que la operación se ha realizado correctamente."),1)            
    
    def opAcercaDe(self):
        dlg=ctrAcercaDe.ctrAcercaDe()
        dlg.exec_()

    def toUtf8(self,mens):
        return unicode(mens,"utf-8")
