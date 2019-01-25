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
    Formulario para guardar datos de los lindes. El campo de geometría debe
    llamarse geom.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Formulario guardar datos de los lindes, incluida la geometría. 
    Hereda de ctrIntrodDatos_NGeom.
"""

import sys
from ctrIntrodDatos_N import ctrIntrodDatos_N
from ctrIntrodDatos_NGeom import ctrIntrodDatos_NGeom
from PyQt4 import QtGui

'''
if sys.platform=='linux2':
    sys.path.append('/opt/liclipse/plugins/org.python.pydev_5.1.2.201606231040/pysrc')
    #sys.path.append('/home/joamona/.eclipse/org.eclipse.platform_3.8_155965261/plugins/org.python.pydev_4.4.0.201510052309/pysrc')
    ##pydevd.settrace()
else:
    sys.path.append("C:/LiClipse/plugins/org.python.pydev_3.9.2.201502042042/pysrc" )
import pydevd #lo marca como error, pero en tiempo de ejecución funciona
'''

class ctrIntrodDatos_NLinde(ctrIntrodDatos_NGeom):
    """
    Añade lindes a la base de datos. Este controlador añade dos propiedades nuevas
    a ctrIntrodDatos_NGeom:
        - self.tipoLinde: Puede ser Existente, Replanteado, Digitalizado o Proyectado
        - self.dlgTipoLinde: cuadro de dialogo para la tabla linde_existente, linde_replanteado, ...,
            según sea self.tipoFinca.
    Dependiendo de qué el introduce el usuario en el cuadro de dialogo de los datos del linde, 
    en el campo tipo_linde, se crea el cuadro adecuado para la
    introducción en una u otra tabla.
    """
    def __init__(self, oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo=False,dicValoresAdd=None, geomWkt=None,esMulti=False):
        """
        La documentación de este constructor es la misma que la del constructor de la clase
        ctrIntrodDatos_NGeom. 
        """
        #Ejecuta el constructor de la clase padre ctrIntroddatos
        #pydevd.settrace()
        ctrIntrodDatos_NGeom.__init__(self, oUtiles,tabla,listaSubDirDescargas,mostrarBttNuevo,dicValoresAdd, geomWkt,esMulti)

        self.dlgTipoLinde=None
        self.tipoLinde=None
        
    def guarda(self):
        """
        Guarda los datos del linde y crea el cuadro de diálogo para introducir los datos 
        del linde:replanteado, digitalizado, proyectado, existente y lo almacena en self.dlgTipoLinde.
        Si el usuario cambia el tipo de linde, hay que borrar los datos
        anticuados en la tabla linde_replanteado, linde_medido, ... Esto debe hacerse desde un disparador
        en la base de datos.
        """
        if self.getModo()=="nuevo":
            self.dicValoresCompleto['gid_finca']=self.oUtiles.gid_finca
            ctrIntrodDatos_NGeom.guarda(self)     
            self.tipoLinde=self.sacaTipoLinde()
            self.set_dlgTipoLinde()
        else:#el modo es nuevo.Se guarda normalmente
            resp=self.cargaDicValoresCompleto_delFormulario(True)
            if resp==False:
                return
            tipo_linde=self.sacaTipoLinde()
            if self.tipoLinde==tipo_linde:
                #no ha cambiado el tipo de linde
                
                ctrIntrodDatos_NGeom.guarda(self)
            else:
                #ha cambiado el tipo de linde
                
                mens=unicode("Ha cambiado el tipo de linde de " + self.tipoLinde + " a " + tipo_linde, "utf-8")
                mens1=unicode(". Esto implica borrar los datos del anterior tipo de linde.","utf-8")
                mens2=unicode(" ¿Seguro que desea continuar?","utf-8")
                mens=mens + mens1 + mens2
                reply = QtGui.QMessageBox.question(self, "Advertencia", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    #hay que borrar los anteriores datos y el anterior cuadro de dialogo
                    #los anteriores datos se eliminan desde aquí, y con un disparador en la base de datos.
                    #cuando cambia el tipo de linde, se borran los datos anteriores en la tabla
                    #del tipo de linde anterior
                    
                    #borro los datos del tipo linde anterior
                    self.dlgTipoLinde.bttBorrar(darMens=False)
                    #id_tipo_linde_borrar=self.dlgTipoLinde.dicValoresCompleto.get("id")
                    #dicCondWhere={}
                    #dicCondWhere["id"]=id_tipo_linde_borrar
                    #self.oUtiles.oConsultasPg.deleteDatos(self.dlgTipoLinde.getNomTabla(),dicCondWhere)
                    
                    #creo el nuevo cuadro de dialogo
                    ctrIntrodDatos_NGeom.guarda(self)
                    self.tipoLinde=tipo_linde
                    self.set_dlgTipoLinde()
                else:
                    self.ui.lbEstado.setText("Establezca el tipo de linde a " + self.tipoLinde)
                    return
                
    def sacaTipoLinde(self):
        tipo_linde=self.dicValoresCompleto.get("tipo_linde")
        if tipo_linde==unicode("Digitalizado sobre ortofoto","utf-8"):
            return "Digitalizado"
        elif tipo_linde==unicode("Existe en el terreno","utf-8"):
            return "Existente"
        elif tipo_linde==unicode("No existe en el terreno y se replantea","utf-8"):
            return "Replanteado"
        elif tipo_linde==unicode("Proyectado en algún documento","utf-8"):
            return "Proyectado"
        else:
            return False 
    
    def set_tipoLinde(self):
        self.tipoLinde=self.sacaTipoLinde()        
    def set_dlgTipoLinde(self, cargarDatosDeBda=False):
        """
        Comprueba que no se haya cambiado el tipo de linde. En tal caso, se deben eliminar
        los datos anteriores de la base de datos y se muestra un cuadro de dialogo nuevo.
        La eliminación de los datos debe hacerse desde un disparador en la base de datos.
        """
        gid=self.dicValoresCompleto.get("gid")
        dicValoresAdd={}
        dicValoresAdd["gid_linde"]=gid
        if self.tipoLinde=="Digitalizado":
            nomTabla=self.oUtiles.get_nomTabla("linde_digitalizado")
        elif self.tipoLinde=="Existente":
            nomTabla=self.oUtiles.get_nomTabla("linde_existente")
        elif self.tipoLinde=="Replanteado":
            nomTabla=self.oUtiles.get_nomTabla("linde_replanteado")        
        elif self.tipoLinde=="Proyectado":
            nomTabla=self.oUtiles.get_nomTabla("linde_proyectado")
        else:
            self.dlgTipoLinde=None
            return None
        
        #self.dlgTipoLinde=ctrIntrodDatos_N(self.oUtiles,nomTabla,self.listaSubDirDescargas,False,False,dicValoresAdd)
        self.dlgTipoLinde=ctrIntrodDatos_N(self.oUtiles,nomTabla,self.listaSubDirDescargas,mostrarBttNuevo=False, dicValoresAdd=dicValoresAdd)
        if cargarDatosDeBda==True:
            dicCondiciones={}
            dicCondiciones["gid_linde"]=self.dicValoresCompleto.get("gid")
            resp=self.dlgTipoLinde.setModoConsultar(mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones=dicCondiciones)
            if isinstance(resp,Exception):
                #no ha podido cargar los datos
                return resp
            elif resp==None:
                #no ha habido ninguno, o más de uno.
                return None
        return True
    def get_dlgTipoLinde(self):
        return self.dlgTipoLinde
    def get_tipoLinde(self):
        return self.tipoLinde