# -*- coding: utf-8 -*-
"""
    Utilidades de uso general.
    
    This program is free software; you can redistribute it and/or modify  
    it under the terms of the GNU General Public License as published by  
    the Free Software Foundation; either version 2 of the License, or     
    (at your option) any later version.
    
    @copyright: (C) 2011 by J. Gaspar Mora Navarro
    @contact: topodelprop@gmail.com
    @author: J. Gaspar Mora navarro.
    @organization: U.P. Valencia. Dep Ing Cart. Geod. y Fotogrametria
    @version: 1
    @summary: Utilidades de uso general.
"""
import sys
import os
import copy
#sys.path.append("C:\eclipse\plugins\org.python.pydev.debug_2.3.0.2011121518\pysrc")
#from pydevd import *

__docformat__ = "epytext"

from PyQt4 import QtCore, QtGui
#import qgis.core
#import qgis

       
class UtilidadesListas(object):
    """
    Utilidades para trabajar con listas
    """
    def existeEltoEnLista(self,lista,elto):
        """
        Devuelve True o False. Nunca da error
        """
        return elto in lista
    def eliminaEltosLista(self,listaEltos,listaEliminar, genError):
        """
        Elimina los elementos que hay en una lista de otra lista. Solo se ha probado con
        listas de cadenas.
        @type listaEltos: lista
        @param listaEltos: lista donde hay que eliminar elementos
        @type listaEliminar: lista
        @param listaEliminar: lista con los elementos a eliminar de la lista listaEltos
        @type genError: Boolean
        @param genError: Si es True, devuelve un exception, en el caso de que haya un elemento de listaEliminar no encontrado en listaEltos
            Si es False, aunque no encuentre los elementos sigue trabajando y devuelve la lista sin los elementos que encuentre.
        @requires: El metodo de esta clase eliminaUnEltoLista
        @return: Una lista si todo va bien. Un Exception si genError es True y hay algun elemento no localizado.     
        """
        """
        listaFin=listaEltos
        i=0
        for valorEliminar in listaEliminar:
            listaFin=self.eliminaUnEltoLista(listaFin,valorEliminar,genError)
            if genError==True:
                if isinstance(listaFin,Exception):
                    return Exception("No se encuentra el elemento {0} de la lista".format(i))
            i=i+1
        return listaFin
        """
        listaFin=listaEltos[:]#copio los elementos
        for valorEliminar in listaEliminar:
            try:
                listaFin.remove(valorEliminar)  
            except Exception, e:
                if genError==True:
                    return Exception("No se encuentra el elemento {0} en la lista".format(valorEliminar))
        return listaFin
    
