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
    Formulario para guardar datos en la tabla comun.trabajos o ed_comun.ed_trabajos.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para guardar datos en la tabla comun.trabajos o ed_comun.ed_trabajos.
"""
from PyQt4 import QtCore, QtGui
import sys
import datetime
from ctrIntrodDatos import ctrIntrodDatos

import sys
"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""

class ctrIntrodDatos_Ntrab(ctrIntrodDatos):
    """
    Permite la introducción de datos en la base de datos de un nuevo trabajo.
    """
    #constructor
    def __init__(self, oUtiles,tabla):

        #Ejecuta el constructor de la clase padre ctrIntroddatos
    
        ctrIntrodDatos.__init__(self,oUtiles,tabla)
        self.setModoNuevo()
        self.connect(self.ui.bttGuardar, QtCore.SIGNAL("clicked()"),self.guarda)
        self.ui.tbSrc_trabajo.setText(str(self.oUtiles.src_trabajo))
    def guarda(self):
        resp=self.cargaDicValoresCompleto_delFormulario(True)#extrae los datos del formulario
            #y prepara el diccionario con los valores que seran enviados a la bda
        if resp==False:
            return
        
        #src=self.dicEnviar["src_trabajo"]
        
        self.dicEnviar.update([["estado_trabajo",unicode("edicion","utf-8")]])
        self.dicValoresCompleto.update([["estado_trabajo",unicode("edicion","utf-8")]])
        returning=["id_trabajo"]
        
        if self.getModo()=="nuevo":
            self.dicEnviar.update([["src_trabajo",unicode(str(self.oUtiles.src_trabajo),"utf-8")]])
            self.dicValoresCompleto.update([["src_trabajo",unicode(str(self.oUtiles.src_trabajo),"utf-8")]])
            self.dicEnviar.update([["municipio",self.oUtiles.municipio]])
            self.dicValoresCompleto.update([["municipio",self.oUtiles.municipio]])
            self.ui.lbEstado.setText("Enviando los datos a la base de datos. Por favor espere ...")
            self.dicEnviar.update([["usuario",unicode(self.oUtiles.oConsultasPg.oConectaPg.usuario,"utf-8")]])
            self.dicValoresCompleto.update([["usuario",unicode(self.oUtiles.oConsultasPg.oConectaPg.usuario,"utf-8")]])
            if self.archivoBytea!=None:
                resp=self.oUtiles.oConsultasPg.insertaDatosDic(self.nomTabla,self.dicEnviar,"archivo", False, None,None,returning)
            else:
                resp=self.oUtiles.oConsultasPg.insertaDatosDic(self.nomTabla,self.dicEnviar,None, False, None,None,returning)                
            if isinstance(resp, Exception):
                mens=unicode("Error. El servidor respondió: ","utf-8")
                mens=mens + resp.message
                self.ui.lbEstado.setText(mens)
            else:
                self.oUtiles.usuario_creador_trabajo=self.oUtiles.usuario 
                self.ui.lbEstado.setText("OK. Datos guardados.")
                self.setEstadoGuardado("guardado")
                datosInsertados=self.oUtiles.oConectaPg.cursor.fetchall()
                id_trabajo=datosInsertados[0][0]#primera fila, primer valor
                #self.oUtiles.src_trabajo=src
                self.oUtiles.id_trabajo=id_trabajo
                self.ui.tbId_trabajo.setText(str(self.oUtiles.id_trabajo))
                #self.ui.tbSrc_trabajo.setText(src)
                self.setModoConsultar()#así la próxima vez que le de a guardar, se modifica el
                self.tablaCambiada=False                      #misno trabajo
                self.actualizarArchivoBytea=False
                self.setListaSubDirDescargas(["memoria"])#directorio para la descaga de la memoria
                
        elif self.getModo()=="editar":
            if self.tablaCambiada==False:
                #no ha cambiado nada. No hace falta enviar los datos
                self.setModoConsultar()
                self.ui.lbEstado.setText("No se han realizado cambios en la tabla")
                return
            """
            if src!=self.oUtiles.src_trabajo:
                self.ui.lbEstado.setText("No se puede cambiar el src de un trabajo. Debe borrarlo y empezar de nuevo, o conservar el src original: " + self.oUtiles.src_trabajo)
                return
            """
            condicionWhere="id_trabajo= %s"
            listaValoresCondWhere=[self.oUtiles.id_trabajo]
            if self.actualizarArchivoBytea==False:
                #dic es el diccionario a enviar sin la clace "archivo"
                resp=self.oUtiles.oConsultasPg.updateDatos(self.nomTabla,self.dicEnviar.keys(), self.dicEnviar.values(),None, False, None,None,condicionWhere,listaValoresCondWhere)
            else:
                resp=self.oUtiles.oConsultasPg.updateDatos(self.nomTabla,self.dicEnviar.keys(), self.dicEnviar.values(),"archivo", False, None,None,condicionWhere,listaValoresCondWhere)
            if isinstance(resp, Exception):
                mens=unicode("Error. El servidor respondió: ","utf-8")
                mens=mens + resp.message
                self.ui.lbEstado.setText(mens)
            else:
                self.ui.lbEstado.setText("OK. Datos actualizados")
                self.setModoConsultar()
                self.actualizarArchivoBytea=False
                self.tablaCambiada=False

    def bttBorrar(self):#sobre escribo el metodo de la clase base
        mens=unicode("Borrar este registro implica borrar todos los datos de este trabajo. ¿Está seguro?.","utf-8")
        reply = QtGui.QMessageBox.question(self, "Advertencia", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return

        dicCondiciones={}
        if "id_trabajo" in self.dicValoresCompleto:
            dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        if "id" in self.dicValoresCompleto:
            dicCondiciones["id"]=self.dicValoresCompleto.get("id")
        elif "gid" in self.dicValoresCompleto:
            dicCondiciones["gid"]=self.dicValoresCompleto.get("gid")
        resp=self.oUtiles.oConsultasPg.deleteDatos(self.nomTabla,dicCondiciones)
        if isinstance(resp, Exception):
            mens="La consulta " + self.oUtiles.oConsultasPg.consulta + " es erronea. El servidor respondio: " + resp.message   
        else:
            mens="Ok. Trabajo borrado."
        self.ui.lbEstado.setText(mens)
        self.setModoNuevo()
        self.estadoGuardado="no guardado"
        self.oUtiles.src_trabajo=None
        self.oUtiles.id_trabajo=None
        self.oUtiles.usuario_creador_trabajo=None