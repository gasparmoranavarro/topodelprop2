# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
import datetime
from forms.frmIntrodDatos import Ui_frmIntrodDatos
import os
import sys


class ctrIntrodDatos(QtGui.QDialog):
    """
    Proporciona la funcionalidad basica para la introducción de datos en la base de datos.
    Carga los valores de las tablas en el formulario, los valores de los dominios, y
    comprueba que todo es correcto.
    Este controlador no tiene programado el evento guardar, ya que, en cada tabla
    hay que considerar casos especiales.
    Este controlador esta pensado como clase padre. Los hijos son los que deben definir
    y programar el evento de guardar.
    """
    #constructor
    def __init__(self, oUtiles,nomTabla):
        """
        Inicializa el cuadro de dialogo.

        @type oUtiles: utils.Utiles
        @param oUtiles: Objeto de la clase utiles
        @type nomTabla: string
        @param nomTabla: Nombre de la tabla que se va a mostrar. Ej: comun.trabajos
        """
        #Ejecuta el constructor de la clase padre QDialog
        QtGui.QDialog.__init__(self,oUtiles.iface)
#        QtGui.QDialog.init(self,dlgPadre)

        #Inicializa el formulario
        self.ui=Ui_frmIntrodDatos() #inicializa la variable local ui al di??logo
        self.ui.setupUi(self)
        self.oUtiles=oUtiles
        self.listaSubDirDescargas=None#directorio para descargarArchivo el archivo bytea. Se descarga en dirTrabajos/id_trabajo/subdirDescargas
        self.listaNomCampos=None#Lista con todos los campos de la tabla.
                                        #No estan los campos archivo ni geom
        self.dicValoresCompleto=None#diccionario campo:valor con todos los valores extraidos de
                        #postgres o de la tabla  del fromulario. No estan los campos archivo ni geom
        self.dicMostrar=None#dicionario con los valores adecuados a mostrar en la tabla del formulario
        self.dicEnviar=None#dicionario con los valores que se enviaran a la base de datos.
                #es igual que self.dicValoresCompleto, sin valores "".
        self.setNomtabla(nomTabla)#nombre incluido el esquema. Ej: "comun.trabajos"
        self.cargaListaNomCamposBDA()
        self.archivoBytea=None
        self.actualizarArchivoBytea=False
        self.tablaCambiada=False#indica si ha habido algún cambio en los datos
        self.estadoGuardado="no guardado"#puede ser 'guardado', 'no guardado'#indica si se ha guardado al menos una vez
        self.listaValoresQlist=None
        if oUtiles.id_trabajo!=None:
            self.ui.tbId_trabajo.setText(str(oUtiles.id_trabajo))
        if oUtiles.src_trabajo!=None:
            self.ui.tbSrc_trabajo.setText(str(oUtiles.src_trabajo))
#        self.setWindowModality(1)
        #Conecta los botones con m??todos de esta clase
