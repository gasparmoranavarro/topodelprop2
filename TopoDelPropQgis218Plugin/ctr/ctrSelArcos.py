# This Python file uses the following encoding: utf-8
'''
Created on 11/05/2012

@author: Gaspar
'''

import sys
import os
from PyQt4 import QtCore, QtGui

from delPropiedad.forms.frmSelArcos import Ui_frmSelArcos

import qgis.core
import qgis.gui
import delPropiedad.utilsPropiedad.utils
import delPropiedad.Atributos 
import pyQgsBibGas.gen.general
import pyQgsBibGas.gen.pypgGas

"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""

class ctrSelArcos(QtGui.QDialog):
    #constructor
    def __init__(self, iface,vPpal):
        #Ejecuta el constructor de la clase padre QDialog
        #vPpal es la ventana primcipal del programa
        QtGui.QDialog.__init__(self, vPpal)
        #Inicializa el formulario
        self.ui=Ui_frmSelArcos() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.vPpal=vPpal
        self.iface=iface
        self.UtilidadesQgs=pyQgsBibGas.gen.general.UtilidadesQgs(self.iface)
        self.mapCanvas=iface.mapCanvas()
        self.layers=self.mapCanvas.layers()
        #self.setWindowModality(1)
        #Conecta los botones con m??todos de esta clase
        self.connect(self.ui.bttGrabarFinca, QtCore.SIGNAL("clicked()"),self.grabarFinca)
        self.connect(self.ui.bttGrabarLindes, QtCore.SIGNAL("clicked()"),self.grabarLindes)
        self.connect(self.ui.bttGrabarImagenes, QtCore.SIGNAL("clicked()"),self.grabarImagenes2)
        self.connect(self.ui.bttCambiaImg, QtCore.SIGNAL("clicked()"),self.cambiaImagen)
        self.show()#muestra el formulario

        """
        #self.connect(self, Qt.SIGNAL('quit()'), self.onQuit)
        #self.connect(self, Qt.SIGNAL('destroyed()'), self.onQuit)
        #self.connect(self, Qt.SIGNAL('triggered()'), self.closeEvent
        """

        oTr=delPropiedad.utilsPropiedad.utils.DirTrabajos()
        self.numTrabajo=22 
        rut=oTr.sacaDir()
        if isinstance(rut,Exception):
            QtGui.QMessageBox.information(self,"Mensaje", rut.message,1)#self es la ventana pasdre que necesita qmessagebox 
            self.close()
            return
        self.rutaTrabajo=rut + "/" + str(self.numTrabajo)
    def grabarFinca(self):
        self.conn=pyQgsBibGas.gen.pypgGas.ConectaPg("pqgis", "joamona", "caren1fe","localhost")
        if self.conn.conectado==False:
            QtGui.QMessageBox.information(self,"Error", self.conn.descripcion_error,1)
            return
        self.oConsultas=pyQgsBibGas.gen.pypgGas.ConsultasPg(self.conn)
        
        layer=self.UtilidadesQgs.get_capa_nombre("n_fincas")
        if layer is None:
            QtGui.QMessageBox.information(self,"Mensaje", "La capa n_fincas no existe o esta desactivada",1)#self es la ventana pasdre que necesita qmessagebox 
            return
        layer.removeSelection(False)#deselecciona todo
        layer.invertSelection()#selecciona todo
        #QtGui.QMessageBox.information(self,"Mensaje", str(layer.selectedFeatureCount()),1)#self es la ventana pasdre que necesita qmessagebox 
             
        nF = layer.selectedFeatureCount()
        if (nF > 0):
            seleccion = layer.selectedFeatures()
            for objeto in seleccion:
                geom=objeto.geometry()
                if geom is None:
                    QtGui.QMessageBox.information(self,"Mensaje", "Los objetos deben estar visibles",1)
                    return
  
                geomT=str(geom.exportToWkt())
                listaCampos=["tipo_finca", "geom"]
                listaValores=["ole mis huevos"]
                listaValores.append(geomT)

                r=self.oConsultas.insertaDatos("h30.fincas",listaCampos, listaValores,None, True, "geom","25830" )
                if isinstance(r,Exception):
                    self.vPpal.muestra_estado(r.message)
                else:
                    self.vPpal.muestra_estado("Insertado con exito " + self.conn.cursor.statusmessage)
                    
        layer.removeSelection(False)#deselecciona todo
        self.conn.cierraConexion()

    def grabarLindes(self):
        self.conn=pyQgsBibGas.gen.pypgGas.ConectaPg("pqgis", "joamona", "caren1fe","localhost")
        if self.conn.conectado==False:
            QtGui.QMessageBox.information(self,"Error", self.conn.descripcion_error,1)
            return
        self.oConsultas=pyQgsBibGas.gen.pypgGas.ConsultasPg(self.conn)
        
        layer=self.UtilidadesQgs.get_capa_nombre("n_lindes")
        if layer is None:
            QtGui.QMessageBox.information(self,"Mensaje", "La capa linde no existe o esta desactivada",1)#self es la ventana pasdre que necesita qmessagebox 
            return
        layer.removeSelection(False)#deselecciona todo
        layer.invertSelection()#selecciona todo
        #QtGui.QMessageBox.information(self,"Mensaje", str(layer.selectedFeatureCount()),1)#self es la ventana pasdre que necesita qmessagebox 
