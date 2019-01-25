# -*- coding: utf-8 -*-
"""
    Utilidades para trabajar con QGis 2.0.
    
    This program is free software; you can redistribute it and/or modify  
    it under the terms of the GNU General Public License as published by  
    the Free Software Foundation; either version 2 of the License, or     
    (at your option) any later version.
    
    @copyright: (C) 2011 by J. Gaspar Mora Navarro
    @contact: topodelprop@gmail.com
    @author: J. Gaspar Mora navarro.
    @organization: U.P. Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @version: 1
    @summary: Modulo que contiene utilidades de uso general para trabajar con QGis
"""
import sys
import os
import copy

"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""

__docformat__ = "epytext"

from PyQt4 import QtCore, QtGui
import qgis.core
import qgis


class UtilidadesQgs(object):
    """
    Clase con utilidades para trabajar con QGis. Todos los métodos llaman
    antes a self.actualizaIface, que actualiza los datos de qgis.
    """
    def __init__(self, iface):
        """
        Constructor
        
        @type  iface: QgisInterface
        @param iface: Interface expuesta por el plugin. Es la que da acceso QGis.
        """
        self.iface=iface
        self.mapCanvas=iface.mapCanvas()
        self.layers=self.mapCanvas.layers()
    
    def actualizaIface(self):
        """
        Actualiza los datos de qgis. Llamar a este método antes de usar
        las funciones.
        """
        self.iface=qgis.utils.iface
        self.mapCanvas=self.iface.mapCanvas()
        self.layers=self.mapCanvas.layers()
        
    def muestra_mensaje(self, titulo, mensaje):
        """
        Muestra cuadro de diálogo con un mensaje en modo modal
        @type  titulo: string
        @param titulo: Titulo del mensaje.
        @type  mensaje: string
        @param mensaje: mensaje mostrado.
        """
        QtGui.QMessageBox.information(self.iface.mainWindow(),titulo, mensaje,1)
        
    def get_capa_nombre(self, nombreCapa):
        """
        Devuelve la referencia a a capa que coincide con el nombre proporcionado
        No utiliza el objeto self.iface porque puede estar anticuado y no reflejar
        los cambios hechos en qgis. Utilizo self.iface=qgis.utils.iface, con lo que
        actualizo los datos de qgis
        @type  nombreCapa: string
        @param nombreCapa: nombre de la capa a retornar. Dan igual las mayúsculas o minúsculas.
        @return: la referencia a la capa buscada o None, si no la encuentra
        """
        self.actualizaIface()
        for i in range(len(self.layers)):        
            layer=self.layers[i]
            nomCapaQgs=layer.name().lower()
            nomCapaMin=nombreCapa.lower()
            if nomCapaQgs==nomCapaMin:
                return layer

    def get_capa_nombre2(self, nombreCapa):
        """
        Devuelve la referencia a a capa que coincide con el nombre proporcionado
        La diferencia con get_capa_nombre es que get_capa_nombre no encuentra las capas
        desactivadas y get_capa_nombre2 sí.
        No utiliza el objeto self.iface porque puede estar anticuado y no reflejar
        los cambios hechos en qgis. Utilizo self.iface=qgis.utils.iface, con lo que
        actualizo los datos de qgis
        @type  nombreCapa: string
        @param nombreCapa: nombre de la capa a retornar. Dan igual las mayúsculas o minúsculas.
        @return: la referencia a la capa buscada o None, si no la encuentra
        """

        dicLayers=qgis.core.QgsMapLayerRegistry.instance().mapLayers()
        for layer in dicLayers.values():        
            nomCapaQgs=layer.name().lower()
            nomCapaMin=nombreCapa.lower()
            if nomCapaQgs==nomCapaMin:
                return layer
            
    def sel_eltos_capa_varias_cond(self,nomCapaQgis,dicCondiciones,seleccionarSoloUno=False):
        """
        Selecciona los elementos de la capa nomCapaQgis que cumplan
        las condiciones de dicCondiciones. Los valores de las condiciones
        deben ses strings unicode, utf-8
        Si dicCondiciones es undiccionario vacío, selecciona todos los elementos
        de la capa.
        Si seleccionarSoloUno es True, selecciona solo el primero y no sigue
        buscando.
        @return: Devuelve una lista con los ids de los elementos seleccionados, None, si no hay ninguno, o 
        genera una excepcion
        """
        n=len(dicCondiciones)
        if n==0:#seleccionar toda la capa
            qSet=self.sel_eltos_capa_una_cond(nomCapaQgis, dicCondicion={}, seleccionarSoloUno=seleccionarSoloUno)
            return qSet
        elementos=dicCondiciones.items()#lista de listas clave-valor
        elemento=elementos.pop(0)#primera condicion nomcampo-valor. pop la elimina de elementos
        dic={}
        dic[elemento[0]]=elemento[1]
        #primera seleccion de elementos de la capa con la primera condicion
        qSet=self.sel_eltos_capa_una_cond(nomCapaQgis, dicCondicion={}, seleccionarSoloUno=seleccionarSoloUno)
        if qSet==None:
            return None
        for elemento in elementos:
            dic={}
            dic[elemento[0]]=elemento[1]
            #primera seleccion de elementos de la capa con la primera condicion
            qSet=self.sel_eltos_capa_una_cond(nomCapaQgis, dicCondicion=dic, seleccionarSoloUno=seleccionarSoloUno)            
            if qSet==None:
                return None       
        return qSet
    
    def sel_eltos_capa_una_cond(self,nomCapaQgis,dicCondicion={},seleccionarSoloUno=False): 
        """
        Selecciona, de los elementos de una capa, los que cumplan una condición.
        Si dicCondicion={}, selecciona todos los elementos.
        Si seleccionarSoloUno=True, cuando seleccione el primero que cumpla, 
        lo selecciona, no sigue comprobando y se sale.
        Devuelve una lista con los ids de los elementos seleccionados, None, si no hay ninguno, o 
        genera una excepcion
        """     
        capa=self.get_capa_nombre(nomCapaQgis)
        if capa==None:
            raise Exception("La capa " + nomCapaQgis + " no existe.")
        provider = capa.dataProvider()
        n=len(dicCondicion)
        if n>1:
            raise Exception("El numero de condiciones en la funcion UtilidadesQgs.sel_eltos_capa_una_cond no puede ser mayor que uno.")
        feat=qgis.core.QgsFeature()
        qSet=[]#lista con los ids de los elementos que se seleccionaran
        if n==0:
            #seleccionar todos los elementos de la capa
            provider.select()
            while provider.nextFeature(feat):
                qSet.append(feat.id())
        else:
            nomCampo=dicCondicion.keys()[0]
            indice = provider.fieldNameIndex(nomCampo)
            if indice == -1:
                raise Exception("El campo " + nomCampo + " no existe en la capa " + nomCapaQgis)
            provider.select([indice])
            while provider.nextFeature(feat):
                dicAtributos = feat.attributeMap()#extrae los atributos a comparar
                #es un  diccionario numero:atributo
                atributo=dicAtributos.get(indice)
                valor=atributo.toString()
                valor=unicode(valor,"utf-8")
                if valor==dicCondicion.get(nomCampo):
                    qSet.append(feat.id())
                    if seleccionarSoloUno==True:
                        break
        n=len(qSet)
        if n>0:
            capa.setSelectedFeatures(qSet)
            return qSet
        else:
            return None
        
    def sel_eltos_de_sel_una_cond(self,nomCapaQgis,dicCondicion,seleccionarSoloUno=False):
        """
        Selecciona, de los elementos seleccionados de una capa, los que
        cumplan una condición
        La el valor de la condición debe ser una cadena unicode.
        Si no hay condición, se quedan seleccionados los mismos elementos.
        Devuelve una lista con los ids de los elementos seleccionados, None, si no hay ninguno, o 
        genera una excepcion
        """
        capa=self.get_capa_nombre(nomCapaQgis)
        if capa==None:
            raise Exception("La capa " + nomCapaQgis + " no existe.")
        n=len(dicCondicion)
        if n>1:
            raise Exception("Solo se permite una condicion en UtilidadesQgs.sel_eltos_de_sel_una_cond")
        if n==0:
            #se deja la misma selección
            return
        nombreCampo=dicCondicion.keys()
        valorCampo=dicCondicion.get(nombreCampo)
        try:
            lDic=self.get_attrSeleccionCapa(nomCapaQgis)
        except Exception,e:
            raise Exception(e.message)
        qSet=[]
        for dic in lDic:
            valor=dic.get(nombreCampo)
            if valor==valorCampo:
                qSet.append(dic.get("featureId"))
                if seleccionarSoloUno==True:
                    break
        n=len(qSet)
        if n>0:
            capa.setSelectedFeatures(qSet)
            return qSet
        else:
            return None
    def get_attrSeleccionCapa(self, nombreCapa, listaCampos,geom=False):
        """
        Devuelve una lista de diccionarios con todos los valores
        de los campos de los elementos seleccionados. Cada elemento
        genera un diccionario con sus valores. El diccionario tiene
        como clave el nombre del campo nombreCampo=valor
        Si geom=True, devuelve tambien las coordenadas de la geometria en wkt
        @type nombreCapa: string
        @param nombreCapa: Nombre de la capa cuyos elementos estan selecc
        @return: lista de diccionarios. Un diccionario por cada elemento
            seleccionado de la capa. Las claves del diccionario son los 
            elementos de la capa. Todos los valores estan en forma de string
        """
        vLayer=self.get_capa_nombre(nombreCapa)
        if vLayer==None:
            raise Exception("No existe la capa " + nombreCapa)            
        nF = vLayer.selectedFeatureCount()
        if nF==0:
            raise Exception("El numero de elementos seleccionados de la capa " + nombreCapa + " es cero.")
        seleccion = vLayer.selectedFeatures()
        lista=[]
        for feat in seleccion:
            dic=self.get_attrElementoCapa(feat, vLayer, listaCampos, geom)
            lista.append(dic)
        return lista

    
