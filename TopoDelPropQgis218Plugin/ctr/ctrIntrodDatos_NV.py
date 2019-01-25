# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import sys
from ctrIntrodDatos_N import ctrIntrodDatos_N

"""
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
from pydevd import *
"""
class ctrIntrodDatos_NV(ctrIntrodDatos_N):
    """
    Permite la introducción de datos en en tablas de la base de datos.
    La tabla puede tener un único campo Bytea, y debe llamarse "archivo".
    También debe tener un campo denominado id o gid, serial y primary key.
    """
    #constructor
    def __init__(self, oUtiles,tabla,subDirDescargas,cargarValoresDeBDA=False,mostrarBttNuevo=False, dicValoresAdd=None):
        """
        Inicializa el cuadro de dialogo.
        
        @type oUtiles: utils.Utiles
        @param oUtiles: Objeto de la clase utiles
        @type tabla: string
        @param tabla: Nombre de la tabla que se va a mostrar. Ej: comun.trabajos
        @param subDirDescargas: String
        @type subDirDescargas: subtirectorio que se usará para descargar el archivo bytea, si hay. 
            El subdirectorio será creado.
        @type cargarValoresDeBDA: Boolean
        @param cargarValoresDeBDA: Si es True, se cargan los valores de la tabla de la BDA, y
            se muestran en el formulario. Para hacer la selección en la tabla, usa los datos
            existentes en oUtiles: id_trabajo y tipo_trabajo.
        @type mostrarBttNuevo: Boolean
        @param mostrarBttNuevo: Si es True muestra el botón nuevo para añadir más registros a la tabla
        @type dicValoresAdd: diccionario
        @param dicValoresAdd: Diccionario nombre_campo: valor a añadir al diccionario 
            self.dicEnviar. Este diccionario es el que se envía a la base de datos.
            Se utiliza para enviar datos que no se preguntan en el cuadro de diálogo,
            por ejemplo el gid_linde.
        """
        #Ejecuta el constructor de la clase padre ctrIntroddatos

        ctrIntrodDatos_N.__init__(self, oUtiles,tabla,subDirDescargas,cargarValoresDeBDA,mostrarBttNuevo, dicValoresAdd)
        self.setSubDirDescargas(subDirDescargas)#directorio para la descaga de la memoria
        self.ui.tbId_trabajo.setText(str(self.oUtiles.id_trabajo))
        self.ui.tbSrc_trabajo.setText(str(self.oUtiles.src_trabajo))
        self.mostrarBttNuevo=mostrarBttNuevo
        self.cargarValoresDeBDA=cargarValoresDeBDA
        
        self.connect(self.ui.bttGuardar, QtCore.SIGNAL("clicked()"),self.guarda)
        self.connect(self.ui.bttNuevo, QtCore.SIGNAL("clicked()"),self.bttNuevo)
        
        self.setModoNuevo()
        self.dicValoresAdd=dicValoresAdd
        self.listaDicValoresCompleto=[]
        self.contadorDicActual=0
        
    def guarda(self):
        """
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
                self.setModoConsultar(self.cargarValoresDeBDA, self.mostrarBttNuevo)
                self.tablaCambiada=False
                self.actualizarArchivoBytea=False
                self.listaDicValoresCompleto.append(self.dicValoresCompleto)
                self.contadorDicActual=self.contadorDicActual+1
        elif self.getModo()=="editar":
            if self.tablaCambiada==False:
                #no ha cambiado nada. No hace falta enviar los datos
                self.setModoConsultar(self.cargarValoresDeBDA, self.mostrarBttNuevo)
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
                
            if self.actualizarArchivoBytea==False:
                #dic es el diccionario a enviar sin la clace "archivo"
                resp=self.oUtiles.oConsultasPg.updateDatos(self.nomTabla,self.dicEnviar.keys(), self.dicEnviar.values(),None, False, None,None,condicionWhere,lvCondWhere)
            else:
                resp=self.oUtiles.oConsultasPg.updateDatos(self.nomTabla,self.dicEnviar.keys(), self.dicEnviar.values(),"archivo", False, None,None,condicionWhere,lvCondWhere)
            if isinstance(resp, Exception):
                mens=unicode("Error. El servidor respondió: ","utf-8")
                mens=mens + resp.message
                self.ui.lbEstado.setText(mens)
            else:
                self.ui.lbEstado.setText("OK. Datos actualizados")
                self.setModoConsultar(self.cargarValoresDeBDA, self.mostrarBttNuevo)
                self.actualizarArchivoBytea=False
                self.tablaCambiada=False
                self.listaDicValoresCompleto.pop(self.contadorDicActual-1)#elimina el dic antiguo
                self.listaDicValoresCompleto.insert(self.contadorDicActual-1, self.dicValoresCompleto)
                #inserto en su lugar el dicValoresCompleto actual
                
    def bttNuevo(self):
        """
        Elimina los valores del formulario y permite introducir un registro nuevo en la
        base de datos.
        """
        self.cargaDicValoresCompletoBDAVacios()#no los carga, unicamente elimina sus valores
        self.setModoNuevo()