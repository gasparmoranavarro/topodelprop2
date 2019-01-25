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
    Formulario guardar datos de las fincas, incluida la geometría. 
    Hereda de ctrIntrodDatos_NGeom.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario guardar datos de las fincas, incluida la geometría. 
    Hereda de ctrIntrodDatos_NGeom.
"""

import sys
from ctrIntrodDatos_N import ctrIntrodDatos_N
from ctrIntrodDatos_NGeom import ctrIntrodDatos_NGeom
from PyQt4 import QtGui

import sys #librería estándar de python

'''
if sys.platform=='linux2':
    sys.path.append('/opt/liclipse/plugins/org.python.pydev_5.1.2.201606231040/pysrc')
    #sys.path.append('/home/joamona/.eclipse/org.eclipse.platform_3.8_155965261/plugins/org.python.pydev_4.4.0.201510052309/pysrc')
    ##pydevd.settrace()
else:
    sys.path.append("C:/LiClipse/plugins/org.python.pydev_3.9.2.201502042042/pysrc" )
import pydevd #lo marca como error, pero en tiempo de ejecución funciona
'''


class ctrIntrodDatos_NFinca(ctrIntrodDatos_NGeom):
    """
    Añade fincas a la base de datos. Este controlador añade dos propiedades nuevas
    a ctrIntrodDatos_NGeom:
        - self.tipoFinca: Puede ser Rustica o Urbana
        - self.dlgTipoFinca: cuadro de dialogo para la tabla ref_cat_rus o ref_cat_urb,
            según sea self.tipoFinca.
    Dependiendo de si el usuario introduce en el cuadro de dialogo de los datos de la finca, 
    en el campo tipo_finca_Cat, Rustica o Urbana, se crea el cuadro adecuado para la
    introducción en una u otra tabla.
    """
    #constructor
    def __init__(self, oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo=False,dicValoresAdd=None, geomWkt=None,esMulti=False):
        """
        La documentación de este constructor es la misma que la del constructor de la clase
        ctrIntrodDatos_NGeom. 
        """

        ctrIntrodDatos_NGeom.__init__(self, oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo,dicValoresAdd, geomWkt,esMulti)
 
        self.dlgTipoFinca=None
        self.tipoFinca=None
        
    def guarda(self):
        """
        Guarda los datos de la finca y crea el cuadro de diálogo para introducir los datos 
        catastrales de rústica o urbana, y lo almacena en self.dlgTipoFinca.
        Si el usuario cambia la finca de rústica a urbana, o viceversa, hay que borrar los datos
        anticuados en la tabla ref_cat_rus o ref_cat_urb. Esto debe hacerse desde un disparador
        en la base de datos.
        """
       
        if self.getModo()=="nuevo":
            self.borra_overlaps()#borro antes de guardar, porque es al guardar cuando
            #se dibujan los gaps, si no hay superposicion
            ctrIntrodDatos_NGeom.guarda(self)
            #pydevd.settrace()
            self.oUtiles.gid_finca=self.dicValoresCompleto.get("gid")
            if self.estadoGuardado!="guardado":
                self.dibuja_overlaps()#comprueba que el problema fue una superposicion
                                #y la dibuja
                
                
            self.tipoFinca=self.sacaTipoFinca()
            self.set_dlgTipoFinca()
        else: 
            resp=self.cargaDicValoresCompleto_delFormulario(True)
            self.oUtiles.gid_finca=self.dicValoresCompleto.get("gid")
            if resp==False:
                return
            tipo_finca=self.sacaTipoFinca()
            
            
            
            if self.tipoFinca==tipo_finca:
                #no ha cambiado el tipo de Finca
                ctrIntrodDatos_NGeom.guarda(self)
                #self.oUtiles.gid_finca=self.dicValoresCompleto.get("gid")
            else:
                #ha cambiado el tipo de Finca
                
                mens=unicode("Ha cambiado el tipo de finca catastral de " + self.tipoFinca + " a " + tipo_finca, "utf-8")
                mens1=unicode(". Esto implica borrar los datos catastrales anteriores.","utf-8")
                mens2=unicode(" ¿Seguro que desea continuar?","utf-8")
                mens=mens + mens1 + mens2
                reply = QtGui.QMessageBox.question(self, "Advertencia", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    #hay que cepillarse los anteriores datos y el anterior cuadro de dialogo
                    #los anteriores datos se eliminan con un disparador en la base de datos.
                    #cuando cambia el tipo de Finca, se borran los datos anteriores en la tabla
                    #del tipo de Finca anterior
                                        
                    self.dlgTipoFinca.bttBorrar(darMens=False)
                    
                    ctrIntrodDatos_NGeom.guarda(self)
                    #self.oUtiles.gid_finca=self.dicValoresCompleto.get("gid")
                    self.tipoFinca=tipo_finca
                    self.set_dlgTipoFinca()
                else:
                    self.ui.lbEstado.setText("Establezca el tipo de finca catastral a " + self.tipoFinca)
                    return
                
    def sacaTipoFinca(self):
        tipo_finca=self.dicValoresCompleto.get("tipo_finca_catastral")
        if tipo_finca==unicode("Rústica","utf-8"):
            return "Rustica"
        elif tipo_finca==unicode("Urbana","utf-8"):
            return "Urbana"
        else:
            return False
    def set_tipoFinca(self):
        self.tipoFinca=self.sacaTipoFinca()   
    def set_dlgTipoFinca(self, cargarDeBda=False):
        """
        Comprueba que no se haya cambiado el tipo de Finca. En tal caso, se eliminan
        los datos anteriores de la base de datos y se muestra un cuadro de dialogo nuevo.
        para que añada el gid del Finca que describe
        """
        gid=self.dicValoresCompleto.get("gid")
        dicValoresAdd={}
        dicValoresAdd["gid_finca"]=gid
        if self.tipoFinca=="Rustica":
            nomTabla=self.oUtiles.get_nomTabla("ref_cat_rus")
        elif self.tipoFinca=="Urbana":
            nomTabla=self.oUtiles.get_nomTabla("ref_cat_urb")
        else:
            self.dlgTipoFinca=None
            return False
        if cargarDeBda==False:
            self.dlgTipoFinca=ctrIntrodDatos_N(self.oUtiles,nomTabla,self.listaSubDirDescargas,mostrarBttNuevo=True, dicValoresAdd=dicValoresAdd)
        else:
            dlg=ctrIntrodDatos_N(self.oUtiles,nomTabla,self.listaSubDirDescargas,mostrarBttNuevo=True,dicValoresAdd=dicValoresAdd)
            resp=dlg.setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones=dicValoresAdd)
            self.dlgTipoFinca=dlg
            return resp
    def get_dlgTipoFinca(self):
        return self.dlgTipoFinca
    def get_tipoFinca(self):
        return self.tipoFinca

    def dibuja_overlaps(self):
        """
        Dibuja la parte de solape de la finca que se intenta insertar
        en la capa ed_overlaps_fincas o overlaps_fincas.
        Este programa no envia la geometria en el modo editar, por lo que no es
        necesario programar nada en ese modo.
        Antes de insertar el solape en la capa gaps, borra lo que había antes para el id_trabajo
        actual, por si se habia intentado insertar antes una geometria con solape, en cuyo caso
        habria un poligono antiguo del error del anterior intento de insercion
        """
        mens=self.ui.lbEstado.text()
        if "Error de superposicion." in mens:
            #script.comprueba_overlaps_wkt(geom_wkt varchar, epsg varchar, 
            #nom_tabla_comprobar varchar,nom_tabla_overlaps varchar, 
            #nom_campo varchar,valor_campo integer, VariaDic gid_excluir integer[]) RETURNS boolean AS $$
            nomTabla=self.nomTabla.split(".")[1]
            nomTablaComprobar="src" + str(self.oUtiles.src_trabajo) + "." + "fincas"
            dicCondWhere={}
            dicCondWhere["id_trabajo"]=self.oUtiles.id_trabajo
            if nomTabla == "ed_fincas":
                nomTablaOverlaps="ed_src" + str(self.oUtiles.src_trabajo) + "." + "ed_overlaps_fincas"
                self.oUtiles.oConectaPg.cursor.callproc("script.comprueba_overlaps_wkt",[self.geomWkt,str(self.oUtiles.src_trabajo),nomTablaComprobar,nomTablaOverlaps,"id_trabajo",self.oUtiles.id_trabajo,-1])
            else:
                nomTablaOverlaps="src" + str(self.oUtiles.src_trabajo) + "." + "overlaps_fincas"
                self.oUtiles.oConectaPg.cursor.callproc("script.comprueba_overlaps_wkt",[self.geomWkt,str(self.oUtiles.src_trabajo),nomTablaComprobar,nomTablaOverlaps,"id_trabajo",self.oUtiles.id_trabajo,-1])
            self.oUtiles.oConectaPg.conn.commit()
    def borra_overlaps(self):
        """
        borra la parte de solape de la finca y los gaps, si los habia
        para ese trabajo.
        Los overlaps se dibujan desde self.dibuja_overlaps. Pero los gaps,
        los dibuja directamente el disparador que hay sobre la tabla fincas
        geom_fincas_def, o geom_fincas_ed
        """
        nomTabla=self.nomTabla.split(".")[1]
        dicCondWhere={}
        dicCondWhere["id_trabajo"]=self.oUtiles.id_trabajo
        if nomTabla == "ed_fincas":
            nomTablaOverlaps="ed_src" + str(self.oUtiles.src_trabajo) + "." + "ed_overlaps_fincas"
            nomTablaGaps="ed_src" + str(self.oUtiles.src_trabajo) + "." + "ed_gaps_fincas"
        else:
            nomTablaOverlaps="src" + str(self.oUtiles.src_trabajo) + "." + "overlaps_fincas"
            nomTablaGaps="src" + str(self.oUtiles.src_trabajo) + "." + "gaps_fincas"
        self.oUtiles.oConsultasPg.deleteDatos(nombreTabla=nomTablaOverlaps,dicCondWhere=dicCondWhere)
        self.oUtiles.oConsultasPg.deleteDatos(nombreTabla=nomTablaGaps,dicCondWhere=dicCondWhere)