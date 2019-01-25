# -*- coding: utf-8 -*-
"""
    Utilidades para trabajar con PostgreSQL.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    @copyright: (C) 2011 by J. Gaspar Mora Navarro
    @contact: upvdelprop@gmail.com
    @author: J. Gaspar Mora navarro.
    @organization: U.P. Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @version: 1
    @summary: Utilidades para trabajar con PostgreSQL.
"""
__docformat__ = "epytext"

import psycopg2
import psycopg2.extensions
import os

import sys
#sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
#from pydevd import *
import pyGenGas

class ConectaPg(object):
    """
    Clase que intenta realizar una conexion a posgres:
    Configura psycopg2 para que todo lo que devuelva postgres este en unicode
    """
    def __init__(self,database, user, password,host, port,connection_timeout=None):
        """
        Constructor:

        Llama a __set_conn para intentar la conexionConfigura postgre
        Configura psycopg2 para que todo lo que nos devuelva postgres este en unicode

        @type  database: string
        @param database: El nombre de la base de datos.
        @type  user: string
        @param user: usuario que intenta la conexion
        @type  password: string
        @param password: contrasenya
        @type  host: string
        @param host: IP del ordenador donde este la base de datos.
        """
        #Configura psycopg2 para que todo lo que devuelva postgres este en unicode
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

        self.database=database
        self.usuario=user
        self.password=password
        self.host=host
        self.port=port
        self.connection_timeout=connection_timeout

        self.__conn=None
        self.__cursor=None
        self.__conectado=False
        self.__error=None
        self.__descripcion_error=""
        if connection_timeout==None:
            cad_conn="dbname=" + database + " user=" + user + " password=" + password + " host=" + host + " port=" + str(port)
        else:
            cad_conn="dbname=" + database + " user=" + user + " password=" + password + " host=" + host + " port=" + port + " connect_timeout=" + str(connection_timeout)
        self.__set_conn(cad_conn)


    def __set_conn(self,cad_conn):
        """
        Intenta conectar con postgress:
            - Si la realiza establece las propiedades a los siguientes valores:
                - conn: la conexion
                - cursor: el cursor de la conexion
                - conectado: True
                - descripcion_error:
                - error: None
            - Si no realiza la conexion establece las propiedades a los siguientes valores:
                - conn: None
                - cursor: None
                - conectado: False
                - descripcion_error: Cadena con la descripcion de postgres
                - error: el error, instancia de Error.
        """
        try:
            self.__conn=psycopg2.connect(cad_conn)
            self.__cursor=self.__conn.cursor()
            self.__conectado=True
            self.__descripcion_error=""
            self.__error=None
        except Exception, e:
            self.__conn=None
            self.__cursor=None
            self.__conectado=False
            self.__error=e
            self.__descripcion_error=e.message
    def __set_usuario(self,usuario):
        self.__usuario=usuario
    def __get_usuario(self):
        return self.__usuario
    def __get_conn(self):
        return self.__conn
    def __get_cursor(self):
        return self.__cursor
    def __get_conectado(self):
        return self.__conectado
    def __get_error(self):
        return self.__error
    def __get_descripcion_error(self):
        return self.__descripcion_error
    def cierraConexion(self):
        """
        Cierra la conexion
        """
        self.__cursor.close()
        self.__conn.close()
        self.__conectado=False

    usuario=property(__get_usuario,__set_usuario,"Numero de usuario. Debe tener una fila en comun.usuarios")
    conn=property(__get_conn,"Solo lectura. La conexion a postgress")
    cursor=property(__get_cursor,"Solo lectura. El cursor de la conexion")
    conectado=property(__get_conectado,"Solo lectura. Es True en si ha realizado la conexion")
    error=property(__get_error,"Solo lectura. El error devuelto por postgres")
    descripcion_error=property(__get_descripcion_error,"Solo lectura. ")