#        settrace()
        nF = layer.selectedFeatureCount()
        if (nF > 0):
            seleccion = layer.selectedFeatures()
            for objeto in seleccion:
                geom=objeto.geometry()
                if geom is None:
                    QtGui.QMessageBox.information(self,"Mensaje", "Los objetos deben estar visibles",1)
                    return
  
                geomT=str(geom.exportToWkt())
                listaCampos=["descripcion_fisica", "geom"]
                listaValores=["ole mis huevos2"]
                listaValores.append(geomT)
                r=self.oConsultas.insertaDatos("h30.linde",listaCampos, listaValores,None, False, "geom","25830" )
                if isinstance(r,Exception):
                    self.vPpal.muestra_estado(r.message)
                else:
                    self.vPpal.muestra_estado("Insertado con exito " + self.conn.cursor.statusmessage)

        layer.removeSelection(False)#deselecciona todo
        self.conn.cierraConexion()

    def grabarImagenes(self):
        oArchivos=pyQgsBibGas.gen.pypgGas.Archivos()
        self.conn=pyQgsBibGas.gen.pypgGas.ConectaPg("pqgis", "joamona", "caren1fe","localhost")
        if self.conn.conectado==False:
            QtGui.QMessageBox.information(self,"Error", self.conn.descripcion_error,1)
            return
        self.oConsultas=pyQgsBibGas.gen.pypgGas.ConsultasPg(self.conn)
        
        layer=self.UtilidadesQgs.get_capa_nombre("n_imagenes")
        if layer is None:
            QtGui.QMessageBox.information(self,"Mensaje", "La capa imagen no existe o esta desactivada",1)#self es la ventana pasdre que necesita qmessagebox 
            return
        layer.removeSelection(False)#deselecciona todo
        layer.invertSelection()#selecciona todo
        #QtGui.QMessageBox.information(self,"Mensaje", str(layer.selectedFeatureCount()),1)#self es la ventana pasdre que necesita qmessagebox 
