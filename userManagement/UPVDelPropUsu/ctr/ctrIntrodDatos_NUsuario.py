# -*- coding: utf-8 -*-
from PyQt4 import QtCore,QtGui
import sys
from ctrFrmPassword import ctrFrmPassword
from ctrIntrodDatos_N import ctrIntrodDatos_N
sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
#from pydevd import *

class ctrIntrodDatos_NUsuario(ctrIntrodDatos_N):
    """
    Añade registros a la tabla comun.usuarios, y, a cada usuario añadido,
    crea un usuario postgres, con el mismo usuario. Antes de guardar el registro,
    y de crear el usuario, solicita la contraseña. Si es menor de 15 cifras, no tiene
    algún número y algún caracter como /@=<>#. No deja crear el usuario.
    """
    def __init__(self, oUtiles,usuarioYaCreado=False):
        """
        Oculta el usuario del formulario de entrada de datos.
        Si usuarioYaCreado=False, pregunta el usuario y lo lo crea,
        Si usuarioYaCreado=True, no lo pregunta. Permite editar sus datos, o borrarlo
        """
        ctrIntrodDatos_N.__init__(self,oUtiles,tabla="comun.usuarios",listaSubDirDescargas=["nada"],mostrarBttNuevo=True, dicValoresAdd=None)
        self.listaCamposOcultar.append("usuario")#no debe poder
        self.usuarioYaCreado=usuarioYaCreado

    def guarda(self):
        if self.usuarioYaCreado==False:
            resp=self.compruebaValores_delFormulario(compTodos=True)
            if resp==False:
                return
            resp=self.cargaDicValoresCompleto_delFormulario(True)#extrae los datos del formulario
            #y prepara el diccionario con los valores que seran enviados a la bda
            if resp==False:
                return
            tipo_usuario=self.dicValoresCompleto.get("tipo_usuario")
            """
            if tipo_usuario==self.toUtf8("admin_propiedad"):
                QtGui.QMessageBox.information(self, "Error", self.toUtf8("Por seguridad no se puede crear un adminitrador desde aquí. Hay que hacerlo manualmente."),1)
                return
            """
            dlg=ctrFrmPassword(self.oUtiles.iface)
            dlg.exec_()
            if dlg.get_ok()==True:
                usuario=dlg.get_usuario()
                self.dicValoresCompleto.update([["usuario",usuario]])
                self.dicEnviar.update([["usuario",usuario]])
                ctrIntrodDatos_N.guarda(self)

                if self.estadoGuardado=="guardado":
                    password=dlg.get_password()
                    try:
                        self.oUtiles.oConsultasPg.creaUsuario(nombreUsuarioUnicode=usuario,passwordUnicode=password)
                    except Exception,e:
                        QtGui.QMessageBox.information(self, "Error", self.toUtf8("No se pudo crear el usuario. Debe comenzar por una letra y no contener caracteres extraños ") + e.message,1)
                        self.bttBorrar(darMens=False,borrarUsuario=False)
                        return
                    activado=self.dicValoresCompleto.get("activado")
                    try:
                        pass
                        self.activaUsuario(usuario,tipo_usuario,activado)
                    except Exception, e:
                        QtGui.QMessageBox.information(self, "Error", "No se pudo activar el usuario " + e.message,1)
                        self.bttBorrar(darMens=False,borrarUsuario=True)
                        return
                    self.usuarioYaCreado=True
        else:
            #si ya ha sido creado, se guardan los datos normalente.
            ctrIntrodDatos_N.guarda(self)
            if self.estadoGuardado=="guardado":
                usuario=self.dicValoresCompleto.get("usuario")
                tipo_usuario=self.dicValoresCompleto.get("tipo_usuario")
                activado=self.dicValoresCompleto.get("activado")
                try:
                    pass
                    self.activaUsuario(usuario,tipo_usuario,activado)
                except Exception, e:
                    QtGui.QMessageBox.information(self, "Error", "No se pudo crear el usuario: " + e.message,1)
                    self.bttBorrar(darMens=True,borrarUsuario=True)


    def activaUsuario(self,usuario,tipo_usuario,activado):
        """
        Elimina el usuario del grupo en el que estuviese y lo introduce en el grupo tipo_usuario.
        Los permisos para cada tipo de usuario son los siguientes:
            - admin_propiedad: modificar cualquier campo y crear nuevos usuarios.
            - editor: permiso de escritura en las tablas de edición. Únicamente puede modificar sus
                propios trabajos, pero puede leer los trabajos completos de los demás editores en las
                capas de edición. También tiene acceso de lectura a las capas espaciales definitivas.
            - consultor autorizado: Tiene permiso de lectura de los trabajos completos en las tablas
                definitivas exclusivamente.
            - consultor: únicamente puede leer las capas de geometría definitivas. Aquí no hay ningún
                dato personal.
        Si activado es "True" (cuidado porque usuario,tipo_usuario y activado deben ser cadenas unicode),
        elimina del grupo en el que estuviese el usuario y lo introduce en el nuevo grupo especificado en
        tipo_usuario. Si Si activado es "False" hace una de las siguientes tareas:
            - Si tipo_usuario="admin_propiedad", "editor" o "consultor_autorizado", lo introduce en el grupo
                de consultores, con lo que solo puede leer las capas espaciales
            - Si tipo_usuario="consultor", lo elimina del grupo, perdiendo los privilegios y no podrá
                realizar ninguna acción ni de lectura ni de escritura.
        @type usuario: string unicode
        @param usuario: nombre del usuario. Es es el valor del campo comun.usuarios.usuario.
        @type tipo_usuario: string unicode
        @param tipo_usuario: Puede ser "admin_propiedad", "editor", "consultor_autorizado" o "consultor".
        @type activado: string unicode
        @param activado: Puede ser "True" o "False".
        @raise exception: Exception con la descripción del error. Antes de devolver el error
            intenta eliminar el usuario, tanto el registro de la tabla comun.usuarios, como el
            usuario de postgres.
        """

        #lo elimino del grupo que tenia, que no se cual es, pero como no falla lo elimino de todos
        self.oUtiles.oConsultasPg.deleteUsuarioDeGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("admin_propiedad"))
        self.oUtiles.oConsultasPg.deleteUsuarioDeGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("editor"))
        self.oUtiles.oConsultasPg.deleteUsuarioDeGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("consultor_autorizado"))
        self.oUtiles.oConsultasPg.deleteUsuarioDeGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("consultor"))

        if tipo_usuario=="admin_propiedad":
            if activado==self.toUtf8("True"):
                self.oUtiles.oConsultasPg.addUsuarioAGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("admin_propiedad"))
            else:
                self.oUtiles.oConsultasPg.addUsuarioAGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("consultor"))
        elif tipo_usuario=="editor":
            if activado==self.toUtf8("True"):
                self.oUtiles.oConsultasPg.addUsuarioAGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("editor"))
            else:
                self.oUtiles.oConsultasPg.addUsuarioAGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("consultor"))
        elif tipo_usuario=="consultor_autorizado":
            if activado==self.toUtf8("True"):
                self.oUtiles.oConsultasPg.addUsuarioAGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("consultor_autorizado"))
            else:
                self.oUtiles.oConsultasPg.addUsuarioAGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("consultor"))
        elif tipo_usuario=="consultor":
            if activado==self.toUtf8("True"):
                self.oUtiles.oConsultasPg.addUsuarioAGrupo(nombreUsuarioUnicode=usuario,grupoUnicode=self.toUtf8("consultor"))


    def bttBorrar(self,darMens=True,borrarUsuario=True):
        """
        Además de borrar el registro de la base de datos, elimina el usuario
        de postgres.
        """
        if darMens==True:
            usuario=self.dicValoresCompleto.get("usuario")
            mens=unicode("Esta acción eliminará el usuario y todos sus trabajos permanentemente, tanto definitivos, como en edición. ¿Desea continuar?","utf-8")
            reply = QtGui.QMessageBox.question(self, "Mensaje", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
                reply = QtGui.QMessageBox.critical(self, "Por segunda vez", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.No:
                    return
        ctrIntrodDatos_N.bttBorrar(self, darMens=False)
        self.usuarioYaCreado=False

        if borrarUsuario==True:
            try:
                self.oUtiles.oConsultasPg.borraUsuario(nombreUsuarioUnicode=usuario)
            except Exception,e:
                QtGui.QMessageBox.information(self, "Error", e.message,1)

    def bttNuevo(self):
        ctrIntrodDatos_N.bttNuevo(self)
        self.usuarioYaCreado=False