class GeneraExpresionesPsycopg2(object):
    """
    Genera expresiones para realizar selects o inserts
    """
    def generaWhere(self,listaCampos, and_or):
        """
        Genera una cadena con la condición where para una consulta sql.
        Recibe una lista como ["dni",nombre","apellido" ], y devuelve una cadena con:
        " dni=%s and nombre=%s and apellido=%s", en el caso de que and_or sea "and"
        si and_or es "or", entonces devuelve
        " dni=%s or nombre=%s or apellido=%s"

        B{NO INTRODUCE LA PALABRA WHERE EN LA CADENA DEVUELTA.}

        @type listaCampos: lista
        @param listaCampos: Lista con los nombres de los campos que deben aparecer en la condicion where
        @type and_or: string
        @param and_or: puede valer "and" u "or".
        @return: un string con la condición where. Si lista campos no tiene elementos, devuelve ""
        """
        if len(listaCampos)<1:
            return None
        #if listaCampos.
        condWhere= " "
        for campo in listaCampos:
            condWhere=condWhere + campo + "=%s " + " " + and_or +" "
        if and_or=="and":
            condWhere=condWhere[:-4]
        else:
            condWhere=condWhere[:-3]
        return condWhere

    def generaInsertPsycopg2(self,nombreTabla, listaCampos):
        """
        Genera una consulta INSERT para ser usada con psycop2. Es del tipo:
            - "INSERT INTO nombreTabla (campo1, campo2, ..) values (%s,%s,...)"

        @type  nombreTabla: string.
        @param nombreTabla: Nombre de la tabla. Si pertenece a un esquema diferente de public hay que poner "nombreEsquema.nombreTabla".
        @type  listaCampos: lista.
        @param listaCampos: lista con los nombres de los campos de la tabla
        @return: Un string con la consulta
        """
        s="insert into " +nombreTabla + " ("
        for campo in listaCampos:
            s=s+campo + ","
        s=s[:-1]#elimino la ultima coma
        s=s+ ") values ("
        for campo in listaCampos:
            s=s+ "%s,"
        s=s[:-1]#elimino la ultima coma
        s=s+")"
        return s

    def generaUpdatePsycopg2(self,nombreTabla, listaCampos, condicionWhere):
        """
        Genera una consulta UPDATE para ser usada con psycop2. Es del tipo:
            - "UPDATE tabla SET campo1=%s, campo2=%s, ...WHERE id=2356"

        @type  nombreTabla: string.
        @param nombreTabla: Nombre de la tabla. Si pertenece a un esquema diferente de public hay que poner "nombreEsquema.nombreTabla".
        @type  listaCampos: lista.
        @param listaCampos: Lista con los campos de la tabla a actualizar.
        @type condicionWhere: string
        @param condicionWhere: condicion que ha de cumplir el registro para ser actualizado. Ejemplo: id=%s and lugar=%s or lugar=%s.
            Como se ve no hay que poner los valores, hay que poner %s. Esos valores los debe introcir Psycopg2 en cursor.execute(cad,valores)
            Deben estar en la lista valores. Se hace así por seguridad. pysicopg2 escapa los caracteres correctamente.

        @return: Un string con la consulta, solo hay que sustituir %s por los valores correctos.
        """
        s="update " + nombreTabla + " set "
        for campo in listaCampos:
            s=s + campo + "=%s,"
        s=s[:-1]#elimino la ultima coma
        if condicionWhere!=None:
            s=s + " where " + condicionWhere
        return s

    def generaInsertPsycopg2Geom(self,nombreTabla, listaCampos, esMulti, nombreCampoGeom, epsg):
        """
        Genera una consulta INSERT para ser usada con psycop2, conm un campo de geometría. Es del tipo:

            - "insert into h30.fincas (tipo_finca,geom) values (%s,ST_multi(ST_geometryfromtext(%s,25830)))"

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  listaCampos: string
        @param listaCampos: Lista con los nombres de los campos. Ej [nombre, direccion, img]. El último nombre en la lista debe ser el del campo bytea
        @type  esMulti: Booleano
        @param esMulti: Si es multi, se deja como estaba, si no, se convierte a multi.
        @type  nombreCampoGeom: srtring
        @param nombreCampoGeom: nombre del campo de geometría. Debe estar incuído en listaCampos.
        @type epsg: string
        @param epsg: codigo EPSG de la tabla donde se insertará la geometria
        @return: la expresión INSERT para ser usada con psycop2.
        """
        s="insert into " +nombreTabla + " ("
        for campo in listaCampos:
            s=s+campo + ","
        s=s[:-1]#elimino la ultima coma
        s=s+ ") values ("
        for campo in listaCampos:
            if nombreCampoGeom==campo:
                if esMulti==False:
                    s=s+ "ST_geometryfromtext(%s," + epsg + "),"
                else:
                    s=s+ "ST_multi(ST_geometryfromtext(%s," + epsg + ")),"
            else:
                s=s+ "%s,"
        s=s[:-1]#elimino la ultima coma
        s=s+")"
        return s

    def generaUpdatePsycopg2Geom(self,nombreTabla, listaCampos, esMulti, nombreCampoGeom, epsg, condicionWhere):
        """
        NO HA SIDO PROBADO

        Genera una consulta UPDATE para ser usada con psycop2, con un campo de geometría. Es del tipo:
            - "UPDATE tabla set tipo_finca=%s, geom=ST_multi(ST_geometryfromtext(%s,25830))"

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  listaCampos: string
        @param listaCampos: Lista con los nombres de los campos. Ej [nombre, direccion, img].
        @type  esMulti: Booleano
        @param esMulti: Si es multi, se deja como estaba, si no, se convierte a multi.
        @type  nombreCampoGeom: srtring
        @param nombreCampoGeom: nombre del campo de geometría. Debe estar incuído en listaCampos.
        @type epsg: string
        @param epsg: codigo EPSG de la tabla donde se insertará la geometria
        @type condicionWhere: string
        @param condicionWhere: condicion que ha de cumplir el registro para ser actualizado. Ejemplo: id=%s and lugar=%s or lugar=%s.
            Como se ve no hay que poner los valores, hay que poner %s. Esos valores los debe introcir pysicopg2 en cursor.execute(cad,valores)
        @return: Un string con la consulta, solo hay que sustituir %s por los valores correctos.
        """

        s="update " + nombreTabla + " set "
        for campo in listaCampos:
            if nombreCampoGeom==campo:
                if esMulti==False:
                    s=s + campo + "=ST_geometryfromtext(%s," + epsg + "),"
                else:
                    s=s+ campo + "=ST_multi(ST_geometryfromtext(%s," + epsg + ")),"
            else:
                s=s + campo + "=%s,"
        s=s[:-1]#elimino la ultima coma
        if condicionWhere!=None:
            s=s + " where " + condicionWhere
        return s

    def generaSelect(self, nombreTabla, listaCampos, condicionWhere=None,orderBy=None,limit=None):
        """
        Genera una expresion select. Lista para ser usada con psycopg2:
            - "SELECT campo1, campo2, .. FROM nombreTabla WHERE campo1=25;"

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  listaCampos: Lista de strings
        @param listaCampos: Lista de strings con los nombres de los campos a recuperar. Ej: ["id", "nombre", "img"]
        @type condicionWhere: string
        @param condicionWhere: condicion que ha de cumplir el registro para ser actualizado. Ejemplo: id=%s and lugar=%s or lugar=%s.
            Como se ve no hay que poner los valores, hay que poner %s. Esos valores los debe introcir Psycopg2 en cursor.execute(cad,valores)
            Deben estar en la lista valores. Se hace así por seguridad. pysicopg2 escapa los caracteres correctamente.
        @return: Un string con la expresion select. Exception si no se ha podido realizar.
        @type orderBy: string
        @param orderBy: Nombre del campo por el cual se quiere ordenar los registros seleccionados
        @type limit: integer
        @param limit: número máximo de registros devueltos.
        """
        if len(listaCampos) < 1:
            raise Exception("Se necesita al menos un campo para realizar la seleccion")

        s="select "
        for campo in listaCampos:
            s=s+campo + ","
        s=s[:-1]#elimino la ?ltima coma
        s= s + " from " + nombreTabla
        if condicionWhere !=None:
            s=s+ " where " + condicionWhere

        if orderBy!=None:
            s= s + " ORDER BY " + orderBy
        return s

        if limit !=None:
            s= s + " LIMIT " + str(limit) + ";"



