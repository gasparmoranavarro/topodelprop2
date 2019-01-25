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
    Formulario para guardar datos en tablas de geometría. El campo de geometría debe
    llamarse geom.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario guardar datos de las fincas, incluida la geometría. 
    Hereda de ctrIntrodDatos_NGeom.
"""
from PyQt4 import QtCore
import sys
from ctrIntrodDatos import ctrIntrodDatos

#sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
#from pydevd import *

class ctrIntrodDatos_NGeom(ctrIntrodDatos):
    """
    Permite la introducción de datos en la base de datos, en tablas que tienen un campo
    de geometría. El campo debe llamarse geom. También debe tener un campo denominado
    id o gid, serial y primary key.
    
    La tabla puede tener un único campo Bytea, y debe llamarse "archivo".
    """
    #constructor
    def __init__(self, oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo=False,dicValoresAdd=None, geomWkt=None,esMulti=False):
        """
        La documentación de este constructor es la misma que la del constructor de la clase
        ctrIntrodDatos_N. Se añaden dos parámetros más geomWkt y esMulti, que se describen a continuación.
        
        IMPORTANTE: En el modo editar no envía los datos geométricos a la base de datos.
        solo lo hace en modo nuevo. Si hay que cambiar la geometría de un objeto,
        se debe hacer gráficamente desde QGis, u otro SIG.
        
        IMPORTANTE: Si se modifica una geometría con QGIS, las áreas, perímetros, etc
        no se actualizan en el formulario inmediatamente. Hay que recargar el trabajo.
        
        @type geomWkt: string
        @param geomWkt: Cadena con las coordenadas del elemento. Se obtiene con
            - dic=self.oUtiles.oUtilidadesQgs.get_attrElementoCapa(objeto, capa, listaCampos,geom=True)
            - geomWkt=dic.get("geom")
            Vea la documentación de la clase UtilidadesQgs, en el módulo gen.general.
        @type featureID: integer
        @param featureID: ID del elemento QGis. Se utiliza para poder seleccionarlo
            al visualizar el cuadro de dialogo
        @type  esMulti: Booleano
        @param esMulti: Si es False, se deja como estaba, si no, se convierte a multi.
            Si ya era multi, no hace nada.
        """
        ctrIntrodDatos.__init__(self,oUtiles,tabla)
        self.setListaSubDirDescargas(listaSubDirDescargas)#directorio para la descaga de la memoria
        self.ui.tbId_trabajo.setText(str(self.oUtiles.id_trabajo))
        self.ui.tbSrc_trabajo.setText(str(self.oUtiles.src_trabajo))
        
        self.mostrarBttNuevo=mostrarBttNuevo
        self.dicValoresAdd=dicValoresAdd
    
        self.connect(self.ui.bttGuardar, QtCore.SIGNAL("clicked()"),self.guarda)
        self.connect(self.ui.bttNuevo, QtCore.SIGNAL("clicked()"),self.bttNuevo)
        self.geomWkt=geomWkt
        self.esMulti=esMulti
        self.featureId=None#es el mismo que el gid en postgis. Sirve para seleccionar el elemento en qgis
        self.dxf_featureId=None
        self.dicValoresAdd=dicValoresAdd
        self.setModoNuevo()
        
    def guarda(self):
        """
        Guarda el registro.
        """
        resp=self.cargaDicValoresCompleto_delFormulario(True)#extrae los datos del formulario
            #y prepara el diccionario con los valores que seran enviados a la bda
        if resp==False:
            return
        self.dicEnviar.update([["id_trabajo",self.oUtiles.id_trabajo]])
        if self.dicValoresAdd!=None:
            self.dicEnviar.update(self.dicValoresAdd.items())
            self.dicValoresCompleto.update(self.dicValoresAdd.items())
        if "id" in self.dicValoresCompleto:
            returning=["id"]
        else:
            returning=["gid"]
        
        if "area_utm" in self.dicValoresCompleto:
            returning.append("area_utm")
        if "area_elip" in self.dicValoresCompleto:
            returning.append("area_elip")
        if "perim_utm" in self.dicValoresCompleto:
            returning.append("perim_utm")
        if "lon_utm" in self.dicValoresCompleto:
            returning.append("lon_utm")   
        if "e_max_area_99" in self.dicValoresCompleto:
            returning.append("e_max_area_99")         
        #inserto una noticia para que algun warnig anterior no sea el ultimo
        self.oUtiles.oConectaPg.cursor.callproc("script.genera_noticia",["ok"])

        if self.getModo()=="nuevo":
            if self.geomWkt != None:#esto sera cierto si estamos en modo nuevo
                #se hace aquí porque si es modo consultar y se ha cargado de la
                #BDA sera none y se machacaría la geometria al entrar en modo editar
                self.dicEnviar.update([["geom",self.geomWkt]])

            self.ui.lbEstado.setText("Enviando los datos a la base de datos. Por favor espere ...")
            #nombreTabla,dicValores,nombreCampoBytea=None, esMulti=False, nombreCampoGeom=None, epsg=None, returning=None):
            
            if self.archivoBytea!=None:
                resp=self.oUtiles.oConsultasPg.insertaDatosDic(self.nomTabla,self.dicEnviar,"archivo", self.esMulti,"geom",self.oUtiles.src_trabajo,returning)
            else:
                resp=self.oUtiles.oConsultasPg.insertaDatosDic(self.nomTabla,self.dicEnviar,None, self.esMulti,"geom",self.oUtiles.src_trabajo,returning)                
            if isinstance(resp, Exception):
                mens="Error. El servidor respondio: "
                mens=mens + resp.message
                self.ui.lbEstado.setText(mens)
            else:
                resp=self.mensajes_ok()
                if resp==False:
                    #inserto una noticia para que el warnin no sea el ultimo
                    #self.oUtiles.oConectaPg.cursor.callproc("script.genera_noticia",["ok"])
                    return
                filas=self.oUtiles.oConectaPg.cursor.fetchall()
                if len(filas)==0:
                    self.ui.lbEstado.setText(self.toUtf8("No se insertó ninguna fila"))
                    return
                if "id" in self.dicValoresCompleto:
                    idd=filas[0][0]
                    self.dicValoresCompleto.update([["id",idd]])
                else:
                    gid=filas[0][0]
                    self.dicValoresCompleto.update([["gid",gid]])
                    self.featureId=gid
                if "area_utm" in returning:#es un poligono. Tiene las dos areas y el perimetro
                    areaUTM=filas[0][1]
                    areaELIP=filas[0][2]
                    perimUTM=filas[0][3]
                    e_max_area_99=filas[0][4]
                    self.dicValoresCompleto.update([["area_utm",areaUTM]])
                    self.dicValoresCompleto.update([["area_elip",areaELIP]])
                    self.dicValoresCompleto.update([["perim_utm",perimUTM]])
                    self.dicValoresCompleto.update([["e_max_area_99",e_max_area_99]])                               
                elif "lon_utm" in returning:#es un arco
                    lonUTM=filas[0][1]
                    self.dicValoresCompleto.update([["lon_utm",lonUTM]])
                #self.ui.lbEstado.setText("OK. Datos guardados.")
                self.setEstadoGuardado("guardado")
                self.setModoConsultar(self.mostrarBttNuevo)
                self.tablaCambiada=False
                self.actualizarArchivoBytea=False
                
        elif self.getModo()=="editar":
            #la geometría no se reenvía a la base de datos. Hay que modificarla
            #en las capas ed_, o definitivas
            if self.tablaCambiada==False:
                #no ha cambiado nada. No hace falta enviar los datos
                self.setModoConsultar(self.mostrarBttNuevo)
                self.ui.lbEstado.setText("No se han realizado cambios en la tabla")
                return
            lvCondWhere=[]
            lCamposCondWhere=[]
            idd=self.dicValoresCompleto.get("id")
            if idd !=None:
                lvCondWhere.append(idd)
                lCamposCondWhere.append("id")
            gid=self.dicValoresCompleto.get("gid")
            if gid !=None:
                lvCondWhere.append(gid)
                lCamposCondWhere.append("gid")
            lvCondWhere.append(self.oUtiles.id_trabajo)
            lCamposCondWhere.append("id_trabajo")
            condicionWhere=self.oUtiles.oConsultasPg.oGeneraExpresionesPsycopg2.generaWhere(lCamposCondWhere, "and")
            #dicEnviar=self.oUtiles.oUtilidades.eliminaEltosDicLClaves(self.dicEnviar,["geom"])

            if self.actualizarArchivoBytea==False:
                #dic es el diccionario a enviar sin la clave "archivo"
                self.dicEnviar=self.oUtiles.oUtilidades.eliminaEltosDicLClaves(self.dicEnviar,["nom_arch","archivo"])
                #updateDatos(self,nombreTabla,listaCampos, listaValores,nombreCampoBytea=None, esMulti=False, nombreCampoGeom=None, epsg=None, condicionWhere=None, listaValoresCondWhere=None,returning=None)
                resp=self.oUtiles.oConsultasPg.updateDatos(self.nomTabla,self.dicEnviar.keys(), self.dicEnviar.values(),None, esMulti=False, nombreCampoGeom=None,epsg=None,condicionWhere=condicionWhere,listaValoresCondWhere=lvCondWhere)
            else:
                resp=self.oUtiles.oConsultasPg.updateDatos(self.nomTabla,self.dicEnviar.keys(), self.dicEnviar.values(),"archivo", esMulti=False,nombreCampoGeom=None,epsg=None,condicionWhere=condicionWhere,listaValoresCondWhere=lvCondWhere)

            if isinstance(resp, Exception):
                mens=unicode("Error. El servidor respondió: ","utf-8")
                mens=mens + resp.message
                self.ui.lbEstado.setText(mens)
            else:
                resp=self.mensajes_ok()
                #inserto una noticia
                self.oUtiles.oConectaPg.cursor.callproc("script.genera_noticia",["ok"])
                if resp==False:
                    #inserto una noticia para que el warnin no sea el ultimo
                    return
                #self.ui.lbEstado.setText("OK. Datos actualizados")
                self.setModoConsultar(self.mostrarBttNuevo)
                self.actualizarArchivoBytea=False
                self.tablaCambiada=False
    def get_featureId(self):
        return self.featureId
    def set_dxf_featureId(self,dxf_featureId):
        """
        Se utiliza para seleccionar el elemento en la capa dxf
        """
        self.dxf_featureId=dxf_featureId
    def mensajes_ok(self):
        """
        Devuelve true o false. True si se ha insertado el registro,
        o False si no se ha insertado.
        """
        nfilas=self.oUtiles.oConectaPg.cursor.rowcount#filas afectadas
        noticias=self.oUtiles.oConectaPg.conn.notices
        if not(noticias is None):
            if len(noticias)>0:
                mens=noticias[len(noticias)-1]#el ultimo mensaje
            else:
                mens=""#no habia mensajes
        else:
            mens=""
                    
        if nfilas==0:
            if "WARNING" in mens:
                self.ui.lbEstado.setText(mens)
            else:
                self.ui.lbEstado.setText(self.toUtf8("Error. No se grabó el registro. Probablemente por problemas de solape. Examine la capa ed_overlaps_fincas"))
            return False
        else:
            if "WARNING" in mens:
                #se ha insertado pero hay un warning. Probablemente por un gap
                self.ui.lbEstado.setText("Registro insertado: " + mens)
            else:
                self.ui.lbEstado.setText("OK. Datos guardados.")  
        return True
                        
    def get_dxf_featureId(self):
        """
        Se utiliza para seleccionar el elemento en la capa dxf
        """
        return self.dxf_featureId
    def setModoConsultar(self, mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones=None):
        """
        Al cagar el registro de la base de datos inicializa self.featureId. Esto es necesario
        para seleccionar los elementos en qgis desde ctrPpal.
        """
        resp=ctrIntrodDatos.setModoConsultar(self, mostrarBttNuevo, dicValoresCompleto, dicCondiciones)

        self.featureId=self.dicValoresCompleto.get("gid")
        return resp

    def bttNuevo(self):
        """
        Elimina los valores del formulario y permite introducir un registro nuevo en la
        base de datos.
        """
        self.cargaDicValoresCompletoBDAVacios()#no los carga, unicamente elimina sus valores
        self.setModoNuevo()