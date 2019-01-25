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
    Clase que tiene una serie de herramientas que utilizan todas las clases de la aplicación.
    Todas las clases de la aplicación reciben una variable, denominada oUtiles, que es 
    una instancia de esta clase.
    Esta clase, se utiliza para conectar con la base de datos, seleccionar el src y el 
    municipio, y almacena en sus propiedades objetos de otras clases que es utilizan
    constantemente en todo el programa.
    @author: J. Gaspar Mora Navarro.
    @organization: Universidad Politécnica de Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @contact: topodelprop@gmail.com
    @version: 0.1
    @summary: Clase que tiene una serie de herramientas que utilizan todas las clases de la aplicación.
        Todas las clases de la aplicación reciben una variable, denominada oUtiles, que es 
        una instancia de esta clase.
        Esta clase, se utiliza para conectar con la base de datos, seleccionar el src y el 
        municipio, y almacena en sus propiedades objetos de otras clases que es utilizan
        constantemente en todo el programa.
"""
import os
import sys
import pickle
import datetime

from PyQt4 import QtCore, QtGui
import pyUPVBib.pyGenGas
import pyUPVBib.pyQgsGas
import pyUPVBib.pyPgGas
from TopoDelProp.ctr.ctrConectar import ctrConectar
from TopoDelProp.ctr.ctrMunicipio import ctrMunicipio
import qgis
import qgis.core


"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""

class DirTrabajos(object):
    """
    Busca en el directorio del plugin el archivo dirTrabajos.txt, o en c:/ y lee la primera linea, 
    que debe ser un directorio donde se almacenaran datos de los trabajos realizados.
    El archivo debe estar guardado en codificacion ANSI y no tener espacios ni acentos
    ni enyes.
    
    @return: un string con la ruta. Exception si hay algun problema
    """
    def sacaDir(self):
        if sys.platform!='linux2':
            if sys.platform!='win32':
                raise Exception('Los sitemas operativos soportados son Windows y Linux')
            
        if sys.platform=='linux2':
            import getpass
            usuario=getpass.getuser()
            ruta='/home/' + usuario + '/dirTrabajos.txt'
            if not(os.path.exists(ruta)):
                e=Exception("No se localiza el archivo " + ruta + ". Debe introducir dos guiones despues de la ruta al directorio de los trabajos. Por ejemplo /home/user/trabajos/topoDelProp--.")
                raise e
        #existe el archivo

        else:#WINDOWS
            dirBase=sys.path[2]#directorio base de la aplicaciÃ³n c:/users/.../.qgis/python/plugins
            ruta=dirBase + "/TopoDelProp/dirTrabajos.txt"
            if not(os.path.exists(ruta)):
                ruta="c:/dirTrabajos.txt"
                if not (os.path.exists(ruta)):
                    e=Exception("No se localiza el archivo dirTrabajos.txt. Debe encontrarse en directorio \
        del plugin TopoDelProp, o en c:/ y contener una linea con la ruta a los trabajos, \
        sin acentos ni enyes, y con barras de dividir. Debe introducir dos guiones despues de la ruta. Por ejemplo c:/delProp--. Guarde el archivo con codifiacion ANSI")
                    raise e
                
        #existe el archivo
        try:
            f=open(ruta,"r")
        except Exception,e:
            e.message="No se puede abrir el archivo dirTrabajos.txt, aunque existe. \
No tiene permiso de lectura en el directorio TopoDelProp"
            raise e
        #se ha abierto con exito
        try:
            ruta2= f.readline()
        except Exception,e:
            e.message="El archivo dirTrabajos.txt, del directorio TopoDelProp del plugin \
debe contener una linea con la ruta a los trabajos, sin acentos ni enyes. \
Debe introducir dos guiones (--) despues de la ruta. \
Por ejemplo c:/delProp--, para Windows, o bien /home/user/trabajos/topoDelProp-- en Linux. En Windows guarde el archivo con codifiacion ANSI"
            raise e
        finally:
            f.close()
        if not "--" in ruta2:
            raise Exception("Debe introducir dos guiones (--) inmediatamente despues de la ruta a los trabajos. Por ejemplo c:/delProp--")
        ruta3=ruta2.split("--")[0]#esto lo hago para eliminar el \n del final de linea, que siempre hacia el directorio erroneo
        #se ha leido la primera linea y se ha cerrado el archivo 

        if not(os.path.isdir(ruta3)):
            ee=Exception("La ruta en el archivo dirTrabajos.txt: " + ruta3 + " no es valida. \
Busque el archivo en el directorio TopoDelProp del plugin, o en c:/ e introduzca una linea \
con la ruta a los trabajos, sin acentos ni enyes, y con barras de dividir para separar las carpetas. \
Debe introducir dos guiones despues de la ruta. Por ejemplo c:/delProp--. \
Guarde el archivo con codifiacion ANSI. En Linux debe ser algo asÃ­: /home/user/trabajos/topoDelProp--")
            raise ee
        else:
            return ruta3 #la ruta leida en el achivo es valida

    def sacaLectorPDF(self):
        if sys.platform=='linux2':
            import getpass
            usuario=getpass.getuser()
            ruta='/home/' + usuario + '/dirTrabajos.txt'
            if not(os.path.exists(ruta)):
                e=Exception("No se localiza el archivo " + ruta + ". Debe introducir dos guiones despues de la ruta al directorio de los trabajos. Por ejemplo /home/user/trabajos/topoDelProp--.")
                raise e
        else:
            dirBase=sys.path[2]#directorio base de la aplicaciÃ³n c:/users/.../.qgis/python/plugins
            ruta=dirBase + "/TopoDelProp/dirTrabajos.txt"
            if not(os.path.exists(ruta)):
                ruta="c:/dirTrabajos.txt"
                if not (os.path.exists(ruta)):
                    e=Exception()
                    e.message="No se localiza el archivo dirTrabajos.txt. Debe encontrarse en directorio \
    del plugin TopoDelProp, o en c:/ y contener una linea con la ruta a los trabajos, \
    sin acentos ni enyes, y con barras de dividir. Por ejemplo c:/delProp--. Guarde el archivo con codificacion ANSI"
                    raise e
        
        #existe el archivo
        try:
            f=open(ruta,"r")
        except Exception,e:
            e.message="No se puede abrir el archivo dirTrabajos.txt, aunque existe. \
No tiene permiso de lectura"
            raise e
        #se ha abierto con exito
        try:
            linea1= f.readline()
            linea2=f.readline()
        except Exception,e:
            e.message="El archivo dirTrabajos.txt, \
debe contener una linea con la ruta al programa para \
leer archivos PDF. No podra mostrar archivos PDF con el programa. \
Escriba debajo de la ruta a los trabajos una linea como la siguiente: \
C:/Program Files (x86)/Adobe/Reader 9.0/Reader/AcroRd32.exe--. \
Note los dos guiones al final de la linea. En Linux podria ser evince--"
            raise e
        finally:
            f.close()
        if not "--" in linea2:
            raise Exception("Debe introducir dos guiones (--) inmediatamente despues de la ruta al programa que lee archivos PDF. \
Escriba debajo de la ruta a los trabajos una linea como la siguiente: \
C:/Program Files (x86)/Adobe/Reader 9.0/Reader/AcroRd32.exe--. \
Guarde el archivo con codifiacion ANSI. En Linux podria ser evince--")
        lectorPDF=linea2.split("--")[0]#esto lo hago para eliminar el \n del final de linea, que siempre hacia el directorio erroneo
        
        #se ha leido la segunda linea y se ha cerrado el archivo 
        if sys.platform=='win32':   
            if not(os.path.exists(lectorPDF)):
                ee=Exception()
                ee.message="El programa lector de PDF " + lectorPDF + " no existe. \
    No podra mostrar archivos PDF con el programa. \
    Escriba debajo de la ruta a los trabajos una linea como la siguiente: \
    C:/Program Files (x86)/Adobe/Reader 9.0/Reader/AcroRd32.exe--. \
    Guarde el archivo con codifiacion ANSI"
                raise ee
            
        return lectorPDF #la ruta leida en el achivo es valida

    def listaDir(self):
        filelist = os.listdir("c:/")
        for f in filelist:
            print f
            if os.path.isdir(os.path.join("c:/",f)):
                print "I am a directory"
            else:
                print "I am NO directory"
                
class Utiles(object):
    """
    Este objeto almacena una instancia de todas las clases programadas para este plugin, 
    que son utilidades, y que se usan prácticamente en todos objetos y los métodos del programa
    """    
    def __init__(self):
        self.__tipo_usuario=None
        self.__prefijo_tipo_trabajo=None#puede ser: "ed_", "", o "hist_", para los trabajos 
                        #en edicion, definitivos o en historico
        self.__lector_pdf=None
        self.__usuario=None
        self.__usuario_creador_trabajo=None
        self.__id_trabajo=None
        self.__gid_finca=None
        self.__municipio=None
        self.__src_trabajo=None
        self.__dTrabajos=None
        self.__oConectaPg=None
        self.__oUtilidadesQgs=None
        self.__iface=None
        self.__oArchivos=None
        self.__oConsultasPg=None
        self.__oVarios=None
        self.__oDicDominios=None
        self.__oUtilidadesListas=None
        self.__oUtilidadesFormularios=None
        self.__oUtilidades=None
        self.__tipo_trabajo=None
        self.__tam_pdf_kb=None
        self.__tam_img_kb=None
        self.__carpeta_archivos=""#carpeta para abrir archivos
    #setters
    def __set_carpeta_archivos(self,carpeta_archivos):
        self.__carpeta_archivos=carpeta_archivos    
    def __set_tam_pdf_kb(self,tam_pdf_kb):
        self.__tam_pdf_kb=tam_pdf_kb    
    def __set_tam_img_kb(self,tam_img_kb):
        self.__tam_img_kb=tam_img_kb    
    def __set_tipo_usuario(self,tipo_usuario):
        self.__tipo_usuario=tipo_usuario
    def __set_lector_pdf(self,lector_pdf):
        self.__lector_pdf=lector_pdf
    def __set_usuario(self,usuario):
        self.__usuario=usuario
    def __set_usuario_creador_trabajo(self,usuario_creador_trabajo):
        self.__usuario_creador_trabajo=usuario_creador_trabajo
    def __set_prefijo_tipo_trabajo(self,tipo_trabajo):
        if tipo_trabajo=="Edicion":
            self.__prefijo_tipo_trabajo="ed_"
        elif tipo_trabajo=="Definitivo":
            self.__prefijo_tipo_trabajo=""
        elif tipo_trabajo=="Historico":
            self.__prefijo_tipo_trabajo="hist_"
        else:
            raise Exception("El prefijo del tipo de trabajo no puede ser establecido correctamente.")      
        self.__tipo_trabajo=str(tipo_trabajo)
    def __set_id_trabajo(self,id_trabajo):
        self.__id_trabajo=id_trabajo

    def __set_gid_finca(self,gid_finca):
        self.__gid_finca=gid_finca


    def __set_src_trabajo(self,src_trabajo):
        self.__src_trabajo=str(src_trabajo)
    def __set_municipio(self,municipio):
        self.__municipio=municipio
    def __set_dTrabajos(self,dTrabajos):
        self.__dTrabajos=dTrabajos
    def __set_oConectaPg(self,oConectaPg):
        self.__oConectaPg=oConectaPg
    def __set_oUtilidadesQgs(self,oUtilidadesQgs):
        self.__oUtilidadesQgs=oUtilidadesQgs
    def __set_iface(self,iface):
        self.__iface=iface
    def __set_oArchivos(self,oArchivos):
        self.__oArchivos=oArchivos
    def __set_oConsultasPg(self,oConsultasPg):
        self.__oConsultasPg=oConsultasPg
    def __set_oVarios(self,oVarios):
        self.__oVarios=oVarios
    def __set_oUtilidadesListas(self,oUtilidadesListas):
        self.__oUtilidadesListas=oUtilidadesListas
    def __set_oUtilidadesFormularios(self,oUtilidadesFormularios):
        self.__oUtilidadesFormularios=oUtilidadesFormularios
    def __set_oUtilidades(self,oUtilidades):
        self.__oUtilidades=oUtilidades
    def set_oDicDominios(self):
        """
        Carga el diccionario de dominios en la propiedad __oDicDominios
        Se hace si no se ha hecho ya.
        De esta forma, solo se cargan los valores de los dominios si hace falta,
        al crear, o editar trabajos. En estos casos hay que llamar a este método,
        antes de usar esta propiedad, de lo contrario, será None.
        @return: True si todo va bien. Exception si hay algún error. 
        """
        if self.oConsultasPg==None: 
            return Exception("Primero debe inicializar la propiedad oConsultasPg")
        if self.__oDicDominios==None:
            oDicDominios=self.__getOdicDominios()
            if isinstance(oDicDominios,Exception):
                return oDicDominios#ahí va la descripcion del error
            else:
                self.__oDicDominios=oDicDominios
                return True#todo ha ido bien
        else:
            return True

    #getters 
    def __get_carpeta_archivos(self):
        return self.__carpeta_archivos 
    def __get_tam_pdf_kb(self):
        return self.__tam_pdf_kb 
    def __get_tam_img_kb(self):
        return self.__tam_img_kb   
    def __get_tipo_usuario(self):
        return self.__tipo_usuario
    def __get_lector_pdf(self):
        return self.__lector_pdf
    def __get_usuario(self):
        return self.__usuario
    def __get_usuario_creador_trabajo(self):
        return self.__usuario_creador_trabajo
    def __get_prefijo_tipo_trabajo(self):
        return self.__prefijo_tipo_trabajo
    def __get_tipo_trabajo(self):
        return self.__tipo_trabajo
    def __get_id_trabajo(self):
        return self.__id_trabajo

    def __get_gid_finca(self):
        return self.__gid_finca
    
    def __get_src_trabajo(self):
        return self.__src_trabajo
    def __get_municipio(self):
        return self.__municipio
    def __get_oUtilidadesListas(self):
        return self.__oUtilidadesListas
    def __get_dTrabajos(self):
        return self.__dTrabajos
    def __get_oConectaPg(self):
        return self.__oConectaPg
    def __get_oUtilidadesQgs(self):
        return self.__oUtilidadesQgs
    def __get_iface(self):
        return self.__iface
    def __get_oArchivos(self):
        return self.__oArchivos
    def __get_oConsultasPg(self):
        return self.__oConsultasPg      
    def __get_oVarios(self):
        return self.__oVarios  
    def __get_oDicDominios(self):
        return self.__oDicDominios
    def __get_oUtilidadesFormularios(self):
        return self.__oUtilidadesFormularios
    def __get_oUtilidades(self):
        return self.__oUtilidades

    def get_nomTabla(self,tabla):
        """
        Recibe el nombre de una tabla y, si tiene un punto, es que no es para un esquema espacial,
        entonces antepone "ed_", tanto al nombre del esquema como al nombre de la tabla, 
        o nada, en funcion de si el tipo de trabajo es en edicion
        o definitivo. El prefijo se localiza en la propiedad self.prefijo_tipo_trabajo. 
        Si no tiene punto, antepone a la tabla "ed_srcXXXXX.ed_" o bien "srcXXXXX.",
        tambien, en función de si el tipo de trabajo es en edición o definitivo. Las XXXXX
        corresponden al src del trabajo actual, localizado en self.src_trabajo.
        Por ejemplo, si self.prefijo_tipo_trabajo es ed_, es una tabla en edicion:
            - get_nomTabla("comun_trabajos") devuelve: "ed_comun.ed_trabajos"
            - get_nomTabla("lindes") devuelve: "ed_srcXXXXX.ed_lindes"
        Si self.prefijo_tipo_trabajo es vacio, es una tabla definitiva:
            - get_nomTabla("comun_trabajos") devuelve: "comun.trabajos"
            - get_nomTabla("lindes") devuelve: "srcXXXXX.lindes"       
        Si self.prefijo_tipo_trabajo es "hist_", es una tabla del historico:
            - get_nomTabla("comun_trabajos") devuelve: "hist_comun.hist_trabajos"
            - get_nomTabla("lindes") devuelve: "hist_srcXXXXX.hist_lindes"             
        @type tabla: string
        @param tabla: nombre de la tabla. Antepone una cosa u otra en función de si lleva punto o no:
        """
        
        prefijoTipoTrabajo=self.prefijo_tipo_trabajo
        lista=tabla.split(".")
        if len(lista)>1:#no es espacial
            #nomTabla= prefijoTipoTrabajo + tabla
            nomTabla=prefijoTipoTrabajo + lista[0] + "." + prefijoTipoTrabajo + lista[1]
        else:
            nomTabla= prefijoTipoTrabajo + "src" + self.src_trabajo + "." + prefijoTipoTrabajo + tabla
        return str(nomTabla)

    def get_nomCapaQgis(self,opcionMenuElegida,nomCapa):
        """
        Recibe la opción elegiga del menu principar ctrPpal, que puede ser nuevo o buscar-editar,
        el nombre de una capa espacial (lindes, imagenes, servidumbres, ...), y
        en función del tipo de trabajo, devuelve dxf_nomCapa, ed_nomCapa, nomCapa o hist_nomCapa.
        Si el usuario utilizo la opcion "buscar-editar", si es el autor del trabajo,  y, si el
        tipo de trabajo es en Edicion, puede que
        desee añadir elementos graficos al trabajo. En ese caso, si en Qgis:
            - Si solo está la capa dxf_nomCapa, se devuelve dxf_nomCapa
            - Si solo está la capa ed_nomCapa, se devuelve ed_nomCapa
            - Si están ambas:
                - Si hay elementos seleccionados en dxf_nomCapa,
                    y es el autor del trabajo, o el administrador, se devuelve dxf_nomCapa,
                    para que pueda añadir elementos. Se pueden añadir elementos nuevos 
                    a la base de datos, pero no editar los existentes ed_nomCapa. Para
                    ello, debe primero deseleccionar los elementos de dxf_nomCapa.
                - Si no hay elementos seleccionados en dxf_nomCapa devuelve ed_nomcapa. 
                    En este caso, si es el autor del trabajo, o el administrador, 
                    puede editar los datos del trabajo actual, sin añadir nuevos.
        @type opcionMenuElegida: string
        @param opcionMenuElegida: Puede ser nuevo, o buscar-editar
        @type nomCapa: string
        @param nomCapa: nombre de la capa que se buscará en Qgis. Ejemplo: "lindes".
        @return: un string con el nombre de la capa a buscar. Si se introduce "lindes",
            se puede obtener "dxf_lindes","ed_lindes","lindes","hist_lindes", o None.
            Se devuelve None en el caso de que la opcion sea buscar-editar y no esté,
            o esté desactivada, la capa dxf_nomCapa, ni ed_nomCapa en Qgis.
        """
        nomCapaQgs=None
        if opcionMenuElegida=="nuevo":
            nomCapaQgs="dxf_" + nomCapa
        elif opcionMenuElegida=="buscar-editar":
            #puede ser trabajos en edicion o definitivos
            if self.tipo_trabajo=="Definitivo":
                capa=self.oUtilidadesQgs.get_capa_nombre(nomCapa)
                if capa==None:
                    nomCapaQgs=None
                else:
                    """
                    nomCapaQgs=nomCapa
                    """
                    #puede ser nom_capa o dxf_nom_capa, si quiere añadir algo. Veamos si hay selección en la capa dxf_nom_capa
                    nomCapaDxf="dxf_" + nomCapa
                    capaDxf=self.oUtilidadesQgs.get_capa_nombre(nomCapaDxf)
                    if capaDxf==None:
                        #no hay capa dxf_nombre en qgis
                        nomCapaQgs=nomCapa
                    else:
                        #la capa dxf_nombre existe. Veamos si hay elementos seleccionados
                        nf = capaDxf.selectedFeatureCount()
                        if nf!=0:
                            #si hay selección, que en la capa dxf, que devuelva la capa dxf_nom_capa
                            nomCapaQgs=nomCapaDxf
                        else:
                            nomCapaQgs=nomCapa
            elif self.tipo_trabajo=="Historico":
                nomCapaQgs="hist_" + nomCapa
            elif self.tipo_trabajo=="Edicion":
                #puede ser dxf_nomCapa, si quiere añadir nuevos lindes
                #o ed_nomCapa, si quiere cambiar algo
                nomCapaDxf="dxf_" + nomCapa
                capaDxf=self.oUtilidadesQgs.get_capa_nombre(nomCapaDxf)
                nomCapaEd="ed_" + nomCapa
                capaEd=self.oUtilidadesQgs.get_capa_nombre(nomCapaEd)
                if capaDxf!=None and capaEd==None:
                    if self.usuario == self.usuario_creador_trabajo or self.tipo_usuario=="admin_propiedad":
                        nomCapaQgs=nomCapaDxf
                    else:
                        nomCapaQgs=nomCapaEd
                elif capaDxf==None and capaEd!=None:
                    nomCapaQgs=nomCapaEd
                elif capaDxf!=None and capaEd!=None:
                    if self.usuario == self.usuario_creador_trabajo or self.tipo_usuario=="admin_propiedad":
                        nf = capaDxf.selectedFeatureCount()
                        if nf!=0:
                            nomCapaQgs=nomCapaDxf
                        else:
                            nomCapaQgs=nomCapaEd
                    else:
                        nomCapaQgs="ed_" + nomCapa
                else:
                    nomCapaQgs=None
        return nomCapaQgs
    def __getOdicDominios(self):
        """
        @return: El dicionario de valores de los dominios, sea leidos de un pickle o de la base de datos
        """
        nomPickle=self.dTrabajos + "/Dom/oDicDominios.dat"#archivo con los datos de los dominios
        if os.path.exists(nomPickle):
            #los dominios estan guardados. Los cargo.
            fPic=open(nomPickle, "r")
            oDicDominios=pickle.load(fPic)
            fPic.close()
            lista=oDicDominios.get("fecha_dom")

            fecha_pic=lista[0]#fecha de los dominios que se han cargado. Es la fecha
                #en la que se crearon o modificaron. No es la fecha de descarga.
            self.oConectaPg.cursor.execute("select script.posterior_fecha_dom(%s)",(fecha_pic,))
            resp=self.oConectaPg.cursor.fetchall()
            #devuelve una lista con una tupla de un elemento, que es True o False
            #si es true es necesario actualizar
            tResp=resp[0]
            if tResp[0]==True:
                #se cargan los dominios de la base de datos
                oDicDominios=self.__cargaDicDominiosBDA()
                if isinstance(oDicDominios,Exception):
                    #no se han podido cargar de la base de datos
                    return oDicDominios
                else:
                    #se graban en el pickle y se devuelven para
                    #que se graben en la clase
                    fPic=open(nomPickle,"w")
                    pickle.dump(oDicDominios, fPic)
                    fPic.close()
                    return oDicDominios

            #no es necesario actualizar, se usan los valores del pickle
            return oDicDominios
        else:
        #no existe la ruta al pickle. Hay que crear el directorio,
        #descargar los datos y crear el pickle
            resp=self.__creaDirDom()
            if isinstance(resp,Exception):
                return resp
            #el directorio se ha creado bien
            oDicDominios=self.__cargaDicDominiosBDA()
            if isinstance(oDicDominios,Exception):
                #no se han podido cargar de la base de datos
                return oDicDominios
            else:
                #se graban en el pickle y se devuelven para
                #que se graben en la clase
                fPic=open(nomPickle,"w")
                pickle.dump(oDicDominios, fPic)
                fPic.close()
                return oDicDominios           

#        QtGui.QMessageBox.information(None,"Herramienta sin programar" , "Primera tabla" + tabla,1)
    
    
    def __cargaDicDominiosBDA(self):
        oDicDominios={}#creo el diccionario

        oCursor=self.oConsultasPg.sacaNombreTablasEsquema_cursor("dom")
        if isinstance(oCursor,Exception):
            return oCursor
        numTablas=oCursor.rowcount
        if numTablas==0:
            return Exception("No hay tablas en el esquema " + "dom")
        listaTablas=oCursor.fetchall()#es una lista de tuplas.
            #cada tupla es una fila. En este caso, la fila tiene un
            #unico elemento, que es el nombre de la tabla.
            #tipoDevuelto=listaTablas[0].__class__.__name__
        for fila in listaTablas:
            #nomTabla=fila[0].encode("utf-8")
            nomTabla=fila[0]
            nomTablaCompleta="dom." + nomTabla
            #oCursor=oConsultasPg.sacaNombresCamposTabla("dom", nomTabla)
            listaCampos=[]
            listaCampos.append(nomTabla)#el campo del dominio se llama como la tabla
            oCursor=self.oConsultasPg.recuperaDatosTablaBytea(nomTablaCompleta, listaCampos)
            if isinstance(oCursor,Exception):
                return oCursor
            numFilas=oCursor.rowcount
            if numFilas==0:
                return Exception("No hay registros en la tabla dom." + nomTabla)          
            listaValores=oCursor.fetchall()#es una lista de tuplas.
                #cada tupla es una fila. En este caso, la fila tiene un
                #unico elemento, que es el valor del dominio.
            lvDef=[]#lista de valores de la tabla
            #depende del ordenador pysycopg2 devuelve str o unicode.
            #los valores de las listas siempre estan en unicode.
            #los nombres de las tablas no les hago nada porque no tienen caracteres extraños
            for fila2 in listaValores:
                valor=fila2[0]
                """
                if isinstance(valor,basestring):
                    valor=valor.encode("utf-8")
                """
                lvDef.append(valor)
            oDicDominios[nomTabla]=lvDef
        return oDicDominios       
    
    def __creaDirDom(self):
        """
        Crea el directorio para los trabajos, si no existe.
        Crea el directorio para guardar el pickle con los dominios \Dom, si no existe
        @type dirTrabajos: string 
        @param dirTrabajos: directorio para guardar datos de los trabajos
        @return: Devuelve True si todo va bien, en caso contrario una instancia del error
        """
        #compruebo que existe el directorio para los trabajos, y si no
        nomDir=self.dTrabajos
        if not(os.path.isdir(nomDir)):
        #si no existe lo creo
            try:
                os.mkdir(nomDir)
            except Exception, e:
                e.message=unicode(e.message,"utf-8")
                QtGui.QMessageBox.information(self,"Error al intentar crear la carpeta para los trabajos" , "Carpeta: " + nomDir,1)
                QtGui.QMessageBox.information(self,"Descripcion del error de Python" , e.message,1)
                return e
        nomDir=nomDir+"/Dom"
        if not(os.path.isdir(nomDir)):
        #si no existe lo creo
            try:
                os.mkdir(nomDir)
            except Exception, e:
                e.message=unicode(e.message,"utf-8")
                QtGui.QMessageBox.information(self,"Error al intentar crear la carpeta para los dominios" , "Carpeta: " + nomDir,1)
                QtGui.QMessageBox.information(self,"Descripcion del error de Python" , e.message,1)
                return e
    tam_pdf_kb=property(__get_tam_pdf_kb,__set_tam_pdf_kb,"Tamaño máximo admintido para archivos PDF")   
    tam_img_kb=property(__get_tam_img_kb,__set_tam_img_kb,"Tamaño máximo admitido para archivos de imagen. Las imágenes son reducidas de forma automática a este tamaño.")   
      
    tipo_usuario=property(__get_tipo_usuario,__set_tipo_usuario,"Tipo de usuario. Puede ser: consultor_autorizado, editor, o admin_propiedad")   
    usuario=property(__get_usuario,__set_usuario,"Usuario actual del programa")   
    usuario_creador_trabajo=property(__get_usuario_creador_trabajo,__set_usuario_creador_trabajo,"Usuario que creó el trabajo")       
    id_trabajo=property(__get_id_trabajo,__set_id_trabajo,"Numero de trabajo actual") 
    gid_finca=property(__get_gid_finca,__set_gid_finca,"Numero de finca actual") 
    prefijo_tipo_trabajo=property(__get_prefijo_tipo_trabajo,__set_prefijo_tipo_trabajo,"Puede ser 'ed_', '', o 'hist_', en funcion del tipo de trabajo: Edicion, Definitivo o Historico, respectivamente.") 
    tipo_trabajo=property(__get_tipo_trabajo,"Puede ser 'Edicion', 'Definitivo', o 'Historico'.") 
    src_trabajo=property(__get_src_trabajo,__set_src_trabajo,"Codigo EPSG del trabajo. Se utiliza para saber el esquema donde se encuentran las lablas espaciales. Si src_trabajo=='25830', esquema = 'src25830'") 
    municipio=property(__get_municipio,__set_municipio,"Municipio del trabajo. Se utiliza para cagar unicamente los datos espaciales del municipio") 
    dTrabajos=property(__get_dTrabajos,__set_dTrabajos,"Directorio para los trabajos") 
    oConectaPg=property(__get_oConectaPg,__set_oConectaPg,"Objeto de la clase ConectaPg") 
    oUtilidadesQgs=property(__get_oUtilidadesQgs,__set_oUtilidadesQgs,"Objeto de la clase UtilidadesQgs") 
    iface=property(__get_iface,__set_iface,"Objeto iface mediante el cual se interactua con qGis") 
    oArchivos=property(__get_oArchivos,__set_oArchivos,"Objeto de la clase Archivos") 
    oConsultasPg=property(__get_oConsultasPg,__set_oConsultasPg,"Objeto de la clase ConsultasPg") 
    oVarios=property(__get_oVarios,__set_oVarios,"Objeto de la clase utils.Varios, con utilidades varias") 
    oDicDominios=property(__get_oDicDominios,"Dicionario con todos los valores de los dominios de las tablas. La clave es el nombre de la tabla, el valor es una lista con los valores del dominio")
    oUtilidadesListas=property(__get_oUtilidadesListas,__set_oUtilidadesListas,"Utilidades para trabajar con listas")
    oUtilidadesFormularios=property(__get_oUtilidadesFormularios,__set_oUtilidadesFormularios,"Utilidades para trabajar con formularios")
    oUtilidades=property(__get_oUtilidades,__set_oUtilidades,"Utilidades de todo tipo")
    lector_pdf=property(__get_lector_pdf,__set_lector_pdf,"Ruta y nombre del programa para leer .PFD. Por ejemplo C:/Program Files (x86)/Adobe/Reader 9.0/Reader/AcroRd32.exe")
    carpeta_archivos=property(__get_carpeta_archivos,__set_carpeta_archivos,"Carpeta para la seleccion de archivos a subir")
class InicializaUtiles(object):
    """
    Solicita host, base de datos, usuario y contraseña mediante un cuadro de dialogo.
    Si consigue conectar y se inicializa todo, devuelve un objeto Utiles,
    en caso contrario, genera una excepción con la descripcion del error.
    @raise exception: Se genera en el caso de que alguna variable
        de la clase Utiles devuelta no se pueda inicializar. En cada caso
        se genera una descripcion del erro personalizado.
    """
    def __init__(self,iface):
        """
        @type  iface: qgsIface
        @param iface: Objeto que permite interactuar con Qgis. 
        """
        #Ejecuta el constructor de la clase padre QDialog
 
        self.iface=iface
        self.utiles=Utiles()
        #inicializa los utiles
        self.inicializa()
        
    def inicializa(self):
        """
        Crea una instancia de todos los objetos que necesita la clase Utiles
        y los guarda en self.utiles, una variable de clase que
        es una instancia de la clase Utiles. Si no puede crear alguna instancia
        lanza un error.
        No inicializa la propiadad oUtiles.oDicDominios
        De esta forma, solo se cargan los valores de los dominios si hace falta,
        al crear, o editar trabajos. En estos casos hay que llamar al método
        oUtiles.set_oDicDominios()
        antes de usar esta propiedad, de lo contrario, oUtiles.oDicDominios, será None.
        Hace una consulta a la tabla comun.usuarios para ver el tipo de usuario que
        se conecta. Luego lo guara en oUtiles.tipo_usuario
        @raise  exception: Lanza un error en el caso de que no pueda inicializar
            alguna variable.
        """
        oTr=DirTrabajos()
        dTrabajos=oTr.sacaDir()#prueba a ver si es todo correcto
        if isinstance(dTrabajos,Exception):
            #si no es correcto muestra un cuadro de dialogo para
            #que elija un directorio para los trabajos, e intenta
            #guardar la ruta en DirTrabajos.txt, en la ruta del plugin
            #si no puede prueba a guadar el archivo en c:/DirTrabajos.txt
            #si no puede genera un error
            from TopoDelProp.ctr.ctrDirTrabajos import ctrDirTrabajos
            dlg=ctrDirTrabajos(self.iface)
            dlg.show()
            dlg.exec_()
            dTrabajos=oTr.sacaDir()
            if isinstance(dTrabajos,Exception):
                raise Exception(dTrabajos.message)
        lectorPDF=oTr.sacaLectorPDF()
        if not(isinstance(lectorPDF,Exception)):
            self.utiles.lector_pdf=lectorPDF
        else:
            raise Exception(lectorPDF.message)
        dlg = ctrConectar(self.iface)
        dlg.show()
        dlg.exec_()
        oConectaPg=dlg.getOConectaPg()
        dlg.hide()
        if oConectaPg==None:
            raise Exception("No ha intentado conectar con la base de datos")
        if oConectaPg.conectado==False:
            raise Exception(oConectaPg.descripcion_error)

        oConsultas=pyUPVBib.pyPgGas.ConsultasPg(oConectaPg)
        oUtilidadesQgs=pyUPVBib.pyQgsGas.UtilidadesQgs(self.iface)
        oUtilidadesListas=pyUPVBib.pyGenGas.UtilidadesListas()
        oUtilidadesFormularios=pyUPVBib.pyGenGas.UtilidadesFormularios()
        oUtilidades=pyUPVBib.pyGenGas.Utilidades()
        oArchivos=pyUPVBib.pyPgGas.Archivos() 
        oVarios=Varios()
        cursor=oConsultas.recuperaDatosTablaBytea("comun.usuarios", ["tipo_usuario"], "usuario=%s",[oConectaPg.usuario])             
        if isinstance(cursor,Exception):
            raise Exception(cursor.message + "Su tipo de usuario no tiene acceso a la aplicacion, aunque puede cargar las capas espaciales desde Qgis.")
        n=cursor.rowcount
        if not(n == 1):
            raise Exception("No existe el usuario " + str(oConectaPg.usuario) + ". No tiene permiso para usar la aplicacion." )
        self.utiles.usuario=oConectaPg.usuario
        tuplaValores=cursor.fetchone()#saca una fila
        self.utiles.tipo_usuario=tuplaValores[0]
        
        condicionWhere="tipo_usuario=%s"
        #settrace()
        listaDic=oConsultas.recuperaDatosTablaByteaDic("dom.config", ["con_timeout","statement_timeout"], condicionWhere,[self.utiles.tipo_usuario])
        if isinstance(listaDic,Exception):
            mens=unicode("Error al descargar el tiempo de espera: ","utf-8") + listaDic.message
            raise Exception(mens)
        if len(listaDic)!=1:
            mens=unicode("Error en inicializaUtiles. Numero de registros seleccionados en dom.config:. Puede que tenga desactivados los privilegios. Consulte al administrador","utf-8")
            raise Exception(mens)
        connection_timeout=listaDic[0].get("con_timeout")
        statement_timeout=listaDic[0].get("statement_timeout")
        if connection_timeout==None:
            mens=unicode("Error. con_timeout en dom.config resultó None.","utf-8")
            raise Exception(mens)
        if statement_timeout==None:
            mens=unicode("Error. statement_timeout en dom.config resultó None.","utf-8")
            raise Exception(mens)

        #conecta de nuevo con el tiempo que le corresponde
        oConectaPg.cierraConexion()
        oConectaPg=pyUPVBib.pyPgGas.ConectaPg(database=oConectaPg.database, user=oConectaPg.usuario, password=oConectaPg.password,host=oConectaPg.host,port=oConectaPg.port,connection_timeout=connection_timeout,statement_timeout=statement_timeout)
        oConsultas=pyUPVBib.pyPgGas.ConsultasPg(oConectaPg)

        #recupera los tamaños mínimos de archivos PDF e imagen
        listaDic=oConsultas.recuperaDatosTablaByteaDic("dom.cfg_tamanos", ["tam_pdf_kb","tam_img_kb"])
        if isinstance(listaDic,Exception):
            mens=unicode("Error al descargar el los tamaños máximos de los archivos: ","utf-8") + listaDic.message
            raise Exception(mens)
        if len(listaDic)!=1:
            mens=unicode("Error en inicializaUtiles. Numero de registros seleccionados en dom.cfg_tamanos: .","utf-8")
            raise Exception(mens)
        tam_pdf_kb=listaDic[0].get("tam_pdf_kb")
        tam_img_kb=listaDic[0].get("tam_img_kb")
    
        if tam_pdf_kb==None or tam_img_kb==None or tam_pdf_kb < 100 or tam_img_kb < 100:
            mens=unicode("Error. Algunos de los tamaños de la tabla dom.cfg_tamanos es inválido. O es Null, o es menor de 100.","utf-8")
            raise Exception(mens)
        
        self.utiles.tam_pdf_kb=tam_pdf_kb
        self.utiles.tam_img_kb=tam_img_kb
        self.utiles.iface=self.iface
        self.utiles.dTrabajos=dTrabajos
        self.utiles.oConectaPg=oConectaPg
        self.utiles.oConsultasPg=oConsultas
        self.utiles.oArchivos=oArchivos
        self.utiles.oUtilidadesQgs=oUtilidadesQgs
        self.utiles.oUtilidadesListas=oUtilidadesListas
        self.utiles.oVarios=oVarios
        self.utiles.oUtilidadesFormularios=oUtilidadesFormularios
        self.utiles.oUtilidades=oUtilidades
        try:
            self.utiles.set_oDicDominios()
        except Exception, e:
            raise Exception("Error descargando los domunios: " + e. message)
        
        dlg = ctrMunicipio(self.utiles)
        dlg.show()
        dlg.exec_()
        dlg.hide()
        if dlg.get_municipio()==None:
            raise Exception("No ha seleccionado un municipio")
        else:
            self.utiles.municipio=dlg.get_municipio()
            if dlg.get_src()==None:
                raise Exception("No ha seleccionado un SRC")
            else:
                self.utiles.src_trabajo=dlg.get_src()#es una cadena unicode 
    def getUtiles(self):
        """
        En el caso de que no se haya lanzado un error, devuelve un objeto
        inicializado de la clase Utiles
        """
        return self.utiles
    
class Varios(object):
    def sacaEsquemaTablaConUri(self,uri,nomTabla,dbname="propiedad"):
        """saca el esquema de una tabla con la cadena uri de conexion a postgis
        de la capa uri=capa.layer.dataProvider().dataSourceUri()
        esquema= oVarios.sacaEsquemaTablaConUri(uri)
        dbname='propiedad' host=localhost port=5432 user='xxx' sslmode=disable key='gid' srid=25830 type=POINT table="ed_src25830"."img_linde" (geom)
        @type nomTabla: string
        @param nomTabla: nombre de la tabla sin esquema
        @type uri: string
        @type dbname: string
        @param dbname: base de datos postgis de donde se carga la capa
        @param uri: cadena uri de conexion a postgis de la capa. uri=capa.provider.dataSourceUri()
        @return: string con el esquema de la tabla, None si la capa no era de la base de
            datos dbname 
        """
        
        uri2=str(uri)
        db="dbname=\'" + dbname + "\'"
        if not(db in uri2):
            return None
        pos=uri2.find("table=",0,len(uri2)-1)
        pos = pos+7 #inicio del nombre del esquema
        pos2=uri2.find(nomTabla,pos,len(uri2)-1)
        pos2=pos2-3
        esquema=uri2[pos:pos2]
        return esquema

    def cargaCapas(self,tipoTrabajo, oUtiles,borrarSiExiste):
        """
        tipoTrabajo puede ser 'edicion' o 'definitivo'
        """
        host=oUtiles.oConectaPg.host
        database=oUtiles.oConectaPg.database
        usuario=oUtiles.oConectaPg.usuario
        password=oUtiles.oConectaPg.password
        port=oUtiles.oConectaPg.port
        municipio=oUtiles.municipio
        src=str(oUtiles.src_trabajo)
        
        tablas=["fincas","parcelas_afectadas","lindes","img_linde","elem_interiores","servidumbres"]
        
        if tipoTrabajo=="definitivo":
            prefijo_src="src"
            prefijo_tabla=""
            tablaTrabajos="comun.trabajos"
        else:
            prefijo_src="ed_src"
            prefijo_tabla="ed_"
            tablas.append("overlaps_fincas")
            tablas.append("gaps_fincas")
            tablaTrabajos="ed_comun.ed_trabajos"
        for tabla in tablas:
            tablaCompleto=prefijo_src + src + "." + prefijo_tabla + tabla
            consulta=self.generaConsultaMunicipio(tablaTrabajos=tablaTrabajos, municipio=municipio)
            try:
                oUtiles.oUtilidadesQgs.cargarCapaPostgis(borrarSiExiste=borrarSiExiste,host=host, database=database,usuario=usuario,password=password,port=port,nombreCompletoTabla=tablaCompleto,campoGeom="geom",condicionSeleccion=consulta,campoGid="gid")
            except Exception, e:
                QtGui.QMessageBox.information(oUtiles.iface.mainWindow(),"Hubo un problema", "No se cargo la capa: " + tablaCompleto + "Error: " + e.message,1)

    def cargaCapasErrorDef(self, oUtiles,borrarSiExiste):
        """
        tipoTrabajo puede ser 'edicion' o 'definitivo'
        """
        host=oUtiles.oConectaPg.host
        database=oUtiles.oConectaPg.database
        usuario=oUtiles.oConectaPg.usuario
        password=oUtiles.oConectaPg.password
        port=oUtiles.oConectaPg.port
        municipio=oUtiles.municipio
        src=str(oUtiles.src_trabajo)
        
        tablas=["gaps_fincas","overlaps_fincas"]

        prefijo_src="src"
        prefijo_tabla=""
        tablaTrabajos="comun.trabajos"

        for tabla in tablas:
            tablaCompleto=prefijo_src + src + "." + prefijo_tabla + tabla
            consulta=self.generaConsultaMunicipio(tablaTrabajos=tablaTrabajos, municipio=municipio)
            try:
                oUtiles.oUtilidadesQgs.cargarCapaPostgis(borrarSiExiste=borrarSiExiste,host=host, database=database,usuario=usuario,password=password,port=port,nombreCompletoTabla=tablaCompleto,campoGeom="geom",condicionSeleccion=consulta,campoGid="gid")
            except Exception, e:
                QtGui.QMessageBox.information(oUtiles.iface.mainWindow(),"Hubo un problema", "No se cargo la capa: " + tablaCompleto + "Error: " + e.message,1)

    
    def generaConsultaMunicipio(self,tablaTrabajos,municipio):
        """
        tablaEspacial: nombre completo, incluyendo el esquema
        Genera la consulta para que solo se carguen los elementos del municipio
        """
        consMuni=unicode("id_trabajo in (select id_trabajo from {0} where municipio='{1}')","utf-8")
        consulta=consMuni.format(tablaTrabajos,municipio)
        return consulta               
   
        