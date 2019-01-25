# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TopoDelProp
                                 A QGIS plugin
 TopoDelProp
                              -------------------
        begin                : 2011-12-19
        copyright            : (C) 2011 by J. Gaspar Mora Navarro
        email                : topodelprop@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
"""
    Formulario principal de la aplicación con la que se gestionan los trabajos.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Esta clase es la que inicializa el diálogo principal y conecta los eventos de los
        controles con funciones de esta misma clase.
        Las opciones del menu desplegable, lo unico que hacen es colocar opciones sobre´
        el control TreeView.
        Cuado se hace doble click sobre el control TreeView, el evento doubleClick,
        examina el nombre de la opcion elegida y muestra el cuadro de dialogo correspondiente.
"""
import os
import datetime

from PyQt4 import QtCore, QtGui
from TopoDelProp.forms.frmPpal import Ui_frmPpal
#from ctrIntrodDatos import ctrIntrodDatos
from ctrIntrodDatos_Ntrab import ctrIntrodDatos_Ntrab
from ctrIntrodDatos_NGeom import ctrIntrodDatos_NGeom
from ctrIntrodDatos_NFinca import ctrIntrodDatos_NFinca
from ctrIntrodDatos_NLinde import ctrIntrodDatos_NLinde
from ctrIntrodDatos_Buscar import ctrIntrodDatos_Buscar
from ctrIntrodDatos_N import ctrIntrodDatos_N
from ctrSelEsquema import ctrSelEsquema
from ctrAcercaDe import ctrAcercaDe
from ctrSelec import ctrSelec
import qgis.core


#from ctrIntrodDatos import ctrIntrodDatos

#import qgis.core
#import qgis.gui
import pyUPVBib.pyGenGas
import pyUPVBib.pyPgGas


import sys

'''
if sys.platform=='linux2':
    sys.path.append('/opt/liclipse/plugins/org.python.pydev_5.1.2.201606231040/pysrc')
    #sys.path.append('/home/joamona/.eclipse/org.eclipse.platform_3.8_155965261/plugins/org.python.pydev_4.4.0.201510052309/pysrc')
    ##pydevd.settrace()
else:
    sys.path.append("C:/LiClipse/plugins/org.python.pydev_3.9.2.201502042042/pysrc" )
import pydevd #lo marca como error, pero en tiempo de ejecución funciona
'''

class ctrPpal(QtGui.QMainWindow):
    #constructor

    ctrIntrodDatos_Ntrab=None#crear nuevos trabajos
    ctrIntrodDatos_Buscar=None#buscar
    ctrIntrodDatos_Plano=None#ultimo plano añadido
    ctrIntrodDatos_Ncli=None#añadir clientes al trabajo
    ctrIntrodDatos_DocEst=None#añadir documentos estudiados
    ctrIntrodDatos_DatFinca=None#añadir documentos estudiados
    ctrIntrodDatos_NPropiet=None#añadir propietarios
    ctrIntrodDatos_MemoTrabajo=None
    ctrIntrodDatos_desplazamiento=None#desplazamientos de la cartografia catastral ed_desp_carto_cat
    lindesAnyadidosTreeView=False#se pueden volver a añadir al treeview
    parcelasAnyadidasTreeView=False#se pueden volver a añadir al treeview
    imagenesAnyadidasTreeWiew=False#se pueden volver a añadir al treeview
    servidumbresAnyadidosTreeView=False#se pueden volver a añadir al treeview
    elementosInterioresAnyadidosTreeView=False
    dicLindes={}#diccionario 'Linde:i':formulario
    dicActasDeslinde={}#las claves son "Linde:1", "Linde:2",...
    dicElementoInterior={}
    dicImgEltosInteriores={}
    dicParcelasAfectadas={}
    dicServidumbres={}
    seleccionLindes=None #elementos seleccionados de las capas dxf_...
    seleccionImagenes=None 
    seleccionServidumbres = None
    seleccionElementosInteriores = None
    seleccionParcelasAfectadas = None
    
    def __init__(self, oUtiles):
        """
        Constructor
        Inicializa la variable self.oUtiles
        @type oUtiles:  UilsPropiedad.Utils.Utiles
        @param oUtiles: Clase con las utilidades necesarias para esta aplicacion
        """
        QtGui.QMainWindow.__init__(self,oUtiles.iface.mainWindow())

        #Inicializa el formulario
        self.ui=Ui_frmPpal() #inicializa la variable local ui al diálogo
        self.ui.setupUi(self)
        self.oUtiles=oUtiles
        
        self.datamodel = QtGui.QStandardItemModel(self)
        self.treeview = self.ui.treeView
        self.treeview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeview.setModel(self.datamodel)
        self.ui.treeView.doubleClicked.connect(self.dobleClicadoTreeView)
        self.ui.treeView.pressed.connect(self.simpleClicadoTreeView)
        self.ui.treeView.setItemsExpandable(False)
        self.ui.treeView.setUpdatesEnabled(True)

        #cuando se hace doble click sobre el treeview, el metodo dobleClicadotreeView
        #lanza el cuadro de dialogo apropiado


        #Conecta las opciones del menu con métodos de esta clase
        #rellena el treeview con las opciones para la opcion del menu elegida     
        #rellenaTreeview con las opciones del nuevo trabajo
        self.connect(self.ui.opNuevoTrabajo, QtCore.SIGNAL("triggered()"), self.opNuevoTrabajo)
        #rellenaTreeview con las opciones de editar trabajo
        self.connect(self.ui.opAgreDivVert, QtCore.SIGNAL("triggered()"), self.opAgreDivVert)
        self.connect(self.ui.opDividirFinca, QtCore.SIGNAL("triggered()"), self.opDividirFinca)
        self.connect(self.ui.opAgregarFinca, QtCore.SIGNAL("triggered()"), self.opAgregarFinca)
        self.connect(self.ui.opSegregarFinca, QtCore.SIGNAL("triggered()"), self.opSegregarFinca)
        
        self.connect(self.ui.opCargarCapasErrores, QtCore.SIGNAL("triggered()"), self.opCargarCapasErrores)
        self.connect(self.ui.opComprobarErroresFinca, QtCore.SIGNAL("triggered()"), self.opComprobarErroresFinca)
        self.connect(self.ui.opBorrarErroresFinca, QtCore.SIGNAL("triggered()"), self.opBorrarErroresFinca)
        self.connect(self.ui.opBorrarErroresSRC, QtCore.SIGNAL("triggered()"), self.opBorrarErroresSRC)
        
        self.connect(self.ui.opValidarTrabajo, QtCore.SIGNAL("triggered()"), self.opValidarTrabajo)
        self.connect(self.ui.opBorrarTrabajo, QtCore.SIGNAL("triggered()"), self.opBorrarTrabajo)

        self.connect(self.ui.opRecargarTrabajo, QtCore.SIGNAL("triggered()"), self.opRecargarTrabajo)
        self.connect(self.ui.opBuscarPorTrabajo, QtCore.SIGNAL("triggered()"), self.opBuscarPorTrabajo)
        self.connect(self.ui.opBuscarPorFinca, QtCore.SIGNAL("triggered()"), self.opBuscarPorFinca)
        self.connect(self.ui.opBuscarPorRefCatRus, QtCore.SIGNAL("triggered()"), self.opBuscarPorRefCatRus)
        self.connect(self.ui.opBuscarPorRefCatUrb, QtCore.SIGNAL("triggered()"), self.opBuscarPorRefCatUrb)
        self.connect(self.ui.opBuscarPorPropietarios, QtCore.SIGNAL("triggered()"), self.opBuscarPorPropietarios)
        self.connect(self.ui.opBuscarPorClientes, QtCore.SIGNAL("triggered()"), self.opBuscarPorClientes)
        self.connect(self.ui.opBuscarPorColindantes, QtCore.SIGNAL("triggered()"), self.opBuscarPorColindantes)
        self.connect(self.ui.opAcercaDe, QtCore.SIGNAL("triggered()"),self.opAcercaDe)

        self.connect(self.ui.opVerHistorico, QtCore.SIGNAL("triggered()"), self.opVerHistorico)        
        
        self.activaOpcionesUsuario(self.oUtiles.tipo_usuario)
        self.opcionMenuElegida=None#opcion del menu elegida: nuevo trabajo, editar trabajo ...
        self.ctrIntrodDatos_Ntrab=None
        
        #cuadros de dialogo
        self.limpiaFormularios()#inicializa las variables de la clase
        self.__elimina_datos_trabajo_oUtiles()
        
    def limpiaFormularios(self,borrarDlgTrabajo=False):
        """
        Crea las variables de la clase y las inicializa. Los diccionarios de formularios se van completando
        con forme se van creando dichos formularios
        
        Todas las claves de diccionarios son str. Hay que convertir
        los QString de los textos del formulario a str para que las
        claves coincidan.
        """
        
        if borrarDlgTrabajo==True:
            self.ctrIntrodDatos_Ntrab=None#crear nuevos trabajos
        self.ctrIntrodDatos_Buscar=None#buscar
        self.ctrIntrodDatos_Plano=None#ultimo plano añadido
        self.ctrIntrodDatos_Ncli=None#añadir clientes al trabajo
        self.ctrIntrodDatos_DocEst=None#añadir documentos estudiados
        self.ctrIntrodDatos_DatFinca=None#añadir documentos estudiados
        self.ctrIntrodDatos_NPropiet=None#añadir propietarios
        self.ctrIntrodDatos_MemoTrabajo=None
        self.ctrIntrodDatos_desplazamiento=None
        self.lindesAnyadidosTreeView=False#se pueden volver a añadir al treeview
        self.parcelasAnyadidasTreeView=False#se pueden volver a añadir al treeview
        self.imagenesAnyadidasTreeWiew=False#se pueden volver a añadir al treeview
        self.servidumbresAnyadidosTreeView=False#se pueden volver a añadir al treeview
        self.elementosInterioresAnyadidosTreeView=False
        self.dicLindes={}#diccionario 'Linde:i':formulario
        self.dicActasDeslinde={}#las claves son "Linde:1", "Linde:2",...
        self.dicElementoInterior={}
        self.dicImgEltosInteriores={}
        self.dicParcelasAfectadas={}
        self.dicServidumbres={}
        self.seleccionLindes=None
        self.seleccionImagenes=None 
        self.seleccionServidumbres = None
        self.seleccionElementosInteriores = None
        self.seleccionParcelasAfectadas = None
        
        #self.opcionMenuElegida=None#puede ser: "nuevo","buscar-editar","validar","ver-hist"
        
        self.ui.txtInfo.setText("U:" + str(self.oUtiles.usuario))
        #self.__elimina_datos_trabajo_oUtiles()
    def activaOpcionesUsuario(self,tipo_usuario):
        """
        Muestra u oculta opciones del menú desplegable en función del tipo de usuario
        que está usando la aplicación.
        """
        if tipo_usuario=="consultor_autorizado":
            self.ui.opNuevoTrabajo.setVisible(False)
            self.ui.opAgreDivVert.setVisible(False)
            self.ui.opDividirFinca.setVisible(False)
            self.ui.opAgregarFinca.setVisible(False)
            self.ui.opSegregarFinca.setVisible(False)
            self.ui.opDividirFinca.setVisible(False)
            self.ui.opValidarTrabajo.setVisible(False)
            self.ui.opBorrarTrabajo.setVisible(False)
            
            self.ui.opCargarCapasErrores.setVisible(False)
            self.ui.opComprobarErroresFinca.setVisible(False)
            self.ui.opBorrarErroresFinca.setVisible(False)
            self.ui.opBorrarErroresSRC.setVisible(False)
            
            self.ui.opRecargarTrabajo.setVisible(True)
            self.ui.opBuscarPorTrabajo.setVisible(True)
            self.ui.opBuscarPorFinca.setVisible(True)
            self.ui.opBuscarPorRefCatRus.setVisible(True)
            self.ui.opBuscarPorRefCatUrb.setVisible(True)
            #se ocultan para no mostrar datos personales
            self.ui.opBuscarPorPropietarios.setVisible(False)
            self.ui.opBuscarPorClientes.setVisible(False)
            self.ui.opBuscarPorColindantes.setVisible(False)
            
            self.ui.opVerHistorico.setVisible(True)
            
        elif tipo_usuario=="editor":
            self.ui.opNuevoTrabajo.setVisible(True)
            self.ui.opAgreDivVert.setVisible(True)
            self.ui.opDividirFinca.setVisible(True)
            self.ui.opAgregarFinca.setVisible(True)
            self.ui.opSegregarFinca.setVisible(True)
            self.ui.opDividirFinca.setVisible(True)
            self.ui.opValidarTrabajo.setVisible(False)
            self.ui.opBorrarTrabajo.setVisible(True)
            
            self.ui.opCargarCapasErrores.setVisible(False)
            self.ui.opComprobarErroresFinca.setVisible(True)
            self.ui.opBorrarErroresFinca.setVisible(False)
            self.ui.opBorrarErroresSRC.setVisible(False)
  
            self.ui.opRecargarTrabajo.setVisible(True)
            self.ui.opBuscarPorTrabajo.setVisible(True)
            self.ui.opBuscarPorFinca.setVisible(True)
            self.ui.opBuscarPorRefCatRus.setVisible(True)
            self.ui.opBuscarPorRefCatUrb.setVisible(True)
            #se ocultan para no mostrar datos personales
            self.ui.opBuscarPorPropietarios.setVisible(False)
            self.ui.opBuscarPorClientes.setVisible(False)
            self.ui.opBuscarPorColindantes.setVisible(False)
            self.ui.opVerHistorico.setVisible(True)
            
        elif tipo_usuario=="admin_propiedad":  
            self.ui.opNuevoTrabajo.setVisible(True)
            self.ui.opAgreDivVert.setVisible(True)
            self.ui.opDividirFinca.setVisible(True)
            self.ui.opAgregarFinca.setVisible(True)
            self.ui.opSegregarFinca.setVisible(True)
            self.ui.opDividirFinca.setVisible(True)
            self.ui.opValidarTrabajo.setVisible(True)
            self.ui.opBorrarTrabajo.setVisible(True)

            self.ui.opCargarCapasErrores.setVisible(True)
            self.ui.opComprobarErroresFinca.setVisible(True)
            self.ui.opBorrarErroresFinca.setVisible(True)
            self.ui.opBorrarErroresSRC.setVisible(True)
                        
            self.ui.opRecargarTrabajo.setVisible(True)
            self.ui.opBuscarPorTrabajo.setVisible(True)
            self.ui.opBuscarPorFinca.setVisible(True)
            self.ui.opBuscarPorRefCatRus.setVisible(True)
            self.ui.opBuscarPorRefCatUrb.setVisible(True)
            #se ocultan para no mostrar datos personales
            self.ui.opBuscarPorPropietarios.setVisible(True)
            self.ui.opBuscarPorClientes.setVisible(True)
            self.ui.opBuscarPorColindantes.setVisible(True)
            self.ui.opVerHistorico.setVisible(True)
    
    def opCargarCapasErrores(self):
        """
        Carga las capas srcXXXXX.overlaps_fincas y srcXXXXX.gaps_fincas
        """
        if self.compExisteTrabActual():
            if self.oUtiles.tipo_trabajo.lower()=="definitivo":
                self.oUtiles.oVarios.cargaCapasErrorDef(self.oUtiles,borrarSiExiste=True)
            else:
                QtGui.QMessageBox.information(self,"Aviso" ,self.toUtf8("El actual tipo de trabajo es de edicion. Al cargar las capas de edicion ya se cargan las capas de errores."),1)
    def opComprobarErroresFinca(self):
        """
        Elimina los errores del trabajo actual, sea en edicion o definitivo, y los vuelve
        a dibujar. Esto hay que hacerlo antes de validar un trabajo y ver los posibles errores,
        Hay que hacerlo ya que es posible que el usuario los haya borrado a mano.
        """
        if not(self.compExisteTrabActual()):
            return
        src=str(self.oUtiles.src_trabajo)
        id_trabajo=int(self.oUtiles.id_trabajo)

        if self.oUtiles.tipo_trabajo.lower()=="edicion":
            try:
                #borra los errores previos y dibuja los nuevos, si los habia
                self.oUtiles.oConectaPg.cursor.callproc("script.comp_over_finca_ed",[src,id_trabajo])
                self.oUtiles.oConectaPg.conn.commit()
                result = self.oUtiles.oConectaPg.cursor.fetchone()
                solape = result[0]
                if solape:
                    QtGui.QMessageBox.information(self,"Mensaje" , "La finca tiene un solape",1)
                self.oUtiles.oConectaPg.cursor.callproc("script.comp_gaps_finca_ed",[src,id_trabajo])
                self.oUtiles.oConectaPg.conn.commit()
                result = self.oUtiles.oConectaPg.cursor.fetchone()
                gaps = result[0]
                if gaps:
                    QtGui.QMessageBox.information(self,"Mensaje" , "La finca puede tener errores gaps",1)
                if not(solape) and not(gaps):
                    QtGui.QMessageBox.information(self,"Mensaje" , "La finca no tiene ni solapes ni gaps",1)                    
            except Exception, e:
                QtGui.QMessageBox.information(self,"Error" , e.message,1)
        elif self.oUtiles.tipo_trabajo.lower()=="definitivo":
            try:
                #borra los errores previos y dibuja los nuevos, si los habia
                #self.oUtiles.oConectaPg.cursor.callproc("script.comp_over_finca_def",[src,id_trabajo])#esto no va. Si va, faltaba el commit()
                self.oUtiles.oConectaPg.cursor.execute("select script.comp_over_finca_def(%s,%s)",[src,id_trabajo])
                self.oUtiles.oConectaPg.conn.commit()
                result = self.oUtiles.oConectaPg.cursor.fetchone()
                resp = result[0]
                if resp==True:
                    QtGui.QMessageBox.information(self,"Mensaje" , "La finca tiene un solape",1)
                #self.oUtiles.oConectaPg.cursor.callproc("script.comp_gaps_finca_def",[src,id_trabajo])
                self.oUtiles.oConectaPg.cursor.execute("select script.comp_gaps_finca_def(%s,%s)",[src,id_trabajo])
                self.oUtiles.oConectaPg.conn.commit()
                result = self.oUtiles.oConectaPg.cursor.fetchone()
                resp = result[0]
                if resp==True:
                    QtGui.QMessageBox.information(self,"Mensaje" , "La finca puede tener errores gaps",1)
                if resp==False:
                    QtGui.QMessageBox.information(self,"Mensaje" , "La finca puede no tiene ni solapes ni gaps",1)                    
            except Exception, e:
                QtGui.QMessageBox.information(self,"Error" , e.message,1)
        else:
            QtGui.QMessageBox.information(self,"Error" , self.toUtf8("Opción no programada para el tipo de trabajo ") + self.toUtf8(self.oUtiles.tipo_trabajo),1)

    def opBorrarErroresFinca(self):
        """
        Borra los errores gaps y overlaps del trabajo actual, sea de edición o definitivo
        """
        if not(self.compExisteTrabActual()):
            return
        src=str(self.oUtiles.src_trabajo)
        id_trabajo=int(self.oUtiles.id_trabajo)
        try:
            if self.oUtiles.tipo_trabajo.lower()=="edicion":
                self.oUtiles.oConectaPg.cursor.callproc("script.borra_gaps_finca_ed",[src,id_trabajo])
                self.oUtiles.oConectaPg.conn.commit()
                self.oUtiles.oConectaPg.cursor.callproc("script.borra_overlaps_finca_ed",[src,id_trabajo])
                self.oUtiles.oConectaPg.conn.commit()
            elif self.oUtiles.tipo_trabajo.lower()=="definitivo":
                self.oUtiles.oConectaPg.cursor.callproc("script.borra_gaps_finca_def",[src,id_trabajo])
                self.oUtiles.oConectaPg.conn.commit()
                self.oUtiles.oConectaPg.cursor.callproc("script.borra_overlaps_finca_def",[src,id_trabajo])
                self.oUtiles.oConectaPg.conn.commit()
            else: 
                QtGui.QMessageBox.information(self,"Error" , self.toUtf8("Opción no programada para el tipo de trabajo ") + self.toUtf8(self.oUtiles.tipo_trabajo),1)
                return
            QtGui.QMessageBox.information(self,"Mensaje" , "Hecho",1)
        except Exception, e:
            QtGui.QMessageBox.information(self,"Error" , e.message,1)
    def opBorrarErroresSRC(self):
        """
        Borra todos los errores del huso actual para el tipo de trabajo actual
        """
        if not(self.compExisteTrabActual()):
            return
        if self.oUtiles.tipo_trabajo.lower()=="edicion":
            self.oUtiles.oConectaPg.cursor.callproc("script.borra_gaps_finca_ed",[str(self.oUtiles.src_trabajo)])
            self.oUtiles.oConectaPg.conn.commit()
            self.oUtiles.oConectaPg.cursor.callproc("script.borra_overlaps_finca_ed",[str(self.oUtiles.src_trabajo)])
            self.oUtiles.oConectaPg.conn.commit()
        elif self.oUtiles.tipo_trabajo.lower()=="definitivo":
            self.oUtiles.oConectaPg.cursor.callproc("script.borra_gaps_finca_def",[str(self.oUtiles.src_trabajo)])
            self.oUtiles.oConectaPg.conn.commit()
            self.oUtiles.oConectaPg.cursor.callproc("script.borra_overlaps_finca_def",[str(self.oUtiles.src_trabajo)])
            self.oUtiles.oConectaPg.conn.commit()
        else: 
            QtGui.QMessageBox.information(self,"Error" , self.toUtf8("Opción no programada para el tipo de trabajo ") + self.toUtf8(self.oUtiles.tipo_trabajo),1)
            return
        QtGui.QMessageBox.information(self,"Mensaje" , "Hecho",1)


    def opNuevoTrabajo(self):
        """
        Pone en el TreeView las opciones para crear un nuevo trabajo
        """
