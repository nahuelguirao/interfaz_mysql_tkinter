import mysql.connector
import os
import subprocess
import datetime

#RECORDAR ACTUALIZAR LOS DATOS DE CONEXIÓN en el modulo carpeta.datos_conexion.py

#Rutas dinamicas 
carpeta_principal = os.path.dirname(__file__)
carpeta_copias_seguridad = os.path.join(carpeta_principal,"copias_seguridad")

class BaseDeDatos():
    #Metodo constructor
    def __init__(self,**kwargs):
        self.conexion = mysql.connector.connect(**kwargs)
        self.host = kwargs["host"]
        self.user = kwargs["user"]
        self.password = kwargs["password"]
        self.cursor = self.conexion.cursor()
        self.conexion_cerrada = False
    
    #FUNCIONES DECORADORAS
    #Funcion decoradora para verificar si existe una base de datos
    def comprobar_bd(funcion_externa):
        def comprobar_bd_interno(self, base_dato, *args):
            #Comprueba si la base de datos del parametro existe
            consulta = f"SHOW DATABASES LIKE '{base_dato}'"
            self.cursor.execute(consulta)
            if not self.cursor.fetchone():
                #Si no existe muestra mensaje y se cierra conexión
                self.resultado = f"'{base_dato}' no existe."
                self.cursor.close()
                self.conexion.close()
                return self.resultado
            return funcion_externa(self, base_dato, *args)
        return comprobar_bd_interno
    #Funcion decoradora para verificar si existe la tabla
    def comprobar_tabla(funcion_externa):
        #Comprueba si existe la tabla en la bd
        def comprobar_tabla_interno(self, base_dato, nombre_tabla, *args):
            self.cursor.execute(f"USE {base_dato};")
            self.cursor.execute(f"SHOW TABLES LIKE '{nombre_tabla}';")
            #Si encuentra resultado continua el proceso
            if self.cursor.fetchone():
                return funcion_externa(self, base_dato, nombre_tabla, *args)
            #Sino se cierra conexión
            else:
                self.resultado = f"La tabla '{nombre_tabla}' no existe."
                self.cursor.close()
                self.conexion.close()
                return self.resultado
        return comprobar_tabla_interno
    #Función decoradora para cerrar cursor y conexión
    def abrir_conexion_cierre(funcion_externa):
        def funcion_interna(self, *args, **kwargs):
            try:
                #Abre la conexión
                if self.conexion_cerrada:
                    self.conexion = mysql.connector.connect(host = self.host, user = self.user, password = self.password)
                    self.cursor = self.conexion.cursor()
                #Ejecuta la funcion externa
                funcion_externa(self, *args, **kwargs)
            except:
                print("Ocurrió un error")
            finally:
                #Si la conexión esta cerrada no hace nada
                if self.conexion_cerrada:
                    pass
                #Cierra la conexión si esta abierta (ya ejecutada la función externa)
                else:
                    self.cursor.close()
                    self.conexion.close()
                    self.conexion_cerrada = True
                #Retorna self.resultado para ejectuar los resultados en la interfaz gráfica una vez cerrada la conexion
                return self.resultado
        return funcion_interna
    
    #METODOS
    #Metodo para ejecutar consultas SQL introduciendola como parametro
    @abrir_conexion_cierre
    @comprobar_bd
    def consultar(self, bd, query):
        try:
            #Ejecuta la consulta
            self.cursor.execute(f"USE {bd};")
            self.cursor.execute(query)
            self.resultado = self.cursor.fetchall()
            #Itera los resultados encontrados y los retorna
            return self.resultado
        except:
            #En caso de que la consulta SQL no sea correcta
            self.resultado = "Algo ha salido mal, revise su consulta SQL y pruebe nuevamente."
            return self.resultado
    
    #Metodo para mostrar todas las bases de datos existentes en el servidor directamente
    @abrir_conexion_cierre
    def mostrar_bd(self):
        #Ejecuta la consulta SHOW DATABASES y retorna los resultados
        self.cursor.execute("SHOW DATABASES;")
        self.resultado = self.cursor.fetchall()
        return self.resultado
    
    #Metodo para crear una base de datos
    @abrir_conexion_cierre
    def crear_bd(self,nombre_bd):
        try:
            #Ejecuta la consulta para crear la bd con el nombre que se pasó como parametro
            self.cursor.execute(f"CREATE DATABASE {nombre_bd}")
            self.resultado = f"'{nombre_bd}' se creó correctamente.\n"
            return self.resultado
        except:
            #Mensaje en caso de que no se pueda crear la base de datos
            self.resultado = f"'{nombre_bd}' no se pudo crear, intente nuevamente.\n"
            return self.resultado

    #Metodo para eliminar una base de datos 
    @abrir_conexion_cierre
    @comprobar_bd
    def eliminar_bd(self,nombre_bd):
        #Ejecuta la consulta para eliminar la base de datos que se pasó como parametro
        self.cursor.execute(f"DROP DATABASE {nombre_bd};")
        self.resultado = f"'{nombre_bd}' se eliminó correctamente."
        return self.resultado
    
    #Metodo para realizar backup de una bd
    @abrir_conexion_cierre
    @comprobar_bd
    def backup(self, nombre_bd):
        try:
            #Obtiene la fecha actual y la formatea con strftime
            fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            with open(f'{carpeta_copias_seguridad}\\{nombre_bd}_{fecha_hora_actual}.sql', 'w') as out:
                #Accedo a la bd con mysqldump y envia los datos recibidos al archivo que se abrio con with open
                subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysqldump --user=root --password={self.password} --databases {nombre_bd}', shell=True, stdout=out,stderr=subprocess.PIPE)
                self.resultado = f"Se creó una copia de seguridad de '{nombre_bd}'."
                return self.resultado
        except:
            self.resultado = "Algo salio mal, intente nuevamente."
            return self.resultado
    
    #Metodo para crear una tabla 
    @abrir_conexion_cierre
    @comprobar_bd
    def crear_tabla(self,base_dato, nombre_tabla, query):
        try:
            #Crea la tabla con el query creado en la interfaz gráfica
            self.cursor.execute(f"USE {base_dato}")
            self.cursor.execute(query)
            self.resultado = f"La tabla '{nombre_tabla}' se creó exitosamente"
            return self.resultado
        except:
            self.resultado = f"Ocurrio un error creando la tabla '{nombre_tabla}', pruebe nuevamente."
            return self.resultado

    #Metodo para eliminar una tabla
    @abrir_conexion_cierre
    @comprobar_bd
    @comprobar_tabla
    def eliminar_tabla(self, base_dato, nombre_tabla):
        #Ejecuta el query eliminando la tabla que se pasa como parametro
        self.cursor.execute(f"USE {base_dato}")
        self.cursor.execute(f"DROP TABLE {nombre_tabla}")
        self.resultado = f"La tabla '{nombre_tabla}' se eliminó correctamente."
        return self.resultado
    
    #Metodo para mostrar las tablas existentes dentro de una bd
    @abrir_conexion_cierre
    @comprobar_bd
    def mostrar_tablas(self, base_dato):
        #En caso de que exista la bd, ejecuta las consultas
        self.cursor.execute(f"USE {base_dato};")
        self.cursor.execute("SHOW TABLES;")
        resultado = self.cursor.fetchall()
        self.resultado = resultado
        if resultado:
            return self.resultado
        #En caso de que no tenga tablas
        else:
            return f"La base de datos '{base_dato}' se ha encontrado pero no posee ninguna tabla."

    #Metodo para borrar un registro (con una condición en particular)
    @abrir_conexion_cierre
    @comprobar_bd
    @comprobar_tabla
    def borrar_registro(self, base_dato, nombre_tabla, condicion):
        try:
            #Ejecuta la consulta 
            self.cursor.execute(f"USE {base_dato}")
            query = f"DELETE FROM {nombre_tabla} WHERE {condicion};"
            self.cursor.execute(query)
            #Guarda los cambios
            self.conexion.commit()
            self.resultado = "Los registros se eliminaron correctamente."
            return self.resultado
        except:
            self.resultado = "Ocurrio un error, compruebe si la condición ingresada es válida."
            return self.resultado
            
    #Metodo para borrar todos los registros de una tabla
    @abrir_conexion_cierre
    @comprobar_bd
    @comprobar_tabla
    def borrar_todos_los_registros(self, base_dato, nombre_tabla):
        #Ejecuta y elimina todos los registros
        self.cursor.execute(f"USE {base_dato};")
        self.cursor.execute(f"TRUNCATE TABLE {nombre_tabla}")
        self.conexion.commit()
        self.resultado = f"Se borraron todos los registros de la tabla '{base_dato}.{nombre_tabla}'"
        return self.resultado 

    #Metodo para actualizar un registro
    @abrir_conexion_cierre
    @comprobar_bd
    @comprobar_tabla
    def actualizar_registro(self, base_dato, nombre_tabla, columnas, condicion):
        #Arma la consulta con los datos del parametro y la ejecuta
        self.cursor.execute(f"USE {base_dato};")
        query = f"UPDATE {nombre_tabla} SET {columnas} WHERE {condicion}"
        self.cursor.execute(query)
        self.conexion.commit()
        self.resultado = "Cambios realizados con exito."
        return self.resultado