class UtilidadesFormularios(object):
    """
    Utilidades para trabajar con objetos de formularios
    """
    def creaQTableWidgetItem(self,valor,nom_campo,avisarErrores=True):
        """
        Intenta crear un QTableWidgetItem con el valor suministrado.
        Si el valor es unicode, lo crea sin problemas, en caso contrario
        intenta pasarlo a string, si se genera un error, devuelve un QTableWidgetItem
        vacio.
        @type valor: unicode, o convertible a str
        @param valor: Valor a introducir en el QTabledWidgetItem
        @type nom_campo: string
        @param nom_campo: Nombre del campo para el cual se quiere crear el objeto.
                    Unicamente se usa para dar un mensaje.
        @type avisarErrores: booleano
        @param avisarErrores: Los valores de los campos
            que sean de tipo string, deben ser unicode, o no tener acentos ni eñes, o provocara
            error. Todos los valores que no sean unicode, se intentara convertir a string. Esto puede
            generar un error. Se avisara del error si avisarErrores es True, y continuara con el proceso.
            En caso contrario, se continua con el resto de valores, sin avisar.
        @return: QTableWidgetItem, con valor o sin valor.
        """
        #settrace()
        if valor.__class__.__name__=="unicode":
            newitem = QtGui.QTableWidgetItem(valor)
        else:
            try:
                val=str(valor)
                newitem = QtGui.QTableWidgetItem(val)
            except Exception,e:
                if avisarErrores==True:
                    QtGui.QMessageBox.information(None,"Error en UtilidadesFormularios.rellenaTableWidgetCursor","El valor del campo " + nom_campo + " no puede ser convertido a string. Se deja en blanco" ,1)
                newitem = QtGui.QTableWidgetItem()
        return newitem

    def rellenaTableWidgetListaDicFilas(self, tableWidget,listaDicFilas,avisarErrores=True):
        """
        Rellena un tableWidget con el contenido de una lista de diccionarios.
        Cada diccionario es una fila de la tabla
        La descripcion es la misma que rellenaTableWidgetCursor
        @type listaDicFilas: lista
        @param listaDicFilas: lista de dicionarios con filas de una tabla.
        """
        if len(listaDicFilas)==0:
            return
        dic=listaDicFilas[0]
        listaNombreCampos=dic.keys()
        filas=[]
        for dic in listaDicFilas:
            fila=dic.values()
            filas.append(fila)
        self.rellenaTableWidgetFilas(tableWidget, filas, listaNombreCampos, avisarErrores)

    def rellenaTableWidgetFilas(self, tableWidget,filas,listaNombreCampos,avisarErrores=True):
        """
        Rellena un tableWidget con el contenido de las filas de un cursor psycopg2.
        @type tableWidget: QtGui.QTableWidget
        @param tableWidget: tabla a rellenar
        @type filas: lista
        @param filas: filas a mostrar. Se obtiene con cursor.fetchall(). Los valores de los campos
            que sean de tipo string, deben ser unicode, o no tener acentos ni eñes, o provocara
            error. Todos los valores que no sean unicode, se intentara convertir a string. Esto puede
            generar un error. Se avisara del error si avisarErrores es True, y continuara con el proceso.
        @type listaNombreCampos: lista
        @param listaNombreCampos: lista con los nombres de los campos. Se utiliza para las cabeceras de la tabla
        @type avisarErrores: booleano
        @param avisarErrores: Los valores de los campos
            que sean de tipo string, deben ser unicode, o no tener acentos ni eñes, o provocara
            error. Todos los valores que no sean unicode, se intentara convertir a string. Esto puede
            generar un error. Se avisara del error si avisarErrores es True, y continuara con el proceso.
            En caso contrario, se continua con el resto de valores, sin avisar.
        """
        if len(filas)==0:
            return
        tableWidget.setRowCount(len(filas))
        tableWidget.setColumnCount(len(listaNombreCampos))
        tableWidget.setHorizontalHeaderLabels(listaNombreCampos)
        tableWidget.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)

        for i,fila in enumerate(filas):#i es el numero de fila
            for j,valor in enumerate(fila):#j es el numero de columna
                if valor==None:
                    valor=""
                newitem=self.creaQTableWidgetItem(valor, listaNombreCampos[j], avisarErrores)
                newitem.setTextAlignment(QtCore.Qt.AlignLeft)
                tableWidget.setItem(i, j, newitem)

    def rellenaTableWidgetVerticalDic(self,tableWidget,dic,avisarErrores=True,enabled=True,ordenar=True):
        """
        Escribe los valores del diccionario dic (nombre_campo: valor)
        en la tabla tableWidget. Los nombres de los campos y los valores,
        se colocan en columna.
        @type tableWidget: QtGui.QTableWidget
        @param tableWidget: tabla a rellenar
        @type dic: diccionario
        @param dic: Diccionario nombre_campo:valor
        @type avisarErrores: booleano
        @param avisarErrores: Los valores de los campos
            que sean de tipo string, deben ser unicode, o no tener acentos ni eñes, o provocara
            error. Todos los valores que no sean unicode, se intentara convertir a string. Esto puede
            generar un error. Se avisara del error si avisarErrores es True, y continuara con el proceso.
            En caso contrario, se continua con el resto de valores, sin avisar.
        @type ordenar: booleano
        @param ordenar: si es true ordena los campos por orden alfabético.
        """
        if len(dic)==0:
            return
        tableWidget.setRowCount(len(dic))
        tableWidget.setColumnCount(1)
        tableWidget.setHorizontalHeaderLabels(["Valor del campo"])
        tableWidget.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
        listaCampos=dic.keys()
        if ordenar==True:
            listaCampos.sort()
        tableWidget.setVerticalHeaderLabels(listaCampos)
        for i,nom_campo in enumerate(listaCampos):#j es el numero de columna
            valor=dic.get(nom_campo)
            if valor==None:
                valor=""
            newitem=self.creaQTableWidgetItem(valor,nom_campo,avisarErrores)
            newitem.setTextAlignment(QtCore.Qt.AlignLeft)
            if enabled==False:
                newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                QColor=QtGui.QColor()
                QColor.setRgb(35,16,141)
                QBrush=QtGui.QBrush()
                QBrush.setColor(QColor)
                newitem.setForeground(QBrush)
            #newitem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate)
            tableWidget.setItem(i, 0, newitem)


    def setEnabledItemsTableWidget(self,tableWidget,enabled):
        """
        Activa o desactiva todos los elementos de una tabla tablewidget
        Funciona en una aplicación normal, pero con QGis no.
        """
        n=tableWidget.columnCount()
        for i in range(n):
            self.setEnabledItemsColumnTableWidget(tableWidget, column=i, enabled=enabled)

    def setEnabledItemsColumnTableWidget(self,tableWidget,column,enabled):
        """
        Activa o desactiva todos los elementos de columna de una tabla tablewidget
        Funciona en una aplicación normal, pero con QGis no.
        """
        n=tableWidget.rowCount()
        for i in range(n):
            item=tableWidget.item(i,column)
            if enabled==True:
                flag=item.flags() | ~QtCore.Qt.ItemIsEnabled
                item.setFlags(flag)
            else:
                item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(i, column, item)  
        
    def treeViewIndexFromTexto(self,textoBuscado,treeView):
        """
        Busca en todo el treeview un elemento cuyo texto es textoBuscado,
        y devuelve su índice (index), o None si no existe.
        @type textoBuscado: string
        @param textoBuscado: Texto que se busca en todos los elementos del treeview
        @type treeView: QTreeView
        @param treeView: Treeview en el que se realiza la búsqueda.
        @requires: buscaHijoItemTreeView
        @return: El index del elemento, si existe, o None si no existe.
        """
        patriarca=treeView.model().invisibleRootItem()
        n=patriarca.rowCount()
        if n==0:
            return
        for i in range(n):
            padre=patriarca.child(i)
            index=self.buscaHijoItemTreeView(textoBuscado,padre)
            if index!=None:
                return index

    def buscaHijoItemTreeView(self, textoBuscado,itemPadre):
        """
        Dado un QStandarItem, se busca un textoBuscado en él o en todos sus hijos, si los tiene.
        Devuelve el index del elemento que coincida con textoBuscado
        @type textoBuscado: string
        @param textoBuscado: Texto buscado en el item o en sus hijos.
        @type itemPadre: QStandarItem
        @param itemPadre: Item donde se busca, en él o en sus hijos.
        """
        padre=itemPadre
        valor=str(padre.index().data())
        if textoBuscado==valor:
            return padre.index()
        n=padre.rowCount()
        if n==0:
            return
        for i in range(n):
            hijo=padre.child(i)
            valor=str(hijo.index().data())
            if textoBuscado==valor:
                return hijo.index()
            index=self.buscaHijoItemTreeView(textoBuscado,hijo)
            if index!=None:
                return index 
                    
    def add_hijo_treeview(self,treeView,indexPadre,texto,posicion=None):
        """
        Añade un hijo al elemento del treeview cuyo índice es indexPadre.
        El parámetro texto se usa como texto del nuevo elemento.
        Si el padre tiene un hijo con el mismo texto no lo añade.
        Si posición es diferente de None, se inserta en esa posición,
        es decir, si es 3, se insertará en la fila 3.
        """
        padre=treeView.model().itemFromIndex(indexPadre)
        n=padre.rowCount()
        for i in range(n):
            item=padre.child(i)
            existente=str(item.text())
            if existente==texto:
                return item.index()
        item = QtGui.QStandardItem(texto)
        item.setEditable(False)
        if posicion!=None:
            padre.insertRow (posicion,item)
        else:
            padre.appendRow(item)
        treeView.expandAll()
        return item.index()
    
    def borra_hijos_treeview(self,treeView,indexPadre):
        """
        Borra todos los hijos del qstandarditem cuyo índice es indexPadre
        """
        padre=treeView.model().itemFromIndex(indexPadre)
        n=padre.rowCount()
        for i in range(n):
            padre.removeRow(0)
            