#     
        if self.ctrIntrodDatos_Ntrab!=None:
            mens=unicode("Esta opción eliminará de la memoria los datos del trabajo actual.¿Está seguro?.","utf-8")
            reply = QtGui.QMessageBox.question(self, "Mensaje", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.limpiaFormularios(borrarDlgTrabajo=True)
                self.__elimina_datos_trabajo_oUtiles()
            else:
                return
        #self.oUtiles.prefijo_tipo_trabajo="Edicion"
        self.oUtiles.prefijo_tipo_trabajo="Edicion"#parece que esta mal, pero mira el metodo y veras que es raro, pero esta bien
        self.opcionMenuElegida="nuevo"
        self.rellenaTreeView("nuevo")
    
    def opRecargarTrabajo(self):
        """
        Elimina todos los formularios de la memoria y crea nuevos, cargando los datos
        de la base de datos. Siempre que se borre algún elemento y el formulario
        no se actualice, hay que recargar el trabajo. Esto hará que se muestre
        correctamente. 
        """
        self.oUtiles.iface=qgis.utils.iface
        self.cargaDatosTrabajo(nomTabla="da igual",buscarTrabajo=False)

    def opBuscarPorTrabajo(self):
        """
        Pemite buscar por datos del trabajo.
        """
        self.cargaDatosTrabajo("comun.trabajos")
    def opBuscarPorFinca(self):
        """
        Pemite buscar por datos de la finca.
        """
        self.cargaDatosTrabajo("fincas")
    def opBuscarPorRefCatRus(self):
        """
        Pemite buscar por datos cartastrales de rústica.
        """
        self.cargaDatosTrabajo("ref_cat_rus")
    def opBuscarPorRefCatUrb(self):
        """
        Pemite buscar por datos cartastrales de urbana.
        """
        self.cargaDatosTrabajo("ref_cat_urb")
    def opBuscarPorClientes(self):
        """
        Pemite buscar por datos de los clientes.
        """
        self.cargaDatosTrabajo("comun.clientes")
    def opBuscarPorPropietarios(self):
        """
        Pemite buscar por datos personales de los propietarios.
        """
        self.cargaDatosTrabajo("comun.propietarios")
    def opBuscarPorColindantes(self):
        """
        Pemite buscar por datos personales de colindantes.
        """
        self.cargaDatosTrabajo("colindantes")
    
    def cargaDatosTrabajo(self,nomTabla,buscarTrabajo=True):
        """
        Carga los datos de un id_trabajo, crea los cuadros de diálogo para poder
        consultarlos, o editarlos y crea las opciones necesarias en el treeview.
        
        Si se quieren añadir elementos gráficos a la BDA, primero hay que 
        seleccionarlos de la capa dxf_nomCapa. Hay que seleccionar primero los 
        elementos a añadir de todas las capas que se deseen, antes de seleccionar
        la opción del menú Buscar-editar->Opción deseada.
        
        En el caso de los datos espaciales, si hay selección en la capa dxf_nomCapa,
        no se carga nada de esa capa de la BDA, se permite que se añadan los objetos
        seleccionados a la BDA, como si fuese un trabajo nuevo. 
        
        Si no hay selección, en dxf_nomCapa o no existe la capa dxf_nomCapa,
        debe estar cargada la capa ed_nomCapa (trabajo en edición) o 
        nom_capa (trabajo definitivo) o hist_nomcapa(trabajo en el historico).

        @type nomTabla: string
        @param nomTabla: nombre de la tabla por la que se va a buscar el id_trabajo.
            No debe tener prefijos
        @type buscarTrabajo: booleano
        @param buscarTrabajo: Si es true muestra un cuadro de diálogo para buscar trabajos,
            según los valores de la tabla nomTabla. Si es False, lo que hace es recargar el trabajo
            actual.
        """
        self.opcionMenuElegida="buscar-editar"

        if buscarTrabajo==True:
            self.limpiaFormularios()
            self.__elimina_datos_trabajo_oUtiles()
            resp=self.buscarTrabajo(nomTabla)#carga todos los datos en oUtiles
            if resp==None:
                return
            #carga de las capas espaciales en qgis. Tiene en cuenta el municipio
            #del trabajo
            if self.oUtiles.tipo_trabajo.lower()=="edicion":
                try:
                    self.oUtiles.oVarios.cargaCapas(tipoTrabajo="edicion", oUtiles=self.oUtiles,borrarSiExiste=True)
                except Exception, e:
                    QtGui.QMessageBox.information(self,"Mensaje" , "No se pudieron cargar las capas en edicion: " + e.message,1)
            elif self.oUtiles.tipo_trabajo.lower()=="definitivo":
                try:
                    self.oUtiles.oVarios.cargaCapas(tipoTrabajo="definitivo", oUtiles=self.oUtiles,borrarSiExiste=True)
                except Exception, e:
                    QtGui.QMessageBox.information(self,"Mensaje" , "No se pudieron cargar las capas definitivas: " + e.message,1)
            else:
                QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("No puede cargar el tipo de trabajo: ") + self.oUtiles.tipo_trabajo ,1)
                return False  
        #si no están los datos del trabajo se sale. No recarga.
        elif self.oUtiles.src_trabajo!=None and self.oUtiles.id_trabajo!=None and self.oUtiles.usuario_creador_trabajo!=None and self.oUtiles.municipio!=None:
            pass
        else:
            QtGui.QMessageBox.information(self,"Mensaje" , "No hay trabajo actual",1)
            return
        #si no es el autor del trabajo, o el administrador, no te deja examinarlo
        
        if self.oUtiles.tipo_usuario!="admin_propiedad":
            if self.oUtiles.tipo_usuario!="consultor_autorizado":
                if self.oUtiles.usuario!=self.oUtiles.usuario_creador_trabajo :
                    #no es el autor
                    QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("No puede cargar un trabajo del que no sea ud. el autor"),1)
                    return
                elif self.oUtiles.prefijo_tipo_trabajo=="" or self.oUtiles.prefijo_tipo_trabajo=="hist_":
                    #es el autor
                    QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("No puede cargar un trabajo en las capas definitivas, ni del histórico. Únicamente puede ver la información gráfica y sus datos asociados. Póngase en contacto con el administrador."),1)
                    return False
            else:#es consultor autorizado
                if self.oUtiles.prefijo_tipo_trabajo=="ed_" :
                    QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("No puede cargar un trabajo en edición. Póngase en contacto con el administrador."),1)
                    return False
                
        self.limpiaFormularios(borrarDlgTrabajo=None)
        #si todo ha ido bien, self.ctrIntrodDatos_Ntrab ya está inicializado
        cad = "U:" + str(self.oUtiles.usuario) + " ID:" + str(self.oUtiles.id_trabajo) + " SRC:" + str(self.oUtiles.src_trabajo)
        self.ui.txtInfo.setText(cad)
        self.rellenaTreeView("consultar")
        index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto("Datos del trabajo",self.ui.treeView)
        self.cambiaAparienciaOpTreeView(index, self.ctrIntrodDatos_Ntrab)
        
        self.muestra_estado(mensaje="Cargando datos del trabajo. Espere ...", tiempo=0)
        self.ctrIntrodDatos_MemoTrabajo=self.cargaTablaNoEspacial("Memoria del trabajo", nomTabla="comun.memorias",listaSubDirDescargas=["memoria"],mostrarBttNuevo=False,dicCondiciones={})    
        self.ctrIntrodDatos_desplazamiento=self.cargaTablaNoEspacial("Desplazamiento carto catastral", nomTabla="comun.desp_carto_cat",listaSubDirDescargas=["memoria"],mostrarBttNuevo=False,dicCondiciones={})    
        self.actualizaTreeviewTablaNoEspacial("Clientes", nomTabla="comun.clientes", nombreHijo="Ver clientes")    
        self.actualizaTreeviewTablaNoEspacial("Planos", nomTabla="comun.planos", nombreHijo="Ver planos")    
        self.actualizaTreeviewTablaNoEspacial("Documentos estudiados", nomTabla="comun.documentos_estudiados",nombreHijo="Ver documentos estudiados")        
        self.actualizaTreeviewTablaNoEspacial("Propietarios", nomTabla="comun.propietarios",nombreHijo="Ver propietarios")        
        avisos=[]
        
        #CARGAR LA FINCA
        self.muestra_estado(mensaje="Cargando la finca ...", tiempo=5000)
        nomCapaQgis=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"fincas")
        #devuelve dxf_fincas, ed_fincas, fincas o hist_fincas
        
        #dic=dict({"id_trabajo":self.toUtf8(str(self.oUtiles.id_trabajo))})
        
        if nomCapaQgis!="dxf_fincas" and nomCapaQgis!=None:#en este caso no hay que hacer nada.
            """
            Si nomCapaQgis=="dxf_fincas" la finca esta seleccionada y cuando el usuario 
            haga doble click sobre "Datos de la finca" en el treeview, se podrá añadir 
            a la base de datos.
            Si if nomCapaQgis!="dxf_fincas", quiere decir que no hay que añadir nada
            al trabajo, hay que cargar los datos de la base de datos, crear los cuadros
            de diálogo y las opciones del treeview
            """
            nomTabla=self.oUtiles.get_nomTabla("fincas")
            
            self.ctrIntrodDatos_DatFinca=ctrIntrodDatos_NFinca(self.oUtiles,tabla=nomTabla,listaSubDirDescargas=["finca"],mostrarBttNuevo=False,dicValoresAdd=None, geomWkt=None,esMulti=None)
            
            resp=self.ctrIntrodDatos_DatFinca.setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones={})
            #carga el gid de la finca en los útiles. Necesario para añadir nuevos elementos interiores
            self.oUtiles.gid_finca=self.ctrIntrodDatos_DatFinca.dicValoresCompleto['gid']
            #pydevd.settrace()
                        
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Error" , resp.message,1)
            elif self.ctrIntrodDatos_DatFinca.get_featureId()==None or self.ctrIntrodDatos_DatFinca.get_featureId()=="":
                #si no hay registro no debe crear el cuadro de diálogo
                self.ctrIntrodDatos_DatFinca=None
            elif resp==True:
                capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgis)
                capa.setSelectedFeatures([self.ctrIntrodDatos_DatFinca.get_featureId()])
                index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto("Datos de la finca",self.ui.treeView)
                self.cambiaAparienciaOpTreeView(index, self.ctrIntrodDatos_DatFinca)
                self.ctrIntrodDatos_DatFinca.set_tipoFinca()
                resp=self.ctrIntrodDatos_DatFinca.set_dlgTipoFinca(cargarDeBda=True)
                self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, self.ctrIntrodDatos_DatFinca.get_tipoFinca())                        
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,"Error cargando el tipo de finca" , resp.message,1)
                elif resp==True:
                    index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto(self.ctrIntrodDatos_DatFinca.get_tipoFinca(),self.ui.treeView)
                    self.cambiaAparienciaOpTreeView(index, self.ctrIntrodDatos_DatFinca.get_dlgTipoFinca())
            else:
                mens=self.toUtf8("No ha seleccionado ninguna finca de la capa dxf_fincas y no hay ninguna de las siguientes capas: ed_fincas, fincas, hist_fincas.")
                avisos.append(mens)
                
        #CARGAR ELEMENTOS INTERIORES
        self.muestra_estado(mensaje="Cargando elementos interiores", tiempo=5000)
        nomCapaQgis=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"elem_interiores")
      
        if nomCapaQgis!="dxf_elem_interiores" and nomCapaQgis!=None:#en este caso no hay que hacer nada.
            nomTabla=self.oUtiles.get_nomTabla("elem_interiores")
            resp=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=nomTabla, listaCampos=["gid"], condicionWhere="id_trabajo=%s",listaValoresCondWhere=[self.oUtiles.id_trabajo])
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Error" , resp.message,1)
            elif len(resp)>0:
                qSet=[]#lista con todos los gid seleccionados
                for dic in resp:
                    qSet.append(dic.get("gid"))
                capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgis)
                capa.setSelectedFeatures(qSet)#los elementos deben estar seleccionads
                index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto("Elementos interiores",self.ui.treeView)
                self.add_elementos_interiores_treeview(index)#añade un enlace Elem interiores:i , por cada elemento interior
                nomTabla=self.oUtiles.get_nomTabla("elem_interiores")
                #listaDicElemInt=self.oUtiles.oUtilidadesQgs.get_attrSeleccionCapa(nombreCapa=nomCapaQgis,listaCampos=["gid"],geom=False)
                listaDicElemInt=resp
                dicCondicionesElem={}               
                for i,dicElemInt in enumerate(listaDicElemInt):
                    clave="Elemento interior" + ":" + str(i)
                    index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto(clave,self.ui.treeView)
                    self.add_datos_BDA_con_geometria(index,nomTablaSinEsquema="elem_interiores",nomCapa="elem_interiores",dicFormularios=self.dicElementoInterior,objetosSeleccionados=self.seleccionElementosInteriores,esMulti=False,cargarDatosDeBda=True)
                    self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,"Add img elto interior:" + str(i))
                    self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,"Ver img elto interior:" + str(i))        
                    #mostrar los nombres de las imagenes
                    dicCondicionesElem.update([["gid_elem_int",dicElemInt.get("gid")]])
                    nomTabla=self.oUtiles.get_nomTabla("img_elem_int")
               
                    
                    index2=self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,"Add img elto interior:" + str(i))
                    self.actualizaIMGTreeview(indexPadre=index2, nomTabla=nomTabla, dicCondiciones=dicCondicionesElem)
                    self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,"Ver img elto interior:" + str(i))
                    
        else:
            mens=self.toUtf8("No ha seleccionado ningún elemento interior de la capa dxf_elem_interiores y no hay ninguna de las siguientes capas: ed_elem_interiores, elem_interiores, hist_elem_interiores.")
            avisos.append(mens)
        
        ################
        #Parcelas afectadas
        self.muestra_estado(mensaje="Cargando parcelas afectadas", tiempo=5000)
        nomCapaQgis=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"parcelas_afectadas")

        if nomCapaQgis!="dxf_parcelas_afectadas" and nomCapaQgis!=None:#en este caso no hay que hacer nada.
            nomTabla=self.oUtiles.get_nomTabla("parcelas_afectadas")
            resp=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=nomTabla, listaCampos=["gid"], condicionWhere="id_trabajo=%s",listaValoresCondWhere=[self.oUtiles.id_trabajo])
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Error" , resp.message,1)
            elif len(resp)>0:
                qSet=[]#lista con todos los gid seleccionados
                for dic in resp:
                    qSet.append(dic.get("gid"))
                capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgis)
                capa.setSelectedFeatures(qSet)#los elementos deben estar seleccionads
                index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto("Parcelas afectadas",self.ui.treeView)
                self.add_parcelas_afectadas_treeview(index)#añade un enlace Elem interiores:i , por cada elemento interior
                for i in range(len(qSet)):
                    clave="Parcela afectada" + ":" + str(i)
                    index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto(clave,self.ui.treeView)
                    self.add_datos_BDA_con_geometria(index,nomTablaSinEsquema="parcelas_afectadas",nomCapa="parcelas_afectadas",dicFormularios=self.dicParcelasAfectadas,objetosSeleccionados=self.seleccionParcelasAfectadas,esMulti=True,cargarDatosDeBda=True)
        else:
            mens=self.toUtf8("No ha seleccionado ninguna parcela de la capa dxf_parcelas_afectadas y no hay ninguna de las siguientes capas: ed_parcelas_afectadas, parcelas_afectadas, hist_parcelas_afectadas.")
            avisos.append(mens)
        #########
        
        #CARGAR SERVIDUMBRES
        self.muestra_estado(mensaje="Cargando servidumbres", tiempo=5000)
        nomCapaQgis=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"servidumbres")

        if nomCapaQgis!="dxf_servidumbres" and nomCapaQgis!=None:#en este caso no hay que hacer nada.
            nomTabla=self.oUtiles.get_nomTabla("servidumbres")
            resp=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=nomTabla, listaCampos=["gid"], condicionWhere="id_trabajo=%s",listaValoresCondWhere=[self.oUtiles.id_trabajo])
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Error" , resp.message,1)
            elif len(resp)>0:
                qSet=[]#lista con todos los gid seleccionados
                for dic in resp:
                    qSet.append(dic.get("gid"))
                capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgis)
                capa.setSelectedFeatures(qSet)#los elementos deben estar seleccionads
                index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto("Servidumbres",self.ui.treeView)
                self.add_servidumbres_treeview(index)#añade un enlace Elem interiores:i , por cada elemento interior
                for i in range(len(qSet)):
                    clave="Servidumbre" + ":" + str(i)
                    index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto(clave,self.ui.treeView)
                    self.add_datos_BDA_con_geometria(index,nomTablaSinEsquema="servidumbres",nomCapa="servidumbres",dicFormularios=self.dicServidumbres,objetosSeleccionados=self.seleccionServidumbres,esMulti=False,cargarDatosDeBda=True)
        else:
            mens=self.toUtf8("No ha seleccionado ninguna servidumbre de la capa dxf_servidumbres y no hay ninguna de las siguientes capas: ed_servidumbres, servidumbres, hist_servidumbres.")
            avisos.append(mens)
            
        #CARGAR LINDES
        self.muestra_estado(mensaje="Cargando datos de los lindes.", tiempo=0)
        nomCapaQgis=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"lindes")
        dic=dict({"id_trabajo":self.toUtf8(str(self.oUtiles.id_trabajo))})
        if nomCapaQgis!="dxf_lindes" and nomCapaQgis!=None:#en este caso no hay que hacer nada.
            nomTabla=self.oUtiles.get_nomTabla("lindes")
            resp=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=nomTabla, listaCampos=["gid"], condicionWhere="id_trabajo=%s",listaValoresCondWhere=[self.oUtiles.id_trabajo])
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Error" , resp.message,1)
            elif len(resp)>0:
                qSet=[]#lista con todos los gid seleccionados
                for dic in resp:
                    qSet.append(dic.get("gid"))
                capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgis)
                capa.setSelectedFeatures(qSet)#los elementos deben estar seleccionads

                index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto("Datos de los lindes",self.ui.treeView)
                self.add_lindes_treeview(index)#añade un enlace Elem interiores:i , por cada elemento interior
                #dicLindes=self.oUtiles.oUtilidadesQgs.get_attrSeleccionCapa(nombreCapa=nomCapaQgis,listaCampos=["gid"],geom=False)
                dicLindes=resp
                for i,dicLinde in enumerate(dicLindes):
                    clave="Linde" + ":" + str(i)
                    dicCondiciones={}
                    dicCondiciones.update([["gid",dicLinde.get("gid")]])
                    #datos del linde
                    index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto(clave,self.ui.treeView)
                    nomTabla=self.oUtiles.get_nomTabla("lindes")
                    self.dicLindes[clave]=ctrIntrodDatos_NLinde(self.oUtiles,tabla=nomTabla,listaSubDirDescargas=[clave],mostrarBttNuevo=False,dicValoresAdd=None, geomWkt=None,esMulti=False)
                    resp=self.dicLindes.get(clave).setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones=dicCondiciones)
                    if isinstance(resp,Exception):
                        QtGui.QMessageBox.information(self,"Error en la carga del linde " + str(i) , resp.message,1)
                        continue#comieza el for de nuevo
                    elif resp==None:
                        QtGui.QMessageBox.information(self,"Error en la carga del linde " + str(i) , self.toUtf8("La consulta sobre los lindes no produjo ningún linde válido"),1)
                        continue
                    self.cambiaAparienciaOpTreeView(index, dlg=self.dicLindes.get(clave))
                    
                    #datos del tipo de linde
                    self.dicLindes.get(clave).set_tipoLinde()
                    tipoLinde=self.dicLindes.get(clave).get_tipoLinde() + ":" + str(i)
                    indexTipoLinde=self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,tipoLinde,0)
                    resp=self.dicLindes.get(clave).set_dlgTipoLinde(cargarDatosDeBda=True)
                    if isinstance(resp,Exception):
                        #no ha podido cargar los datos del linde
                        QtGui.QMessageBox.information(self,"Error en la carga del tipo de linde " + str(i) , resp.message,1)
                        continue#comieza el for de nuevo
                    #puede que no se introdugeran los datos del linde
                    elif resp==True:
                        #Estaban los datos del linde
                        self.cambiaAparienciaOpTreeView(index=indexTipoLinde, dlg=self.dicLindes.get(clave).get_dlgTipoLinde())
                    
                    #acta de deslinde
                    texto="Acta deslinde:" + str(i)
                    indexActaDeslinde=self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,texto)
                    dirDescargas=["ActaDeslinde",str(dicLinde.get("gid"))]
                    nomTabla="actas_deslinde"#sin prefijo.Lo hace dentro de la función
                    dicCondiciones={}
                    dicCondiciones.update([["gid_linde",dicLinde.get("gid")]])
                    resp=self.cargaTablaNoEspacial(nombreOpcion=texto, nomTabla=nomTabla, listaSubDirDescargas=dirDescargas, mostrarBttNuevo=False, dicCondiciones=dicCondiciones)
                    if isinstance(resp,Exception):
                        QtGui.QMessageBox.information(self,"Error en la carga del tipo del acta de deslinde " + str(i) , resp.message,1)
                        continue#comieza el for de nuevo
                    elif resp!=None:   
                        #había acta de deslinde
                        clave="Linde" + ":" + str(i)
                        self.dicActasDeslinde[clave]=resp
                        self.cambiaAparienciaOpTreeView(index=indexActaDeslinde, dlg=self.dicActasDeslinde.get(clave))
                    
                    #colindantes
                    clave="Add colindantes:" + str(i)
                    self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,clave)
                    clave2="Ver colindantes:" + str(i)
                    self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,clave2)
                    self.actualizaTreeviewTablaNoEspacial(nombreOpcion=clave, nomTabla="colindantes", nombreHijo=None, dicCondiciones=dicCondiciones)
                    
                    #imagenes
                    clave="Add imagenes linde:" + str(i)
                    indexAddImagenes=self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,clave)
                    clave2="Ver imagenes linde:" + str(i)
                    self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,clave2)
                    nomTabla=self.oUtiles.get_nomTabla("img_linde")
                    self.actualizaIMGTreeview(indexPadre=indexAddImagenes, nomTabla=nomTabla, dicCondiciones=dicCondiciones)                    
                    self.imagenesAnyadidasTreeWiew=True
            else:
                mens=self.toUtf8("No ha seleccionado ningún elemento interior de la capa dxf_lindes y no hay ninguna de las siguientes capas: ed_lindes, lindes, hist_lindes.")
                avisos.append(mens)
        self.oUtiles.iface.mapCanvas().zoomToSelected()
        self.muestra_estado(mensaje="Datos cargados", tiempo=3000)
        for aviso in avisos:
            QtGui.QMessageBox.information(self,"Error" , aviso,1)
            
    def actualizaTreeviewTablaNoEspacial(self,nombreOpcion,nomTabla,nombreHijo=None,dicCondiciones=None):
        """
        Se utiliza para tablas que pueden tener varios registros en el mismo trabajo,
        por ejemplo: clientes, propietarios, documentos estudiados,...
        Comprueba si hay datos en la base de datos de la tabla para el trabajo actual y,
        si es así, pone la opción index en negrita y, si nombreHijo es diferente de None,
        añade un hijo con el texto nombreHijo.
        Por ejemplo para la tabla clientes sería:
            - index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto("Clientes",self.ui.treeView)
            - self.actualizaTreeviewVarios(index, nomTabla="comun.clientes", nombreHijo="Ver clientes")
        """
        index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto(nombreOpcion,self.ui.treeView)
        nomTabla=self.oUtiles.get_nomTabla(nomTabla)
        if dicCondiciones==None:
            listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=nomTabla, listaCampos=["id_trabajo"], condicionWhere="id_trabajo=%s",listaValoresCondWhere=[self.oUtiles.id_trabajo])
        else:
            condicionWhere=self.oUtiles.oConsultasPg.oGeneraExpresionesPsycopg2.generaWhere(dicCondiciones.keys(),"and")
            listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=nomTabla, listaCampos=["id_trabajo"], condicionWhere=condicionWhere,listaValoresCondWhere=dicCondiciones.values())
        if isinstance(listaDic,Exception):
            self.muestra_estado(mensaje=listaDic.message, tiempo=5000)
            return
        if len(listaDic)>0:
            self.cambiaAparienciaOpTreeView(index, self.ctrIntrodDatos_Ntrab)
            if nombreHijo!=None:
                self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, nombreHijo)
            
    def cargaTablaNoEspacial(self,nombreOpcion,nomTabla,listaSubDirDescargas=None,mostrarBttNuevo=False, dicCondiciones={}):
        """
        Carga un registro de la BDA y crea un cuadro de dialogo con los datos de ese registro.
        Devuelve el cuadro creado.
        @type nombreOpcion: string
        @param nombreOpcion: Nombre de la opción del treeview enlazado con el cuadro de diálogo.
        @type nomTabla: string
        @param nomTabla: Nombre de la tabla no espacial, sin prefijos. Ej: comun.memorias.
        @type listaSubDirDescargas: lista
        @param listaSubDirDescargas: Lista con los directorios a crear en el caso de descargar un
            archivo.
        @type mostrarBttNuevo: Boolean
        @param mostrarBttNuevo: Si es true, si el usuario puede modificar el trabajo, se muestra
            el botón Nuevo.
        @return: un dialogo si todo va bien, None si no había registros coincidentes, Exception en caso de error.
        """
        nomTabla=self.oUtiles.get_nomTabla(nomTabla)
        dlg=ctrIntrodDatos_N(self.oUtiles,tabla=nomTabla,listaSubDirDescargas=listaSubDirDescargas,mostrarBttNuevo=mostrarBttNuevo)
        resp=dlg.setModoConsultar(mostrarBttNuevo, dicValoresCompleto=None,dicCondiciones=dicCondiciones)
        if isinstance(resp,Exception):
            QtGui.QMessageBox.information(self,"Error" , resp.message,1)
        if resp==True:
            index=self.oUtiles.oUtilidadesFormularios.treeViewIndexFromTexto(nombreOpcion,self.ui.treeView)
            self.cambiaAparienciaOpTreeView(index=index, dlg=dlg)
            return dlg
        else:
            return None
    
    def buscarTrabajo(self,nomTabla):
        """
        Busca el id_trabajo de cualquier tabla de la base de datos, carga
        el cuadro de dialogo trabajos en self.ctrIntrodDatos_Ntrab
        También guarda en oUtiles el id_trabajo, el src_trabajo, municipio y el creador del trabajo.
        Si hay algún problema, devuelve -1 y se limpian las variables de 
        oUtiles: id_trabajo y el creador del trabajo. El src_trabajo y el municipio,
        se establecen de la conexion
        @type nomTabla: string
        @param nomTabla: nombre de la tabla en la que se va a buscar el trabajo.
            Si la tabla está en el esquema comun, nomTabla debe ser "comun.nombre".
            Si está en algún esquema de las tablas espaciales src_XXXXX, nomTabla
            va sin el nombre del esquema. Por ejemplo: "colindantes"
        @return: None si hay algún problema. id_trabajo, en caso contrario.
        """
        self.datamodel.clear()
        if nomTabla=="comun.trabajos":
            dlgSelEsquema=ctrSelEsquema(self.oUtiles,False)
        else:
            dlgSelEsquema=ctrSelEsquema(self.oUtiles,True)
        dlgSelEsquema.exec_()
        if dlgSelEsquema.getTipoTrabajo()==None:
            return
        
        if dlgSelEsquema.getSrc()==None and nomTabla!="comun.trabajos":
            return
        self.__elimina_datos_trabajo_oUtiles()

        #self.oUtiles.tipo_trabajo=dlgSelEsquema.getTipoTrabajo()#esta mal. es de solo lectura
        self.oUtiles.prefijo_tipo_trabajo=dlgSelEsquema.getTipoTrabajo()#parece erroneo, pero mira la documentacion de, __set_prefijo_tipo_trabajo

        self.oUtiles.src_trabajo=dlgSelEsquema.getSrc()
        nomTablaCompleto=self.oUtiles.get_nomTabla(nomTabla)
        self.muestra_estado(mensaje="Solicitando datos. Espere ...", tiempo=0)
        dlgBus=ctrIntrodDatos_Buscar(self.oUtiles,nomTablaCompleto)
        ntrab=dlgBus.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
        if ntrab==-1:
            #QtGui.QMessageBox.information(self,"Mensaje" , "No se ha elegido ningun trabajo",1)
            self.__elimina_datos_trabajo_oUtiles()
            return 
        self.oUtiles.id_trabajo=dlgBus.id_trabajo
        
        nomTablaTrabajos=self.oUtiles.get_nomTabla("comun.trabajos")
        self.ctrIntrodDatos_Ntrab=ctrIntrodDatos_Ntrab(self.oUtiles,nomTablaTrabajos)
        #cargo el registro en el cuadro de dialogo, usando el id_trabajo de oUtiles
        self.ctrIntrodDatos_Ntrab.setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones={})
        dic=self.ctrIntrodDatos_Ntrab.dicValoresCompleto
        self.ctrIntrodDatos_Ntrab.ui.tbId_trabajo.setText(str(dic.get("id_trabajo")))
        self.ctrIntrodDatos_Ntrab.ui.tbSrc_trabajo.setText(str(dic.get("src_trabajo")))
        self.oUtiles.usuario_creador_trabajo=dic.get("usuario")
        self.oUtiles.src_trabajo=str(dic.get("src_trabajo"))
        self.oUtiles.municipio=str(dic.get("municipio"))
        return self.oUtiles.id_trabajo
    
    def cargaDatoTrabajo2(self,id_trabajo,tipo_trabajo):
        """
        Dado un id_trabajo y un tipo trabajo, carga todos los datos del trabajo.
        Este método se usa desde la clase clsPropiedad, para cargar trabajos
        seleccionando un objeto con Qgis.
        """
        if tipo_trabajo.lower()=="edicion":
            nomTablaTrabajos="ed_comun.ed_trabajos"
            tipo_trabajo="Edicion"
        elif tipo_trabajo.lower()=="definitivo":
            nomTablaTrabajos="comun.trabajos"
            tipo_trabajo="Definitivo"
        else:
            QtGui.QMessageBox.information(self,"Error" , "No esta programada la carga de datos de tipo trabajo " + tipo_trabajo,1)
            return
        self.datamodel.clear()
        self.__elimina_datos_trabajo_oUtiles()

        self.oUtiles.id_trabajo=id_trabajo
        self.oUtiles.prefijo_tipo_trabajo=tipo_trabajo##parece erroneo, pero mira la documentacion de __set_prefijo_tipo_trabajo
        self.ctrIntrodDatos_Ntrab=ctrIntrodDatos_Ntrab(self.oUtiles,nomTablaTrabajos)
        #cargo el registro en el cuadro de dialogo, usando el id_trabajo de oUtiles
        resp=self.ctrIntrodDatos_Ntrab.setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones={})
        if resp!=True:
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Error" , resp.message,1)
                return
            else:
                QtGui.QMessageBox.information(self,"Error" , "Hubo algun problema en la carga del trabajo " + str(id_trabajo),1)
                return
        dic=self.ctrIntrodDatos_Ntrab.dicValoresCompleto
        self.oUtiles.src_trabajo=str(dic.get("src_trabajo"))
        self.oUtiles.municipio=dic.get("municipio")
        self.oUtiles.usuario_creador_trabajo=dic.get("usuario")
        self.ctrIntrodDatos_Ntrab.ui.tbId_trabajo.setText(str(dic.get("id_trabajo")))
        self.ctrIntrodDatos_Ntrab.ui.tbSrc_trabajo.setText(str(dic.get("src_trabajo")))
        self.opRecargarTrabajo()

    def opValidarTrabajo(self):
        """
        Copia todos los datos del trabajo de las capas de edición a las capas definitivas.
        Si hay algún error, deja la base de datos como estaba antes de elegir esta opcioón.
        """
        #settrace()
        if self.oUtiles.src_trabajo!=None and self.oUtiles.id_trabajo!=None and self.oUtiles.usuario_creador_trabajo!=None:
            pass
        else:
            QtGui.QMessageBox.information(self,"Mensaje" , "No hay trabajo actual",1)
            return
        if self.ctrIntrodDatos_Ntrab.getNomTabla()!="ed_comun.ed_trabajos":
            QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("El trabajo actual no está en edición."),1)
            return
        mens=unicode("Primero debe comprobar si hay errores gaps en el trabajo. ¿Desea continuar?","utf-8")
        reply = QtGui.QMessageBox.question(self, "Recordatorio", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return        
        """
        mens=unicode("Esta acción copiará el trabajo actual de edición en el nivel definitivo. Después deberá eliminar el trabajo actual. ¿Desea continuar?","utf-8")
        reply = QtGui.QMessageBox.question(self, "Mensaje", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return
        """
        dicSoloOldTrab=dict({"id_trabajo":self.oUtiles.id_trabajo})#diccionario
            #con el id_trabajo en edición para seleccionar las tablas en edición   
        #Tabla trabajos
        try:
            fecha=str(datetime.datetime.now())
            dic_fecha_val={'fecha_validacion':fecha}
            #diccionario con solo el id_trabajo nuevo, se usa para actualizar los lindes, memorias,... en el esquema definitivo
            dicSoloNuevoTrab=self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen="ed_comun.ed_trabajos",tablaDestino="comun.trabajos",listaCamposCopiar="todos",listaCamposNoCopiar=["id_trabajo"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=False,puedenSerCero=False,dicValoresCambiar=None,dicValoresAdd=dic_fecha_val,borrarOrigen=False, listaCamposReturning=["id_trabajo"])
        except Exception,e:
            QtGui.QMessageBox.information(self,"Error al copiar el trabajo" , e.message,1)
            return
        try:#este try cubre todas las operaciones por si hay algún error inesperado
            
            #memorias
            try:
                self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen="ed_comun.ed_memorias",tablaDestino="comun.memorias",listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=False,puedenSerCero=False,dicValoresCambiar=dicSoloNuevoTrab,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar la memoria del trabajo de edicion", "Error al copiar la memoria del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return

            #desplazamiento
            try:
                self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen="ed_comun.ed_desp_carto_cat",tablaDestino="comun.desp_carto_cat",listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=False,puedenSerCero=True,dicValoresCambiar=dicSoloNuevoTrab,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar los datos del desplazamiento del trabajo de edicion", "Error al copiar los datos del desplazamiento del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return

            #planos
            try:
                self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen="ed_comun.ed_planos",tablaDestino="comun.planos",listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=True,puedenSerCero=False,dicValoresCambiar=dicSoloNuevoTrab,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar los planos del trabajo de edicion", "Error al copiar los planos del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
    
            #clientes
            try:
                self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen="ed_comun.ed_clientes",tablaDestino="comun.clientes",listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=True,puedenSerCero=False,dicValoresCambiar=dicSoloNuevoTrab,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar los clientes del trabajo de edicion", "Error al copiar los clientes del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
    
            #documentos estudiados
            try:
                self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen="ed_comun.ed_documentos_estudiados",tablaDestino="comun.documentos_estudiados",listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=True,puedenSerCero=False,dicValoresCambiar=dicSoloNuevoTrab,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar los documentos_estudiados del trabajo de edicion", "Error al copiar los documentos_estudiados del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
    
            #propietarios
            try:
                self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen="ed_comun.ed_propietarios",tablaDestino="comun.propietarios",listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=True,puedenSerCero=False,dicValoresCambiar=dicSoloNuevoTrab,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar los propietarios del trabajo de edicion", "Error al copiar los propietarios del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
            
            #finca
            nomTablaOrigen="ed_src" + str(self.oUtiles.src_trabajo) +".ed_fincas"
            nomTablaDestino="src" + str(self.oUtiles.src_trabajo) +".fincas"
            try:
                dicGidFinca=self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigen,tablaDestino=nomTablaDestino,listaCamposCopiar="todos",listaCamposNoCopiar=["gid"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=False,puedenSerCero=False,dicValoresCambiar=dicSoloNuevoTrab,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=["gid"])
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar la finca del trabajo de edicion", "Error al copiar la finca del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
    
            dicNuevoTrabGidFinca={}
            dicNuevoTrabGidFinca["id_trabajo"]=dicSoloNuevoTrab.get("id_trabajo")
            dicNuevoTrabGidFinca["gid_finca"]=dicGidFinca.get("gid")#añade al diccionario la clave gid:num
            #datos catastrales de la finca
            #veamos si es de rústica
            #selecciono los datos catastrales solo con el id_trabajo, ya que solo puede haber una finca por
            #trabajo, aunque pueden haber varias referencias catastrales tanto de rustica como de 
            #urbana para la finca.
            nomTablaOrigen="ed_src" + str(self.oUtiles.src_trabajo) +".ed_ref_cat_rus"
            nomTablaDestino="src" + str(self.oUtiles.src_trabajo) +".ref_cat_rus"
            try:
                dicId=self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigen,tablaDestino=nomTablaDestino,listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=True,puedenSerCero=True,dicValoresCambiar=dicNuevoTrabGidFinca,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=["id"])
                if len(dicId)!=1:#no era de rustica. Veamos si tiene valores en urbana
                    nomTablaOrigen="ed_src" + str(self.oUtiles.src_trabajo) +".ed_ref_cat_urb"
                    nomTablaDestino="src" + str(self.oUtiles.src_trabajo) +".ref_cat_urb"                
                    try:
                        dicId=self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigen,tablaDestino=nomTablaDestino,listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=True,puedenSerCero=False,dicValoresCambiar=dicNuevoTrabGidFinca,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=["id"])
                    except Exception,e:
                        QtGui.QMessageBox.information(self,"Error al copiar los la ref. cat. de urbana del trabajo de edicion", "Error al copiar la ref. cat. de urbana del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Lo mas probable es que no se hayan introducido los datos catastrales de rustica ni de urbana. Se deshacen todos los cambios.",1)
                        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                        if isinstance(resp,Exception):
                            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                        return           
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar los la ref. cat. de rustica del trabajo de edicion", "Error al copiar ref. cat. de rustica del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return    
       
            #servidumbres
            nomTablaOrigen="ed_src" + str(self.oUtiles.src_trabajo) +".ed_servidumbres"
            nomTablaDestino="src" + str(self.oUtiles.src_trabajo) +".servidumbres"
            try:
                self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigen,tablaDestino=nomTablaDestino,listaCamposCopiar="todos",listaCamposNoCopiar=["gid"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=True,puedenSerCero=True,dicValoresCambiar=dicNuevoTrabGidFinca,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar las servidumbres del trabajo de edicion", "Error al copiar las servidumbres del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
    
            #parcelas afectadas
            nomTablaOrigen="ed_src" + str(self.oUtiles.src_trabajo) +".ed_parcelas_afectadas"
            nomTablaDestino="src" + str(self.oUtiles.src_trabajo) +".parcelas_afectadas"
            try:
                self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigen,tablaDestino=nomTablaDestino,listaCamposCopiar="todos",listaCamposNoCopiar=["gid"],dicCondWhere=dicSoloOldTrab,puedenSerVarios=True,puedenSerCero=True,dicValoresCambiar=dicSoloNuevoTrab,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error al copiar las parcelas afectadas del trabajo de edicion", "Error al copiar las parcelas fectadas del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
    
            #datos de los lindes:
            nomTablaOrigen="ed_src" + str(self.oUtiles.src_trabajo) +".ed_lindes"
            nomTablaDestino="src" + str(self.oUtiles.src_trabajo) +".lindes"        
            dicLindes=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=nomTablaOrigen, listaCampos=["gid","tipo_linde"], condicionWhere="id_trabajo=%s",listaValoresCondWhere=[self.oUtiles.id_trabajo],bytea_output_to_escape=False)
            if isinstance(dicLindes,Exception):
                QtGui.QMessageBox.information(self,"Error al seleccionar los lindes del trabajo de edicion","Error al seleccionar los lindes del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + ". Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
            elif len(dicLindes)>0:
                """
                QtGui.QMessageBox.information(self,"Error al seleccionar los lindes del trabajo de edicion","Error al seleccionar los lindes del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + ". Descripcion del error: No hay lindes . Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
                """
                dicOldTrabGidLinde={}#se utiliza para seleccionar el linde en la capa de edición     
                dicOldTrabGidLinde["id_trabajo"]=self.oUtiles.id_trabajo
                dicNuevoTrabGidLinde={}#Se usa para actualizar el id_trabajo y el gid_linde en las tablas en el esquema definitivo. A este diccionario le añado después el nuevo gid_linde.
                dicNuevoTrabGidLinde["id_trabajo"]=dicSoloNuevoTrab.get("id_trabajo")
                for dicGidOld in dicLindes:#diccionarios con los gids antiguos
                    dicOldTrabGidLinde.update([["gid",dicGidOld.get("gid")]])#gid del antiguo linde. Cambia el anterior gid por el del la iteración actual. 
                    try:
                        dicNuevoGidLinde=self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigen,tablaDestino=nomTablaDestino,listaCamposCopiar="todos",listaCamposNoCopiar=["gid"],dicCondWhere=dicOldTrabGidLinde,puedenSerVarios=False,puedenSerCero=False,dicValoresCambiar=dicNuevoTrabGidFinca,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=["gid"])
                    except Exception,e:
                        QtGui.QMessageBox.information(self,"Error al copiar los lindes del trabajo de edicion", "Error al copiar los lindes del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + " Descripcion del error: " + e.message + ". Lo mas probable es que no se hayan introducido los datos catastrales de rustica ni de urbana. Se deshacen todos los cambios.",1)
                        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                        if isinstance(resp,Exception):
                            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                        return
                    dicNuevoTrabGidLinde.update([["gid_linde",dicNuevoGidLinde.get("gid")]])#gid del nuevo linde. Cambia el anterior gid, por el del la iteración actual.  
                    #cambio ahora todos los datos asociados al linde, que necesitan el nuevo id_trabajo y el nuevo gid_linde
           
                    #datos del tipo de linde
                    tipo_linde=dicGidOld.get("tipo_linde")
                    if tipo_linde=="Digitalizado sobre ortofoto":
                        nomTablaTipoLinde="linde_digitalizado"
                    elif tipo_linde=="Existe en el terreno":
                        nomTablaTipoLinde="linde_existente"
                    elif tipo_linde=="No existe en el terreno y se replantea":
                        nomTablaTipoLinde="linde_replanteado"
                    elif tipo_linde==self.toUtf8("Proyectado en algún documento"):
                        nomTablaTipoLinde="linde_proyectado"
                    else:
                        QtGui.QMessageBox.information(self,"Error al copiar datos del linde del trabajo de edicion", "Error al copiar los datos del linde del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + ". gid del linde del trabajo en edicion: " + str(dicGidOld.get("gid")) + ". No se ha especificado el tipo de linde. Se deshacen todos los cambios.",1)
                        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                        if isinstance(resp,Exception):
                            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                        return    
                    nomTablaOrigenTipoLin="ed_src" + str(self.oUtiles.src_trabajo) + ".ed_" + nomTablaTipoLinde
                    nomTablaDestinoTipoLin="src" + str(self.oUtiles.src_trabajo) + "." + nomTablaTipoLinde
                    
                    dicOldTrabGidLindeDatos={}#sirve para seleccionar los registros de las tablas que describen los lindes
                    dicOldTrabGidLindeDatos["gid_linde"]=dicGidOld.get("gid")
                    dicOldTrabGidLindeDatos["id_trabajo"]=self.oUtiles.id_trabajo
                    dicNuevoTrabGidLindeDatos={}#sirve para cambiar los datos de los lines en los registros de las tablas definitivas que describen los lindes
                    dicNuevoTrabGidLindeDatos["gid_linde"]=dicNuevoGidLinde.get("gid")
                    dicNuevoTrabGidLindeDatos["id_trabajo"]=dicSoloNuevoTrab.get("id_trabajo")
                    
                    try:
                        #selecciona por id_trabajo y gid_linde antiguos y copia cambiando los id_trabajo y gid_linde por los nuevos
                        self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigenTipoLin,tablaDestino=nomTablaDestinoTipoLin,listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicOldTrabGidLindeDatos,puedenSerVarios=False,puedenSerCero=False,dicValoresCambiar=dicNuevoTrabGidLindeDatos,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
                    except Exception,e:
                        QtGui.QMessageBox.information(self,"Error al copiar datos del linde del trabajo de edicion", "Error al copiar los datos del linde del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + ". gid del linde del trabajo en edicion: " + str(dicGidOld.get("gid")) + ". No se han introducido los datos del tipo de linde: Replanteado, Proyectado, Existente o Digitalizado. Se deshacen todos los cambios. Descripcion del error: " + e.message,1)
                        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                        if isinstance(resp,Exception):
                            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                        return
        
                    #acta de deslinde
                    nomTablaOrigenActaDes="ed_src" + str(self.oUtiles.src_trabajo) + ".ed_actas_deslinde"
                    nomTablaDestinoActaDes="src" + str(self.oUtiles.src_trabajo) + ".actas_deslinde"
                    try:
                        #el acta de deslinde no es obligatoria. Puede que no haya
                        self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigenActaDes,tablaDestino=nomTablaDestinoActaDes,listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicOldTrabGidLindeDatos,puedenSerVarios=False,puedenSerCero=True,dicValoresCambiar=dicNuevoTrabGidLindeDatos,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
                    except Exception,e:
                        QtGui.QMessageBox.information(self,"Error al copiar datos del acta de deslinde del trabajo de edicion", "Error al copiar los datos del acta de deslinde del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + ". gid del linde del trabajo en edicion: " + str(dicGidOld.get("gid")) + ". Descripcion del error: " + e.message +  ". Se deshacen todos los cambios.",1)
                        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                        if isinstance(resp,Exception):
                            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                        return
            
                    #colindantes
                    nomTablaOrigenColin="ed_src" + str(self.oUtiles.src_trabajo) + ".ed_colindantes"
                    nomTablaDestinoColin="src" + str(self.oUtiles.src_trabajo) + ".colindantes"
                    try:
                        #el acta de deslinde no es obligatoria. Puede que no haya
                        self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigenColin,tablaDestino=nomTablaDestinoColin,listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicOldTrabGidLindeDatos,puedenSerVarios=True,puedenSerCero=True,dicValoresCambiar=dicNuevoTrabGidLindeDatos,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
                    except Exception,e:
                        QtGui.QMessageBox.information(self,"Error al copiar los datos de los colindantes del trabajo de edicion", "Error al copiar los datos de los colindantes del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + ". gid del linde del trabajo en edicion: " + str(dicGidOld.get("gid")) + ". Descripcion del error: " + e.message +  ". Se deshacen todos los cambios.",1)
                        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                        if isinstance(resp,Exception):
                            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                        return
        
                    #imagenes
                    nomTablaOrigenColin="ed_src" + str(self.oUtiles.src_trabajo) + ".ed_img_linde"
                    nomTablaDestinoColin="src" + str(self.oUtiles.src_trabajo) + ".img_linde"
                    try:
                        #el acta de deslinde no es obligatoria. Puede que no haya
                        self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigenColin,tablaDestino=nomTablaDestinoColin,listaCamposCopiar="todos",listaCamposNoCopiar=["gid"],dicCondWhere=dicOldTrabGidLindeDatos,puedenSerVarios=True,puedenSerCero=True,dicValoresCambiar=dicNuevoTrabGidLindeDatos,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
                    except Exception,e:
                        QtGui.QMessageBox.information(self,"Error al copiar los datos de las imagenes del trabajo de edicion", "Error al copiar los datos de las imagenes del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + ". gid del linde del trabajo en edicion: " + str(dicGidOld.get("gid")) + ". Descripcion del error: " + e.message +  ". Se deshacen todos los cambios.",1)
                        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                        if isinstance(resp,Exception):
                            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                        return
                
            #Elementos interiores
            nomTablaOrigen="ed_src" + str(self.oUtiles.src_trabajo) +".ed_elem_interiores"
            nomTablaDestino="src" + str(self.oUtiles.src_trabajo) +".elem_interiores"        
            listaDicEIOld=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=nomTablaOrigen, listaCampos=["gid"], condicionWhere="id_trabajo=%s",listaValoresCondWhere=[self.oUtiles.id_trabajo],bytea_output_to_escape=False)
            if isinstance(listaDicEIOld,Exception):
                QtGui.QMessageBox.information(self,"Error al seleccionar los elementos interiores del trabajo de edicion","Error al seleccionar los elementos interiores del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + ". Descripcion del error: " + e.message + ". Se deshacen todos los cambios.",1)
                resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                return
    
            dicOldTrabGidEltoI={}#para seleccionar EI en edicion
            dicOldTrabGidEltoI["id_trabajo"]=self.oUtiles.id_trabajo
    
            dicOldTrabGidEltoIImg={}#para seleccionar las imagenes del EI en edicion
            dicOldTrabGidEltoIImg["id_trabajo"]=self.oUtiles.id_trabajo
      
            dicNuevoTrabGidEltoIImg={}#para actualizar las imagenes del EI definitivo
            dicNuevoTrabGidEltoIImg["id_trabajo"]=dicSoloNuevoTrab.get("id_trabajo")
    
          
            nomTablaOrigenImgEI="ed_src" + str(self.oUtiles.src_trabajo) + ".ed_img_elem_int"
            nomTablaDestinoImgEI="src" + str(self.oUtiles.src_trabajo) + ".img_elem_int" 
      
            for dicEIOld in listaDicEIOld:#diccionarios con los gids antiguos
                dicOldTrabGidEltoI.update([["gid",dicEIOld.get("gid")]])#gid del antiguo linde. Cambia el anterior gid por el del la iteración actual. 
                dicOldTrabGidEltoIImg.update([["gid_elem_int",dicEIOld.get("gid")]])
                try:
                    dicNuevoGidEI=self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigen,tablaDestino=nomTablaDestino,listaCamposCopiar="todos",listaCamposNoCopiar=["gid"],dicCondWhere=dicOldTrabGidEltoI,puedenSerVarios=False,puedenSerCero=False,dicValoresCambiar=dicNuevoTrabGidFinca,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=["gid"])
                except Exception,e:
                    QtGui.QMessageBox.information(self,"Error al copiar los elementos interiores del trabajo de edicion", "Error al copiar los elementos interiores del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + ". gid del elemento interior del trabajo en edicion: " + str(dicEIOld.get("gid")) + ". Descripcion del error: " + e.message +  ". Se deshacen todos los cambios.",1)
                    resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                    if isinstance(resp,Exception):
                        QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                    return
                dicNuevoTrabGidEltoIImg.update([["gid_elem_int",dicNuevoGidEI.get("gid")]])#gid del nuevo EI.
                try:
                    self.oUtiles.oConsultasPg.mueveRegistros(tablaOrigen=nomTablaOrigenImgEI,tablaDestino=nomTablaDestinoImgEI,listaCamposCopiar="todos",listaCamposNoCopiar=["id"],dicCondWhere=dicOldTrabGidEltoIImg,puedenSerVarios=True,puedenSerCero=True,dicValoresCambiar=dicNuevoTrabGidEltoIImg,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None)
                except Exception,e:
                    QtGui.QMessageBox.information(self,"Error al copiar las imagenes de los elementos interiores del trabajo de edicion", "Error al copiar las imagenes de los elementos interiores del trabajo de edicion id_trabajo:" + str(self.oUtiles.id_trabajo) + " al trabajo definitivo id_trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")) + ". gid del elemento interior del trabajo en edicion: " + str(dicEIOld.get("gid")) + ". Descripcion del error: " + e.message +  ". Se deshacen todos los cambios.",1)
                    resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
                    if isinstance(resp,Exception):
                        QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios. Permanecen datos en el trabajo: " + str(dicSoloNuevoTrab.get("id_trabajo")),1)
                    return
            
        except Exception,e:
            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "Se deshacen los cambios.",1)
            resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="comun.trabajos",dicCondWhere=dicSoloNuevoTrab)
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudieron deshacer los cambios.",1)
            return
        #borro el trabajo de edición recien copiado.
        """
        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla="ed_comun.ed_trabajos",dicCondWhere=dicSoloOldTrab)
        if isinstance(resp,Exception):
            QtGui.QMessageBox.information(self,self.toUtf8("Hubo un problema") , e.message + "No se pudo eliminar el trabajo en edicion.",1)
            return
        self.limpiaFormularios(borrarDlgTrabajo=True)
        self.datamodel.clear()
        """
        QtGui.QMessageBox.information(self,self.toUtf8("Copia realizada con éxito.") , "Compruebe las capas overlaps_fincas y gaps_fincas para el trabajo definitivo " + str(dicSoloNuevoTrab.get("id_trabajo")) + ". Si todo es correcto borre el trabajo de edicion " + str(self.oUtiles.id_trabajo) + ". Si hay algun hueco, borre el trabajo definitivo y corrija el trabajo de edicion",1)

    def opBorrarTrabajo(self,darMens=True):
        """
        Borra el trabajo actual. 
            - Si darMens es True pregunta dos veces si se quiere
        eliminar el trabajo, y luego avisa de que se ha borrado correctamente.
        Si es false no hace nada de lo dicho anteriormente.
            - Si todo va bien limpia los datos de los formularios de la clase y devuelve True.
            - Si hay algún problema. Da un mensaje, independientemente del valor de
        darMens, y devuelve un Exception. 
            - Si no hay trabajo actual da un mensaje y devuelve
        False. 
            - Si el usuario  no es administrador y  no es el creador del trabajo, da
        un mensaje y devuelve False.
        """
        if self.oUtiles.src_trabajo!=None and self.oUtiles.id_trabajo!=None and self.oUtiles.usuario_creador_trabajo!=None:
            pass
        else:
            QtGui.QMessageBox.information(self,"Mensaje" , "No hay trabajo actual",1)
            return False
        
        if self.oUtiles.tipo_usuario!="admin_propiedad":
            if self.oUtiles.usuario!=self.oUtiles.usuario_creador_trabajo :
                #no es el autor
                QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("No puede eliminar un trabajo que no sea ud. el autor"),1)
                return False
            elif self.oUtiles.prefijo_tipo_trabajo=="" or self.oUtiles.prefijo_tipo_trabajo=="hist_":
                #es el autor
                QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("No puede eliminar un trabajo en las capas definitivas, ni del histórico. Póngase en contacto con el administrador."),1)
                return False
        
        if darMens==True:
            mens=unicode("Esta acción eliminará el trabajo completo permanantemente. ¿Desea continuar?","utf-8")
            reply = QtGui.QMessageBox.question(self, "Mensaje", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
    
            mens=unicode("¿Esta acción eliminará el trabajo completo permanantemente. ¿Desea continuar?","utf-8")
            reply = QtGui.QMessageBox.critical(self, "Por segunda vez", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
            
        dicCondWhere=dict({"id_trabajo":int(self.oUtiles.id_trabajo)})
        nomTabla=self.oUtiles.get_nomTabla("comun.trabajos")
        resp=self.oUtiles.oConsultasPg.deleteDatos(nombreTabla=nomTabla,dicCondWhere=dicCondWhere)
       
        if isinstance(resp,Exception):
            reply = QtGui.QMessageBox.information(self, "No se pudo eliminar el trabajo", "El servidor respondio: " + resp.message, 1)
            return resp
        else:
            self.limpiaFormularios(borrarDlgTrabajo=True)
            self.__elimina_datos_trabajo_oUtiles()
            if darMens==True:
                QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("Trabajo eliminado con éxito"),1)
        return True
    
    def opVerHistorico(self):
        """
        Pone en el TreeView las opciones para ver el historico de una finca
        """
        QtGui.QMessageBox.information(self,"Herramienta sin programar" , "Ver historico",1)

    def opAgreDivVert(self):
        """
        Pone en el TreeView las opciones para añadir una división vertical
        """
        QtGui.QMessageBox.information(self,"Herramienta sin programar" , "Agregar division vertical",1)

    def opDividirFinca(self):
        """
        Pone en el TreeView las opciones para dividir una finca
        """
        QtGui.QMessageBox.information(self,"Herramienta sin programar" , "Dividir",1)

    def opAgregarFinca(self):
        """
        Pone en el TreeView las opciones para agregar una finca a otra
        """
        QtGui.QMessageBox.information(self,"Herramienta sin programar" , "Agregar",1)

    def opSegregarFinca(self):
        """
        Pone en el TreeView las opciones para segregar una finca
        """
        QtGui.QMessageBox.information(self,"Herramienta sin programar" , "Segregar",1)
 
    def __elimina_datos_trabajo_oUtiles(self):
        """
        Establece a None las propiedades  self.oUtiles.id_trabajo y self.oUtiles.usuario_creador_trabajo.
        El src y el municipio se conservan.
        """
        #self.oUtiles.src_trabajo=self.src_trabajo_conexion
        self.oUtiles.id_trabajo=None
        self.oUtiles.usuario_creador_trabajo=None
        #self.oUtiles.municipio=self.municipio_conexion
        self.datamodel.clear()
        cad = "U:" + str(self.oUtiles.usuario) + "SRC:" + self.oUtiles.src_trabajo
        self.ui.txtInfo.setText(cad)

    def muestra_estado(self,mensaje,tiempo=0):
        """
        Muestra un mensaje en el estatus bar.
        """
        men=mensaje
        self.ui.statusbar.showMessage(men,tiempo)
    
    def rellenaTreeView(self,opcion):
        """
        Rellena el treeview con las opciones necesarias para la opcion 'opcion'
        """
        self.datamodel.clear()
        parentItem = self.datamodel.invisibleRootItem()
        item = QtGui.QStandardItem("Datos del trabajo")
        item.setEditable(False)
        parentItem.appendRow(item)

        item = QtGui.QStandardItem("Desplazamiento carto catastral")
        item.setEditable(False)
        parentItem.appendRow(item)
        
        item = QtGui.QStandardItem("Memoria del trabajo")
        item.setEditable(False)
        parentItem.appendRow(item)
        
        item = QtGui.QStandardItem("Planos")
        item.setEditable(False)
        parentItem.appendRow(item)

        item = QtGui.QStandardItem("Clientes")
        item.setEditable(False)
        parentItem.appendRow(item)
        
        item = QtGui.QStandardItem("Documentos estudiados")
        item.setEditable(False)
        parentItem.appendRow(item)
        
        item = QtGui.QStandardItem("Propietarios")
        item.setEditable(False)
        parentItem.appendRow(item)
 
        item = QtGui.QStandardItem("Datos de la finca")
        item.setEditable(False)
        parentItem.appendRow(item)
       
        item = QtGui.QStandardItem("Parcelas afectadas")
        item.setEditable(False)
        parentItem.appendRow(item)
        
        item = QtGui.QStandardItem("Datos de los lindes")
        item.setEditable(False)
        parentItem.appendRow(item)

        item = QtGui.QStandardItem("Servidumbres")
        item.setEditable(False)
        parentItem.appendRow(item)        

        item = QtGui.QStandardItem("Elementos interiores")
        item.setEditable(False)
        parentItem.appendRow(item)        
      
        
        self.ui.treeView.expandAll()#expande todos los elementos
        
        #pone el texto de cabecera
        cabecera="Nuevo trabajo"
        lista=[cabecera]
        self.datamodel.setHorizontalHeaderLabels(lista)

    def dobleClicadoTreeView(self, index):
        """
        Manejador del evento doubleClick del TreeView.
        Las opciones elegidas pueden añadir más elementos al treeview. 
        Todas son manejadas desde este método.
        """
        datos=index.data()
        op= str(datos)#opcion elegida
        if op!="Datos del trabajo":
            if self.oUtiles.id_trabajo==None:
                mens1=unicode("Atención","utf-8")
                mens2=unicode("No hay trabajo actual. Cree uno nuevo o seleccione uno para editar","utf-8")
                QtGui.QMessageBox.information(self,mens1 , mens2,1)   
                return
        
        if op == "Datos del trabajo":
            self.add_trabajo(index)
        elif op =="Desplazamiento carto catastral":
            self.add_desplazamiento(index)
        elif op == "Memoria del trabajo":
            self.add_memoria_trabajo(index)
        elif op == "Planos":
            self.add_planos(index)
        elif op == "Clientes":         
            self.add_clientes(index)
        elif op == "Documentos estudiados":
            self.add_documentos_estudiados(index)
        elif op == "Datos de la finca":

            self.add_finca(index)
        elif op == "Propietarios":
            self.add_propietarios(index)                
        elif op == "Datos de los lindes":
            if self.lindesAnyadidosTreeView==False:
                self.add_lindes_treeview(index)
            else:
                mens=unicode("Ya se han añadido los elementos. Si desea añadir más elementos, selelecciónelos de la capa " + str(index.data()) + " y recargue el trabajo.","utf-8")
                QtGui.QMessageBox.information(self,"Aviso" , mens,1)
        elif op == "Parcelas afectadas":
            if self.parcelasAnyadidasTreeView==False:
                self.add_parcelas_afectadas_treeview(index)
            else:
                mens=unicode("Ya se han añadido las parcelas. Si desea añadir más, selelecciónelos de la capa " + str(index.data()) + " y recargue el trabajo.","utf-8")
                QtGui.QMessageBox.information(self,"Aviso" , mens,1)

        elif op == "Servidumbres":
            if self.servidumbresAnyadidosTreeView==False:
                self.add_servidumbres_treeview(index)
            else:
                mens=unicode("Ya se han añadido los elementos. Si desea añadir más elementos, selelecciónelos de la capa " + str(index.data()) + " y recargue el trabajo.","utf-8")
                QtGui.QMessageBox.information(self,"Aviso" , mens,1)
        elif op == "Elementos interiores":
            if self.elementosInterioresAnyadidosTreeView==False:
                self.add_elementos_interiores_treeview(index)
            else:
                mens=unicode("Ya se han añadido los elementos. Si desea añadir más elementos, selelecciónelos de la capa " + str(index.data()) + " y recargue el trabajo.","utf-8")
                QtGui.QMessageBox.information(self,"Aviso" , mens,1)  
        else:
            #Es una opcion secundaria. Hay que ver cual es
            lista= op.split(":")
            subOp=lista[0]
            if subOp=="Rustica" or subOp=="Urbana":
                #hay que mostrar los datos catastrales de la finca
                self.add_datosCatFinca(index)
            elif subOp=="Linde":
                #datos de alguno de los lindes
                self.add_linde(index)
            elif subOp=="Add colindantes":
                #datos de colindantes de alguno de los lindes
                self.add_colindantes(index)
            elif subOp=="Ver colindantes":
                #datos de colindantes de alguno de los lindes
                self.ver_colindantes(index)
            elif subOp=="Digitalizado" or subOp=="Existente" or subOp=="Replanteado" or subOp=="Proyectado":
                #datos del tipo de linde
                self.add_linde_datos(index)
            elif subOp=="Add imagenes linde":
                #datos de alguna imagen
                self.add_img_linde(index)
            elif subOp=="Ver imagenes linde":
                #datos de alguna imagen
                self.ver_img_linde(index)
            elif subOp=="Acta deslinde":
                self.add_acta_deslinde(index)
            elif subOp=="Servidumbre":
                #datos de alguna servidumbre
                self.add_servidumbre(index)
            elif subOp=="Elemento interior":
                #datos de algun elemento interior
                self.add_elemento_interior(index)
            elif subOp=="Parcela afectada":
                #datos de las parcelas afectadas
                self.add_parcela_afectada(index)
            elif subOp=="Add img elto interior":
                #datos de algun elemento interior
                self.add_img_elto_interior(index)
            elif subOp=="Ver img elto interior":
                #datos de algun elemento interior
                self.ver_img_elto_interior(index)
            elif subOp=="Ver clientes":
                self.ver_clientes(index)
            elif subOp=="Ver planos":
                self.ver_planos(index)
            elif subOp=="Ver propietarios":
                self.ver_propietarios(index)
            elif subOp=="Ver documentos estudiados":
                self.ver_documentos_estudiados(index)            
            else:
                mens=unicode("No hay nada programado para esta opción","utf-8")
                QtGui.QMessageBox.information(self,"Aviso" , mens,1)

    def deselecciona_eltos_trabajo(self):
        nomCapaQgs=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"fincas")
        if nomCapaQgs!=None:
            capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgs)
            if capa!=None:
                capa.removeSelection()

        nomCapaQgs=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"lindes")
        if nomCapaQgs!=None:
            capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgs)
            if capa!=None:
                capa.removeSelection()

        nomCapaQgs=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"servidumbres")
        if nomCapaQgs!=None:
            capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgs)
            if capa!=None:
                capa.removeSelection()
                
        nomCapaQgs=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"elem_interiores")
        if nomCapaQgs!=None:
            capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgs)
            if capa!=None:
                capa.removeSelection()
                
    def simpleClicadoTreeView(self, index):
        """
        Manejador del evento click del TreeView.
        Selecciona el elemento de la capa ed_ o definitiva
        """
        
        datos=index.data()
        op= str(datos)#opcion elegida
        if op=="Datos del trabajo":
            return
        elif op == "Memoria del trabajo":
            return
        elif op == "Planos":
            return
        elif op == "Clientes":         
            return
        elif op == "Documentos estudiados":
            return
        elif op == "Propietarios":
            return                
        elif op == "Datos de la finca":
            if self.ctrIntrodDatos_DatFinca!=None:
                if self.ctrIntrodDatos_DatFinca.get_featureId!=None:
                    self.sel_elto("fincas",self.ctrIntrodDatos_DatFinca.get_featureId()) 
        elif op == "Datos de los lindes":
            return
        elif op == "Servidumbres":
            return
        elif op == "Elementos interiores":
            return
        else:
            #Es una opcion secundaria. Hay que ver cual es
            lista= op.split(":")
            subOp=lista[0]
            if len(lista)>1:
                num=lista[1]
            else:
                if subOp=="Rustica" or subOp=="Urbana":
                    if self.ctrIntrodDatos_DatFinca!=None:
                        if self.ctrIntrodDatos_DatFinca.get_featureId()!=None:
                            self.sel_elto("fincas",self.ctrIntrodDatos_DatFinca.get_featureId())
                return
            if subOp=="Linde" or subOp=="Add colindantes" or subOp=="Ver colindantes" or subOp=="Digitalizado" or subOp=="Existente" or subOp=="Replanteado" or subOp=="Proyectado" or subOp=="Add imagenes linde" or subOp=="Ver imagenes linde" or subOp=="Acta deslinde":
                #datos de alguno de los lindes
                if self.dicLindes!=None:
                    clave="Linde:" + num
                    dlgLinde=self.dicLindes.get(clave)
                    if dlgLinde!=None:
                        feat=dlgLinde.get_featureId()
                        if feat!=None:
                            self.sel_elto("lindes",feat)
            elif subOp=="Servidumbre":
                if self.dicServidumbres!=None:
                    dlgServ=self.dicServidumbres.get(op)
                    if dlgServ!=None:
                        feat=dlgServ.get_featureId()
                        if feat!=None:
                            self.sel_elto("servidumbres",feat)
                
            elif subOp=="Elemento interior" or subOp=="Add img elto interior" or subOp=="Ver img elto interior":
                if self.dicElementoInterior!=None:
                    clave="Elemento interior:" + num
                    dlgEi=self.dicElementoInterior.get(clave)
                    if dlgEi!=None:
                        feat=dlgEi.get_featureId()
                        if feat!=None:
                            self.sel_elto("elem_interiores",feat)
        
    def sel_elto(self,nomCapa,featureId):
        nomCapaQgs=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,nomCapa)
        if nomCapaQgs==None:
            #self.muestra_estado(mensaje="No hay capa Qgis", tiempo=5000)
            return
        if "dxf_" in nomCapaQgs:
            return

        #self.muestra_estado(mensaje="Capa Qgis: " + nomCapaQgs, tiempo=5000)
        capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgs)
        
        if capa==None:
            #self.muestra_estado(mensaje="La capa esta desactivada", tiempo=5000)
            return
        try:
            self.deselecciona_eltos_trabajo()
            capa.setSelectedFeatures([featureId])
        except:
            #self.muestra_estado(mensaje= nomCapaQgs +": No se pudo seleccionar el objeto", tiempo=5000)
            pass
        
    def add_trabajo(self, index):
        """
        Muestra el cuadro de dialogo para crear un nuevo trabajo. Una vez guardado,
        permite editarlo.
        """
        
        if self.ctrIntrodDatos_Ntrab==None:
            nomTabla=self.oUtiles.get_nomTabla("comun.trabajos")
            self.ctrIntrodDatos_Ntrab=ctrIntrodDatos_Ntrab(self.oUtiles,nomTabla)
            self.ctrIntrodDatos_Ntrab.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
        else:
            self.ctrIntrodDatos_Ntrab.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
        self.cambiaAparienciaOpTreeView(index,self.ctrIntrodDatos_Ntrab)
        if self.ctrIntrodDatos_Ntrab.getEstadoGuardado()=="guardado":
            cad = "U:" + str(self.oUtiles.usuario) + " ID:" + str(self.oUtiles.id_trabajo) + " SRC:" + str(self.oUtiles.src_trabajo)
            self.ui.txtInfo.setText(cad)
        if self.oUtiles.id_trabajo==None:#Si borra el trabajo esto sera None
            self.limpiaFormularios()
            self.__elimina_datos_trabajo_oUtiles()
            self.rellenaTreeView("nuevo")
            self.muestra_estado(mensaje="Tabajo eliminado completamente", tiempo=3000)
    def add_memoria_trabajo(self,index):
        """
        Permite añadir una memoria al trabajo.
        """
        self.ctrIntrodDatos_MemoTrabajo=self.add_datos_BDA_sin_geometria(index, self.ctrIntrodDatos_MemoTrabajo, "comun.memorias",["memoria"])

    def add_desplazamiento(self,index):
        """
        Permite añadir una memoria al trabajo.
        """
        self.ctrIntrodDatos_desplazamiento=self.add_datos_BDA_sin_geometria(index, self.ctrIntrodDatos_desplazamiento, "comun.desp_carto_cat",["desplazamiento"])
    
    def add_datos_BDA_sin_geometria(self,index,dlg,nomTabla,listaSubDirDescargas,mostrarBttNuevo=False, dicValoresAdd=None):
        """
        Crea cuadros de diálogo utilizando la clase ctrIntrodDatos_N para guardar
        los datos de la tabla en la BDA. El cuadro de diálogo es devuelto y guardado
        en memoria para no tener que acceder a la base de datos cada vez que se 
        quiera consultar.
        """
        if dlg==None or mostrarBttNuevo==True:
            nomTabla=self.oUtiles.get_nomTabla(nomTabla)
            dlg=ctrIntrodDatos_N(self.oUtiles,nomTabla,listaSubDirDescargas,mostrarBttNuevo, dicValoresAdd)
            dlg.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
        else:
            dlg.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
        self.cambiaAparienciaOpTreeView(index,dlg)
        return dlg

    def add_planos(self, index):
        """
        Permite añadir planos a la base de datos.
        """
        self.ctrIntrodDatos_Plano=self.add_datos_BDA_sin_geometria(index, self.ctrIntrodDatos_Plano, "comun.planos",["planos"],mostrarBttNuevo=True)
        self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, "Ver planos")

    def add_clientes(self, index):
        """
        Permite añadir clientes a la base de datos.
        """
        self.ctrIntrodDatos_Ncli=self.add_datos_BDA_sin_geometria(index, self.ctrIntrodDatos_Ncli, "comun.clientes",["clientes"],mostrarBttNuevo=True)
        self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, "Ver clientes")
    def add_propietarios(self, index):
        """
        Permite añadir propietarios a la base de datos.
        """
        self.ctrIntrodDatos_NPropiet=self.add_datos_BDA_sin_geometria(index, self.ctrIntrodDatos_NPropiet, "comun.propietarios",["propietarios"],mostrarBttNuevo=True)
        self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, "Ver propietarios")
    def add_documentos_estudiados(self, index):
        """
        Permite añadir documentos estudiados a la base de datos.
        """
        self.ctrIntrodDatos_DocEst=self.add_datos_BDA_sin_geometria(index, self.ctrIntrodDatos_DocEst, "comun.documentos_estudiados",["doc_est"],mostrarBttNuevo=True)
        self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,indexPadre=index, texto="Ver documentos estudiados")
    def add_datos_BDA_con_geometria(self,index,nomTablaSinEsquema,nomCapa,dicFormularios,objetosSeleccionados,esMulti=False,cargarDatosDeBda=False):
        """
        Añade elementos gráficos a la base de datos. Para ello utiliza un cuadro de diálogo
        generado con la clase ctrIntrodDatos_NGeom. Cada nuevo cuadro de diálogo es guardado
        en un diccionario. Antes de crear un nuevo cuadro de diálogo, se comprueba el diccionario,
        por si existe. Si existe, se muestra sin crear uno nuevo.
        Cada clave del diccionario apunta a un cuadro de diálogo. La clave es el texto
        del treeview sobre el que se ha hecho doble click.
        Las claves acaban en un número 1,2, .... Este número se usa para seleccionar
        el elemento en QGis. Para ello se usa el nombre de la capa donde se encuentran
        y el conjunto de elementos seleccionados previamente de la capa.
        @type index: QIndex
        @param index: indice del elemento sobre el que se ha hecho doble click en el treeview
        @type nomTablaSinEsquema: string
        @param nomTablaSinEsquema: nombre de la tabla. Ej: elem_interiores
        @type nomCapa: string
        @param nomCapa: nombre de la capa donde se encuentra el elemento a añadir. Se utiliza
            para seleccionarlo y que el usuario vea con qué elemento está trabajando. 
            Se pasa sin prefijo (dxf_,ed_,...). El metodo oUtiles.get_nomCapaQgis, le pone
            el prefijo necesario en funcion del contexto
        @type dicFormularios: dicionario
        @param dicFormularios: diccionario sobre el que de comprueba si existe el formulario.
            Si no existe, se añade.
        @type objetosSeleccionados: coleccion de objetos QGis
        @param objetosSeleccionados: Coleccion de objetos seleccionados de la capa nomCapaDXF.
            También se utiliza para seleccionarlo y que el usuario vea con qué elemento está trabajando
        @type esMulti: boolean
        @param esMulti: Si es true se tranforma el objeto a multi. Si es false, se deja como está.
        """
        datos=index.data()
        op= str(datos)
        lista=op.split(":")#De 'Linde:1' devuelve ['Linde','1']
        i=int(lista[1])#numero de elemento
        nomCapaDXF=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,nomCapa)
        if nomCapaDXF==None:
            QtGui.QMessageBox.information(self,"Error" ,"la capa " + nomCapaDXF + " no existe o esta desactivada.",1)
            return

        capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaDXF)
        if capa==None:
            QtGui.QMessageBox.information(self,"Error" ,"la capa " + nomCapaDXF + " no existe o esta desactivada.",1)
            return
        objeto=objetosSeleccionados[i]
        dic=self.oUtiles.oUtilidadesQgs.get_attrElementoCapa(objeto, capa, listaCampos=[],geom=True)
        oQset=[]
        oQset.append(dic.get("featureId"))
        capa.setSelectedFeatures(oQset)#deselecciona todo
            #y selecciona el punto actual
        geomWkt=dic.get("geom")
        clave=op
        #prefijoTipoTrabajo=self.oUtiles.prefijo_tipo_trabajo
        if dicFormularios.get(clave)==None:
            #pydevd.settrace()
            if 'elem_interiores' in nomTablaSinEsquema or 'servidumbres' in nomTablaSinEsquema:                  
                dicValoresAdd={}
                dicValoresAdd['gid_finca']=self.oUtiles.gid_finca
                
            nomTabla=self.oUtiles.get_nomTabla(nomTablaSinEsquema)
            #__init__(self, oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo=False,dicValoresAdd=None, geomWkt=None,esMulti=False):
            if cargarDatosDeBda==False:
                dlg=ctrIntrodDatos_NGeom(self.oUtiles,nomTabla,[clave],mostrarBttNuevo=False,dicValoresAdd=dicValoresAdd,geomWkt=geomWkt,esMulti=esMulti)
                dlg.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
                dlg.set_dxf_featureId(dxf_featureId=dic.get("featureId"))
            else:
                dlg=ctrIntrodDatos_NGeom(self.oUtiles,nomTabla,[clave],mostrarBttNuevo=False,dicValoresAdd=dicValoresAdd, geomWkt=None,esMulti=False)
                dicCond=self.oUtiles.oUtilidadesQgs.get_attrElementoCapa(objeto, capa, listaCampos=["gid"],geom=False)
                dicCond=self.oUtiles.oUtilidades.eliminaEltosDicLClaves(dicCond,listaClaves=["featureId"],genError=True)
                if isinstance(dicCond,Exception):
                    QtGui.QMessageBox.information(self,"Error eliminando condiciones" , dicCond.message,1)
                    return                    
                resp=dlg.setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones=dicCond)
                if isinstance(resp,Exception):
                    QtGui.QMessageBox.information(self,"Error cargando los elementos interiores" , resp.message,1)
                    return
            dicFormularios[clave]=dlg
        else:
            if "dxf_" in nomCapaDXF:
                capa.setSelectedFeatures([dicFormularios.get(clave).get_dxf_featureId()])
                dicFormularios.get(clave).geomWkt=geomWkt#actualiza la geometria
            else:
                capa.setSelectedFeatures([dicFormularios.get(clave).get_featureId()])
            dicFormularios.get(clave).exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialog
            capa.removeSelection()
        self.cambiaAparienciaOpTreeView(index,dicFormularios.get(clave))

    def add_acta_deslinde(self,index):
        """
        Añade un acta de deslinde al linde.
        """
        nomTabla=self.oUtiles.get_nomTabla("actas_deslinde")
        clave=self.saca_clave_padre(index)
        if self.dicActasDeslinde.get(clave)==None:
            gid_linde=self.saca_gid_linde(index)
            if gid_linde==None:
                return
            dicValoresAdd={}
            dicValoresAdd["gid_linde"]=gid_linde
            dirDescargas=["ActaDeslinde",str(gid_linde)]
            #dlg=ctrIntrodDatos_N(self.oUtiles,nomTabla,dirDescargas,False,False,dicValoresAdd)
            dlg=ctrIntrodDatos_N(self.oUtiles,nomTabla,dirDescargas,mostrarBttNuevo=False, dicValoresAdd=dicValoresAdd)
            self.dicActasDeslinde[clave]=dlg
        else:
            dlg=self.dicActasDeslinde.get(clave)
        dlg.exec_()
        self.cambiaAparienciaOpTreeView(index,dlg)

    def add_linde_datos(self,index):
        """
        Añade los datos descriptivos del linde. Los datos se introducen en una de las
        tablas siguientes:
            - linde_replanteado
            - linde_existente
            - linde_proyectado
            - linde_digitalizado
        Ello depende del tipo de linde existente en la tabla linde. Por eso, si se cambia
        el tipo de linde, hay que introducir datos en otra tabla y borrar los de la tabla
        anterior. Esto debe programarse en la bda, en un disparador.
        """
        clave=self.saca_clave_padre(index)
        if self.dicLindes.get(clave)==None:
            return
        dlgDatosLinde=self.dicLindes.get(clave).get_dlgTipoLinde()
        if dlgDatosLinde==None:
            return          
        dlgDatosLinde.exec_()       
        self.cambiaAparienciaOpTreeView(index,self.dicLindes.get(clave).get_dlgTipoLinde())        

    def add_colindantes(self,index):
        """
        Muestra un cuadro de diálogo para añadir los colindantes del linde
        actual.
        """
        nomTabla=self.oUtiles.get_nomTabla("colindantes")
        #saco el gid del linde para que se añada a los colindantes
        gid_linde=self.saca_gid_linde(index)
        if gid_linde == None:
            return  
        dicValoresAdd={}
        dicValoresAdd["gid_linde"]=gid_linde
        listaSubDir=["colindantes",str(gid_linde)]
        #dlg=ctrIntrodDatos_N(self.oUtiles,nomTabla,listaSubDir,False,True,dicValoresAdd)
        dlg=ctrIntrodDatos_N(self.oUtiles,nomTabla,listaSubDir,mostrarBttNuevo=True, dicValoresAdd=dicValoresAdd)
        dlg.exec_()
        self.cambiaAparienciaOpTreeView(index,dlg)

    def saca_gid_linde(self,index):
        """
        Recibe el index de un elemento clicado, obtiene el padre, que es la clave del cuadro
        de diálogo de los datos del linde en dicLindes, y obtiene el gid del linde.
        @return: el gid del linde del elemento clicado, o None, si hay algún problema
        """
        clave=self.saca_clave_padre(index)
        if self.dicLindes.get(clave)==None:
            QtGui.QMessageBox.information(self,"Error" , "La clave del linde " + clave + " no tiene formulario asociado.",1)
            return None
        gid_linde= self.dicLindes.get(clave).dicValoresCompleto.get("gid")
        if gid_linde == None:
            QtGui.QMessageBox.information(self,"Error" , "El linde no tiene GID.",1)
            return  None
        return gid_linde
    def saca_clave_padre(self,index):
        """
        Devuelve el texto del treeview del padre del elemento que se pasa a este método
        """
        hijo=self.datamodel.itemFromIndex(index)
        padre=hijo.parent()
        index2=padre.index()
        datos=index2.data()
        clave= datos#opcion elegida
        return str(clave)
    def ver_clientes(self,index):
        """
        Muestra los clientes de este trabajo.
        Obtiene la condición id_trabajo, crea un diccionario y
        llama a L{ver_varios}. El resultado es que se muestran todos los
        clientes del trabajo actual.
        """
        nomTabla=self.oUtiles.get_nomTabla("comun.clientes")
        dicCondiciones={}
        dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        self.ver_varios(index,nomTabla,dicCondiciones,["clientes"])
    def ver_planos(self,index):
        """
        Muestra los planos de este trabajo.
        Obtiene la condición id_trabajo, crea un diccionario y
        llama a L{ver_varios}. El resultado es que se muestran todos los
        clientes del trabajo actual.
        """
        nomTabla=self.oUtiles.get_nomTabla("comun.planos")
        dicCondiciones={}
        dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        self.ver_varios(index,nomTabla,dicCondiciones,["planos"])
    def ver_documentos_estudiados(self,index):
        """
        Muestra los documentos estudiados de este trabajo.
        Obtiene la condición id_trabajo, crea un diccionario y
        llama a L{ver_varios}. El resultado es que se muestran todos los
        documentos estudiados del trabajo actual.
        """
        nomTabla=self.oUtiles.get_nomTabla("comun.documentos_estudiados")
        dicCondiciones={}
        dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        self.ver_varios(index,nomTabla,dicCondiciones,["doc_est"])

    def ver_propietarios(self,index):
        """
        Muestra los propietarios de la finca de este trabajo.
        Obtiene la condición id_trabajo, crea un diccionario y
        llama a L{ver_varios}. El resultado es que se muestran todos los propietarios
        del la finca actual.
        """
    
        nomTabla=self.oUtiles.get_nomTabla("comun.propietarios")
        dicCondiciones={}
        dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        self.ver_varios(index,nomTabla,dicCondiciones,["propietarios"])
    
    def ver_colindantes(self,index):
        """
        Obtiene las condiciones id_trabajo y el gid del linde, crea un diccionario y
        llama a L{ver_varios}. El resultado es que se muestran todos los colindantes
        del linde clicado.
        """
        #necesito id_trabajo,src,gid_linde

        lista=str(index.data()).split(":")
        i=lista[1]
        nomTabla=self.oUtiles.get_nomTabla("colindantes")
        #saco el gid del linde para que se añada a los colindantes
        clave_linde="Linde:" + str(i)
        gid_linde=self.dicLindes.get(clave_linde).dicValoresCompleto.get("gid")
        dicCondiciones={}
        dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        dicCondiciones["gid_linde"]=gid_linde
        self.ver_varios(index,nomTabla,dicCondiciones,["colindantes"])
    
    def actualizaIMGTreeview(self,indexPadre,nomTabla,dicCondiciones,nomCampo="nom_arch"):
        """
        Realiza una consulta a la tabla nomTabla con las condiciones dicCondiciones,
        elimina todos los hijos del elemento indexPadre y añade hijo por cada registro
        seleccionado. El texto añadido es el del valor del campo nomCampo
        nomTabla es el nombre de la tabla completo ed_ccccc.ed.cccccc
        """
        condicionWhere=self.oUtiles.oConsultasPg.oGeneraExpresionesPsycopg2.generaWhere(dicCondiciones.keys(),"and")
        listaNomCampos=[nomCampo]
        listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nomTabla, listaNomCampos, condicionWhere,dicCondiciones.values())
        
        if isinstance(listaDic, Exception):
            mens=unicode("Error actualizaIMG. El servidor respondió: ","utf-8")
            mens=mens + listaDic.message
            QtGui.QMessageBox.information(self,"Error actualizaIMG",mens ,1)#self es la ventana pasdre que necesita qmessagebox
            return
        self.oUtiles.oUtilidadesFormularios.borra_hijos_treeview(treeView=self.treeview,indexPadre=indexPadre)
        for dic in listaDic:
            nomArch=dic.get(nomCampo)#ya está en utf8
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,indexPadre=indexPadre,texto=nomArch,posicion=None)
        self.ui.treeView.expandAll()

    def ver_varios(self,index,nomTabla,dicCondiciones,listaSubDirDescargas, ver_usuarios=False):
        """
        Muestra un cuadro de diálogo con todos los registros de la tabla nomTabla. La tabla
        no debe tener datos espaciales.
        dicCondiciones es un diccionario nombre_campo:valor, con las condiciones que deben
        cumplir los registros para ser mostrados en el cuadro de diálogo.
        Una vez se acepta el cuadro de diálogo, si se ha seleccionado un registro,
        se muestra en otro cuadrode diálogo, que permite su edición.
        listaSubDirDescargas: ["d1","d2", ...]-->subdirectorio que se creara
        para la descarga de documentos. Se crea a partir de dTrabajos/id_trabajo/
        """
                
        lista=str.split(nomTabla,".")
        esquema=lista[0]
        tabla=lista[1]
        listaNomCampos=self.oUtiles.oConsultasPg.sacaNombresCamposTabla_lista(esquema, tabla)
        listaNomCampos=self.oUtiles.oUtilidadesListas.eliminaEltosLista(listaNomCampos,["geom","archivo"], False)
        if dicCondiciones.__class__.__name__=="dict":
            condicionWhere=self.oUtiles.oConsultasPg.oGeneraExpresionesPsycopg2.generaWhere(dicCondiciones.keys(),"and")
            listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nomTabla, listaNomCampos, condicionWhere,dicCondiciones.values())
        else:
            listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nomTabla, listaNomCampos, condicionWhere=None,listaValoresCondWhere=None)
            
        if isinstance(listaDic, Exception):
            mens=unicode("Error. El servidor respondió: ","utf-8")
            mens=mens + listaDic.message
            QtGui.QMessageBox.information(self,"Error",mens ,1)#self es la ventana pasdre que necesita qmessagebox
        else:
            if len(listaDic)==0:
                mens=unicode("Ningún registro coincide con los criterios elegidos","utf-8")
                QtGui.QMessageBox.information(self,"Error",mens ,1)#self es la ventana pasdre que necesita qmessagebox
                return
            dlgSel=ctrSelec(self, listaDic, self.oUtiles.oUtilidadesFormularios)
            fila=dlgSel.exec_()
            if fila==-1:
                #mens=unicode("Se ha cancelado la selección de un registro","utf-8")
                #QtGui.QMessageBox.information(self,"Error",mens ,1)#self es la ventana pasdre que necesita qmessagebox
                return
            dic=listaDic[fila]
            #oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo=False, dicValoresAdd=None)
            if ver_usuarios==False:
                dlg=ctrIntrodDatos_N(self.oUtiles,nomTabla,listaSubDirDescargas)
            else:
                QtGui.QMessageBox.information(self,"Error" , "Esto no iba a funcionar. dlg=ctrIntrodDatos_NUsuario(self.oUtiles,nomTabla,listaSubDirDescargas). Pongase en contacto con el administrador",1)
                #dlg=ctrIntrodDatos_NUsuario(self.oUtiles,nomTabla,listaSubDirDescargas)
                return
            dlg.setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=dic)
            dlg.exec_()
            if index!=None:
                item=self.datamodel.itemFromIndex(index)
                padre=item.parent()
                self.cambiaAparienciaOpTreeView(padre.index(), dlg)

    def add_finca(self, index):
        """
        Muestra el cuadro de dialogo para añadir una finca. Una vez guardado el cliente,
        permite editarlo.
        """
        
        if self.ctrIntrodDatos_DatFinca==None:
            nomCapaQgis=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"fincas")
            #devuelve dxf_fincas, ed_fincas, fincas o hist_fincas
            
            if nomCapaQgis==None:
                QtGui.QMessageBox.information(self,"Error" , self.creaMensajeCapa(nomCapa="fincas"),1)
                return
            
            capaFinca=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgis)
            if capaFinca==None:
                QtGui.QMessageBox.information(self,"Error" , self.creaMensajeCapa(nomCapa="fincas"),1)
                return
            
            if nomCapaQgis=="dxf_fincas":#en este caso hay que añadir la finca seleccionada.
                tipoGeomCapaQgs=self.oUtiles.oUtilidadesQgs.get_tipoGeomCapa(capaFinca)
                if tipoGeomCapaQgs!="Polygon":
                    QtGui.QMessageBox.information(self,"Error" , "La capa dxf_finca debe ser de tipo Polygon" ,1)
                    return       
                nf = capaFinca.selectedFeatureCount()
                
                if nf==0:
                    QtGui.QMessageBox.information(self,"Error" , "La finca a enviar a la base de datos debe estar seleccionada en la capa dxf_finca.",1)
                    return
                if nf>1:
                    mens=unicode("Hay más de un polígono seleccionado en la capa dxf_finca. Si los poligonos son de la misma finca, conviértalos a un multipolígono con la herramienta: Combinar objetos espaciales seleccionados.")
                    QtGui.QMessageBox.information(self,"Error" , mens,1)            
                    return
                listaObjetos=capaFinca.selectedFeatures()
                objeto=listaObjetos[0]
                listaCampos=[]
                dic=self.oUtiles.oUtilidadesQgs.get_attrElementoCapa(objeto, capaFinca, listaCampos,geom=True)
                capaFinca.setSelectedFeatures([dic.get("featureId")])
                geomWkt=dic.get("geom")
                
                nomTabla=self.oUtiles.get_nomTabla("fincas")

                self.ctrIntrodDatos_DatFinca=ctrIntrodDatos_NFinca(self.oUtiles,nomTabla,["doc_est"],mostrarBttNuevo=False,dicValoresAdd=None, geomWkt=geomWkt,esMulti=True)
                self.ctrIntrodDatos_DatFinca.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
                self.ctrIntrodDatos_DatFinca.set_dxf_featureId(dxf_featureId=dic.get("featureId"))
                estadoGuardado=self.ctrIntrodDatos_DatFinca.getEstadoGuardado()
                if estadoGuardado=="guardado":
                    self.ctrDatosCat=self.ctrIntrodDatos_DatFinca.get_dlgTipoFinca()
                    if self.ctrDatosCat==None:
                        return
    
                #añado la opcion al treeview
                    padre=self.datamodel.itemFromIndex(index)
                    item = QtGui.QStandardItem(self.ctrIntrodDatos_DatFinca.get_tipoFinca())
                    item.setEditable(False)
                    padre.appendRow(item)
                    self.ui.treeView.expandAll()
            else:
                QtGui.QMessageBox.information(self,"Mensaje" , self.toUtf8("La capa DXF_fincas no existe o está desactivada "),1) 
                return
        else:
            nomCapaQgis=self.oUtiles.get_nomCapaQgis("buscar-editar","fincas")
            
            #le cambio el modo para que no devuelva dxf_fincas si ha recargado
            #el trabajo, ya que lo establece des`pues a "nuevo"
            #devuelve dxf_fincas, ed_fincas, fincas o hist_fincas
    
            if nomCapaQgis==None:
                QtGui.QMessageBox.information(self,"Error" , self.creaMensajeCapa(nomCapa="fincas"),1)
                return
            
            capaFinca=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgis)
            if capaFinca==None:
                QtGui.QMessageBox.information(self,"Error" , self.creaMensajeCapa(nomCapa="fincas"),1)
                return
            
            if nomCapaQgis=="dxf_fincas":
                capaFinca.setSelectedFeatures([self.ctrIntrodDatos_DatFinca.get_dxf_featureId()])                
                #no se renueva la geometría cada vez que pulsa add_finca y
                #hay seleccion en dxf_finca
                #self.ctrIntrodDatos_DatFinca.geomWkt=geomWkt
            else:
                capaFinca.setSelectedFeatures([self.ctrIntrodDatos_DatFinca.get_featureId()])
            
            self.ctrIntrodDatos_DatFinca.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
            capaFinca.removeSelection()
            estadoGuardado=self.ctrIntrodDatos_DatFinca.getEstadoGuardado()
            if estadoGuardado=="guardado":
            #por si cambia el tipo de finca de rustica a urbana, esto cambia el texto en el
            #treeview
                padre=self.datamodel.itemFromIndex(index)
                hijo=padre.child(0)
                if hijo==None:
                    self.ctrDatosCat=self.ctrIntrodDatos_DatFinca.get_dlgTipoFinca()
                    if self.ctrDatosCat==None:
                        return
            #añado la opcion al treeview
                    padre=self.datamodel.itemFromIndex(index)
                    item = QtGui.QStandardItem(self.ctrIntrodDatos_DatFinca.get_tipoFinca())
                    item.setEditable(False)
                    padre.appendRow(item)
                    self.ui.treeView.expandAll()
                    hijo=padre.child(0)     
                indice=hijo.index()
                dat=indice.data()
                tipoFinca=str(dat)
                tipo_finca=self.ctrIntrodDatos_DatFinca.get_tipoFinca()
                if tipoFinca!=tipo_finca:
                #hay que cambiar el tipo de linde
                    padre.removeRow(0)
                    item = QtGui.QStandardItem(self.ctrIntrodDatos_DatFinca.get_tipoFinca())
                    item.setEditable(False)
                    padre.appendRow(item)
                    self.ui.treeView.expandAll()
            elif estadoGuardado=="borrado":
                self.oUtiles.oUtilidadesFormularios.borra_hijos_treeview(treeView=self.treeview,indexPadre=index)
                self.cambiaAparienciaOpTreeView(index,self.ctrIntrodDatos_DatFinca)
                self.ctrIntrodDatos_DatFinca=None       
            
        self.cambiaAparienciaOpTreeView(index,self.ctrIntrodDatos_DatFinca)
        
    def add_datosCatFinca(self,index):
        """
        Muestra el cuadro de diálogo para añadir los datos de la referencia catastral
        de la finca. Si la finca es rústica se muestra la tabla ref_cat_rus, y 
        ref_cat_urb, si es urbana. Este cuadro de diálogo se encuentra dentro del cuadro
        de diálogo de la tabla fincas (self.ctrIntrodDatos_DatFinca), y se obtiene con el
        método self.ctrIntrodDatos_DatFinca.get_dlgTipoFinca()
        """
        if self.ctrIntrodDatos_DatFinca==None:
            return
        ctrDatosCat=self.ctrIntrodDatos_DatFinca.get_dlgTipoFinca()
        if ctrDatosCat==None:
            return
        ctrDatosCat.exec_()
        self.cambiaAparienciaOpTreeView(index,ctrDatosCat)
    
    def add_servidumbre(self,index):
        """
        Añade una servidumbre a la finca.
        """
        self.add_datos_BDA_con_geometria(index, "servidumbres", "servidumbres", self.dicServidumbres,self.seleccionServidumbres,True)#es multipoligono

    def add_elemento_interior(self, index):
        """
        Añade un elemento interior a la finca.
        """
        self.add_datos_BDA_con_geometria(index, "elem_interiores", "elem_interiores", self.dicElementoInterior,self.seleccionElementosInteriores,True)#es multipoligono
        clave= str(index.data())
        lista=clave.split(":")
        estadoGuardado=self.dicElementoInterior.get(clave).getEstadoGuardado()
        if estadoGuardado=="borrado":
            self.oUtiles.oUtilidadesFormularios.borra_hijos_treeview(self.treeview,index)
        elif estadoGuardado=="guardado":
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,"Add img elto interior:" + lista[1])
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index,"Ver img elto interior:" + lista[1])
        self.cambiaAparienciaOpTreeView(index, self.dicElementoInterior.get(clave))
    
    def add_parcela_afectada(self,index):
        """
        Añade una parcela afectada.
        """
        self.add_datos_BDA_con_geometria(index, "parcelas_afectadas", "parcelas_afectadas", self.dicParcelasAfectadas,self.seleccionParcelasAfectadas,True)#es multipoligono
        clave= str(index.data())
        lista=clave.split(":")
        estadoGuardado=self.dicParcelasAfectadas.get(clave).getEstadoGuardado()
        if estadoGuardado=="borrado":
            self.oUtiles.oUtilidadesFormularios.borra_hijos_treeview(self.treeview,index)
        self.cambiaAparienciaOpTreeView(index, self.dicParcelasAfectadas.get(clave))
        
    def add_linde(self,index):
        """
        Añade un linde a la base de datos. Los lindes se numeran del 0 al N.
        El cuadro de diálogo de cada linde se añade al diccionario self.dicLindes.
        Las claves de este diccionario son Linde1, Linde2 .... LindeN.
        Dentro de cada cuadro de diálogo hay una referencia a otro cuadro de diálogo (B),
        con los datos del tipo de linde. Este cuadro de diálogo se obtiene con el método
        get_dlgLindeTipoLinde(), del linde actual, es decir 
        B=self.dicLindes.get(lindeActual).get_dlgLindeTipoLinde().
        B tiene el método B.get_tipoLinde(), que devuelve:
            - Replanteado
            - Digitalizado
            - Existente
            - Proyectado
        Este texto es añadido al treeview, como hijo del linde actual, para poder acceder
        al cuadro de diálogo de los datos del tipo de linde, mediante el método
        self.add_linde_datos. Este método es llamado desede self.dobleClicadoTreeview,
        cuando el usuario hace doble click sobre, la opción Replanteado, Digitalizado, ...
        
        Añade, como hijo del linde actual, una opcion "Colindantes", que permite añadir 
        los colindantes al linde. Para ello se ejecuta add_colindantes. Este método es llamado desede self.dobleClicadoTreeview,
        cuando el usuario hace doble click sobre la opción Colindantes del treeview.
        
        También añade, como hijo del linde actual, una opcion "Ver colindantes", que permite ver y editar
        los colindantes del linde añadidos anteriormente. Para ello se ejecuta ver_colindantes. 
        Este método es llamado desede self.dobleClicadoTreeview,
        cuando el usuario hace doble click sobre la opción Ver colindantes del treeview.
        """
        geomWkt=None
        datos=index.data()
        op= str(datos)
        lista=op.split(":")#De 'Linde:1' devuelve ['Linde','1']
        i=int(lista[1])#numero de elemento
        clave="Linde:" + str(i)
        #capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre("dxf_lindes")
        #if capa==None:
        #    QtGui.QMessageBox.information(self,"Aviso" , "La capa dxf_lindes no existe o esta desactivada.",1)
        #    return

        nomCapa=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"lindes")
        if nomCapa==None:
            QtGui.QMessageBox.information(self,"Aviso en los lindes a" ,self.creaMensajeCapa("lindes"),1)
            return
        capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapa)
        if capa==None:
            QtGui.QMessageBox.information(self,"Aviso en los lindes b" ,self.creaMensajeCapa("lindes"),1)
            return
        
        if nomCapa=="dxf_lindes":
            objeto=self.seleccionLindes[i]
            if objeto.geometry().isGeosValid()==False:
                QtGui.QMessageBox.information(self,"Error" ,self.toUtf8("La geometría de este linde no es válida."),1)
                return
            listaCampos=[]
            dic=self.oUtiles.oUtilidadesQgs.get_attrElementoCapa(objeto, capa, listaCampos,geom=True)
            oQset=[]
            oQset.append(dic.get("featureId"))
            capa.setSelectedFeatures(oQset)#deselecciona todo
            #y selecciona el punto actual
            geomWkt=dic.get("geom")
        
        if self.dicLindes.get(clave)==None:
            if geomWkt==None:
                QtGui.QMessageBox.information(self,"Error","Vuelva a seleccionar al menos un linde de la finca" ,1)
                return
            nomTabla=self.oUtiles.get_nomTabla("lindes")
            dicValoresAdd={}
            dicValoresAdd['gid_finca']=self.oUtiles.gid_finca
            #oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo=False,dicValoresAdd=None, geomWkt=None,esMulti=False
            dlgLinde=ctrIntrodDatos_NLinde(self.oUtiles,nomTabla,["lindes"],mostrarBttNuevo=False,dicValoresAdd=dicValoresAdd,geomWkt=geomWkt,esMulti=False)
            dlgLinde.exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
            dlgLinde.set_dxf_featureId(dxf_featureId=oQset[0])
            self.dicLindes[clave]=dlgLinde
            estado=dlgLinde.getEstadoGuardado()
            if estado!="guardado":
                self.dicLindes[clave]=None
                return
            self.dicLindes.get(clave).set_tipoLinde()
            self.dicLindes.get(clave).set_dlgTipoLinde(cargarDatosDeBda=False)
            dlgDatosLinde=self.dicLindes.get(clave).get_dlgTipoLinde()
            if dlgDatosLinde==None:
                QtGui.QMessageBox.information(self,"Error" , "Hubo un problema con el tipo de linde.",1)
                self.dicLindes[clave]=None
                return
            texto=str(dlgLinde.get_tipoLinde()) + ":" + str(i)
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, texto)
            texto="Acta deslinde:" + str(i)
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, texto)           
            texto="Add colindantes:" + str(i)
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, texto)
            texto="Ver colindantes:" + str(i)
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, texto)
            texto="Add imagenes linde:" + str(i)
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, texto)
            texto="Ver imagenes linde:" + str(i)
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, texto)            
        else:
            
            if nomCapa=="dxf_lindes":#el id almacenado en el cuadro de dialog es el de la tabla ed_srcXXXXX.ed_lindes
                capa.setSelectedFeatures([self.dicLindes.get(clave).get_dxf_featureId()])            
                self.dicLindes.get(clave).geomWkt=geomWkt
            else:
                capa.setSelectedFeatures([self.dicLindes.get(clave).get_featureId()])
            self.dicLindes.get(clave).exec_()#detiene la ejecucion hasta que se cierre el cuadro de dialogo
            capa.removeSelection()
            estado=self.dicLindes.get(clave).getEstadoGuardado()
            if estado=="borrado":
                self.oUtiles.oUtilidadesFormularios.borra_hijos_treeview(treeView=self.treeview,indexPadre=index)
                self.cambiaAparienciaOpTreeView(index,self.dicLindes.get(clave))
                self.dicLindes[clave]=None
                return
            #esto lo hago por si cambia el tipo de linde
            padre=self.datamodel.itemFromIndex(index)
            hijo=padre.child(0)
            indice=hijo.index()
            dat=indice.data()
            tipoLinde=str(dat).split(":")[0]
            tipo_linde=self.dicLindes.get(clave).get_tipoLinde()
            if tipoLinde!=tipo_linde:
                #hay que cambiar el tipo de linde
                padre.removeRow(0)
                texto=str(self.dicLindes.get(clave).get_tipoLinde())+ ":" + str(i)
                self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, texto,0)
 
        self.cambiaAparienciaOpTreeView(index,self.dicLindes.get(clave))

    def add_img_linde(self,index):
        """
        Añade las imágenes seleccionadas al linde.
        """
        #if self.imagenesAnyadidasTreeWiew==True:#no hace falta porque no pude duplicar imagenes
        #    QtGui.QMessageBox.information(self,"Aviso" , self.toUtf8("Todas las imágenes han sido ya cargadas de la BDA. Si desea añadir imágenes a un linde, seleccione el linde, en la capa dxf_lindes y elija la opción Buscar-editar->Recargar trabajo") ,1)
        #    return    
        
        nomCapaQgis=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,"imagenes")
        if nomCapaQgis==None:
            QtGui.QMessageBox.information(self,"Error" ,self.toUtf8("La capa dxf_imagenes no existe, o esta desactivada, o no tiene seleccionado ningún punto" ),1)
            return              
        tipoGeomCapaQgs=self.oUtiles.oUtilidadesQgs.get_tipoGeomNomCapa(nomCapaQgis)
        if isinstance(tipoGeomCapaQgs,Exception):
            QtGui.QMessageBox.information(self,"Error" ,tipoGeomCapaQgs.message ,1)
            return              
        if tipoGeomCapaQgs!="Point":
            QtGui.QMessageBox.information(self,"Error" , "La capa " + nomCapaQgis + " debe ser de tipo Point" ,1)
            return  
        gid_linde=self.saca_gid_linde(index)
        if gid_linde==None:
            return
        dirImgEntrada=self.oUtiles.dTrabajos + "/edicion/" + str(self.oUtiles.id_trabajo) + "/lindes/imagenes" 

        if not(os.path.isdir(dirImgEntrada)):
            listaSubDir=["edicion",str(self.oUtiles.id_trabajo),"lindes","imagenes"]
            resp=self.oUtiles.oUtilidades.creaDir(self.oUtiles.dTrabajos,listaSubDir,True)
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Error" , "No se ha podido crear el directorio para las imagenes de los lindes " + dirImgEntrada + ". Cree el directorio Ud. mismo y vuelva a probar.",1)
                return
            else:
                QtGui.QMessageBox.information(self,"Mensaje" , "Se ha creado el directorio " + dirImgEntrada + ". Debe copiar dentro las imagenes (png,jpg) de los lindes. El nombre de la imagen debe coincidir con el del campo Text de la tabla de atributos de la capa dxf_imagenes.",1)
                return                   
        dirImgSalida=self.oUtiles.dTrabajos + "/edicion/" + str(self.oUtiles.id_trabajo) + "/lindes/imagenes/" + str(gid_linde) 
        if not(os.path.isdir(dirImgSalida)):
            listaSubDir=["edicion",str(self.oUtiles.id_trabajo),"lindes","imagenes",str(gid_linde)]
            resp=self.oUtiles.oUtilidades.creaDir(self.oUtiles.dTrabajos,listaSubDir,True)
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Error" , "No se ha podido crear el directorio para las imagenes de los lindes " + dirImgSalida + ". Cree el directorio Ud. mismo y vuelva a probar.",1)
                return

        nomTabla=self.oUtiles.get_nomTabla("img_linde")
        #listaCampos=["id_trabajo", "id_linde", "nom_imagen","imagen", "geom"]
        oArchivos=pyUPVBib.pyPgGas.Archivos()
        listaCamposQgis=["Text"]
        try:
            listaDic=self.oUtiles.oUtilidadesQgs.get_attrSeleccionCapa(nomCapaQgis, listaCamposQgis,True)
        except Exception,e:
            QtGui.QMessageBox.information(self,"Error" , e.message,1)
            return
        n=len(listaDic)
        if n==0:
            QtGui.QMessageBox.information(self,"Error" , "No hay puntos seleccionados en la capa " + nomCapaQgis,1)
            return
        for dic in listaDic:
            geomWkt=dic.get("geom")
            if geomWkt is None:
                QtGui.QMessageBox.information(self,"Mensaje", "Los puntos de la capa " + nomCapaQgis + " deben estar seleccionados y visibles",1)
                return
            nomImagen=dic.get("Text")
            imgEntrada=dirImgEntrada +  "/" + nomImagen
            imgSalida=dirImgSalida + "/" + nomImagen
            
            #nuevo
            #como PIL no funciona, de momento hago una copia de la imagen, si ocupa menos de 200000 bites
            #resp=oArchivos.cambiaTamanoImagen(imgEntrada,imgSalida,self.oUtiles.tam_img_kb)
            if not(os.path.isfile(imgEntrada)):
                QtGui.QMessageBox.information(self,"Mensaje", "El archivo de imagen " + imgEntrada + " no existe" ,1)
                return
            
            if os.path.getsize(imgEntrada)>(self.oUtiles.tam_img_kb *1000):
                QtGui.QMessageBox.information(self,"Mensaje", "El archivo de imagen " + imgEntrada + " ocupa mas de " + str(self.oUtiles.tam_img_kb) +" Kb" ,1)
                return
            
            imgSalida=imgEntrada
            #fin de lo nuevo
            """
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Mensaje", resp.message,1)
                return
            """
            
            img=oArchivos.leeDatBinarios(imgSalida)
            if isinstance(img,Exception):
                QtGui.QMessageBox.information(self,"Mensaje", img.message,1)
                return
            listaNomCampos=["id_trabajo","gid_linde","nom_arch","geom","archivo","descripcion"]
            listaValores=[self.oUtiles.id_trabajo, gid_linde, nomImagen, geomWkt, img,"imagen"]
            #(self,nombreTabla,listaCampos, listaValores,nombreCampoBytea=None, esMulti=False, nombreCampoGeom=None, epsg=None, returning=None)
            r=self.oUtiles.oConsultasPg.insertaDatos(nomTabla,listaNomCampos, listaValores,"archivo", False, "geom",self.oUtiles.src_trabajo )
            if isinstance(r,Exception):
                QtGui.QMessageBox.information(self,"Error", r.message,1)
                return
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, nomImagen)
            
    def ver_img_linde(self,index):
        """
        Muestra un cuadro de diálogo con una lista con las imágenes del linde.
        Si se elige un registro, se puede editar, borrar ...
        """
        nomTabla=self.oUtiles.get_nomTabla("img_linde")
        clave=self.saca_clave_padre(index)
        dlgImgLinde=self.dicLindes.get(clave)
        if dlgImgLinde==None:
            return
        gid_linde=dlgImgLinde.dicValoresCompleto.get("gid")
        dicCondiciones={}
        dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        dicCondiciones["gid_linde"]=gid_linde
        listaSubDir=["imagenes",str(gid_linde)]
        self.ver_varios(index,nomTabla,dicCondiciones,listaSubDir)
        
        itemActual=self.datamodel.itemFromIndex(index)
        fila=itemActual.row()
        padre=itemActual.parent()
        itemAddImg=padre.child(fila-1)
        self.actualizaIMGTreeview(itemAddImg.index(),nomTabla,dicCondiciones)
        
    def add_img_elto_interior(self,index):
        """
        Añade una o varias imágenes al elemento interior actual.
        """
        nomTabla=self.oUtiles.get_nomTabla("img_elem_int")
        clave=self.saca_clave_padre(index)
        dlgEltoInt=self.dicElementoInterior.get(clave)
        if dlgEltoInt==None:
            return
        gid_elto_interior=dlgEltoInt.dicValoresCompleto.get("gid")
        dicValoresAdd={}
        dicValoresAdd["gid_elem_int"]=gid_elto_interior
        dirDescargas=["Elem_interior", str(gid_elto_interior)]
        #oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo=False, dicValoresAdd=None):
        dlg=ctrIntrodDatos_N(self.oUtiles,nomTabla,dirDescargas,mostrarBttNuevo=True,dicValoresAdd=dicValoresAdd)
        dlg.exec_()
        self.cambiaAparienciaOpTreeView(index,dlg)
        
        dicCondiciones={}
        dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        dicCondiciones["gid_elem_int"]=gid_elto_interior
        self.actualizaIMGTreeview(index,nomTabla,dicCondiciones)
        
    def ver_img_elto_interior(self, index):
        """
        Muestra una lista con las imágenes del elemento interior.
        """
        nomTabla=self.oUtiles.get_nomTabla("img_elem_int")
        clave=self.saca_clave_padre(index)
        dlgEltoInt=self.dicElementoInterior.get(clave)
        if dlgEltoInt==None:
            return
        gid_elto_interior=dlgEltoInt.dicValoresCompleto.get("gid")
        dicCondiciones={}
        dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        dicCondiciones["gid_elem_int"]=gid_elto_interior
        listaSubDir=["Elem_interior",str(gid_elto_interior)]
        self.ver_varios(index,nomTabla,dicCondiciones,listaSubDir)
        
        itemActual=self.datamodel.itemFromIndex(index)
        fila=itemActual.row()
        padre=itemActual.parent()
        itemAddImg=padre.child(fila-1)
        self.actualizaIMGTreeview(itemAddImg.index(),nomTabla,dicCondiciones)
    def add_lindes_treeview(self,index):
        """
        Cuando el usuario presiona sobre Datos de los lindes, se busca, en la capa
        dxf_lindes, el número de lindes. Se genera una opción en el treeview, que cuelga de 
        Datos de los lindes, para cada linde.
        """                       
        if self.oUtiles.gid_finca == None or self.oUtiles.gid_finca == '':
            QtGui.QMessageBox.information(self,'Primero debe añadir una finca' , 'Primero debe añadir una finca',1)
            return
        
        lindes=self.add_elementos_treeview(index, nomCapa="lindes",tipoGeomCapa="Line", nombreItems="Linde")
        if isinstance(lindes,Exception):
            QtGui.QMessageBox.information(self,"Error" , lindes.message,1)
            return 
        self.lindesAnyadidosTreeView=True
        self.seleccionLindes = lindes   
    
    def add_parcelas_afectadas_treeview(self,index):
        """
        Cuando el usuario presiona sobre Parcelas afectadas, se busca, en la capa
        dxf_parcelas_afectadas, el número de parcelas. Se genera una opción en el treeview, que cuelga de 
        Parcelas afectadas, para cada parcela.
        
        Estas son las parcelas a mofificar en catastro al actualizar la forma de la finca.
        Se usan solo para el gml que hay que enviar al catastro
        """                       
    
        parcelas=self.add_elementos_treeview(index, nomCapa="parcelas_afectadas",tipoGeomCapa="Polygon", nombreItems="Parcela afectada")
        if isinstance(parcelas,Exception):
            QtGui.QMessageBox.information(self,"Error" , parcelas.message,1)
            return 
        self.parcelasAnyadidasTreeView=True
        self.seleccionParcelasAfectadas = parcelas   
    
    def add_elementos_interiores_treeview(self,index):
        """
        La documentación es la misma que la de L{add_servidumbres_treeview}, con la capa
        dxf_elem_interiores.
        """
        
        if self.oUtiles.gid_finca == None or self.oUtiles.gid_finca == '':
            QtGui.QMessageBox.information(self,'Primero debe añadir una finca' , 'Primero debe añadir una finca',1)
            return  
        
        ei=self.add_elementos_treeview(index, nomCapa="elem_interiores",tipoGeomCapa="Polygon", nombreItems="Elemento interior")
        
        if isinstance(ei,Exception):
            QtGui.QMessageBox.information(self,"Error" , ei.message,1)
            return 
        self.elementosInterioresAnyadidosTreeView=True
        self.seleccionElementosInteriores = ei

    def add_servidumbres_treeview(self,index):
        """
        Busca en la capa dxf_servidumbres y añade un elemento al treeview por cada elemento.
        Los elementos añadidos al treeview se numeran. Cada elemento se usarça como clave
        para un diccionario clave:formulario, que apunta la formulario con el que se han
        introducido los datos de cada elemento en la base de datos. Usa L{add_elementos_treeview}.
        """
        if self.oUtiles.gid_finca == None or self.oUtiles.gid_finca == '':
            QtGui.QMessageBox.information(self,'Primero debe añadir una finca' , 'Primero debe añadir una finca',1)
            return 
        
        servidumbres=self.add_elementos_treeview(index, nomCapa="servidumbres",tipoGeomCapa="Polygon", nombreItems="Servidumbre")
        if isinstance(servidumbres,Exception):
            QtGui.QMessageBox.information(self,"Error" , servidumbres.message,1)
            return 
        self.servidumbresAnyadidosTreeView=True
        self.seleccionServidumbres = servidumbres
          
    def add_elementos_treeview(self,index,nomCapa,tipoGeomCapa,nombreItems):
        """
        Selecciona todos los elementos de la capa capa, y añade un enlace en el treeview
        para cada elemento. El padre de todos es el elemento index. El nombre de los
        elementos añadidos es nombreItems:Numero, donde Numero es el numero de elemento.
        @return: los elementos seleccionados de la capa.
        """  
        nomCapaQgis=self.oUtiles.get_nomCapaQgis(self.opcionMenuElegida,nomCapa)      
        if nomCapaQgis==None:
            mens=self.creaMensajeCapa(nomCapa)
            return Exception(mens)
        if self.opcionMenuElegida=="nuevo":
            if not ("dxf_" in nomCapaQgis):
                return Exception(self.toUtf8("Para añadir elementos geográficos, debe seleccionar objetos en una capa cuyo nombre comience por dxf_"))
        capa=self.oUtiles.oUtilidadesQgs.get_capa_nombre(nomCapaQgis)
        if capa==None:
            return Exception("La capa " + nomCapaQgis + " esta desactivada o no existe.")
        nf = capa.selectedFeatureCount()
        if nf==0:
            return Exception("La capa " + nomCapaQgis + " debe tener los elementos a enviar a la base de datos  seleccionados.")           
        tipoGeomCapaQgs=self.oUtiles.oUtilidadesQgs.get_tipoGeomCapa(capa)
        if tipoGeomCapaQgs!=tipoGeomCapa:
            return Exception("La capa " + nomCapaQgis + "debe ser de tipo " + tipoGeomCapa)
        for i in range(nf):
            nombre=nombreItems + ":" + str(i)
            self.oUtiles.oUtilidadesFormularios.add_hijo_treeview(self.treeview,index, nombre)
        return capa.selectedFeatures()
  
    def add_hijo_treeview(self,indexPadre,texto,posicion=None):
        """
        Añade un hijo al elemento del treeview cuyo índice es indexPadre.
        El parámetro texto se usa como texto del nuevo elemento.
        Si el padre tiene un hijo con el mismo texto no lo añade.
        """
        padre=self.datamodel.itemFromIndex(indexPadre)
        n=padre.rowCount()
        for i in range(n):
            item=padre.child(i)
            existente=str(item.text())
            if existente==texto:
                return
        item = QtGui.QStandardItem(texto)
        item.setEditable(False)
        if posicion!=None:
            padre.insertRow (posicion,item)
        else:
            padre.appendRow(item)
        self.ui.treeView.expandAll()

    def opAcercaDe(self):
        """
        Muestra el cuadro de diálogo Acerca de.
        """
        dlg=ctrAcercaDe()
        dlg.exec_()
    
    def compExisteTrabActual(self):
        """
        Devuelve true o false, en función de si hay trabajo actual o no.
        """
        if self.oUtiles.src_trabajo!=None and self.oUtiles.id_trabajo!=None and self.oUtiles.usuario_creador_trabajo!=None and self.oUtiles.municipio!=None:
            return True
        else:
            QtGui.QMessageBox.information(self,"Mensaje" , "No hay trabajo actual",1)
            return False
        
    def toUtf8(self,mens):
        """
        Transforma en utf-8 la cadena mens y la retorna.
        """
        return unicode(mens,"utf-8")

    def creaMensajeCapa(self,nomCapa):
        """
        Crea un mensaje indicando que no existe una capa, o que no se cumplen determinadas condiciones
        con la capa.
        """
        cad1=self.toUtf8("Problema: Ninguna de las capas ")
        cad2=self.toUtf8("dxf_" + nomCapa + ", ed_" + nomCapa + ", " + nomCapa + ", hist_" + nomCapa)
        cad3=self.toUtf8(" existe. Para ser detectada, tambien debe estar activada. Si desea añadir elementos de DXF, además, debe primero seleccionar los elementos a añadir de la capa dxf_" + nomCapa)
        mens=cad1 + cad2 + cad3
        return mens
        
    def cambiaAparienciaOpTreeView(self,index,dlg):
        """
        Cambia la fuente del treeview. 
        La fuente indica si se han introducido datos en la tabla y si hay cambios sin guardar:
            - Si no ha guardado ni hecho cambios en el cuadro de dialogo: normal (sin negrita, ni italica)
            - Si ha hecho cambios en cl cuadro y no ha guardado ni una vez: sin negrita, italica 
            - Si los ultimos cambios en el cuadro de dialogo se guardaron: negrita, sin italica
            - Si esta salvado una vez, pero hay cambios en el cuadro de dialogo sin salvar: negrita, italica.
        """
        item=self.datamodel.itemFromIndex(index)
        font=item.font()
        if dlg==None:
            font.setBold(False)
            font.setItalic(False)
        elif dlg.getEstadoGuardado()=="guardado":
            #Ha guardado por lo menos una vez
                #poner en negrita
            font.setBold(True)
            if dlg.getTablaCambiada()==False:
                #Esta todo salvado. Poner negrita normal
                font.setItalic(False)
            else:
                #poner negrita cursiva
                font.setItalic(True)
        elif dlg.getEstadoGuardado()=="borrado":
            font.setBold(False)
            font.setItalic(False)
        else:
            #No ha guardado ninguna vez
            if dlg.getTablaCambiada()==True:
                #Ha hecho cambios.
                #poner en cursiva
                font.setItalic(True)
        item.setFont(font)
    
    def closeEvent(self, event):
        pass
        """
        Evento que permite abrir una
        ventana de dialogo para confirmar la salida del programa
        """
        #Se genera la respuesta de la confirmacion de salir
        #self.oUtiles.oConectaPg.cierraConexion()
        """
        mens=unicode("¿Seguro que desea salir?","utf-8")
        reply = QtGui.QMessageBox.question(self, "Mensaje", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.oUtiles.oConectaPg.cierraConexion()
            event.accept()
        else:
            event.ignore()
        """
