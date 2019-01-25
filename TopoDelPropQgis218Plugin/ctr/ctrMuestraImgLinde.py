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
    Formulario para descargar y mostrar las imágenes de los lindes.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para descargar y mostrar las imágenes de los lindes.
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

class ctrMuestraImgLinde(QtGui.QDialog):
    """
    Formulario que muestra las imagenes de la capa imagenes.
    Se necesita que la capa exista, que sea de tipo Point y que haya puntos seleccionados
    """
    #constructor
    def __init__(self, oUtiles):
        """
        @type oUtiles:  UilsPropiedad.Utils.Utiles
        @param oUtiles: Clase con las utilidades necesarias para esta aplicacion
        """
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self,oUtiles.iface.mainWindow())

        #Inicializa el formulario
        self.ui=Ui_frmMuestraImg() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.tblDatos=self.ui.tblDatos #tabla con los datos del punto
        self.oUtiles=oUtiles
        
        #self.oUtiles.ntrabajo=self.oUtiles.id_trabajo
        #settrace()
        
        self.connect(self.ui.bttAnterior, QtCore.SIGNAL("clicked()"),self.imgAnterior)
        self.connect(self.ui.bttSiguiente, QtCore.SIGNAL("clicked()"),self.imgSiguiente)
        
        self.ok=False
#        self.setAttribute(QtCore.Qt.WA_DeleteOnClose,True)#esto es para que se destruya el formulario
#        settrace()
        #self.layer=self.oUtiles.oUtilidadesQgs.get_capa_nombre("img_linde")
        self.layer=self.oUtiles.iface.activeLayer()
        if self.layer==None:
            QtGui.QMessageBox.information(self,"Error" , "La capa espacial img_linde, o ed_img_linde de Postgis debe estar en el proyecto QGis",1)
            self.ok=False
            return
        self.tipoTrabajo=None
        nombre=str(self.layer.name())
        if not(nombre=="ed_img_linde" or nombre=="img_linde" or nombre=="hist_img_linde"):
            QtGui.QMessageBox.information(self,"Error" , "La capa activa debe ser ed_img_linde, img_linde o hist_img_linde. Los puntos de la localizacion de las imagenes deben estar seleccionados",1)
            self.ok=False
            return            
        if nombre=="ed_img_linde":
            self.tipoTrabajo="edicion"
        elif nombre=="img_linde":
            self.tipoTrabajo="definitivos"
        else:
            self.tipoTrabajo="historico"
            
        self.listaValores=self.extraeListaValores() #elementos seleccionados 
        self.i=-1
        if self.ok==True:
            self.imgSiguiente()#muestra la primera imagen
        
    def extraeListaValores(self):
        """
        Devuelve la lista de diccionarios de los valores de atributo
        de los elementos seleccionado de la capa imagenes.
        Tambien cambia el valor de la variable de la clase self.ok.
        La establece a True si todo ha ido bien y, el formulario se
        puede mostrar. A false en caso contrario.
        @return: la lista de diccionarios
        """

        try:
            #hay que descubrir como acceder a la lista de nombres de los
            #campos de una tabla para quitar esta lista fija de codigo
            listaCampos=["gid", "id_trabajo", "gid_linde", "nom_arch"]
            listaValores=self.oUtiles.oUtilidadesQgs.get_attrSeleccionCapa(str(self.layer.name()),listaCampos,True)
            self.ok=True
            return listaValores
        except Exception, e:
            self.ok = False
            QtGui.QMessageBox.information(self,"Error", e.message)

    def imgSiguiente(self):
        """
        Muestra la imagen siguiente
        """
        #settrace()
        nF=len(self.listaValores)#numero de elementos
        if self.i < nF -1:
            self.i=self.i+1
            dic=self.listaValores[self.i]
            cad="Imagen " + str(self.i + 1) + " de " + str(nF)
            self.ui.lbMensaje.setText(cad)
            #extraigo el numero de imagen de cada punto
            self.muestraImagen(dic)
            self.muestraValores(dic)

    def imgAnterior(self):
        """
        Muestra la imagen anterior
        """
        #settrace()
        nF=len(self.listaValores)
        if self.i > 0:#si el elemento actual no es el primero
            self.i=self.i-1
            dic=self.listaValores[self.i]
            cad="Imagen " + str(self.i + 1) + " de " + str(nF)
            self.ui.lbMensaje.setText(cad)
            self.muestraImagen(dic)
            self.muestraValores(dic)
            
    def muestraImagen(self,dic):
        """
        Muestra la imagen.
        Primero comprueba que la imagen no haya sido descargada ya,
        en tal caso no hace falta que vuelva a descargarse del servidor
        """
        #settrace()
        oQset=[]
        oQset.append(dic.get("featureId"))
        self.layer.setSelectedFeatures(oQset)#deselecciona todo
            #y selecciona el punto actual
        
        nomImagen=dic.get("nom_arch")
        gid_linde=str(dic.get("gid_linde"))
        id_trabajo=str(dic.get("id_trabajo"))
        nomImagen=self.oUtiles.dTrabajos + "/"  + self.tipoTrabajo + "/" + id_trabajo + "/lindes/imagenes/" + gid_linde + "/" + nomImagen
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
        listaSubDir=[self.tipoTrabajo,id_trabajo,"lindes","imagenes",gid_linde]
        rr=self.oUtiles.oUtilidades.creaDir(self.oUtiles.dTrabajos,listaSubDir,darMens=True)
        if isinstance(rr,Exception):
            QtGui.QMessageBox.information(self,"Error al crear el directorio.", e.message,1)
            self.ok=False
            return
        

        #esquema=self.layer.dataProvider().dataSourceUri().schema()
        """
        uri=self.layer.dataProvider().dataSourceUri()#obtengo la cadena de conexion
        #para obtener el esquema de la tabla
        try:
            esquema=self.oUtiles.oVarios.sacaEsquemaTablaConUri(uri,"img_linde")
        except Exception,e:
            QtGui.QMessageBox.information(self,"Error al obtener el esquema de la tabla", e.message,1)
            self.ok=False
            return
        """
        esquema=str(self.oUtiles.src_trabajo)
        if "ed_" in str(self.layer.name()):
            esquema="ed_src" + esquema
        else:
            esquema="src" + esquema
        self.ui.lbEstado.setText("Recuperando de la base de datos. Espere ...")
        gid=dic.get("gid")
        nombreTabla=esquema + "." + str(self.layer.name())
        listaCampos=["archivo"]
        #recuperaDatosTablaByteaDic(self, nombreTabla, listaCampos, condicionWhere=None,listaValoresCondWhere=None,bytea_output_to_escape=False):
        lDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(nombreTabla, listaCampos, "gid=%s",[gid])
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
        listaNombreCampos=dic.keys()#devuelve todas las claves del diccionario
        self.tblDatos.setRowCount(len(listaNombreCampos))
        self.tblDatos.setColumnCount(1)
        self.tblDatos.setHorizontalHeaderLabels(['Valor del campo'])
        self.tblDatos.setVerticalHeaderLabels(listaNombreCampos)

        listaValores=dic.values()
        i=0
        for valor in listaValores:
            newitem = QtGui.QTableWidgetItem(str(valor))
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