class Archivos(object):
    """
    Clase con métodos para trabajar con archivos en formato binario.
    Se utiliza para leer un archivo y, con la clase ConsultasPG
    enviarlo a PostgreSQL.

    También se puede usar para escribir a archivo datos binarios
    recibidos de PostgreSQL. Estos datos binarios se pueden recibir
    tambien usando la clase ConsultasPg
    """

    def leeDatBinarios(self, nombreArchivo):
        """
        Lee el archivo completo en binario

        @type  nombreArchivo: string.
        @param nombreArchivo: Nombre del archivo a leer".
        @return: Los datos binarios leidos. Si no se puede leer el archivo, devuelve un IOError
        """
        try:
            f=open(nombreArchivo, "rb")
            try:
                binary = f.read()
                return binary
            finally:
                if f is not None:
                    f.close()
        except IOError, e:
            e.message=unicode("No se ha podido leer el archivo " + nombreArchivo,"utf-8)")
            return e

    def EscribeDatBinarios(self, nombreArchivo, datBinarios):
        """
        Escribe en el archivo los datos binarios. Si el archivo existe, elimina sus datos

        @type  nombreArchivo: string.
        @param nombreArchivo: Nombre del archivo a escribir".
        @return: True si todo va bien. Si no se puede escribir el archivo, devuelve un IOError
        """

        if datBinarios==None:
            return Exception("La variable datBinarios es None.")
        try:
            f=open(nombreArchivo, "wb")
            try:
                f.write(datBinarios)
                return True
            finally:
                if f is not None:
                    f.close()
        except IOError, e:
            e.message=unicode("No se ha podido leer el archivo ","utf-8") + nombreArchivo
            return e

    def copiaArchivo(self, nombreArchOrigen, nombreArchDestino):
        """
        Realiza la copia de un archivo

        @type  nombreArchOrigen: string.
        @param nombreArchOrigen: Nombre del archivo a copiar".
        @type  nombreArchDestino: string.
        @param nombreArchDestino: Nombre del archivo crear".
        @return: True si todo va bien. Si no se puede escribir el archivo, devuelve un Exception
        """
        binary=self.leeDatBinarios(nombreArchOrigen)
        if isinstance(binary,Exception):
            return binary
        r=self.EscribeDatBinarios(nombreArchDestino,binary)
        if isinstance(r,Exception):
            return r
        return True

    def cambiaTamanoImagen(self, imgEntrada,imgSalida,numColSalida):
        """
        Crea una nueva imagen de un tamaño menor. Si el numero de columnas
        numColsalida es mayor o igual que las columnas de la imagen de entrada,
        se hace una copia de la imagen de entrada.

        @requires: la librería PIL (python imagin library)
        @type imgEntrada: string
        @param imgEntrada: Ruta y nombre de la imagen de entrada
        @type imgSalida: string
        @param imgSalida: Ruta y nombre de la imagen de salida
        @type numColSalida: integer
        @param numColSalida: numero de columnas de salida. La función calcula
        proporcionalmente las filas de salida.

        @return: Si todo va bien devuelve None. Si algo ha salido mal, devuelve
        un tipo Exception con el mensaje de error
        """
        try:
            import PIL.Image
            import os
        except Exception, e:
            e.message="No se ha instalado el paquete PIL. Debe copiarse en el directorio /Quantum GIS Lisboa/apps/Python27/Lib/site-packages"
            return e
#        file, ext = os.path.splitext(nombreImg)
        try:
            im = PIL.Image.open(imgEntrada)
        except Exception, e:
            e.message="No se ha podido leer la imagen " + imgEntrada + " No deben haber ni acentos, ni enyes en la ruta"
            return e
        tamX=im.size[0]
        factor=float(numColSalida)/tamX
        #factor de escalado para que tenga el numero de columnas deseado
        #convierto a float el numerador para que el resultado sea flotante
        #si no trunca los decimales y factor seria 0
        try:
            if factor<1:
                tam= int(im.size[0]*factor),int(im.size[1]*factor) #creo una tupla
                out = im.resize(tam)
                out.save(imgSalida)
            else:
                #si el factor es mayor o igual que 1 hace una copia
                im.save(imgSalida)
        except Exception, e:
            e.message="No se ha podido escribir la imagen " + imgSalida + ". Es posible que no tenga permiso de escritura en el directorio. No deben haber ni acentos, ni eñes en la ruta"
            return e

    def descargaYgrabaArchivo(self,oConsultasPg,nomTabla,nomCampoBytea,condWhere,lvCondWhere,nom_arch):
        """
        Descarga un archivo de un campo bytea y lo escribe en el archivo dado.
        Si el archivo existe, se mantiene y devuelve una excepcion.

        @type oConsultasPg: ConsultasPg
        @param oConsultasPg: Objeto de la clase ConsultasPg inicializado
        @type nomTabla: string
        @param nomTabla: Nombre completo de la tabla, incluido el esquema: comun.trabajos
        @type nomCampoBytea: string
        @param nomCampoBytea: Nombre del camo que contiene los datos biarios a descargar.
        @type condWhere: string
        @param condWhere: Condicion where que se ha de cumplir para seleccionar el registro adecuado.
        Ejemplo: "id_trabajo=%s and provincia=%s"

        @type lvCondWhere: lista
        @param lvCondWhere: lista de valores correspondientes a los %s que hay la cadena condWhere.
        @type nom_arch: string
        @param nom_arch: nombre del archivo a crear con el contenido del campo bytea.

        @return: True si todo va bien. Exception si hay algun error.
        """
        #primero comprueba que el archivo no haya sido descargado ya,
        #en tal caso no hace falta que vuelva a descargarse del servidor
        if os.path.exists(nom_arch):
            mens="El archivo ya estaba descargado en: " + nom_arch
            return Exception(mens)

        #El archivo no ha sido descargado

        cursor=oConsultasPg.recuperaDatosTablaBytea(nomTabla, [nomCampoBytea], condWhere,lvCondWhere)
        if isinstance(cursor, Exception):
            mens=unicode("No se pudo descargar: ","utf-8")
            mens=mens+ cursor.message
            return Exception(mens)
        n=cursor.rowcount
        if not(n == 1):
            mens=unicode("Resultados incorrectos. Consulta:","utf-8")
            mens=mens + oConsultasPg.consulta
            return Exception(mens)
        tuplaValores=cursor.fetchone()
        binary=tuplaValores[0]
        if binary==None:
            return Exception("El registro no tiene datos binarios en el campo archivo")
        oArchivos=Archivos()
        res=oArchivos.EscribeDatBinarios(nom_arch, binary)
        if isinstance(res,Exception):
            mens="No se pudo escribir el archivo: " + res.message
            return Exception(mens)
        return True