#        settrace()
   
        nF = layer.selectedFeatureCount()
        if (nF > 0):
            seleccion = layer.selectedFeatures()
            for objeto in seleccion:
                #extraigo el numero de imagen de cada punto
                atributos=objeto.attributeMap()
                attrIndex=atributos.fieldNameIndex("Text")
                if attrIndex == -1:
                    QtGui.QMessageBox.information(self,"Mensaje", "La capa no tiene el campo Text necesario para saber el numero de foto.",1)
                    return

                img=oArchivos.leeDatBinarios("c:/temp/img.jpg")
                geom=objeto.geometry()
                if geom is None:
                    QtGui.QMessageBox.information(self,"Mensaje", "Los objetos deben estar visibles",1)
                    return
                
                geomT=str(geom.exportToWkt())
                listaCampos=["descripcion_fisica","imagen", "geom"]
                listaValores=["ole mis huevos2",img]
                listaValores.append(geomT)
                r=self.oConsultas.insertaDatos("h30.imagenes",listaCampos, listaValores,"imagen", False, "geom","25830" )
                if isinstance(r,Exception):
                    self.vPpal.muestra_estado(r.message)
                else:
                    self.vPpal.muestra_estado("Insertado con exito " + self.conn.cursor.statusmessage)

        layer.removeSelection(False)#deselecciona todo
        self.conn.cierraConexion()
    def cambiaImagen(self):
        oArchivos=pyQgsBibGas.gen.pypgGas.Archivos()
        rr=oArchivos.cambiaTamanoImagen("c:/campeón coño/img.jpg","c:/campeón coño/pp.jpg",1000)
        if isinstance(rr,Exception):
            self.vPpal.muestra_estado(rr.message)
        else:
            self.vPpal.muestra_estado("Imagen grabada con exito")

    def grabarImagenes2(self):
        id_linde=18
        oArchivos=pyQgsBibGas.gen.pypgGas.Archivos()
        self.conn=pyQgsBibGas.gen.pypgGas.ConectaPg("pqgis", "joamona", "caren1fe","localhost")
        if self.conn.conectado==False:
            QtGui.QMessageBox.information(self,"Error", self.conn.descripcion_error,1)
            return
        self.oConsultas=pyQgsBibGas.gen.pypgGas.ConsultasPg(self.conn)
        vlayer=self.UtilidadesQgs.get_capa_nombre("dxf_imagenes")
        if vlayer is None:
            QtGui.QMessageBox.information(self,"Mensaje", "La capa dxf_imagen no existe o esta desactivada",1)#self es la ventana pasdre que necesita qmessagebox 
            return
        provider = vlayer.dataProvider()
        feat = qgis.core.QgsFeature()
        # start data retreival: fetch geometry and all attributes for each feature
        fldDesc = provider.fieldNameIndex("Text")#retorna el indice del campo Text del DXF
        if fldDesc == -1:
            QtGui.QMessageBox.information(self,"Mensaje", "El campo Text con el numero de foto debe existir en la capa dxf_imagenes",1)
            return
        provider.select([fldDesc])#selecciona unicamente ese campo a retornar con fetch
 
        listaCampos=["id_trabajo", "id_linde", "nom_imagen","imagen", "geom"]
        while provider.nextFeature(feat):
            # fetch geometry
            geom = feat.geometry()
            if geom is None:
                QtGui.QMessageBox.information(self,"Mensaje", "Los objetos deben estar visibles",1)
                return
                
            geomT=str(geom.exportToWkt())

            # fetch map of attributes
            dicAttr = feat.attributeMap()#dicAttr es un dictionary: key = field index, value = QgsFeatureAttribute
            qgsVAttr=dicAttr.get(fldDesc)
            nomImagen=str(qgsVAttr.toString())
            imgEntrada=self.rutaTrabajo + "/imagenes/" + nomImagen
            imgSalida=self.rutaTrabajo + "/imagenes/reducidas/" + nomImagen
            imgEntrada=str(imgEntrada)
            imgSalida=str(imgSalida)
            resp=oArchivos.cambiaTamanoImagen(imgEntrada,imgSalida,1000)
            if isinstance(resp,Exception):
                QtGui.QMessageBox.information(self,"Mensaje", resp.message,1)
                return
#            settrace()
            img=oArchivos.leeDatBinarios(imgSalida)
            if isinstance(img,Exception):
                QtGui.QMessageBox.information(self,"Mensaje", img.message,1)
                return
            listaValores=[self.numTrabajo,id_linde,nomImagen,img,geomT]
            r=self.oConsultas.insertaDatos("h30.imagenes",listaCampos, listaValores,"imagen", False, "geom","25830" )
            if isinstance(r,Exception):
                QtGui.QMessageBox.information(self,"Error", r.message,1)
            else:
                QtGui.QMessageBox.information(self,"Insertado con exito", self.conn.cursor.statusmessage,1)

        vlayer.removeSelection(False)#deselecciona todo
        self.conn.cierraConexion()


def cerrado(self, event):
    """Evento que permite abrir una
    ventana de dialogo para confirmar la salida del programa
    """
    #Se genera la respuesta de la confirmacion de salir
    reply = QtGui.QMessageBox.question(self, "Mensaje","Seguro que desea salir?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    
    
    #Si se selecciona Si se acepta el evento, si se selecciona
    #no se ignora el evento
    if reply == QtGui.QMessageBox.Yes:
        event.accept()
    else:
        event.ignore()
    
        
        """
                settrace()

                tVal=tuple(listaValores)
                nombreTabla="h30.fincas"
                nombreCampo="geom"
                consulta="insert into h30.fincas (tipo_finca,geom) values (%s,ST_multi(ST_geometryfromtext(%s,25830)))"
                try:
                    self.conn.cursor.execute(consulta,tVal)
                    self.conn.conn.commit()
                    self.vPpal.muestra_estado("Insertado con exito " + self.conn.cursor.statusmessage)
                except Exception, e:
                    self.vPpal.muestra_estado(e.message)
                
                
        #QtGui.QMessageBox.information(self,"Mensaje", "A mostrar",1)#self es la ventana pasdre que necesita qmessagebox  
        #a=int(self.ui.txtA.text())
        #b=int(self.ui.txtB.text())
        #c=a+b
        #self.ui.txtResultado.setText(str(c))
        #para acceder a las capas, se pasa por la propiedad mapcanvas del
        #objeto iface
#        for i in range(len(self.layers)):        
            #layer=self.layers[i]
            #QtGui.QMessageBox.information(self,"Mensaje", layer.name(),1)#self es la ventana pasdre que necesita qmessagebox  
         
                """

      
        
        
        
        
        
    
  
