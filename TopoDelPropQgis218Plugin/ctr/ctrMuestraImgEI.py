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
    Formulario para descargar y mostrar las imágenes de los elementos interiores.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para descargar y mostrar las imágenes de los elementos interiores.
"""
import sys
import os
from PyQt4 import QtCore, QtGui
from TopoDelProp.forms.frmMuestraImg import Ui_frmMuestraImg

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

 
"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""

class ctrMuestraImgEI(QtGui.QDialog):
    """
    Formulario que muestra las imagenes de los elementos interiores 
    (tablas ed_img_elem_int o img_elem_int).
    Se necesita que la capa exista, que sea de tipo multipolygon y que 
    haya un elemento seleccionado.
    """
    #constructor
    def __init__(self, oUtiles):
        """
        @type oUtiles:  UilsPropiedad.Utils.Utiles
        @param oUtiles: Clase con las utilidades necesarias para esta aplicacion
        """
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self, oUtiles.iface.mainWindow())
        
        #Inicializa el formulario
        self.ui=Ui_frmMuestraImg() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.tblDatos=self.ui.tblDatos #tabla con los datos del punto
        self.oUtiles=oUtiles
        
        #self.oUtiles.ntrabajo=self.oUtiles.id_trabajo
                
        self.connect(self.ui.bttAnterior, QtCore.SIGNAL("clicked()"),self.imgAnterior)
        self.connect(self.ui.bttSiguiente, QtCore.SIGNAL("clicked()"),self.imgSiguiente)
        
        self.ok=False
#        self.setAttribute(QtCore.Qt.WA_DeleteOnClose,True)#esto es para que se destruya el formulario
#        
        #self.layer=self.oUtiles.oUtilidadesQgs.get_capa_nombre("img_linde")
        self.layer=self.oUtiles.iface.activeLayer()
        if self.layer==None:
            QtGui.QMessageBox.information(self,"Error" , "La capa espacial elem_interiores o ed_elem_interiores de Postgis debe estar en el proyecto QGis",1)
            self.ok=False
            return
        self.tipoTrabajo=None
        nombre=str(self.layer.name())
        if not(nombre=="ed_elem_interiores" or nombre=="elem_interiores"):
            QtGui.QMessageBox.information(self,"Error" , "La capa activa debe ser ed_elem_interiores o elem_interiores.",1)
            self.ok=False
            return            
        if nombre=="ed_elem_interiores":
            self.tipoTrabajo="edicion"
        elif nombre=="elem_interiores":
            self.tipoTrabajo="definitivos"
        else:
            self.tipoTrabajo="historico"
        #settrace()
        nf = self.layer.selectedFeatureCount()
        if nf==0:
            QtGui.QMessageBox.information(self,"Error" , "Debe haber un objeto seleccionado en la capa activa: " + nombre,1)
            return
        if nf>1:
            mens=unicode("Hay más de un objeto seleccionado en la capa activa: ", "utf8") + nombre
            QtGui.QMessageBox.information(self,"Error" , mens,1)            
            return
        self.dicEI=None#diccionario campo:valor con todos los datos del elemento interior
        self.nombreCompletoTablaImgEI=None
        self.listaDicNomImagenes=None#lista con diccionarios (id, nom_arch) de todas las imagenes del elemento interior 
        self.esquema=None#esquema de las tablas
        self.cargaDicValores()#inicializa self.dicEI, self.listaDicNomImagenes, self.esquema,self.nombreCompletoTablaImgEI
        self.i=-1
        if self.ok==True:
            self.imgSiguiente()#muestra la primera imagen
        
    def cargaDicValores(self):
        """
        Carga la lista de diccionarios con las imagenes del elemento_interior
        Y los datos del elemento interior en otro diccionario.
        Tambien cambia el valor de la variable de la clase self.ok.
        La establece a True si todo ha ido bien y, el formulario se
        puede mostrar. A false en caso contrario.
        @return: la lista de diccionarios
        """

        #hay que descubrir como acceder a la lista de nombres de los
        #campos de una tabla para quitar esta lista fija de codigo
        #uri=self.layer.dataProvider().dataSourceUri()
        #esquema=self.oUtiles.oVarios.sacaEsquemaTablaConUri(uri=uri,nomTabla=self.layer.name(),dbname="propiedad")
        esquema=str(self.oUtiles.src_trabajo)
        if "ed_" in str(self.layer.name()):
            esquema="ed_src" + esquema
        else:
            esquema="src" + esquema
        self.esquema=esquema
        listaCampos=self.oUtiles.oConsultasPg.sacaNombresCamposTabla_lista(esquema, str(self.layer.name()))
        if isinstance(listaCampos,Exception):
            QtGui.QMessageBox.information(self,"Error", listaCampos.message)
            self.ok=False
            return
        listaCampos=self.oUtiles.oUtilidadesListas.eliminaEltosLista(listaEltos=listaCampos,listaEliminar=["geom"], genError=True)
        if isinstance(listaCampos,Exception):
            QtGui.QMessageBox.information(self,"Error", listaCampos.message)
            self.ok=False
            return
        listaObjetos=self.layer.selectedFeatures()
        objeto=listaObjetos[0]
        try:
            self.dicEI=self.oUtiles.oUtilidadesQgs.get_attrElementoCapa(feat=objeto, vLayer=self.layer, listaCampos=listaCampos,geom=False)
            
        except Exception,e:
            QtGui.QMessageBox.information(self,"Error", "Error obteniendo los valores de atributo: " + e.message)
            self.ok=False
            return
        

        if self.tipoTrabajo=="edicion":
            self.nombreCompletoTablaImgEI=esquema + ".ed_img_elem_int"
        else:
            self.nombreCompletoTablaImgEI=esquema + ".img_elem_int"
        
        lValores=[self.dicEI.get("gid")]
        self.listaDicNomImagenes=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla=self.nombreCompletoTablaImgEI, listaCampos=["id","id_trabajo","gid_elem_int","nom_arch"], condicionWhere="gid_elem_int=%s",listaValoresCondWhere=lValores,bytea_output_to_escape=False, orderBy=None,limit=None)
        
        if isinstance(self.listaDicNomImagenes,Exception):
            QtGui.QMessageBox.information(self,"Error", e.message)
            self.ok=False
            return
        elif len(self.listaDicNomImagenes)==0:
            QtGui.QMessageBox.information(self,"Aviso", "El elemento no tiene imagenes.")
            self.ok=False
            return
        self.ok=True       
    def imgSiguiente(self):
        """
        Muestra la imagen siguiente.
        """
        nF=len(self.listaDicNomImagenes)#numero de imagenes
        if self.i < nF -1:
            self.i=self.i+1
            dic=self.listaDicNomImagenes[self.i]
            cad="Imagen " + str(self.i + 1) + " de " + str(nF)
            self.ui.lbMensaje.setText(cad)
            #extraigo el numero de imagen de cada punto
            self.muestraImagen(dic)
            self.muestraValores(self.dicEI)

    def imgAnterior(self):
        """
        Muestra la imagen anterior.
        """
        nF=len(self.listaDicNomImagenes)
        if self.i > 0:#si el elemento actual no es el primero
            self.i=self.i-1
            dic=self.listaDicNomImagenes[self.i]
            cad="Imagen " + str(self.i + 1) + " de " + str(nF)
            self.ui.lbMensaje.setText(cad)
            self.muestraImagen(dic)
            self.muestraValores(self.dicEI)
            
    def muestraImagen(self,dic):
        """
        Muestra la imagen en el formulario.
        """       
        #primero comprueba que la imagen no haya sido descargada ya,
        #en tal caso no hace falta que vuelva a descargarse del servidor
        nomImagen=dic.get("nom_arch")
        gid_ei=str(dic.get("gid_elem_int"))
        id_trabajo=str(dic.get("id_trabajo"))
        nomImagen=self.oUtiles.dTrabajos + "/"  + self.tipoTrabajo + "/" + id_trabajo + "/elem_interiores/" + gid_ei + "/" + nomImagen
        if os.path.exists(nomImagen):
            try:
                self.ui.lbImg.setPixmap(QtGui.QPixmap(_fromUtf8(nomImagen)))
                self.ui.lbEstado.setText("Imagen encontrada en: " + nomImagen)
                return
            except Exception, e:
                QtGui.QMessageBox.information(self,"Error al cargar la imagen" , e.message + ". Imagen: " + nomImagen,1)
                self.ok=False
                return
        
        #la imagen no habia sido descargada
        #compruebo que los directorios existen y si no los creo
        listaSubDir=[self.tipoTrabajo,id_trabajo,"elem_interiores",gid_ei]
        rr=self.oUtiles.oUtilidades.creaDir(self.oUtiles.dTrabajos,listaSubDir,darMens=True)
        if isinstance(rr,Exception):
            QtGui.QMessageBox.information(self,"Error al crear el directorio.", e.message,1)
            self.ok=False
            return
             
        self.ui.lbEstado.setText("Recuperando de la base de datos. Espere ...")
        idd=dic.get("id")
        nombreTabla=self.nombreCompletoTablaImgEI
        listaCampos=["archivo"]
        #recuperaDatosTablaByteaDic(self, nombreTabla, listaCampos, condicionWhere=None,listaValoresCondWhere=None,bytea_output_to_escape=False):
        lDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla, listaCampos, "id=%s",[idd])
        if isinstance(lDic, Exception):
            QtGui.QMessageBox.information(self,"La consulta no es correcta", "Consulta: " + self.oUtiles.oConsultasPg.consulta,1)
            QtGui.QMessageBox.information(self,"La consulta no es correcta", "Error: " + lDic.message,1)
            self.ok=False
            return
        n=len(lDic)
        if not(n == 1):
            QtGui.QMessageBox.information(self,"La consulta produjo cero o mas de un resultado", "Consulta: " + self.oUtiles.oConsultasPg.consulta,1)
            self.ok=False
            return
        binary=lDic[0].get("archivo")
        res=self.oUtiles.oArchivos.EscribeDatBinarios(nomImagen, binary)
        if isinstance(res,Exception):
            QtGui.QMessageBox.information(self,"No se pudo escribir el archivo descargado", "Archivo: " + nomImagen,1)
            QtGui.QMessageBox.information(self,"Descripcion del error", "Error: " + res.message,1)
            self.ok=False
            return
        try:
            self.ui.lbImg.setPixmap(QtGui.QPixmap(_fromUtf8(nomImagen)))
            self.ui.lbEstado.setText("Hecho. Guardada en: " + nomImagen)
            return
        except Exception, e:
            QtGui.QMessageBox.information(self,"Error al cargar la imagen" , e.message + ". Imagen: " + nomImagen,1)
            self.ok=False
            
    def muestraValores(self,dic):
        """
        Muestra los valores de los campos en el formulario.
        """
        listaNombreCampos=dic.keys()#devuelve todas las claves del diccionario
        self.tblDatos.setRowCount(len(listaNombreCampos))
        self.tblDatos.setColumnCount(1)
        self.tblDatos.setHorizontalHeaderLabels(['Valor del campo'])
        self.tblDatos.setVerticalHeaderLabels(listaNombreCampos)

        listaValores=dic.values()
        i=0
        for valor in listaValores:
            try:
                newitem = QtGui.QTableWidgetItem(str(valor))
            except:
                try:
                    newitem = QtGui.QTableWidgetItem(valor)
                except:
                    try:
                        newitem = QtGui.QTableWidgetItem(valor.toString())
                    except Exception,e:
                        QtGui.QMessageBox.information(self,"Error al cargar la imagen" , "Problemas de codificación de caractéres: " + e.message,1)
            self.tblDatos.setItem(i, 0, newitem)
            i=i+1
        
    def getOk(self):
        """
        Devuelve True o False.
        @return: True si todo va bien y el formulario puede mostrarse
                 False si ha habido algun problema y el formulario no
                 puede mostrarse
        """
        return self.ok

