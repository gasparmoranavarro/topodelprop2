#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Gaspar
#
# Created:     11/09/2012
# Copyright:   (c) Gaspar 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import pyGenGas
import pyPgGas

class UtilesPgTriggers(object):
    def __init__(self,bda,usuario,psw,host, port):
        self.oConectaPg=pyPgGas.ConectaPg(bda,usuario,psw,host,port)
        self.oConsultasPg=pyPgGas.ConsultasPg(self.oConectaPg)
        self.expresionesPG=pyPgGas.GeneraExpresionesPsycopg2()
        self.oUtilidadesListas=pyGenGas.UtilidadesListas()

    def creaTriggerListaTablas(self,nombreFuncion,listaTablas,beforAfter,cadenaEventos):
        """
        crea un trigger llamado nombre_funcion_nombreTabla para cada tabla.
        Ejemplo:
            - creaTriggerListaTablas(nombreFuncion=["script.acceso_trabajo"],listaTablas=["ed_comun.ed_planos"],
                        beforAfter="BEFORE",cadenaEventos="INSERT OR DELETE OR UPDATE")
        Crea el trigger acceso_trabajo_ed_planos para la tabla "ed_comun.ed_planos", que ejecuta la funcion
        disparadora "script.acceso_trabajo", antes de insertar, borrar o actualizar.
        Los nombre de las tablas deben llevar el esquema delante, aunque sea el esquema public
        nombreFuncion va sin paréntesis Y con el nombre del esquema delante, aunque sea public.nombre_funcion
        "CREATE TRIGGER comprueba_superposicion_finca BEFORE insert or update ON huso30.fincas FOR EACH ROW EXECUTE PROCEDURE comprueba_superposicion()"
        @raise: Exception
        """


        for nomTablaCompleto in listaTablas:
            nomTabla=nomTablaCompleto.split(".")[1]
            nombreFun=nombreFuncion.split(".")[1]
            consulta="CREATE TRIGGER " + nombreFun + "_" + nomTabla + " " + beforAfter + " " + cadenaEventos + " ON " + nomTablaCompleto + " FOR EACH ROW EXECUTE PROCEDURE " + nombreFuncion + "()"
            try:
                self.oConectaPg.cursor.execute(consulta)
                self.oConectaPg.conn.commit()
                print consulta + ": OK."
            except Exception,e:
                self.oConectaPg.conn.commit()
                print e.message
                raise Exception(e.message)
                exit

    def dropTriggerListaTablas(self,nombreFuncion,listaTablas):
        """
        Borra de las tablas el trigger
        Los nombre de las tablas deben llevar el esquema delante, aunque sea el esquema public
        nombreFuncion va sin paréntesis Y con el nombre del esquema delante, aunque sea public.nombre_funcion
        drop trigger if exists nombre_trigger on nombreTablaCompleto
        @raise: Exception
        """
        for nomTablaCompleto in listaTablas:
            nomTabla=nomTablaCompleto.split(".")[1]
            nombreFun=nombreFuncion.split(".")[1]
            consulta="DROP TRIGGER IF EXISTS " + nombreFun + "_" + nomTabla + "  ON " + nomTablaCompleto
            try:
                self.oConectaPg.cursor.execute(consulta)
                self.oConectaPg.conn.commit()
                print consulta + ": OK."
            except Exception,e:
                self.oConectaPg.conn.commit()
                print e.message
                raise Exception(e.message)
                exit