class ConsultasPg(object):
    """
    Inserta y recupera datos de postgres. Puede recuperar
    e insertar campos con geometría o datos binarios de imagenes.
    de campos bytea

    Tiene una propiedad, denominada consulta que devuelve la cosulta efectuada
    """

    def __init__(self, oConectaPg):
        """
        Constructor
        @type  oConectaPg: una instancia de la clase conectaPg
        @param oConectaPg: una instancia de la clase conectaPg
        """
        self.__cursor=oConectaPg.cursor
        self.__conn=oConectaPg.conn
        self.__consulta=None
        self.__oGeneraExpresionesPsycopg2=GeneraExpresionesPsycopg2()
        self.oConectaPg=oConectaPg

    def __set_oConectaPg(self,oConectaPg):
        self.__oConectaPg=oConectaPg
    def __get_oConectaPg(self):
        return self.__oConectaPg
    def __get_oGeneraExpresionesPsycopg2(self):
        return self.__oGeneraExpresionesPsycopg2
    def insertaDatosTablaBytea(self,nombreTabla,listaCampos, listaValores, nombreCampoBytea):
        """
        Inserta un registro en una tabla con un campo bytea

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  listaCampos: string
        @param listaCampos: Lista con los nombres de los campos. Ej [nombre, direccion, img]. El último nombre en la lista debe ser el del campo bytea
        @type  listaValores: lista
        @param listaValores: Lista con los valores de los campos. El último valor debe ser la variable de los datos binarios a almacenar en el campo Bytea. Es lo que devuelve el método leeDatBinarios.
        @return: True si se ha realizado. Exception si no se ha podido realizar.
        """
        i=0
        for campo in listaCampos:
            if campo==nombreCampoBytea:
                listaValores[i]=psycopg2.Binary(listaValores[i])#sustituyo los
                    #datos binarios por los datos binarios escapados
            i=i+1

        tuplaValores=tuple(listaValores)
        #c=GeneraExpresionesPsycopg2()
        c=self.oGeneraExpresionesPsycopg2
        consulta=c.generaInsertPsycopg2(nombreTabla, listaCampos)
        self.__consulta=consulta

        try:
#            self.__cursor.execute("insert into %s (%s,%s,%s) values (%s,%s,%s)", (nombreTabla,listaCampos[0],listaCampos[1],listaCampos[2],listaValores[0],listaValores[1],psycopg2.Binary(listaValores[2])))
            self.__cursor.execute(consulta, tuplaValores)
            self.__conn.commit()
            return True
        except Exception, e:
            self.__conn.commit()
            e.message=unicode(e.message,"utf-8")
            return e

    def insertaDatosTablaGeom(self,nombreTabla,listaCampos, listaValores,esMulti, nombreCampoGeom, epsg ):
        """
        Inserta un registro en una tabla con un campo de geometria

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  listaCampos: string
        @param listaCampos: Lista con los nombres de los campos. Ej [nombre, direccion, img]. El último nombre en la lista debe ser el del campo bytea
        @type  listaValores: lista
        @param listaValores: Lista con los valores de los campos. El último valor debe ser la variable de los datos binarios a almacenar en el campo Bytea. Es lo que devuelve el método leeDatBinarios.
        @type  esMulti: Booleano
        @param esMulti: Si es multi, se deja como estaba, si no, se convierte a multi.
        @type  nombreCampoGeom: srtring
        @param nombreCampoGeom: nombre del campo de geometría. Debe estar incuído en listaCampos.
        @type epsg: string
        @param epsg: codigo EPSG de la tabla donde se insertará la geometria
        @return: True si se ha realizado. Exception si no se ha podido realizar.
        """

        tuplaValores=tuple(listaValores)
        #c=GeneraExpresionesPsycopg2()
        c=self.oGeneraExpresionesPsycopg2
        consulta=c.generaInsertPsycopg2Geom(nombreTabla, listaCampos, esMulti, nombreCampoGeom, epsg)
        self.__consulta=consulta
        try:
#            self.__cursor.execute("insert into %s (%s,%s,%s) values (%s,%s,%s)", (nombreTabla,listaCampos[0],listaCampos[1],listaCampos[2],listaValores[0],listaValores[1],psycopg2.Binary(listaValores[2])))
            self.__cursor.execute(consulta, tuplaValores)
            self.__conn.commit()
            return True
        except Exception, e:
            self.__conn.commit()
            e.message=unicode(e.message,"utf-8")
            return e

    def insertaDatos(self,nombreTabla,listaCampos, listaValores,nombreCampoBytea=None, esMulti=False, nombreCampoGeom=None, epsg=None, returning=None):
        """
        Inserta un registro en una tabla. La tabla puede contener un campo bytea, para almacenar archivos
        o un campo de geometría, o ambos.

        El valor del campo Bytea es lo que devuelve el método leeDatBinarios de la clase Archivos.
        El valor del campo de geometrái debe ser como el ejemlo que sigue:
            - 'POLYGON((716929.025919 4350081.309705,716981.909594 4350174.233877,...,716929.025919 4350081.309705))'
            - se obtiene con el método exportToWkt() de la clase qgsGeometry de QGis
                - seleccion = layer.selectedFeatures()
                - for objeto in seleccion:
                    - geom=objeto.geometry()
                    - geomT=str(geom.exportToWkt())

        Si returning es una lista de campos, puede devolver los valores insertados en la tabla
        para esos campos. Estos valores se pueden recuperar con cursor.fetchall()

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  listaCampos: string
        @param listaCampos: Lista con los nombres de los campos, incluídos, en su caso, el nombre del campo de geometría, y el nombre del campo bytea . Ej [nombre, direccion, img, geom].
        @type  listaValores: lista
        @param listaValores: Lista con los valores de los campos. El campo Bytea es lo que devuelve el método leeDatBinarios de la clase Archivos.
        @type  esMulti: Booleano
        @param esMulti: Si es multi, se deja como estaba, si no, se convierte a multi.
        @type  nombreCampoGeom: srtring
        @param nombreCampoGeom: nombre del campo de geometría. Debe estar incuído en listaCampos.
        @type epsg: string
        @param epsg: codigo EPSG de la tabla donde se insertará la geometria
        @type returning: lista
        @param returning: Lista de campos de la insercion a retornar. Se pueden recuperar con cursor.fetchall(), despues de la insercion. Si es None, no retorna nada.
        @return: True si lo consigue. Una instancia del error en caso contrario.
        """
        if nombreCampoBytea is not None:
            i=0
            for campo in listaCampos:
                if campo==nombreCampoBytea:
                    listaValores[i]=psycopg2.Binary(listaValores[i])#sustituyo los
                        #datos binarios por los datos binarios escapados
                i=i+1

        #c=GeneraExpresionesPsycopg2()
        c=self.oGeneraExpresionesPsycopg2
        if nombreCampoGeom is None:
            consulta=c.generaInsertPsycopg2(nombreTabla, listaCampos)
        else:
            consulta=c.generaInsertPsycopg2Geom(nombreTabla, listaCampos, esMulti, nombreCampoGeom, epsg)
        try:
#            self.__cursor.execute("insert into %s (%s,%s,%s) values (%s,%s,%s);", (nombreTabla,listaCampos[0],listaCampos[1],listaCampos[2],listaValores[0],listaValores[1],psycopg2.Binary(listaValores[2])))
            if returning != None:
                consulta=consulta + " returning "
                for campo in returning:
                    consulta=consulta + campo + ","
                consulta=consulta[:-1]#elimino la ultima coma
            tuplaValores=tuple(listaValores)
            self.__consulta=consulta
            self.__cursor.execute(consulta, tuplaValores)
            self.__conn.commit()
            return True
        except Exception, e:
            self.__conn.commit()
            e.message=unicode(e.message,"utf-8")
            return e

    def insertaDatosDic(self,nombreTabla,dicValores,nombreCampoBytea=None, esMulti=False, nombreCampoGeom=None, epsg=None, returning=None):
        """
        Es igual que L{insertaDatos}, solo que, en vez de recibir dos listas, una con los nombres de los campos
        y otra con los nombres de los valores, recibe un diccionario campo:valor
        """
        resp=self.insertaDatos(nombreTabla,dicValores.keys(), dicValores.values(),nombreCampoBytea, esMulti, nombreCampoGeom, epsg, returning)
        return resp

    def updateDatos(self,nombreTabla,listaCampos, listaValores,nombreCampoBytea=None, esMulti=False, nombreCampoGeom=None, epsg=None, condicionWhere=None, listaValoresCondWhere=None,returning=None):
        """
        Actualiza un registro en una tabla. La tabla puede contener un campo bytea, para almacenar archivos
        o un campo de geometría, o ambos. El valor del campo Bytea es lo que devuelve el método leeDatBinarios de la clase Archivos.

        El valor del campo de geometria debe ser como el ejemlo que sigue:
            - 'POLYGON((716929.025919 4350081.309705,716981.909594 4350174.233877,...,716929.025919 4350081.309705))'

        Se obtiene con el método exportToWkt() de la clase qgsGeometry de QGis
            - seleccion = layer.selectedFeatures()
            - for objeto in seleccion:
            - geom=objeto.geometry()
            - geomT=str(geom.exportToWkt())

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  listaCampos: string
        @param listaCampos: Lista con los nombres de los campos. Ej [nombre, direccion, img]. El último nombre en la lista debe ser el del campo bytea
        @type  listaValores: lista
        @param listaValores: Lista con los valores de los campos. El campo Bytea es lo que devuelve el método leeDatBinarios de la clase Archivos.
        @type  esMulti: Booleano
        @param esMulti: Si es multi, se deja como estaba, si no, se convierte a multi.
        @type  nombreCampoGeom: srtring
        @param nombreCampoGeom: nombre del campo de geometría. Debe estar incuído en listaCampos.
        @type epsg: string
        @param epsg: codigo EPSG de la tabla donde se insertará la geometria
        @type condicionWhere: string
        @param condicionWhere: condicion que ha de cumplir el registro para ser actualizado. Ejemplo: id=%s and lugar=%s or lugar=%s.
            Como se ve no hay que poner los valores, hay que poner %s. Esos valores los debe introcir Psycopg2 en cursor.execute(cad,valores)
            Deben estar en la lista valores. Se hace así por seguridad. pysicopg2 escapa los caracteres correctamente.
        @type listaValoresCondWhere: lista
        @param listaValoresCondWhere: lista de valores de la condicion Where, que han de sustituir a los %s de la condicion Where.
        @return: True si lo consigue. Una instancia del error en caso contrario.
        """
        if nombreCampoBytea is not None:
            i=0
            for campo in listaCampos:
                if campo==nombreCampoBytea:
                    listaValores[i]=psycopg2.Binary(listaValores[i])#sustituyo los
                        #datos binarios por los datos binarios escapados
                i=i+1

        #c=GeneraExpresionesPsycopg2()
        c=self.oGeneraExpresionesPsycopg2
        if nombreCampoGeom is None:
            consulta=c.generaUpdatePsycopg2(nombreTabla, listaCampos, condicionWhere)
        else:
            consulta=c.generaUpdatePsycopg2Geom(nombreTabla, listaCampos, esMulti, nombreCampoGeom, epsg, condicionWhere)
            if returning != None:
                consulta=consulta + " returning "
                for campo in returning:
                    consulta=consulta + campo + ","
                consulta=consulta[:-1]#elimino la ultima coma
        try:
            if listaValoresCondWhere!=None:
                listaValores2=listaValores[:]#hago una copia para no modificar la lista en el exterior del metodo
                listaValores2.extend(listaValoresCondWhere)#añade una lista a otra
            tuplaValores=tuple(listaValores2)
            self.__consulta=consulta
            self.__cursor.execute(consulta, tuplaValores)
            self.__conn.commit()
            return True
        except Exception, e:
            self.__conn.commit()
            e.message=unicode(e.message,"utf-8")
            return e

    def deleteDatos(self,nombreTabla,dicCondWhere=None):
        """
        Borra los registros de una tabla que coinciden con todos los valores de campo de
        dicCondWhere. Si dicCondWhere==None, borra todos los registros de la tabla
        @return: True si todo va bien, Exception si hay algún problema.
        """
        if dicCondWhere==None or len(dicCondWhere)==0:
            consulta= "delete from " + nombreTabla#borra todos los registros
        else:
            c=GeneraExpresionesPsycopg2()
            condWhere=c.generaWhere(dicCondWhere.keys(),"and")
            consulta="delete from " + nombreTabla + " where " + condWhere
        self.__consulta=consulta
        try:
            if dicCondWhere==None or len(dicCondWhere)==0:
                self.__cursor.execute(consulta)
                self.__conn.commit()
                return True
            else:
                tuplaValores=tuple(dicCondWhere.values())
                self.__cursor.execute(consulta, tuplaValores)
                self.__conn.commit()
                return True
        except Exception, e:
            self.__conn.commit()
            e.message=unicode(e.message,"utf-8")
            return e

    def insertaArchivoPG(self,nombreTabla,nombreCampo,datosBinarios):
        """
        Inserta un archivo en postgres

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  nombreCampo: string
        @param nombreCampo: Nombre del campo bytea destino".
        @type  datosBinarios: datos binarios
        @param datosBinarios: datos binarios del archivo. Se pueden obtener con el metodo leeDatBinarios de esta clase.
        @return: True si se ha realizado. Exception si no se ha podido realizar.
        """

        #el comapo img es de tipo bytea
        consulta="insert into " + nombreTabla + "(" + nombreCampo + ")" + " values (%s)"
        self.__consulta=consulta
        try:
            self.__cursor.execute(consulta, (nombreTabla,nombreCampo,psycopg2.Binary(datosBinarios)))
            self.__conn.commit()
            return True
        except Exception, e:
            self.__conn.commit()
            e.message=unicode(e.message,"utf-8")
            return e

    def recuperaDatosTablaBytea(self, nombreTabla, listaCampos, condicionWhere=None,listaValoresCondWhere=None,bytea_output_to_escape=False,orderBy=None,limit=None):
        """
        Recupera el contenido de una tabla, tenga o no, un campo bytea de postgres

        @type  nombreTabla: string
        @param nombreTabla: Nombre de la tabla. ej1:"imagenes" ej2: "esquemaPG.imagenes".
        @type  listaCampos: Lista de strings
        @param listaCampos: Lista de strings con los nombres de los campos a recuperar. Ej: ["id", "nombre", "img"]
        @type condicionWhere: string
        @param condicionWhere: condicion que ha de cumplir el registro para ser actualizado. Ejemplo: id=%s and lugar=%s or lugar=%s.
            Como se ve no hay que poner los valores, hay que poner %s. Esos valores los debe introcir Psycopg2 en cursor.execute(cad,valores)
            Deben estar en la lista valores. Se hace así por seguridad. pysicopg2 escapa los caracteres correctamente.
        @type listaValoresCondWhere: lista
        @param listaValoresCondWhere: lista de valores de la condicion Where, que han de sustituir a los %s de la condicion Where.
        @type bytea_output_to_escape: boolean
        @param bytea_output_to_escape : Si es True, ejecuta cur.execute("SET bytea_output TO escape;"), necesario para postgres 9.0 o posterior
            con psycopg2 versiones anteriores a la 2.4.1. Si no no recupera bien los campos bytea.
            A partir de la version 2.4.1 ya no hace falta esta linea.
        @return: Una referencia al cursor que contiene las filas seleccionadas. Exception si no se ha podido realizar.
        """

        #c=GeneraExpresionesPsycopg2()
        c=self.oGeneraExpresionesPsycopg2
        try:
            consulta=c.generaSelect(nombreTabla, listaCampos, condicionWhere,orderBy,limit)
            self.__consulta=consulta
        except Exception, e:
            e.message=unicode(e.message,"utf-8")
            return e
        if condicionWhere==None:
            try:
                if bytea_output_to_escape==True:
                    self.__cursor.execute("SET bytea_output TO escape;")
                self.__cursor.execute(consulta)
                self.__conn.commit()
            except Exception, e:
                self.__conn.commit()
                e.message=unicode(e.message,"utf-8")
                return e
        else:
            tuplaValores=tuple(listaValoresCondWhere)
            try:
                self.__cursor.execute("SET bytea_output TO escape;")
                self.__cursor.execute(consulta, tuplaValores)
                self.__conn.commit()
            except Exception, e:
                self.__conn.commit()
                e.message=unicode(e.message,"utf-8")
                return e