#        self.connect(self.ui.bttExplorar, QtCore.SIGNAL("clicked()"),self.explora)
        self.connect(self.ui.bttTerminar,QtCore.SIGNAL('clicked()'),self.terminar)#si
        self.connect(self.ui.bttEditar,QtCore.SIGNAL('clicked()'),self.setModoEditar)
        self.connect(self.ui.listWidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.insertaValor)
        self.connect(self.ui.tableWidget, QtCore.SIGNAL("cellClicked(int,int)"), self.tabla_click)
        self.connect(self.ui.tableWidget, QtCore.SIGNAL("cellChanged(int,int)"), self.tabla_cambiada)
        self.connect(self.ui.bttDescargar, QtCore.SIGNAL('clicked()'), self.descargarArchivo)
        self.connect(self.ui.txtFiltrar, QtCore.SIGNAL("textChanged(const QString &)"),self.txtFiltrar)
        self.connect(self.ui.bttBorrar, QtCore.SIGNAL('clicked()'),self.bttBorrar)

    def bttBorrar(self,darMens=True):
        if darMens==True:
            mens=unicode("Borrar este registro implica borrar todos los datos relacionados de otras tablas. ¿Está seguro?.","utf-8")
            reply = QtGui.QMessageBox.question(self, "Advertencia", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
        dicCondiciones={}
        if "id_trabajo" in self.dicValoresCompleto:
            dicCondiciones["id_trabajo"]=self.oUtiles.id_trabajo
        if "id" in self.dicValoresCompleto:
            dicCondiciones["id"]=self.dicValoresCompleto.get("id")
        elif "gid" in self.dicValoresCompleto:
            dicCondiciones["gid"]=self.dicValoresCompleto.get("gid")
        resp=self.oUtiles.oConsultasPg.deleteDatos(self.nomTabla,dicCondiciones)
        if isinstance(resp, Exception):
            mens="La consulta " + self.oUtiles.oConsultasPg.consulta + " es erronea. El servidor respondio: " + resp.message
        else:
            mens="Ok. Registro borrado"
        self.ui.lbEstado.setText(mens)
        self.setModoNuevo()
        self.estadoGuardado="borrado"

    def txtFiltrar(self):
        if self.listaValoresQlist==None:
            return
        cad=unicode(self.ui.txtFiltrar.text().toUtf8(),"utf-8")
        cad=cad.lower()
        if cad=="" or cad==None:
            return

        self.ui.listWidget.clear()
        for valor in self.listaValoresQlist:
            valor2=valor.lower()
            if cad in valor2:
                self.ui.listWidget.addItem(valor)

    def setNomtabla(self,nomTabla):
        """
        Establece el nombre de la tabla con la que trabaja el formulario
        """
        self.nomTabla=nomTabla
    def getNomTabla(self):
        """
        Devuelve el nombre de la tabla con la que trabaja el formulario
        """
        return self.nomTabla
    def setListaSubDirDescargas(self,listaSubDirDescargas):
        """
        Es una lista de subdirectorios, que colgarán de dTrabajos/id_trabajo.
        Es donde se descarga el archivo bytea. Los datos binarios deben estar en el
        campo archivo de la tabla actual. Ver L{descargarArchivo}
        @type listaSubDirDescargas: lista
        @param listaSubDirDescargas: lista con el subdirectorio a crear para la
            descarga del archivo. No debe incluir ni dTrabajos ni id_trabajo.
            Ejemplo ["lindes", "imagenes", "126"]
            'Edicion', 'Definitivo', o 'Historico'
        """
        self.listaSubDirDescargas=listaSubDirDescargas

    def cargaListaNomCamposBDA(self):
        """
        Lee de la BDA los nombres de los campos de la tabla actual y los carga en la
        variable self.listaNomCampos. A esta lista se le eliminan los campos "geom","archivo",
        que no se deben mostrar nunca en el formulario.
        """
        lista=str.split(self.nomTabla,".")
        esquema=lista[0]
        tabla=lista[1]
        self.listaNomCampos=self.oUtiles.oConsultasPg.sacaNombresCamposTabla_lista(esquema, tabla)
        self.listaNomCampos=self.oUtiles.oUtilidadesListas.eliminaEltosLista(self.listaNomCampos,["geom","archivo"], False)

    def cargaDicValoresCompletoBDAVacios(self):
        """
        Crea un dicciomario nombre_campo:None, y la guarda en self.dicValoresCompleto.
        Todos los valores son inicializados a None. Este diccionario se utiliza para
        mostrar el nombre de los campos en el formulario.
        """
        dic={}
        for campo in self.listaNomCampos:
            dic[campo]=unicode("","utf-8")#si no hago esto no carga los acentos en el formulario
                #la tabla se crea con strings y luego ya no toma unicode.
        self.dicValoresCompleto=dic

    def cargaDicValoresCompletoBDARellenos(self,dicCondiciones):
        """
        Extrae los valores de la base de datos y los introduce en el dicionario self.dicValoresCompleto.
        Este diccionario representa un registro de la tabla actual, sin el campo bytea, si lo tiene.

        @type dicCondiciones: diccionario
        @param dicCondiciones: Si el diccionario está vacío, se carga el registro que
            coincide con el id_trabajo actual. Si contiene elementos nombre_campo:valor,
            se carga el registro cuyo (ELIMINAR id_trabajo coincide con el id_trabajo actual),
            más las condiciones que haya en este diccionario.
        @return: True si todo va bien, None si hay cero o más de un registro seleccionado,
            exception si hay algun problema.
        """

        self.ui.lbEstado.setText("Solicitando datos de la tabla " + self.nomTabla + " al servidor")

        #dic no tiene el campo bytea
        if len(dicCondiciones)==0:
            if "id_trabajo" in self.listaNomCampos:
                lvCondWhere=[self.oUtiles.id_trabajo]
                listaCampos=["id_trabajo"]
        else:
            if "id_trabajo" in self.listaNomCampos:
                lvCondWhere=[self.oUtiles.id_trabajo]+dicCondiciones.values()
                listaCampos=["id_trabajo"]+dicCondiciones.keys()
            else:
                lvCondWhere=dicCondiciones.values()
                listaCampos=dicCondiciones.keys()
        condWhere=self.oUtiles.oConsultasPg.oGeneraExpresionesPsycopg2.generaWhere(listaCampos,"and")
        listaDic=self.oUtiles.oConsultasPg.recuperaDatosTablaByteaDic(self.nomTabla, self.listaNomCampos, condWhere,lvCondWhere)
        if isinstance(listaDic,Exception):
            self.ui.lbEstado.setText(listaDic.message)
            #QtGui.QMessageBox.information(self,"Error en preparaLValoresDeTabla", listaDic.message,1)#self es la ventana pasdre que necesita qmessagebox
            return listaDic
        if len(listaDic)!=1:
            mens="Con los criterios elegidos hay un numero de registros de: " + str(len(listaDic))
            self.ui.lbEstado.setText(mens)
            #QtGui.QMessageBox.information(self,"Error en ctrIntroddatos.cargaDicValoresCompletoBDARellenos", mens,1)#self es la ventana pasdre que necesita qmessagebox
            return None
        self.dicValoresCompleto=listaDic[0]
        return True

    def muestra_DicMostrar_EnFormulario(self,enabled=True):
        """
        Muestra los valores del diccionario self.dicMostrar en el formulario.
        dicMostrar se inicializa con L{prepara_dicMostrar}
        """
        self.oUtiles.oUtilidadesFormularios.rellenaTableWidgetVerticalDic(self.ui.tableWidget,self.dicMostrar,avisarErrores=True,enabled=enabled)
        self.tablaCambiada=False

    def setModoNuevo(self):
        """
        Permite introducir datos en el formulario.
        Carga los nombres de los campos de la BDA.
        Este modo establece los valores de la tabla en blanco.
        Oculta los campos:
            - ["archivo","fecha", "id", "id_trabajo", "gid", "gid_linde", "gid_finca","gid_elem_int","estado_trabajo","usuario"]
        Para que no se puedan introducir valores.
        """
        self.modo="nuevo"
        self.listaCamposOcultar=["archivo","fecha", "id", "id_trabajo", "gid", "gid_linde","gid_elem_int", "gid_finca","estado_trabajo","usuario"]
#       self.ui.tableWidget.setGeometry(QtCore.QRect(10, 40, 701, 401))
        self.cargaDicValoresCompletoBDAVacios()
        self.prepara_DicMostrar()
        self.muestra_DicMostrar_EnFormulario()

        self.ui.tableWidget.setGeometry(QtCore.QRect(10, 40, 741, 401))
        self.ui.tableWidget.setColumnWidth(0,600)#ancho de la columna
        self.ui.tableWidget.setEnabled(True)
        self.ui.listWidget.setVisible(True)
        self.ui.txtFiltrar.setVisible(True)
        self.ui.lbLista.setVisible(True)
        self.ui.bttGuardar.setEnabled(True)
        self.ui.bttBuscar.setVisible(False)
        self.ui.bttDescargar.setVisible(False)
        self.ui.bttNuevo.setVisible(False)

        self.ui.bttEditar.setEnabled(False)
        self.ui.bttBorrar.setVisible(False)
        lista=self.nomTabla.split(".")
        nom=lista[1]
        if nom=="trabajos":
            self.ui.tbId_trabajo.setText("")
            self.ui.tbSrc_trabajo.setText("")

    def setModoEditar(self,dicValoresCompleto=None,dicCondiciones=None):
        """
        Oculta los campos:
            - ["archivo","fecha", "id", "src_trabajo","id_trabajo", "gid","gid_linde", "gid_finca","usuario","estado_trabajo"]
        Para que no se puedan introducir valores.
        @type dicValoresCompleto: None o diccionario
        @param dicValoresCompleto: Si es True carga los valores de la BDA y los muestra
            para que puedan ser modificados. Si es False, lo único que hace
            es permitir cambiar los valores que ya hay en el formulario.
        @type dicCondiciones: boolean
        @param dicCondiciones: Si es True carga los valores de la BDA y los muestra
            para que puedan ser modificados. Si es False, lo único que hace
            es permitir cambiar los valores que ya hay en el formulario.
        """
        self.modo="editar"
        self.listaCamposOcultar=["archivo","fecha", "id", "src_trabajo","id_trabajo", "gid","gid_linde", "gid_finca","gid_elem_int","usuario","estado_trabajo"]
#       self.ui.tableWidget.setGeometry(QtCore.QRect(10, 40, 701, 401))
        self.ui.tableWidget.setGeometry(QtCore.QRect(10, 40, 741, 401))
        self.ui.tableWidget.setColumnWidth(0,600)#ancho de la columna
        self.ui.tableWidget.setEnabled(True)
        self.ui.listWidget.setVisible(True)
        self.ui.txtFiltrar.setVisible(True)
        self.ui.lbLista.setVisible(True)
        self.ui.bttGuardar.setEnabled(True)
        self.ui.bttBuscar.setVisible(False)
        self.ui.bttDescargar.setVisible(False)
        self.ui.bttNuevo.setVisible(False)

        self.ui.bttEditar.setEnabled(False)
        self.ui.bttBorrar.setVisible(True)

        if dicValoresCompleto!=None:
            self.dicValoresCompleto=dicValoresCompleto
        elif dicCondiciones!=None:
            self.cargaDicValoresCompletoBDARellenos(dicCondiciones)

        self.prepara_DicMostrar()
        self.muestra_DicMostrar_EnFormulario()

    def setModoConsultar(self, mostrarBttNuevo=False, dicValoresCompleto=None, dicCondiciones=None):
        """
        No deja editar valores y muestra todos los campos de la tabla
        menos los de la lista ["archivo","id_trabajo","src_trabajo","geom"], que el campo bytea de la tabla y
        el de la geometria. Estos campos no se mostraran nunca.

        Si dicValoresCompleto=None y dicCondiciones=None, lo único que hace
        es deshabilitar los controles para que no se puedan modificar los valores.

        @type mostrarBttNuevo: boolean
        @param mostrarBttNuevo: Si es true, muestra el botón Nuevo, que da la posibilidad
            de añadir nuevos registros a la tabla.
        @type dicValoresCompleto: None o Diccionario
        @param dicValoresCompleto: Diccionario con los valores del registro de la tabla
            con el que se quiere trabajar en el cuadro de diálogo. Se asigna directamente,
            sin ninguna consulta a la BDA.
            El diccionario es nombre_campo:valor. con todos los valores de los campos,
            sin campo Bytea. Si este parámetro es diferente de None, da igual el siguiente
            parámetro.
        @type dicCondiciones: None o diccionario
        @param dicCondiciones: Si es None no se carga nada de la BDA. Si es un
            diccionario vacio {}, se carga el registro de la tabla que
            coincide con el id_trabajo actual. Si es un diccionario con valores,
            se carga el registro cuyo id_trabajo
            coincide con el id_trabajo actual, más las condiciones que haya en este diccionario.
            El diccionario es nombre_campo:valor.
        @return: True si todo va bien, None si hay cero o más de un registro seleccionado,
            exception si hay algun problema.
        """
        if dicValoresCompleto!=None:
            if dicValoresCompleto.__class__.__name__=="dict":
                self.dicValoresCompleto=dicValoresCompleto
            else:
                return Exception("El parametro dicValoresCompleto, debe ser diciconario o None")
        elif dicCondiciones!=None:
            if dicCondiciones.__class__.__name__=="dict":
                resp=self.cargaDicValoresCompletoBDARellenos(dicCondiciones)
                if isinstance(resp,Exception):
                    self.setEstadoGuardado(nuevoEstado="no guardado")
                    return resp
                elif resp!=True:
                    self.setEstadoGuardado(nuevoEstado="no guardado")
                    return None
            else:
                return Exception("El parametro dicCondiciones, debe ser diciconario o None")

        self.modo="consultar"
        self.listaCamposOcultar=["archivo","id_trabajo","src_trabajo"]

        self.setEstadoGuardado(nuevoEstado="guardado")
        self.ui.tableWidget.setGeometry(QtCore.QRect(10, 40, 961, 401))
        self.ui.tableWidget.setColumnWidth(0,820)#ancho de la columna
        self.ui.tableWidget.setEnabled(False)
        self.ui.listWidget.setVisible(False)
        self.ui.txtFiltrar.setVisible(False)
        self.ui.lbLista.setVisible(False)
        self.ui.bttGuardar.setEnabled(False)
        self.ui.bttBuscar.setVisible(False)

        if self.oUtiles.tipo_usuario=="admin_propiedad":
            self.ui.bttEditar.setEnabled(True)
            self.ui.bttBorrar.setVisible(False)
            if mostrarBttNuevo==True:
                self.ui.bttNuevo.setVisible(True)
            else:
                self.ui.bttNuevo.setVisible(False)
        elif self.oUtiles.usuario==self.oUtiles.usuario_creador_trabajo and self.oUtiles.prefijo_tipo_trabajo=="ed_":
            #si no es administrador o es el mismo que ha creado el trabajo
            #y el trabajo esta en edicion, no debe editar, borrar o añadir datos
            #esto tabien debe ser proramado en la base de datos
            self.ui.bttEditar.setEnabled(True)
            self.ui.bttBorrar.setVisible(False)
            if mostrarBttNuevo==True:
                self.ui.bttNuevo.setVisible(True)
            else:
                self.ui.bttNuevo.setVisible(False)
        else:
            self.ui.bttEditar.setEnabled(False)
            self.ui.bttBorrar.setVisible(False)
            self.ui.bttNuevo.setVisible(False)

        try:
            nom_arch=self.dicValoresCompleto["nom_arch"]
            if nom_arch!="":
                self.ui.bttDescargar.setVisible(True)
        except:
            pass

        self.prepara_DicMostrar()
        self.muestra_DicMostrar_EnFormulario(enabled=False)
        self.setEstadoGuardado(nuevoEstado="guardado")
        return True
    def setModoBuscar(self):
        """
        Muestra todos los campos de la tabla a editar menos los de la lista:
            - ["archivo", "geom"].
        Esta disponible el boton bttBuscar. Este botón no está programado en esta clase.
        sino en la clase ctrIntrodatos_Buscar.
        Este botón busca registros coincidentes
        con los datos introducidos en el cuadro de dialogo. La busqueda se realiza en
        la tabla self.nomTabla, que es la tabla actual del formulario. Si hay resultados,
        se muestran en otro cuadro de dialogo. De ese cuadro de dialogo, se selecciona
        una fila, y se muestra el trabajo completo en ctrPpal.
        """
        self.modo="buscar"
        self.listaCamposOcultar=["archivo"]
        self.ui.tableWidget.setGeometry(QtCore.QRect(10, 40, 741, 401))
        self.ui.tableWidget.setColumnWidth(0,600)#ancho de la columna
        self.ui.tableWidget.setEnabled(True)
        self.ui.listWidget.setVisible(True)
        self.ui.txtFiltrar.setVisible(True)
        self.ui.lbLista.setVisible(True)
        self.ui.bttGuardar.setEnabled(False)
        self.ui.bttBuscar.setVisible(True)
        self.ui.bttDescargar.setVisible(False)
        self.ui.bttNuevo.setVisible(False)

        self.ui.bttEditar.setEnabled(False)
        self.ui.bttBorrar.setVisible(False)

        self.cargaDicValoresCompletoBDAVacios()
        self.prepara_DicMostrar()
        self.muestra_DicMostrar_EnFormulario()

    def prepara_DicMostrar(self):
        """
        Elimina, del diccionario que representa la tabla completa de la bda,
        los campos que no deben mostrarse, según el modo actual.
        Este metodo debe ejecutarse despues de cargaDicValoresCompletoBDARellenos o
        cargadicValoresCompletoVacios, para que self.dicValoresCompleto esté inicializado.
        """
        self.dicMostrar=self.oUtiles.oUtilidades.eliminaEltosDicLClaves(self.dicValoresCompleto,self.listaCamposOcultar,False)
        #self.muestra_DicMostrar_EnFormulario()
        titulo=QtCore.QString("Modo " + self.modo + ". Datos de " + self.nomTabla)
        self.setWindowTitle(titulo)
        self.tablaCambiada=False

    def cargaDicValoresCompleto_delFormulario(self,compTodos=True):
        """
        Extrae los valores del formulario y prepara el diccionario,
        self.dicValoresCompleto con los nombres de los campos de la tabla
        y los valores introducidos.
        Examina la variable self.archivoBytea y self.actualizaArchivoBytea
        para saber si se añade al diccionario el archivo bytea.
        Si hay algun problema. El anterior archivo se borrara.
        Tabien genera la variable self.dicEnviar, que elimina todos los campos
        que no tienen valor.
        Se encarga de avisar con una ventana de si hay algún problema.
        @type compTodos: boolean
        @param compTodos: Si es False comprueba unicamente los valores de los campos
            que tienen valor, por lo que acepta valores de dominio en blanco. Si es
            True, da un mensaje y, devuelve False, si hay un campo de dominio sin su valor correcto o en blanco.
        @return: True si todo va bien, False si hay algun problema
        """

        resp=self.compruebaValores_delFormulario(compTodos)
        if resp==False:
            self.ui.lbEstado.setText("Datos no correctos. Corrija los datos y vuelva a intentarlo.")
            return False
        n=self.ui.tableWidget.rowCount()
        for i in range(n):#devuelve un iterador 0...n-1
            #if valorTablaForm != "":
            valorTablaForm=unicode(self.ui.tableWidget.item(i,0).text().toUtf8(),"utf-8")
            if valorTablaForm==unicode("","utf-8"):
                valorTablaForm=None
            nomCampo=unicode(self.ui.tableWidget.verticalHeaderItem(i).text().toUtf8(),"utf-8")
            self.dicValoresCompleto.update([[nomCampo,valorTablaForm]])

        if self.getModo()!="buscar":#si el modo es buscar no debe añadir la fecha actual
                #si no se añade como una de las condiciones a la hora de buscar
            existeFecha=self.oUtiles.oUtilidadesListas.existeEltoEnLista(self.dicValoresCompleto.keys(),"fecha")
            if existeFecha:
                #añado la fecha actual si existe. No dejo que la ponga el usuario
                fecha=datetime.date.today()
                self.dicValoresCompleto.update([["fecha",fecha]])
        else:
            self.oUtiles.oUtilidades.eliminaEltosDicLClaves(self.dicValoresCompleto,["fecha"],False)

        self.limpiaDicValoresEnviar()#elimino los valores con campos en blanco

        #tratamiento del archivo bytea
        if self.getModo()=="nuevo":
            if self.archivoBytea!=None:#tiene algo. Puede ser tambien " ", lo cual boora el archivo
                #de la base de datos
                self.dicEnviar.update([["archivo",self.archivoBytea]])
        elif self.getModo()=="editar":
            if self.actualizarArchivoBytea==False:
                self.dicEnviar=self.oUtiles.oUtilidades.eliminaEltosDicLClaves(self.dicEnviar,["archivo"],False)
            else:
                #hay que actualizar
                self.dicEnviar.update([["archivo",self.archivoBytea]])
        return True

    def limpiaDicValoresEnviar(self):
        """
        Almacena en self.dicEnviar el diccionario que se enviara a la base de datos.
        Lo que hace es eliminar de self.dicValoresCompleto los valores en blanco.
        """
        self.dicEnviar=self.oUtiles.oUtilidades.eliminaEltosDicLValores(self.dicValoresCompleto,[""])

    def insertaValor(self, elemClicado):
        """
        Inserta en la fila actual de la tabla, el elemento de la lista en el que se ha
        hecho doble click
        """
        filaSeleccionada=self.ui.tableWidget.currentRow()
        if filaSeleccionada==None:
            QtGui.QMessageBox.information(self,"Mensaje", "No hay ninguna fila seleccionada",1)#self es la ventana pasdre que necesita qmessagebox
        else:
#            newitem = QtGui.QTableWidgetItem(elemClicado.text())
#            self.ui.tableWidget.setItem(filaSeleccionada, 0, newitem)
            self.ui.tableWidget.item(filaSeleccionada, 0).setText(elemClicado.text())
    def tabla_cambiada(self,filaSeleccionada, columna):
        """
        Se ejecuta cada vez que hay un cambio en la tabla. Se utiliza para saber si hay
        que enviar los datos a la base de datos o no.
        """
        self.tablaCambiada=True

    def tabla_click(self,filaSeleccionada, columna):
        """
        Evento clic en la tabla de datos.
        Si el usuario cambia de campo, este método cambia los posibles valores en la
        lista, es decir carga los valores de los dominios.
        """
        item=self.ui.tableWidget.verticalHeaderItem(filaSeleccionada)
        nombreCampo=str(item.text().toUtf8()) #esto funciona, pero hace que los nombres de los campos no puedan tener acentos ni eñes
        self.listaValoresQlist=None
        self.ui.listWidget.clear()
        self.ui.txtFiltrar.setText("")
        if nombreCampo=="nom_arch":
            #Hay que seleccionar un archivo
            self.seleccionaArchivo(filaSeleccionada)
            return
        listaValores = self.oUtiles.oDicDominios.get(nombreCampo)
        self.listaValoresQlist=listaValores

        if listaValores==None:#el campo no tiene posibles valores
            return
        #tipoDevuelto=listaValores[0].class.name #debe ser siempre unicode
        for valor in listaValores:
            self.ui.listWidget.addItem(valor)

    def terminar(self):
        """
        Cierra el formulario
        """
        self.close()

    def descargarArchivo(self):
        """
        Descarga el archivo, guardado en el campo "archivo" de la tabla self.nomTabla
        y lo guarda en self.oUtiles.dTrabajos + "/"+ self.oUtiles.id_trabajo
        + "/" + ...self.listaSubDirDescargas... + "/"+ nom_arch
        """
        try:
            nom_arch=self.dicValoresCompleto["nom_arch"]
        except Exception,e:
            mens=unicode("Error. El campo nom_arch no está entre los nombres de los campos","utf-8")
            self.ui.lbEstado.setText(mens)
            return
        subDir=self.oUtiles.oUtilidades.uneSubDir(self.listaSubDirDescargas)
        nom_arch=self.oUtiles.dTrabajos + subDir + nom_arch

        #primero comprueba que el archivo no haya sido descargado ya,
        #en tal caso no hace falta que vuelva a descargarArchivose del servidor
        if os.path.exists(nom_arch):
            mens="El archivo ya estaba descargado en: " + nom_arch
            self.ui.lbEstado.setText(mens)
            return

        #la imagen no habia sido descargada
        #compruebo que los directorios existen y si no los creo
        rr=self.oUtiles.oUtilidades.creaDir(self.oUtiles.dTrabajos,self.listaSubDirDescargas,True)#devuelve Exception si no va bien
        if isinstance(rr,Exception):
            self.ui.lbEstado.setText(rr.message)
            return#no hace falta dar mensajes, ya se ha avisado de lo
            #que pasa en la funcion creaDirImagenes

        self.ui.lbEstado.setText("Recuperando de la base de datos. Espere ...")
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
        condWhere=self.oUtiles.oConsultasPg.oGeneraExpresionesPsycopg2.generaWhere(lCamposCondWhere, "and")
        resp=self.oUtiles.oArchivos.descargaYgrabaArchivo(self.oUtiles.oConsultasPg,self.nomTabla,"archivo",condWhere,lvCondWhere,nom_arch)
        if isinstance(resp, Exception):
            mens=resp.message
        else:
            mens="Archivo descargado en: " + nom_arch
        self.ui.lbEstado.setText(mens)

    def compruebaValores_delFormulario(self,compTodos=True):
        """
        Comprueba que todos los valores introducidos en los campos con dominio
        no han sido modificados.
        @type compTodos: Boolean
        @param compTodos: Si es False, no comprueba los campos de la tabla sin valor.
        @return: True, si todos los valores cumplen: False en caso contrario
        """

        n=self.ui.tableWidget.rowCount()
        for i in range(n):#devuelve un iterador 0...n-1
            if compTodos==False:
                if self.ui.tableWidget.item(i,0).text()=="":
                    continue#se salta la comprobacion de valores vacios
            nomCampo=unicode(self.ui.tableWidget.verticalHeaderItem(i).text().toUtf8(),"utf-8")
            listaValores = self.oUtiles.oDicDominios.get(nomCampo)
            if listaValores!=None:#el campo tiene posibles valores
                existe=False
                valorTablaForm=unicode(self.ui.tableWidget.item(i,0).text().toUtf8(),"utf-8")#saco del formulario y lo
                        #vuelvo a transformar en UTF-8, que es lo que viene de la bda
                existe=self.oUtiles.oUtilidadesListas.existeEltoEnLista(listaValores,valorTablaForm)

                if existe==False:
                    #no lo ha encontrado. No coincide con ningun valor del dominio
                    mens=QtCore.QString("El valor para el campo " + nomCampo + " no esta en la lista de valores")
                    QtGui.QMessageBox.information(self,"Error en los valores",mens ,1)#self es la ventana pasdre que necesita qmessagebox
                    return False
            else:
                #compruebo que no exceda de 100 caracteres
                valorTablaForm=self.ui.tableWidget.item(i,0).text().toUtf8()
                if len(valorTablaForm)>100:
                    mens=unicode("El valor para el campo ", "utf-8")
                    mens=mens + unicode(nomCampo,"utf-8")
                    mens=mens + unicode(" excede de 100 caracteres","utf-8")
                    QtGui.QMessageBox.information(self,"Error en los valores",mens ,1)#self es la ventana pasdre que necesita qmessagebox
                    return False

    def seleccionaArchivo(self,filaSeleccionada):
        """
        Abre un cuadro de dialogo para seleccionar el archivo de memoria. Debe ser un PDF.
        Carga el archivo y lo almacena en un string de binarios, listo para ser enviado
        a un campo bytea.
        Si se esta en modo editar y se realizan cambios, pero no se cambia e archivo,
        el archivo no se vuelve a enviar a la base de datos.
        Si se esta en modo editar, y se cambia el nombre del archivo, se vuelve a cargar.
        La variable de clase self.actualizarArchivoBytea cambia a True, para que sea
        enviado de nuevo a la base de datos desde el método self.guardar
        En el campo nom_arch de la tabla del formulario, unicamente se queda el nombre 
        del archivo, que es lo que se enviara a la base de datos
        """
        if self.getModo()=="editar":
            self.actualizarArchivoBytea=True
        else:
            self.actualizarArchivoBytea=False
            
        qf= QtGui.QFileDialog()
        qf.setFileMode(QtGui.QFileDialog.AnyFile)
#        fileName = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open SVG File"),self.currentPath, "*.svg")
        if "img_" in self.nomTabla:
            nombreArchivo= QtGui.QFileDialog.getOpenFileName(self, "Seleccionar archivo","","*.jpg *.png")
        else:
            nombreArchivo= QtGui.QFileDialog.getOpenFileName(self, "Seleccionar archivo","","*.pdf")
        nombreArchivo=unicode(nombreArchivo.toUtf8(),"utf-8")
        if os.path.exists(nombreArchivo):
            self.ui.tableWidget.item(filaSeleccionada, 0).setText(nombreArchivo)
            if os.path.getsize(nombreArchivo)>1024000: #1 mb
                mens=unicode("Archivo demasiado grande. El tamaño esta limitado a 1 mb (1024 kb). Debe comprimir las imágenes antes de introducirlas en el PDF.","utf-8")
                self.ui.lbEstado.setText(mens)
                self.ui.tableWidget.item(filaSeleccionada, 0).setText(unicode("","utf-8"))
                self.archivoBytea=None
                return
            self.ui.lbEstado.setText("Cargando el archivo en memoria. Espere ...")
            self.archivoBytea=self.oUtiles.oArchivos.leeDatBinarios(nombreArchivo)
            if isinstance(self.archivoBytea,Exception):
                QtGui.QMessageBox.information(self,"Mensaje", self.archivoBytea.message,1)
                self.ui.lbEstado.setText("Error al cargar el archivo.")
                self.archivoBytea=None
                self.ui.tableWidget.item(filaSeleccionada, 0).setText(unicode("","utf-8"))
                return
            nom=os.path.basename(nombreArchivo)
            self.ui.tableWidget.item(filaSeleccionada, 0).setText(nom)
            mens=unicode("Archivo cargado en memoria con éxito.","utf-8")
            self.ui.lbEstado.setText(mens)     
        else:
            self.ui.tableWidget.item(filaSeleccionada, 0).setText(unicode("","utf-8"))
            self.ui.lbEstado.setText("El archivo no existe.")
            self.archivoBytea=None

    def getModo(self):
        """
        Devuelve el modo de uso del formulario. Puede ser:
            - nuevo.
            - editar.
            - consultar
            - buscar
        """
        return self.modo
    def getTablaCambiada(self):
        """
        @return: Devuelve True si la tabla ha sido cambiada y es necesario
            reenviar los datos a la BDA.
        """
        return self.tablaCambiada
    def setEstadoGuardado(self,nuevoEstado):
        """
        Establece si la tabla ha sido guardada al menos una vez.
        @type nuevoEstado: strind
        @param nuevoEstado: Puede ser "guardado" o None
        """
        self.estadoGuardado=nuevoEstado
    def getEstadoGuardado(self):
        """
        Devuelve "guardado" si la tabla ha sido guardada al menos una vez.
        @return: "guardado" si la tabla ha sido guardada al menos una vez.
            None en caso contrario.
        """
        return self.estadoGuardado

    def closeEvent(self, event):
        """
        Evento que permite abrir una
        ventana de dialogo para confirmar la salida del programa
        """
        #Se genera la respuesta de la confirmacion de salir
        if self.tablaCambiada==True:
            mens=unicode("Datos no salvados. ¿Seguro que desea salir?","utf-8")
            reply = QtGui.QMessageBox.question(self, "Mensaje", mens, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                #event.accept()
                self.setVisible(False)
            else:
                event.ignore()
        else:
            self.setVisible(False)

    def toUtf8(self,mens):
        return unicode(mens,"utf-8")