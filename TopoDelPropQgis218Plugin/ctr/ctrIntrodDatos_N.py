# -*- coding: utf-8 -*-
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
    Formulario para guardar datos en la base de datos. Hereda de ctrIntrodDatos, y le añade
    el método guardar. Puede utilizarse para cualquier tabla.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para guardar datos en la base de datos. Hereda de ctrIntrodDatos, y le añade
        el método guardar. Puede utilizarse para cualquier tabla.
"""
from PyQt4 import QtCore
import sys
from ctrIntrodDatos import ctrIntrodDatos
"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""
class ctrIntrodDatos_N(ctrIntrodDatos):
    """
    Permite la introducción de datos en en tablas de la base de datos.
    La tabla puede tener un único campo Bytea, y debe llamarse "archivo".
    También debe tener un campo denominado id o gid, serial y primary key.
    """
    #constructor
    def __init__(self, oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo=False, dicValoresAdd=None):
        """
        Inicializa el cuadro de dialogo.
        
        @type oUtiles: utils.Utiles
        @param oUtiles: Objeto de la clase utiles
        @type tabla: string
        @param tabla: Nombre de la tabla que se va a mostrar. Ej: comun.trabajos
        @param subDirDescargas: String
        @type subDirDescargas: subtirectorio que se usará para descargar el archivo bytea, si hay. 
            El subdirectorio será creado.
        @type mostrarBttNuevo: Boolean
        @param mostrarBttNuevo: Si es True muestra el botón nuevo para añadir más registros a la tabla
                @type dicValoresCompleto: None o Diccionario
        @type dicValoresAdd: diccionario
        @param dicValoresAdd: Diccionario nombre_campo: valor a añadir al diccionario 
            self.dicEnviar. Este diccionario es el que se envía a la base de datos.
            Se utiliza para enviar datos que no se preguntan en el cuadro de diálogo,
            por ejemplo el gid_linde.
        """
        #Ejecuta el constructor de la clase padre ctrIntroddatos

        ctrIntrodDatos.__init__(self,oUtiles,tabla)
        self.setListaSubDirDescargas(listaSubDirDescargas)#directorio para la descaga de la memoria
        self.ui.tbId_trabajo.setText(str(self.oUtiles.id_trabajo))
        self.ui.tbSrc_trabajo.setText(str(self.oUtiles.src_trabajo))
        
        self.mostrarBttNuevo=mostrarBttNuevo
        self.dicValoresAdd=dicValoresAdd
        
        self.connect(self.ui.bttGuardar, QtCore.SIGNAL("clicked()"),self.guarda)
        self.connect(self.ui.bttNuevo, QtCore.SIGNAL("clicked()"),self.bttNuevo)
        
        self.setModoNuevo()
        
        
    def guarda(self):
        """
        @type tiene_id_trabajo: booleano
        @param tiene_id_trabajo: Si es false, no añade el campo id_trabajo a la lista
            de valores a enviar a la tabla. Por ejemplo, la tabla usuarios no tiene este campo
        Envía los datos existentes en dicEnviar a la base de datos.
        Antes de hacerlo comprueba que todos los datos son correctos y añade
        los datos de self.dicValoresAdd, si no es None.
            - Si es la primera vez que se guardan los datos, y hay algún problema, no se hace nada.
                Si todo es correcto:
                - Se envían los datos y se pasa a modo "consulta".
            - Si ya se han enviado los datos una vez, se está en modo "editar".
                si todo es correcto:
                - Se envían los datos y se pasa al modo consulta.
        """
        resp=self.cargaDicValoresCompleto_delFormulario(True)#extrae los datos del formulario
            #y prepara el diccionario con los valores que seran enviados a la bda
        if resp==False:
            return
        if "id_trabajo" in self.listaNomCampos:
            self.dicEnviar.update([["id_trabajo",self.oUtiles.id_trabajo]])
        if self.dicValoresAdd!=None:
            self.dicEnviar.update(self.dicValoresAdd.items())
            self.dicValoresCompleto.update(self.dicValoresAdd.items())
        if "id" in self.dicValoresCompleto:
            returning=["id"]
        else:
            returning=["gid"]
        if self.getModo()=="nuevo":
            self.ui.lbEstado.setText("Enviando los datos a la base de datos. Por favor espere ...")
            if self.archivoBytea!=None:
                resp=self.oUtiles.oConsultasPg.insertaDatosDic(self.nomTabla,self.dicEnviar,"archivo", False, None,None,returning)
            else:
                #resp=self.oUtiles.oConsultasPg.insertaDatosDic(self.nomTabla,self.dicEnviar,"archivo", False, None,None,returning)
                resp=self.oUtiles.oConsultasPg.insertaDatosDic(self.nomTabla,self.dicEnviar,None, False, None,None,returning)                
            if isinstance(resp, Exception):
                mens=unicode("Error. El servidor respondió: ","utf-8")
                mens=mens + resp.message
                self.ui.lbEstado.setText(mens)
            else:
                filas=self.oUtiles.oConectaPg.cursor.fetchall()
                if "id" in self.dicValoresCompleto:
                    idd=filas[0][0]
                    self.dicValoresCompleto.update([["id",idd]])
                else:
                    gid=filas[0][0]
                    self.dicValoresCompleto.update([["gid",gid]])   
                self.ui.lbEstado.setText("OK. Datos guardados.")
                self.setEstadoGuardado("guardado")
                #self.setModoConsultar(self.cargarValoresDeBDA, self.mostrarBttNuevo)
                self.setModoConsultar(self.mostrarBttNuevo)
                self.tablaCambiada=False
                self.actualizarArchivoBytea=False
                
        elif self.getModo()=="editar":
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
            if "id_trabajo" in self.listaNomCampos:
                lvCondWhere.append(self.oUtiles.id_trabajo)
                lCamposCondWhere.append("id_trabajo")
            condicionWhere=self.oUtiles.oConsultasPg.oGeneraExpresionesPsycopg2.generaWhere(lCamposCondWhere, "and")
            if self.actualizarArchivoBytea==False:
                #dic es el diccionario a enviar sin la clave "archivo"
                resp=self.oUtiles.oConsultasPg.updateDatos(self.nomTabla,self.dicEnviar.keys(), self.dicEnviar.values(),None, False, None,None,condicionWhere,lvCondWhere)
            else:
                resp=self.oUtiles.oConsultasPg.updateDatos(self.nomTabla,self.dicEnviar.keys(), self.dicEnviar.values(),"archivo", False, None,None,condicionWhere,lvCondWhere)
            if isinstance(resp, Exception):
                mens=unicode("Error. El servidor respondió: ","utf-8")
                mens=mens + resp.message
                self.ui.lbEstado.setText(mens)
            else:
                self.ui.lbEstado.setText("OK. Datos actualizados")
                self.setModoConsultar(self.mostrarBttNuevo)
                self.actualizarArchivoBytea=False
                self.tablaCambiada=False
    
    def bttNuevo(self):
        """
        Elimina los valores del formulario y permite introducir un registro nuevo en la
        base de datos.
        """
        self.cargaDicValoresCompletoBDAVacios()#no los carga, unicamente elimina sus valores
        self.setModoNuevo()