#            if self.__cursor.rowcount==0:
#                mens="No hay ninguna imagen en la BDA que coincida con este criterio: " + condicionWhere
#                raise Exception(mens)
#            if self.__cursor.rowcount > 1:
#                mens="Hay varias imagenes en la BDA que coinciden con este criterio: " + condicionWhere
#                raise Exception(mens)
        return self.__cursor

    def recuperaDatosTablaByteaDic(self, nombreTabla, listaCampos, condicionWhere=None,listaValoresCondWhere=None,bytea_output_to_escape=False, orderBy=None,limit=None):
        """
        La documentacion es la misma que la del metodo L{recuperaDatosTablaBytea}.
        La diferencia es que este metodo no devuelve un cursor, si no una lista con todas las
        filas seleccionadas. Cada elemento de la lista es un diccionario {nombre_campo:valor,nombre_campo:valor,....}
        Si un valor de campo no tiene valor, el valor para el campo en el diccionario es None.

        @return: Una lista de diccionarios. Un diccionario por fila seleccionada.
            Si no hay selección, la lista estará vacía.
            Exception si hay error.
        """
        cursor=self.recuperaDatosTablaBytea(nombreTabla, listaCampos, condicionWhere,listaValoresCondWhere,bytea_output_to_escape,orderBy,limit)
        if isinstance(cursor,Exception):
            return cursor
        filas=cursor.fetchall()
        listaDic=[]
        for fila in filas:
            dic={}
            for i,valor in enumerate(fila):
                dic[listaCampos[i]]=valor
            listaDic.append(dic)
        return listaDic

    def sacaNombreTablasEsquema_cursor(self,esquema):
        """
        Devuelve un cursor con los nombres de las tablas de un esquema.

        Saber las tablas de un schema. pg_tables es una vista
            - SELECT tablename FROM pg_tables WHERE schemaname = 'public'

        @type  esquema: string
        @param esquema: Nombre del esquema
        @return: Una referencia al cursor que contiene las filas seleccionadas. Exception si no se ha podido realizar.

        """
        consulta="SELECT tablename FROM pg_tables WHERE schemaname = %s"
        lis=[]
        lis.append(esquema)
        try:
            self.__cursor.execute(consulta,lis)
            if self.__cursor.rowcount==0:
                mens="No hay ninguna tabla en el esquema " + esquema
                mens=unicode(mens,"utf-8")
                return Exception(mens)

        except Exception, e:
            self.__conn.commit()
            e.message=unicode(e.message,"utf-8")
            return e
        self.__consulta=consulta

        return self.__cursor

    def sacaNombreTablasEsquema_lista(self,esquema,anteponerEsquema=False):
        """
        Devuelve una lista con los nombres de las tablas de un esquema.
        @type esquema: string
        @param esquema: Nombre del esquema
        @return: Una lista que contiene las filas seleccionadas. Exception si no se ha podido realizar.
        """
        oCursor=self.sacaNombreTablasEsquema_cursor(esquema)
        if isinstance(oCursor,Exception):
            return oCursor#devuelve la excepcion

        listaValores=oCursor.fetchall()#es una lista de tuplas.
                #cada tupla es una fila. En este caso, la fila tiene un
                #unico elemento, que es el nombre del campo.
        listaNombreTablas=[]
        for fila2 in listaValores:
            valor=fila2[0]
            if anteponerEsquema==True:
                valor=esquema + "." + valor
            listaNombreTablas.append(valor)
        return listaNombreTablas


    def sacaNombresCamposTabla_cursor(self,esquema, nomTabla):
        """
        Devuelve un cursor con los nombres de los campos de una tabla.
        @type  esquema: string
        @param esquema: nombre del esquema que contiene la tabla. Ejemplo "h30"
        @type  nomTabla: string
        @param nomTabla: nombre de la tabla. Ejemplo "linde"
        @return: Una referencia al cursor que contiene las filas seleccionadas. Exception si no se ha podido realizar.

        saber las columnas de una tabla:
        SELECT column_name FROM information_schema.columns WHERE table_schema='h30' and table_name = 'linde';
        """

        consulta="SELECT column_name FROM information_schema.columns WHERE table_schema=%s and table_name = %s";

        lis=[]
        lis.append(esquema)
        lis.append(nomTabla)
        try:
#            self.__cursor.execute(consulta,lis)
            self.__cursor.execute(consulta,lis)
            if self.__cursor.rowcount==0:
                mens=unicode("No hay ninguna tabla en el esquema " + esquema,"utf-8")
                self.__conn.commit()
                return Exception(mens)

        except Exception, e:
            e.message=unicode(e.message,"utf-8")
            return e
        self.__consulta=consulta
        self.__conn.commit()
        return self.__cursor

    def sacaNombresCamposTabla_lista(self,esquema, nomTabla):
        """
        Devuelve una lista con los nombres de los campos de una tabla.
        @type  esquema: string
        @param esquema: nombre del esquema que contiene la tabla. Ejemplo "h30"
        @type  nomTabla: string
        @param nomTabla: nombre de la tabla. Ejemplo "linde"
        @return: una lista con los nombres de los campos. Exception si hay error
        """
        oCursor=self.sacaNombresCamposTabla_cursor(esquema, nomTabla)
        if isinstance(oCursor,Exception):
            return oCursor#devuelve la excepcion

        listaValores=oCursor.fetchall()#es una lista de tuplas.
                #cada tupla es una fila. En este caso, la fila tiene un
                #unico elemento, que es el nombre del campo.
        listaNombreCampos=[]
        for fila2 in listaValores:
            valor=fila2[0]
            listaNombreCampos.append(valor)
        return listaNombreCampos

    def mueveRegistros(self,tablaOrigen,tablaDestino,listaCamposCopiar,listaCamposNoCopiar=None,dicCondWhere={},puedenSerVarios=False,puedenSerCero=False,dicValoresCambiar=None,dicValoresAdd=None,borrarOrigen=False, listaCamposReturning=None):
        """
        Copia registros de tablaOrigen a tablaDestino.
        @type tablaOrigen: string
        @param tablaOrigen: nombre completo de la tabla origen.
        @type tablaDestino: string
        @param tablaDestino: nombre completo de la tabla destino.
        @type listaCamposCopiar: lista, o string
        @param listaCamposCopiar: lista con los campos a copiar de una tabla a otra.
            Si se pasa "todos", se extraen todos los nombres de campos de la tabla.
        @type listaCamposNoCopiar: lista
        @param listaCamposNoCopiar: Lista con los campos a eliminar de la lista listaCamposCopiar.
            Está pensado para cuando listaCamposCopiar sea "todos", pero que haya que eliminar
            algún campo, por ejemplo el id, o gid. Este campo debe ser serial primary key,
            y lo debe asignar la BDA.
        @type dicCondWhere: diccionario
        @param dicCondWhere: diccionario nombreCampo:condición a cumplir para ser seleccionado
            Deben estar en la lista valores. Se hace así por seguridad. pysicopg2 escapa los caracteres correctamente.
        @type puedenSerVarios: booleano
        @param puedenSerVarios: Si es false y resultan varios registros seleccionados de la
            tabla origen, se genera un error.
        @type puedenSerCero: booleano
        @param puedenSerCero: Si es false y resultan cero registros seleccionados de la
            tabla origen, se genera un error.
        @type dicValoresCambiar: diccionario
        @param dicValoresCambiar: diccionario nombreCampo: valor. Se puede utilizar para cambiar
            algún valor de la tabla destino, es decir, la tabla destino tendrá, en los campos
            indicados los valores de este diccionario, no los de la tabla origen.
        @type borrarOrigen: booleano
        @param borrarOrigen: Si es True, se borran todos los registros seleccionados en la tabla
            origen.
        @type listaCamposReturning: lista
        @param listaCamposReturning: si no es None, se devuelve un diccionario con
            los valores de los campos indicados. Estos valores son devueltos por el
            servidor, después de insertar el registro.
        @raise Exception: Si, de la selección, resultan varios registros y debe ser uno.
            Si la selección o la inserción generan algún error.
        @return: Un diccionario con los campos especificados en listaCamposReturning.
            Un diccionario vacío, si listaCamposReturning es None.
        """
        if listaCamposCopiar=="todos":
            lista=tablaOrigen.split(".")
            listaCampos=self.sacaNombresCamposTabla_lista(esquema=lista[0], nomTabla=lista[1])
            if isinstance(listaCampos,Exception):
                raise Exception(listaCampos.message)
        else:
            listaCampos=listaCamposCopiar
        if listaCamposNoCopiar.__class__.__name__=="list":
            oUtilidadesListas=pyGenGas.UtilidadesListas()
            listaCampos=oUtilidadesListas.eliminaEltosLista(listaEltos=listaCampos,listaEliminar=listaCamposNoCopiar, genError=True)
            if isinstance(listaCampos,Exception):
                raise Exception(listaCampos.message)

        expre=GeneraExpresionesPsycopg2()
        condicionWhere=expre.generaWhere(listaCampos=dicCondWhere.keys(), and_or="and")
        dicSelOrigen=self.recuperaDatosTablaByteaDic(nombreTabla=tablaOrigen, listaCampos=listaCampos, condicionWhere=condicionWhere, listaValoresCondWhere=dicCondWhere.values(), bytea_output_to_escape=False)
        if isinstance(dicSelOrigen,Exception):
            raise Exception(dicSelOrigen.message)
        n=len(dicSelOrigen)
        if n==0:
            if puedenSerCero==False:
                raise Exception("Resultaron seleccionados cero elementos de la tabla " + tablaOrigen + " que cumplan " + condicionWhere)
            else:
                return {}
        if n>1:
            if puedenSerVarios==False:
                raise Exception("Resultaron seleccionados " + str(n)+ " elementos de la tabla " + tablaOrigen + " que cumplan " + condicionWhere)

        if dicValoresCambiar.__class__.__name__=="dict":
            for campoCambiar in dicValoresCambiar.keys():
                if not(campoCambiar in listaCampos):
                    raise Exception("El campo a cambiar de valor " + campoCambiar + " no esta en la lista de campos a recuperar de la tabla.")
            for dic in dicSelOrigen:
                dic.update(dicValoresCambiar.items())
        if dicValoresAdd.__class__.__name__=="dict":
            for dic in dicSelOrigen:
                dic.update(dicValoresAdd.items())
        for dic in dicSelOrigen:
            resp=self.insertaDatosDic(nombreTabla=tablaDestino, dicValores=dic, nombreCampoBytea=None, esMulti=None, nombreCampoGeom=None, epsg=None, returning=listaCamposReturning)
            if isinstance(resp,Exception):
                raise Exception(resp.message)
            if borrarOrigen==True:
                resp=self.deleteDatos(nombreTabla=tablaOrigen, dicCondWhere=dicCondWhere)
                if isinstance(resp,Exception):
                    raise Exception(resp.message)
        dic={}
        if listaCamposReturning.__class__.__name__=="list":
            resp=self.oConectaPg.cursor.fetchall()
            try:
                fila=resp[0]
                for i,columna in enumerate(listaCamposReturning):
                    dic[columna]=fila[i]
                return dic
            except Exception, e:
                raise Exception("Error en los campos returning de mueveRegistros: " + e.message)
        else:
            return dic

    def creaUsuario(self, nombreUsuarioUnicode,passwordUnicode):
        """
        Crea un usuario postgres a partir del nombre y el password
        Nombre usuario y password deben estar en Unicode
        @raise exception: Exception
        """
        consulta = self.toUtf8("create user ") + nombreUsuarioUnicode + self.toUtf8(" with encrypted password '") + passwordUnicode + self.toUtf8("' login")
        try:
            self.__cursor.execute(consulta)
            self.__conn.commit()
        except Exception,e:
            self.__conn.commit()
            mens=self.toUtf8("No se pudo crear el usuario de postgres ") + nombreUsuarioUnicode
            mens=self.toUtf8(". El servidor respondió: ") + e.message
            raise Exception(mens)
        return True

    def borraUsuario(self,nombreUsuarioUnicode):
        """
        Borra un usuario de postgres.
        @raise exception: Exception
        """
        consulta=self.toUtf8("drop user ") + nombreUsuarioUnicode
        try:
            self.__cursor.execute(consulta)
            self.__conn.commit()
        except Exception,e:
            self.__conn.commit()
            mens=self.toUtf8("No se pudo borrar el usuario de postgres ") + nombreUsuarioUnicode + self.toUtf8(". Debe hacerlo Ud. Manualmente.")
            mens=self.toUtf8(". El servidor respondió: ") + e.message
            raise Exception(mens)
        return True

    def addUsuarioAGrupo(self,nombreUsuarioUnicode,grupoUnicode):
        """
        Añade un usuario a un grupo de postgres
        @raise exception: Exception
        """

        consulta=self.toUtf8("grant ") +  grupoUnicode + self.toUtf8(" to ") + nombreUsuarioUnicode
        try:
            self.__cursor.execute(consulta)
            self.__conn.commit()
        except Exception,e:
            self.__conn.commit()
            mens=self.toUtf8("No se pudo añadir el usuario de postgres ") + nombreUsuarioUnicode + self.toUtf8(" al grupo ") + grupoUnicode
            mens=self.toUtf8(". El servidor respondió: ") + e.message
            raise Exception(mens)
        return True

    def deleteUsuarioDeGrupo(self,nombreUsuarioUnicode,grupoUnicode):
        """
        Borra un usuario de un grupo de postgres
        @raise exception: Exception
        """
        consulta=self.toUtf8("revoke ") +  grupoUnicode + self.toUtf8(" from ") + nombreUsuarioUnicode
        try:
            self.__cursor.execute(consulta)
            self.__conn.commit()
        except Exception,e:
            self.__conn.commit()
            mens=self.toUtf8("No se pudo eliminar el usuario de postgres ") + nombreUsuarioUnicode + self.toUtf8(" del grupo ") + grupoUnicode
            mens=self.toUtf8(". El servidor respondió: ") + e.message
            raise Exception(mens)
        return True



    def toUtf8(self,mens):
        return unicode(mens,"utf-8")

    def sacaNombresCamposTabla_lista2(self,nomTablaCompleto):
        """
        Devuelve una lista con los nombres de los campos de una tabla.
        @type nomTablaCompleto: string
        @param nomTablaCompleto: Nombre de la tabla, incluido el esquema.
        @return: una lista con los nombres de los campos. Exception si hay error
        """
        lista=str.split(nomTablaCompleto,".")
        esquema=lista[0]
        tabla=lista[1]
        return self.sacaNombresCamposTabla_lista(esquema, tabla)

    def __get_consulta(self):
        return self.__consulta

    consulta=property(__get_consulta,"Solo lectura. La consulta realizada")
    oConectaPg=property(__get_oConectaPg,__set_oConectaPg,"Objeto de la clase ConectaPg")
    oGeneraExpresionesPsycopg2=property(__get_oGeneraExpresionesPsycopg2,"Objeto de la clase GeneraExpresionesPsycopg2")

