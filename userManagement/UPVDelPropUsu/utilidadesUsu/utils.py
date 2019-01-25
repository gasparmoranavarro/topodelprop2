# -*- coding: utf-8 -*-import sys
'''
Created on 11/05/2012
@author: J. Gaspar Mora Navarro
'''

from PyQt4 import QtCore, QtGui
import pyUPVBib.pyGenGas
import pyUPVBib.pyPgGas
from ctr.ctrConectar import ctrConectar
import sys

class Utiles(object):
    """
    Este objeto almacena una instancia de todas las clases programadas para este plugin,
    que son utilidades, y que se usan prácticamente en todos objetos y los métodos del programa
    """
    def __init__(self):
        self.__oConectaPg=None
        self.__oUtilidadesQgs=None
        self.__iface=None
        self.__oArchivos=None
        self.__oConsultasPg=None
        self.__oUtilidadesListas=None
        self.__oUtilidadesFormularios=None
        self.__oUtilidades=None
        self.id_trabajo=None
        self.src_trabajo=None
        self.oDicDominios=None
        self.tipo_usuario="admin_propiedad"
    #setters
    def __set_oConectaPg(self,oConectaPg):
        self.__oConectaPg=oConectaPg
    def __set_iface(self,iface):
        self.__iface=iface
    def __set_oArchivos(self,oArchivos):
        self.__oArchivos=oArchivos
    def __set_oConsultasPg(self,oConsultasPg):
        self.__oConsultasPg=oConsultasPg
    def __set_oUtilidadesListas(self,oUtilidadesListas):
        self.__oUtilidadesListas=oUtilidadesListas
    def __set_oUtilidadesFormularios(self,oUtilidadesFormularios):
        self.__oUtilidadesFormularios=oUtilidadesFormularios
    def __set_oUtilidades(self,oUtilidades):
        self.__oUtilidades=oUtilidades

    def __get_oUtilidadesListas(self):
        return self.__oUtilidadesListas
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
    def __get_oUtilidadesFormularios(self):
        return self.__oUtilidadesFormularios
    def __get_oUtilidades(self):
        return self.__oUtilidades

    oConectaPg=property(__get_oConectaPg,__set_oConectaPg,"Objeto de la clase ConectaPg")
    iface=property(__get_iface,__set_iface,"Objeto iface mediante el cual se interactua con qGis")
    oArchivos=property(__get_oArchivos,__set_oArchivos,"Objeto de la clase Archivos")
    oConsultasPg=property(__get_oConsultasPg,__set_oConsultasPg,"Objeto de la clase ConsultasPg")
    oUtilidadesListas=property(__get_oUtilidadesListas,__set_oUtilidadesListas,"Utilidades para trabajar con listas")
    oUtilidadesFormularios=property(__get_oUtilidadesFormularios,__set_oUtilidadesFormularios,"Utilidades para trabajar con formularios")
    oUtilidades=property(__get_oUtilidades,__set_oUtilidades,"Utilidades de todo tipo")



class InicializaUtiles(object):
    """
    Solicita host, base de datos, usuario y contraseña mediante un cuadro de dialogo.
    Si consigue conectar y se inicializa todo, devuelve un objeto Utiles,
    en caso contrario, genera una excepción con la descripcion del error.
    @raise exception: Se genera en el caso de que alguna variable
        de la clase Utiles devuelta no se pueda inicializar. En cada caso
        se genera una descripcion del erro personalizado.
    """
    def __init__(self):
        """
        @type  iface: qgsIface
        @param iface: Objeto que permite interactuar con Qgis.
        """
        #Ejecuta el constructor de la clase padre QDialog

        self.iface=None
        self.utiles=Utiles()

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
        app = QtGui.QApplication(sys.argv)#requerido por todas las aplicaciones Qt antes de inicicializar el formulario
        dlg = ctrConectar(self.iface)
        dlg.show()
        app.exec_()#requerido por todas las aplicaciones Qt despues de inicializar el formulario

        oConectaPg=dlg.getOConectaPg()
        if oConectaPg==None:
            raise Exception("No ha intentado conectar con la base de datos")
        if oConectaPg.conectado==False:
            raise Exception(oConectaPg.descripcion_error)

        oConsultas=pyUPVBib.pyPgGas.ConsultasPg(oConectaPg)
        oUtilidadesListas=pyUPVBib.pyGenGas.UtilidadesListas()
        oUtilidadesFormularios=pyUPVBib.pyGenGas.UtilidadesFormularios()
        oUtilidades=pyUPVBib.pyGenGas.Utilidades()
        oArchivos=pyUPVBib.pyPgGas.Archivos()
        cursor=oConsultas.recuperaDatosTablaBytea("comun.usuarios", ["tipo_usuario"], "usuario=%s",[oConectaPg.usuario])
        if isinstance(cursor,Exception):
            raise Exception(cursor.message + "Su tipo de usuario no tiene acceso a la aplicacion, aunque puede cargar las capas espaciales desde Qgis.")
        n=cursor.rowcount
        if not(n == 1):
            raise Exception("No existe el usuario " + str(oConectaPg.usuario) + ". No tiene permiso para usar la aplicacion." )
        self.utiles.usuario=oConectaPg.usuario
        tuplaValores=cursor.fetchone()#saca una fila
        tipo_usuario=tuplaValores[0]
        if tipo_usuario!="admin_propiedad":
            raise Exception("Necesita ser administrador para utilizar esta aplicacion." )
        condicionWhere="tipo_usuario=%s"
        listaDic=oConsultas.recuperaDatosTablaByteaDic("dom.config", ["con_timeout"], condicionWhere,[tipo_usuario])
        if isinstance(listaDic,Exception):
            mens=unicode("Error al descargar el tiempo de espera: ","utf-8") + listaDic.message
            raise Exception(mens)
        if len(listaDic)!=1:
            mens=unicode("Error en inicializaUtiles. Numero de registros seleccionados en dom.config: .","utf-8")
            raise Exception(mens)
        connection_timeout=listaDic[0].get("con_timeout")
        if connection_timeout==None:
            mens=unicode("Error. El tiempo de espera en dom.config resultó None.","utf-8")
            raise Exception(mens)
        #conecta de nuevo con el tiempo que le corresponde
        oConectaPg.cierraConexion()
        #                                    bda, usuario, psw,host2, port, connection_timeout=10
        oConectaPg=pyUPVBib.pyPgGas.ConectaPg(database=oConectaPg.database, user=oConectaPg.usuario, password=oConectaPg.password,host=oConectaPg.host,port=oConectaPg.port,connection_timeout=connection_timeout)
        oConsultas=pyUPVBib.pyPgGas.ConsultasPg(oConectaPg)
        self.utiles.iface=self.iface
        self.utiles.oConectaPg=oConectaPg
        self.utiles.oConsultasPg=oConsultas
        self.utiles.oArchivos=oArchivos
        self.utiles.oUtilidadesListas=oUtilidadesListas
        self.utiles.oUtilidadesFormularios=oUtilidadesFormularios
        self.utiles.oUtilidades=oUtilidades
        dic={}
        listaActivado=[unicode("True","utf-8"),unicode("False","utf-8")]
        listaTipoUsuario=[unicode("admin_propiedad","utf-8"),unicode("editor","utf-8"),unicode("consultor_autorizado","utf-8"),unicode("consultor","utf-8")]
        dic["activado"]=listaActivado
        dic["tipo_usuario"]=listaTipoUsuario
        self.utiles.oDicDominios=dic

    def getUtiles(self):
        """
        En el caso de que no se haya lanzado un error, devuelve un objeto
        inicializado de la clase Utiles
        """
        return self.utiles

