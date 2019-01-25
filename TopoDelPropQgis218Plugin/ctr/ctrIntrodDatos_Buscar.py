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
    Formulario para realizar búsquedas en la base de datos.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario para realizar búsquedas en la base de datos.
"""
from PyQt4 import QtCore, QtGui
import sys
import datetime
from ctrIntrodDatos import ctrIntrodDatos
from ctrSelec import ctrSelec

import sys
"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""
class ctrIntrodDatos_Buscar(ctrIntrodDatos):
    #constructor
    """
    Realiza la seleccion de registros en la base de datos que coincida con todas
    las condiciones introducidas en el cuadro de dialogo.
    Lanza otro cuadro de dialogo (A) que muestra los registros seleccionados para
    que el usuario elija uno.
    Al cerrar el cuadro de dialogo (A), se obtiene el numero de fila seleccionada,
    con ella se obtiene el valor del campo clave, especificado en el parámetro nomCampoClave
    especificado en el constructor, y se establecen las propiedades
    de esta clase: self.id_trabajo, y self.src_trabajo. Si la tabla no era la de
    trabajos self.src_trabajo vale -1. Si la tabla no tiene el campo id_trabajo,
    self.id_trabajo vale -1
    @return: el valor del campo clave o -1 si hay algún problema.
    """
    def __init__(self, oUtiles,tablaBuscar,nomCampoClave="id_trabajo"):
        """
        Inicializa el cuadro de dialogo con la configuracion de buscar.
        @type oUtiles: utiles
        @param oUtiles: objeto de la clase utiles
        @type tablaBuscar: string
        @param tablaBuscar: Nombre de la tabla donde se va a buscar. Ej: comun.trabajos.
        @type nomCampoClave: string
        @param nomCampoClave: Campo clave a recuperar del registro seleccionado
        """

        #Ejecuta el constructor de la clase padre ctrIntroddatos

        ctrIntrodDatos.__init__(self,oUtiles,tablaBuscar)
        self.setModoBuscar()
        self.connect(self.ui.bttBuscar, QtCore.SIGNAL("clicked()"),self.busca)
        self.__id_trabajo=-1
        if self.oUtiles.src_trabajo==None:
            self.__src_trabajo=-1
        else:
            self.__src_trabajo=self.oUtiles.src_trabajo
        self.nomCampoClave=nomCampoClave
        
    def busca(self):
        """
        Realiza la seleccion de registros en la base de datos que coincida con todas
        las condiciones introducidas en el cuadro de dialogo.
        Lanza otro cuadro de dialogo (A) que muestra los registros seleccionados para
        que el usuario elija uno.
        Al cerrar el cuadro de dialogo (A), se obtiene el numero de fila seleccionada,
        con ella se obtiene el numero de trabajo, y se establecen las propiedades
        de esta clase: self.id_trabajo, y self.src_trabajo. Si la tabla no era la de
        trabajos self.src_trabajo vale -1.
        """
        resp=self.cargaDicValoresCompleto_delFormulario(False)#extrae los datos del formulario 
            #y prepara el diciconario self.dicEnviar, con los valores de la consulta        
        if resp==False:
            return
        condicionWhere="tipo_usuario=%s"
        listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic("dom.config", ["limite"], condicionWhere,[self.oUtiles.tipo_usuario])
        if isinstance(listaDic,Exception):
            mens=unicode("Error al descargar el número máximo de registros: .","utf-8")
            mens=mens + listaDic.message
            self.ui.lbEstado.setText(mens)
            return
        if len(listaDic)!=1:
            mens=unicode("Error numero de registros seleccionados en dom.config: .","utf-8")
            mens=mens + unicode(str(len(listaDic)))
            self.ui.lbEstado.setText(mens)
            return
        limiteRegistros=listaDic[0].get("limite")
        if limiteRegistros==None:
            mens=unicode("Error. El número máximo de registros (limite) en dom.config resultó None.","utf-8")
            self.ui.lbEstado.setText(mens)
            return
            
        if "id" in self.listaNomCampos:
            campoOrderBy="id"
        elif "gid" in self.listaNomCampos:
            campoOrderBy="gid"
        elif "id_trabajo" in self.listaNomCampos:
            campoOrderBy="id_trabajo"
        else:
            mens=unicode("Es necesario que en la tabla esté uno de los siguientes campos: id, gid o id_trabajo.","utf-8")
            self.ui.lbEstado.setText(mens)
            return
        self.dicEnviar=self.oUtiles.oUtilidades.eliminaEltosDicLValores(self.dicValoresCompleto,[None])

        if len(self.dicEnviar)==0:#no se ha rellenado ningun campo de busqueda
            mens=unicode("No se ha especificado ningún criterio de búsqueda. Se mostrarán un máximo de: ","utf-8")
            mens=mens + unicode(str(limiteRegistros)) + " registros."
            reply = QtGui.QMessageBox.question(self, "Aviso", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply != QtGui.QMessageBox.Yes:
                return
            else:
                #se selecciona toda la tabla
                self.ui.lbEstado.setText("Buscando coincidencias en la base de datos. Por favor espere ...")
                listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(self.nomTabla, self.listaNomCampos)
        else:        
            condicionWhere=self.oUtiles.oConsultasPg.oGeneraExpresionesPsycopg2.generaWhere(self.dicEnviar.keys(),"and")
            self.ui.lbEstado.setText("Buscando coincidencias en la base de datos. Por favor espere ...")
            listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(self.nomTabla, self.listaNomCampos, condicionWhere,self.dicEnviar.values(),orderBy=campoOrderBy,limit=limiteRegistros)
        
        if isinstance(listaDic, Exception):
            mens=unicode("Error. El servidor respondió: ","utf-8")
            mens=mens + listaDic.message
            self.ui.lbEstado.setText(mens)
        else:
            if len(listaDic)==0:
                mens=unicode("Ningún registro coincide con los criterios elegidos","utf-8")
                self.ui.lbEstado.setText(mens)
                return
            self.ui.lbEstado.setText("OK. Mostrando datos seleccionados")
            if len(listaDic)==1:
                fila=0
            else:
                dlgSel=ctrSelec(self, listaDic, self.oUtiles.oUtilidadesFormularios)
                fila=dlgSel.exec_()
                if fila==-1:
                    self.ui.lbEstado.setText("Se ha cancelado la seleccion de un registro")
                    self.id_trabajo=-1
                    return
            try:
                self.id_trabajo=listaDic[fila][self.nomCampoClave]
                if self.nomTabla=="ed_comun.trabajos" or self.nomTabla=="comun.trabajos" or self.nomTabla=="hist_comun.trabajos":
                    self.src_trabajo=listaDic[fila]["src_trabajo"]
                self.done(self.id_trabajo) #devuelve el numero de trabajo seleccionado
            except Exception,e:
                QtGui.QMessageBox.information(self,"Error","El campo " +  self.nomCampoClave + " no esta entre los campos de la tabla " + self.nomTabla + ". Este campo es necesario" ,1)#self es la ventana pasdre que necesita qmessagebox
                self.id_trabajo=-1
                self.done(-1)

    def closeEvent(self, event):
        """
        Evento que permite abrir una
        ventana de dialogo para confirmar la salida del programa
        """
        #Se genera la respuesta de la confirmacion de salir
        self.id_trabajo=-1
        self.done(-1)
    def __set_id_trabajo(self,id_trabajo):
        self.__id_trabajo=id_trabajo
    def __get_id_trabajo(self):
        return self.__id_trabajo
    id_trabajo=property(__get_id_trabajo,__set_id_trabajo,"Identificador del trabajo seleccionado. -1 si no hay seleccion")
    
    def __set_src_trabajo(self,src_trabajo):
        self.__src_trabajo=src_trabajo
    def __get_src_trabajo(self):
        return self.__src_trabajo
    src_trabajo=property(__get_src_trabajo,__set_src_trabajo,"SRC del trabajo seleccionado.")
    
            