class Utilidades(object):
    def creaDir(self, dirBase,listaSubDir,darMens=True):
        """
        Crea directorios
        Si no existe dirBase (directorio base. ej "c:/delProp"). Intenta crearlo. Si no lo
        consigue devuelve un error.
        listaSubDir, es una lista de subdirectorios a crear, uno dentro de otro.
        Antes de intentar crear los subdirectorios, comprueba que no existan.
        si listaSubDir es ["trab1258","memoria"], intenta crear el subdirectorio
        c:/delProp/trab1258, si no puede devuelve el error. Si lo consigue, 
        intenta crear c:/delProp/trab1258/memoria. Si no lo consigue devuelve el error.
        Asi sucesivamente con todos los elementos de listaSubDir.
        Si darMens es True, antes de devolver el error da un mensaje.
        Si todo va bien, devuelve True
        @type dirBase: string
        @param dirBase: Directorio base a partir del que cuelgan los demas: "c:/delProp"
        @type listaSubDir: lista
        @param listaSubDir: Lista de subdirectorios a crea. Cada uno cuelga del anterior, y todos
            a partir de dirbase.
        @type darMens: boolean
        @param darMens: Si es True da mensajes si hay errores.
        @return: Exception si hay algun error. True si todo va bien. 
        """
        nomDir=dirBase
        #compruebo que existe el directorio del trabajo
        if not(os.path.isdir(nomDir)):
        #si no existe lo creo
            try:
                os.mkdir(nomDir)
            except Exception, e:
                mens=unicode("Error al intentar crear la carpeta: " + nomDir)
                QtGui.QMessageBox.information(None,"Error al intentar crear la carpeta" , mens,1)
                e.message=mens
                return e
        for nom in listaSubDir:
            nomDir=nomDir + "/" + nom
            if not(os.path.isdir(nomDir)):
            #si no existe lo creo
                try:
                    os.mkdir(nomDir)
                except Exception, e:
                    mens=unicode("Error al intentar crear la carpeta: " + nomDir)
                    QtGui.QMessageBox.information(None,"Error al intentar crear la carpeta" , mens,1)
                    e.message=mens
                    return e
        return True
    def uneSubDir(self,listaSubDir):
        """
        Recibe una lista de subdirectorios ["d1", "d2", "d3"], y devuelve
        "/d1/d2/d3/"
        """
        cad="/"
        for elto in listaSubDir:
            cad=cad + elto + "/"
        return cad
    
    def eliminaEltosDicLClaves(self,dic,listaClaves,genError=False):
        """
        Elimina los elementos del diccionario que tienen claves coincidentes en la lista
        listaClaves. 
        Si genError=True, si algun elemento de listaClaves no es una clave del diccionario
        devuelve un error.
        @return: un nuevo diccionario con los elementos eliminados, o Exception si hay error.
        """
        copiaDic=copy.deepcopy(dic)
        for clave in listaClaves:
            try:
                del copiaDic[clave]
            except Exception,e:
                if genError==True:
                    return e
        return copiaDic

    def eliminaEltosDicLValores(self,dic,listaValoresEliminar):
        """
        Elimina los elementos del diccionario que tienen algun valor coincidente en la lista
        listaValoresEliminar. 
        @return: un nuevo diccionario con los elementos eliminados, o Exception si hay error.
        """
        copiaDic=copy.deepcopy(dic)
        for valorElim in listaValoresEliminar:
            for fila in copiaDic.items():
                clave=fila[0]
                valor=fila[1]
                if valor==valorElim:
                    del copiaDic[clave]
        return copiaDic

