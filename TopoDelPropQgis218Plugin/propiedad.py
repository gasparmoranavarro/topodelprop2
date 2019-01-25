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

from PyQt4 import QtCore, QtGui
from qgis.core import *
import qgis.utils
import sys
# Initialize Qt resources from file resources.py
import resources
# Importo el dialogo principal
from ctr.ctrPpal import ctrPpal
from ctr.ctrMuestraImgLinde import ctrMuestraImgLinde
from ctr.ctrMuestraImgEI import ctrMuestraImgEI
import TopoDelProp.utilsPropiedad.utils
#Esto es para de depuración

import sys

"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""

class clsPropiedad:

    def __init__(self, iface):
        """
        Constructor
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.inicializado=False
        self.oUtiles=None
        self.dlgPPal=None

            
    def initGui(self):
        # Create action that will start plugin configuration
        
        self.actionConectar = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/conectar.png"),"Conectar", self.iface.mainWindow())
        self.actionDesconectar = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/desconectar.png"),"Desconectar", self.iface.mainWindow())
        self.actionTrabajos = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/trabajos.png"),"Trabajos", self.iface.mainWindow())
        self.actionCargarTrabajo = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/cargaTrabajo.png"),"Cargar los datos del trabajo de un elemento seleccionado", self.iface.mainWindow())
        self.actionCargarEdicion = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/cargaCapasEd.png"),"Cargar capas edicion", self.iface.mainWindow())
        self.actionCargarDefinitivas = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/cargaCapasDef.png"),"Cargar capas definitivas", self.iface.mainWindow())
        self.actionAddImagen = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/imagenes.png"),"Ver imagenes de los lindes", self.iface.mainWindow())
        self.actionImgEI = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/imgEI.png"),"Ver imagenes de elementos interiores", self.iface.mainWindow())
        self.actionAyuda = QtGui.QAction(QtGui.QIcon(":/plugins/TopoDelProp/iconos/ayuda.png"),"Ayuda", self.iface.mainWindow())
 
        # connect the action to the run method
        
        QtCore.QObject.connect(self.actionConectar, QtCore.SIGNAL("triggered()"), self.conectar)
        QtCore.QObject.connect(self.actionDesconectar, QtCore.SIGNAL("triggered()"), self.desconectar)
        QtCore.QObject.connect(self.actionTrabajos, QtCore.SIGNAL("triggered()"), self.muestraFrmPPal)
        QtCore.QObject.connect(self.actionCargarTrabajo, QtCore.SIGNAL("triggered()"), self.cargarTrabajo)
        QtCore.QObject.connect(self.actionCargarEdicion, QtCore.SIGNAL("triggered()"), self.cargarEdicion)
        QtCore.QObject.connect(self.actionCargarDefinitivas, QtCore.SIGNAL("triggered()"), self.cargarDefinitivas)
        QtCore.QObject.connect(self.actionAddImagen, QtCore.SIGNAL("triggered()"), self.muestraImagenes)
        QtCore.QObject.connect(self.actionImgEI, QtCore.SIGNAL("triggered()"), self.muestraImagenesEI)
        QtCore.QObject.connect(self.actionAyuda, QtCore.SIGNAL("triggered()"), self.ayuda)

        # Add toolbar button
        self.iface.addToolBarIcon(self.actionConectar)
        self.iface.addToolBarIcon(self.actionDesconectar)
        self.iface.addToolBarIcon(self.actionTrabajos)
        self.iface.addToolBarIcon(self.actionCargarTrabajo)
        self.iface.addToolBarIcon(self.actionCargarEdicion)
        self.iface.addToolBarIcon(self.actionCargarDefinitivas)
        self.iface.addToolBarIcon(self.actionAddImagen)
        self.iface.addToolBarIcon(self.actionImgEI)
        self.iface.addToolBarIcon(self.actionAyuda)
        #Add to menu Complementos
        self.iface.addPluginToMenu("&TopoDelProp", self.actionConectar)
        self.iface.addPluginToMenu("&TopoDelProp", self.actionDesconectar)
        self.iface.addPluginToMenu("&TopoDelProp", self.actionTrabajos)
        self.iface.addPluginToMenu("&TopoDelProp", self.actionCargarTrabajo)
        self.iface.addPluginToMenu("&TopoDelProp", self.actionCargarEdicion)
        self.iface.addPluginToMenu("&TopoDelProp", self.actionCargarDefinitivas)
        self.iface.addPluginToMenu("&TopoDelProp", self.actionAddImagen)
        self.iface.addPluginToMenu("&TopoDelProp", self.actionImgEI)
        self.iface.addPluginToMenu("&TopoDelProp", self.actionAyuda)
        
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&TopoDelProp",self.actionConectar)
        self.iface.removePluginMenu("&TopoDelProp",self.actionDesconectar)
        self.iface.removePluginMenu("&TopoDelProp",self.actionCargarEdicion)
        self.iface.removePluginMenu("&TopoDelProp",self.actionTrabajos)
        self.iface.removePluginMenu("&TopoDelProp",self.actionCargarTrabajo)
        self.iface.removePluginMenu("&TopoDelProp",self.actionCargarDefinitivas)
        self.iface.removePluginMenu("&TopoDelProp",self.actionAddImagen)
        self.iface.removePluginMenu("&TopoDelProp",self.actionImgEI)
        self.iface.removePluginMenu("&TopoDelProp",self.actionAyuda)
        self.iface.removeToolBarIcon(self.actionConectar)
        self.iface.removeToolBarIcon(self.actionDesconectar)
        self.iface.removeToolBarIcon(self.actionCargarEdicion)
        self.iface.removeToolBarIcon(self.actionTrabajos)
        self.iface.removeToolBarIcon(self.actionCargarTrabajo)
        self.iface.removeToolBarIcon(self.actionCargarDefinitivas)
        self.iface.removeToolBarIcon(self.actionAddImagen)
        self.iface.removeToolBarIcon(self.actionImgEI)
        self.iface.removeToolBarIcon(self.actionAyuda)
        
    def conectar(self):
        """
        Conecta con la base de datos. Si lo consigue, inicializa el objeto oUtiles
        """
        
        if self.inicializado==True:
            self.oUtiles.oConectaPg.cierraConexion()
            self.inicializado=False
        self.inicializa()
        
    def desconectar(self):
        """
        Cierra la conexión con la base de datos.
        """
        #settrace()
        a=25
        if self.inicializado==True:
            self.oUtiles.oConectaPg.cierraConexion()
            self.inicializado=False
            if self.dlgPPal!=None:
                self.dlgPPal.close()
                self.dlgPPal=None
            QtGui.QMessageBox.information(self.iface.mainWindow(),"Mensaje", "Desconectado",1)
    # run method that performs all the real work
    def cargarTrabajo(self):
        """
        Si hay seleccionado un objeto, y tiene un campo id_trabajo, se carga todo el trabajo
        en el formulario ppal de la aplicación
        """
        # create and show the dialog principal
        self.inicializa()
        if self.inicializado==False:
            return
        layer=self.oUtiles.iface.activeLayer()
        if layer==None:
            QtGui.QMessageBox.information(self.iface.mainWindow(),"Error" , "Debe activar una capa y seleccionar un elemento espacial",1)
            return
        nf = layer.selectedFeatureCount()
        if nf==0:
            QtGui.QMessageBox.information(self.iface.mainWindow(),"Error" , "Debe haber un objeto seleccionado en la capa activa.",1)
            return
        if nf>1:
            mens=unicode("Hay más de un objeto seleccionado en la capa activa.","utf-8")
            QtGui.QMessageBox.information(self.iface.mainWindow(),"Error" , mens,1)            
            return
        listaObjetos=layer.selectedFeatures()
        objeto=listaObjetos[0]
        listaCampos=["id_trabajo"]
        try:
            dic=self.oUtiles.oUtilidadesQgs.get_attrElementoCapa(objeto, layer, listaCampos,geom=False)
        except Exception,e:
            QtGui.QMessageBox.information(self.iface.mainWindow(),"Error" , e.message,1)            
            return
        id_trabajo=dic.get("id_trabajo")
        prefijo=layer.name()[:3]#tres primeros caracteres
        if prefijo=="ed_":
            tipo_trabajo="Edicion"
        elif prefijo=="his":
            tipo_trabajo="Historico"
        else:
            tipo_trabajo="Definitivo"
        if tipo_trabajo=="Definitivo":
            if self.oUtiles.tipo_usuario=="editor":
                QtGui.QMessageBox.information(self.iface.mainWindow(),"Error" , "Un usuario editor no tiene permiso para cargar datos de un trabajo en el nivel definitivo",1)            
                return                
        if self.dlgPPal==None:
            self.dlgPPal = ctrPpal(self.oUtiles)
        #settrace()
        self.dlgPPal.cargaDatoTrabajo2(id_trabajo=id_trabajo, tipo_trabajo=tipo_trabajo)
        self.dlgPPal.show()
    
    def salvaTrabajoArchivo(self):
        """
        Salva el trabajo actual a un archivo, para ser guardado en otra base de datos
        """
        pass
    
    def cargarTrabajoArchivo(self):
        """
        Carga en trabajo de un archivo
        """
        pass
        
    def muestraFrmPPal(self):
        """
        Muestra el formulario ppal de la aplicación.
        """
        # create and show the dialog principal
        self.inicializa()
        if self.inicializado==False:
            return
        if self.dlgPPal==None:
            self.dlgPPal = ctrPpal(self.oUtiles)
        self.dlgPPal.show()
        #self.inicializado=False#cada vez que el usuario cierra el formulario ppal, debe volver a conectarse de nuevo.
#        dlg.exec_()
#        try:
#            dlg.exec_()
#        except TypeError:
#            self.UtilidadesQgs.muestra_mensaje( "Error", err.message)
#            dlg.muestra_estado("Error.")
    
    def muestraImagenes(self):
        """
        Muestra las imágenes de los lindes. Debe haber seleccionados puntos en la 
        capa ed_img_lindes o img_lindes.
        """
        self.inicializa()
        if self.inicializado==False:
            return
        dlg=ctrMuestraImgLinde(self.oUtiles)
        if dlg.getOk()==True:
            dlg.show()

    def muestraImagenesEI(self):
        """
        Muestra imagenes de los elementos interiores, es necesario un solo objeto seleccionado
        en la capa ed_img_elem_int o img_elem_int.
        """
        self.inicializa()
        if self.inicializado==False:
            return
        dlg=ctrMuestraImgEI(self.oUtiles)
        if dlg.getOk()==True:
            dlg.show()

    def cargarEdicion(self):
        """
        Carga las capas de objetos espaciales de edición, incluidas las que muestran los errores de superposición y huecos.
        Si las capas ya estaban cargadas, las vuelve a cargar.
        """
        self.inicializa()
        if self.inicializado==False:
            return 
        self.oUtiles.oVarios.cargaCapas(tipoTrabajo="edicion", oUtiles=self.oUtiles,borrarSiExiste=True)
           
    def cargarDefinitivas(self):
        """
        Carga las capas de objetos espaciales definitivas, 
        no se carga las que muestran los errores de superposición y huecos.
        Si las capas ya estaban cargadas, las vuelve a cargar.
        """
        self.inicializa()
        if self.inicializado==False:
            return 
        
        self.oUtiles.oVarios.cargaCapas(tipoTrabajo="definitivo", oUtiles=self.oUtiles,borrarSiExiste=True)
    
    def inicializa(self):
        """
        Conecta con la base de datos y, si ha sido posible, inicializa el objeto oUtiles.
        """

        if self.inicializado==False:
            try:
                oUt=TopoDelProp.utilsPropiedad.utils.InicializaUtiles(self.iface)
                oUtiles=oUt.getUtiles()
                self.inicializado=True
                self.oUtiles=oUtiles
#                self.utiles.oConectaPg.cierraConexion()
            except Exception, e:
                QtGui.QMessageBox.information(self.iface.mainWindow(),"Hubo un problema", e.message,1)
                self.inicializado=False
                return
    def ayuda(self):
        qgis.utils.showPluginHelp(filename="ayuda/index")
        