#     def get_attrElementoCapa(self, feat, vLayer, listaCampos,geom=False):
#         """
#         Devuelve un diccionario con los valores de los campos solicitados
#         en listaCampos. El diccionario tiene
#         como clave el nombre del campo nombreCampo=valor
#         Si geom=True, devuelve tambien las coordenadas de la geometria en wkt
#         @type feat: elemento de qgis
#         @param feat: se obtiene de una seleccion de elementos de una capa con seleccion = vLayer.selectedFeatures(). 
#             Los elementos de pueden extraer con: for feat in seleccion:
#         @type vLayer: qgsVectorLayer
#         @param vLayer: capa que contiene el elemento
#         @return: lista de diccionarios. Un diccionario por cada elemento
#             seleccionado de la capa. Las claves del diccionario son los 
#             elementos de la capa. Todos los valores estan en formato unicode.
#             Las claves featureId y geom, contienen el identificador del objeto
#             y el la geometria en wkt. 
#         @raise exception: la descripcion del error
#         """       
# 
#         provider = vLayer.dataProvider()
#         allAttrs = provider.attributeIndexes()
#         provider.select(allAttrs)#selecciona todos los atributos de la capa
#         attrs = feat.attributeMap()#extrae todos los atributos
#         dic={}#creo el diccionario
#         dic["featureId"]=feat.id()
#         for nomCampo in listaCampos:
#             fldDesc = provider.fieldNameIndex(nomCampo)#saco el indice del campo que busco
#             if fldDesc==-1:
#                 raise Exception("El campo " + nomCampo + " no existe en la capa " + vLayer.name())
#             attr=attrs.get(fldDesc)#saco el atributo que busco
#             try:
#                 valor= unicode(attr.toString(),"utf-8")
#             except:
#                 try:
#                     valor= attr.toString()
#                 except:
#                     valor=str(attr)
#             dic[nomCampo]=valor#añado al diccionario la clace y su valor
#         if geom==True:#Añado tambien la geometria en wkt
#             geom = feat.geometry()
#             if geom is None:
#                 raise Exception("Los elementos deben estar visibles en el mapa")
#             geomT=str(geom.exportToWkt())
#             dic["geom"]=geomT
#         return dic


    def get_attrElementoCapa(self, feat, vLayer, listaCampos,geom=False):
        """
        Devuelve un diccionario con los valores de los campos solicitados
        en listaCampos. El diccionario tiene
        como clave el nombre del campo nombreCampo=valor
        Si geom=True, devuelve tambien las coordenadas de la geometria en wkt
        @type feat: elemento de qgis
        @param feat: se obtiene de una seleccion de elementos de una capa con seleccion = vLayer.selectedFeatures(). 
            Los elementos de pueden extraer con: for feat in seleccion:
        @type vLayer: qgsVectorLayer
        @param vLayer: capa que contiene el elemento
        @return: lista de diccionarios. Un diccionario por cada elemento
            seleccionado de la capa. Las claves del diccionario son los 
            elementos de la capa. Todos los valores estan en formato unicode.
            Las claves featureId y geom, contienen el identificador del objeto
            y el la geometria en wkt. 
        @raise exception: la descripcion del error
        """       
 
        dic={}#creo el diccionario
        dic["featureId"]=feat.id()
        for nomCampo in listaCampos:
            #try:
            idx = vLayer.fieldNameIndex(nomCampo)
            valor=feat.attributes()[idx]
            #except:
            #    raise Exception("El campo " + nomCampo + " no esta en la lista de atributos de la capa")
            dic[nomCampo]=valor#añado al diccionario la clace y su valor
        if geom==True:#Añado tambien la geometria en wkt
            geom = feat.geometry()
            if geom is None:
                raise Exception("Los elementos deben estar visibles en el mapa")
            geomT=str(geom.exportToWkt())
            dic["geom"]=geomT
        return dic
 
    def get_tipoGeomNomCapa(self,nomCapa):
        """
        Recibe el nombre de una capa vectorial y devuelve Point, Line, Polygon o Exception 
        si no es de ningún tipo anterior.
        """
        capa=self.get_capa_nombre(nomCapa)
        if capa==None:
            return Exception("La capa " + nomCapa + " no esta activada o no existe en este proyecto.")
        return self.get_tipoGeomCapa(capa)
    
    def get_tipoGeomCapa(self,capa):
        """
        Recibe un objeto QgsVectorLayer y devuelve Point, Line, Polygon o Exception 
        si no es de ningún tipo anterior.
        """
        if capa==None:
            return Exception("La capa es None.")

        tipoGeomCapaQgs=str(capa.geometryType())#devuelve 0,1,2. Que sigunifica Point, Line, Polygon
        if tipoGeomCapaQgs=="0":
            return "Point"
        elif tipoGeomCapaQgs=="1":
            return "Line"
        elif tipoGeomCapaQgs=="2":
            return "Polygon"
        else:
            return Exception("El tipo de capa no es ni Point, ni Line, ni Polygon")
        
    def cargarCapaPostgis(self,borrarSiExiste ,host, database,usuario,password,port,nombreCompletoTabla,campoGeom,condicionSeleccion,campoGid,almacenarCredenciales=False):
        """
        Carga una capa de postgis.
        @type borrarSiExiste: boolean
        @param borrarSiExiste: Si es true, si existe la capa, la borra la capa y la vuelve a cargar: 
        @type host: string
        @param host: direccción ip de del servidor que tiene instalado postgresql
        @type database: string
        @param database: nombre de la base de datos
        @type usuario: string
        @param usuario: nombre del usuario
        @type password: string
        @param password: contraseña
        @type port: string
        @param port: puerto de la conexión a postgres
        @type nombreCompletoTabla: string
        @param nombreCompletoTabla: nombre de la tabla, incluído el esquema, aunque sea public.
        @type campoGeom: string
        @param campoGeom: nombre del campo de geometría
        @type condicionSeleccion: string
        @param condicionSeleccion: Condición de selección de los registros de la tabla. Ejemplo:
            consMuni=unicode("id_trabajo in (select id_trabajo from ed_comun.ed_trabajos where municipio='{0}')","utf-8")
            consulta=consMuni.format(municipio)
            Si el valor del campo es numérico hay que eliminar las comillas simples: '{0}' pasa a -->{0}
        @type campoGid: string
        @param campoGid: nombre del campo clave de la tabla
        @type almacenarCredenciales: boolean
        @param almacenarCredenciales: Si es true almacena el usuario y la contraseña en el proyecto
            Qgis. Lo almacena en texto plano, por lo que es peligroso. Si es false,
            no almacena esta información en el proyecto. Solicita usuario y contraseña, una vez, 
            al abrir el proyecto, y luego lo usa para el resto de capas. 
        @return: Si la capa existe, devuelve la capa, sin modificar. Si no existía devuelve la nueva capa.
        @raise exception: Genera un error en caso de error
        """
        nombreCapa=nombreCompletoTabla.split(".")[1]
        capa=self.get_capa_nombre2(nombreCapa)
        if capa !=None:
            if borrarSiExiste==True:
                if capa.isEditable()==True:
                    raise Exception("Debe detener la edicion en la capa " + nombreCapa)
                qgis.core.QgsMapLayerRegistry.instance().removeMapLayer(capa.id())
            else:
                return capa
            
        uri = qgis.core.QgsDataSourceURI()
        #uri.setConnection(host, port, database, usuario, password)
        if almacenarCredenciales==False:
            uri.setConnection(host, port, database,"","")
        else:
            uri.setConnection(host, port, database, usuario, password)
        # set database schema, table name, geometry column and optionaly subset (WHERE clause)
        nombres=nombreCompletoTabla.split(".")
        if len(nombres) < 2:
            raise Exception("Falta el nombre del esquema en el nombre de la tabla")
        esquema=nombres[0]
        tabla=nombres[1]

        uri.setDataSource(esquema, tabla, campoGeom, condicionSeleccion,campoGid)
        #uri.setEncodedUri(uri.uri())
        #urie=uri.encodedUri()
        #vlayer=qgis.core.QgsVectorLayer(urie, tabla, "postgres")

        vlayer = qgis.core.QgsVectorLayer(uri.uri(), tabla, "postgres")

        if not vlayer.isValid():
            raise IOError, "Fallo al abrir la capa espacial"
        # add layer to the registry

        qgis.core.QgsMapLayerRegistry.instance().addMapLayer(vlayer)

        return vlayer
        # set extent to the extent of our layer
        #self.iface.mapCanvas().setExtent(vlayer.extent())