import customtkinter as ctk
import tkinter as tk
import os 
from PIL import Image
import carpeta.datos_conexion as conexion
import carpeta.base_datos_clase as bd

#RECORDAR ACTUALIZAR LOS DATOS DE CONEXIÓN MYSQL en el modulo carpeta.datos_conexion.py

#Carpetas y Rutas
carpeta_principal = os.path.dirname(__file__)
carpeta_img = os.path.join(carpeta_principal,"img")
icono = os.path.join(carpeta_img,"logito.ico")

#Instanciación de la clase
base_datos = bd.BaseDeDatos(**conexion.datos_acceso)

#Font Family
font_family = ("Raleway", 16, tk.font.BOLD)

#Color y Tema
ctk.set_appearance_mode("system")  #System tomará el modo de aparencia predeterminado por el sistema (Ya sea claro u oscuro)
ctk.set_default_color_theme("blue") 

#Ventana Login
class Login:
    def __init__(self):
        #Ventana Login
        self.root = ctk.CTk()
        self.root.title("Proyecto")
        self.root.iconbitmap(icono)
        #Para que aparezca centrada la ventana al emerger
        dimesion = 325
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion) // 2
        eje_y = (alto_pantalla - dimesion) // 2
        self.root.geometry(f"{dimesion}x{dimesion}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        self.root.resizable(False,False)
        #imagen
        imagen = ctk.CTkImage(Image.open(os.path.join(carpeta_img,"pera.png")),size=(50,50))
        etiqueta_1 = ctk.CTkLabel(master= self.root, image=imagen, text="")
        etiqueta_1.pack(pady = 15)
        #User
        ctk.CTkLabel(self.root, text="Usuario:", pady=10).pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Ingrese usuario.")
        self.usuario.bind("<Button-1>", lambda x: self.usuario.delete(0, 'end'))
        self.usuario.pack()
        #Password
        ctk.CTkLabel(self.root, text="Contraseña:", pady= 10).pack()
        self.password = ctk.CTkEntry(self.root, show="*")
        self.password.insert(0,"*"*7)
        self.password.bind("<Button-1>", lambda x: self.password.delete(0,'end'))
        self.password.pack()
        #Button
        ctk.CTkButton(self.root, text="Ingresar",command=self.verificar_login).pack(pady=30)
        #Mantener la ventana abierta
        self.root.mainloop()
    #Método para verificar login válido
    def verificar_login(self):
        #Obtiene los datos ingresados en los entrys
        usuario = self.usuario.get()
        password = self.password.get()
        #Si los datos son correctos
        if usuario == conexion.datos_acceso["user"] and password == conexion.datos_acceso["password"]:
            #Corrobora si hay un label previo (en caso de que si lo elimina)
            if hasattr(self,"info_login"):
                self.info_login.destroy()
            self.info_login = ctk.CTkLabel(self.root, text=f"Bienvenido {usuario}! Aguarde un momento.")
            self.info_login.pack()
            #Destruye la ventana de login en caso de que se ingresen datos correctos
            self.root.destroy()
            #Instancia la ventana con las opciones una vez logeado
            ventana_opciones = Opciones()
        #Si los datos no son correctos
        else:
            if hasattr(self,"info_login"):
                self.info_login.destroy()
            self.info_login = ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectas.",width=200)
            self.info_login.pack()

#Ventanas TopLevel Funciones
class Funciones:
    def consulta_sql(self):
        #Ventana 
        ventana = ctk.CTkToplevel()
        ventana.title("Consulta SQL")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (800,575)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=10,padx=10)
        #Label bd
        self.label_bd = ctk.CTkLabel(frame,text="Ingrese base de datos: ", font=font_family)
        self.label_bd.grid(row=0,column=0,padx=10,pady=10,sticky='e')
        #Entry base datos
        self.entry_bd = ctk.CTkEntry(frame,width=400, font=font_family)
        self.entry_bd.grid(row=0,column=1,padx=10,pady=10)
        #Label query
        self.label_query = ctk.CTkLabel(frame,text="Consulta SQL: ",font=font_family)
        self.label_query.grid(row=1,column=0,padx=10,pady=5,sticky='e')
        #Entry query
        self.entry_query = ctk.CTkEntry(frame,width=400)
        self.entry_query.configure(font=font_family)
        self.entry_query.grid(row=1,column=1,padx=10,pady=10)
        #Método interno busqueda resultados
        def registros():
            #Obtiene los entry
            bd = self.entry_bd.get()
            query = self.entry_query.get()
            #Si hay datos viejos los elimina
            self.texto.delete("1.0","end")
            #Obtiene los resultados
            resultado = base_datos.consultar(bd,query)
            #Si esta mal la consulta SQL
            if resultado == "Algo ha salido mal, revise su consulta SQL y pruebe nuevamente.":
                self.contador.configure(text="Consulta SQL invalida, pruebe nuevamente.")
            #Si el entry bd esta vacío
            elif bd == "":
                self.contador.configure(text="Ingrese el nombre de la base de datos.")
            #Si la bd no existe
            elif resultado == f"'{bd}' no existe.":
                self.contador.configure(text=f"La base de datos {bd} no existe")
            #Si no existen resultados
            elif not resultado:
                self.contador.configure(text="0 coincidencias")
            #Si se encontraron coincidencias
            else:
                for r in resultado:
                    self.texto.insert("end",r)
                    self.texto.insert("end","\n")
                    self.contador.configure(text=f"Coincidencias {len(resultado)}")
        #Método que se usará para eliminar contenido de widgets
        def borrar():
            self.texto.delete("1.0","end")
            self.contador.configure(text="Ingrese su consulta SQL")
            self.entry_query.delete(0,ctk.END)
            self.entry_bd.delete(0,ctk.END)
        #Button enviar
        boton_enviar = ctk.CTkButton(frame, text="Enviar",command=registros,width=400)
        boton_enviar.grid(row=2,column=1,padx=10,pady=10)
        #Button eliminar
        boton_eliminar = ctk.CTkButton(frame, text="Borrar",command=borrar,width=400)
        boton_eliminar.grid(row=5,columnspan=3,padx=10,pady=10)
        #TextBox
        self.texto = ctk.CTkTextbox(frame, width=720, height=300)
        self.texto.grid(row=3, columnspan=3, padx=10, pady=10)
        #Contador
        self.contador = ctk.CTkLabel(frame,text="Ingrese su consulta SQL", width=720)
        self.contador.grid(row=4, columnspan=3, padx=10, pady=10)
            
    def mostrar_bases_de_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Bases de datos existentes")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (600,450)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=10, pady=10)
        #Label informativo
        ctk.CTkLabel(frame,text="Listado de las bases de datos existentes en el servidor: ",font=font_family).grid(row=0,column=0,columnspan=2,padx=10,pady=10)
        #Caja de texto
        self.texto = ctk.CTkTextbox(frame,font=font_family,width=500,height=250)
        self.texto.grid(row=1,column=0,columnspan=2,padx=10,pady=10)
        #Etiqueta contador
        self.contador = ctk.CTkLabel(frame,text="")
        self.contador.grid(row=2,column=0,columnspan=2,pady=10)
        #Función interna para ejecutar la busqueda de bases de datos
        def buscar():
            resultado = base_datos.mostrar_bd()
            cantidad_resultados = len(resultado)
            if cantidad_resultados == 1:
                self.contador.configure(text=f"Se encontró {cantidad_resultados} resultado.")
            else:
                self.contador.configure(text=f"Se encontraron {cantidad_resultados} resultados.")
            self.texto.delete("1.0","end")
            if not resultado:
                self.texto.insert("No se encontró ninguna base de datos.")
            else:
                for i in resultado:
                    self.texto.insert("end",f"-{i[0]}.")
                    self.texto.insert("end","\n")
        #Metodo interno borrar datos
        def borrar():
            self.texto.delete("1.0","end")
            self.contador.configure(text="Click en el botón 'Buscar'.")
        #Boton Buscar
        boton_busqueda = ctk.CTkButton(frame,text="Buscar",command=buscar)
        boton_busqueda.grid(row=3,column=0,pady=10)
        #Boton Eliminar
        boton_eliminar = ctk.CTkButton(frame,text="Borrar",command=borrar)
        boton_eliminar.grid(row=3,column=1)

    def crear_bases_de_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Crear base de datos")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (450,200)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=10,pady=10)
        #Label fija
        label = ctk.CTkLabel(frame,text="Ingrese nombre:", font=font_family,width=400)
        label.grid(column=0,row=0,padx=10,pady=10)
        #Entry nombre
        entry_nombre = ctk.CTkEntry(frame)
        entry_nombre.grid(column=0,row=1,padx=10,pady=10)
        #Metodo interno crear bd
        def crear():
            nombre_bd = entry_nombre.get()
            resultado = base_datos.crear_bd(nombre_bd)
            label_resultado.configure(text=resultado)
        #Boton crear
        boton = ctk.CTkButton(frame,text="Crear",command=crear)
        boton.grid(column=0,row=2,padx=10,pady=10)
        #Label resultado
        label_resultado = ctk.CTkLabel(frame,text="")
        label_resultado.grid(column=0,row=3,padx=10,pady=10)
    
    def eliminar_base_de_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Eliminar base de datos")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (450,200)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=10,padx=10)
        #Label input
        label_input = ctk.CTkLabel(frame,text="Ingrese nombre:", font=font_family,width=400)
        label_input.grid(row=0,padx=10,pady=10)
        #Entry
        entry = ctk.CTkEntry(frame)
        entry.grid(row=1,padx=10,pady=10)
        #Función interna
        def eliminar():
            input = entry.get()
            resultado = base_datos.eliminar_bd(input)
            label_resultado.configure(text=f"{resultado}")
        #Botón
        boton = ctk.CTkButton(frame,text="Eliminar",command=eliminar)
        boton.grid(row=2,padx=10,pady=10)
        #Label resultado
        label_resultado = ctk.CTkLabel(frame,text="")
        label_resultado.grid(row=3,padx=10,pady=10)
    
    def copia_seguridad(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Crear copia de seguridad")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion =(600,210)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=10,pady=10)
        #Label
        label = ctk.CTkLabel(frame,text="Ingrese el nombre de la base de datos que desea hacer un backup",font=font_family,padx=10,pady=10)
        label.grid(row=0,padx=10,pady=10)
        #Entry 
        entry = ctk.CTkEntry(frame,width=500)
        entry.grid(row=1,padx=10,pady=10)
        #Función interna
        def copia_seguridad():
            input = entry.get().lower()
            if not input:
                label_resultado.configure(text="Ingrese el nombre de la base de datos.")
            elif input:
                resultado = base_datos.backup(input)
                label_resultado.configure(text=resultado)
        #Boton
        boton = ctk.CTkButton(frame,text="Backup",command=copia_seguridad)
        boton.grid(row=2,padx=10,pady=10)
        #Label resultado
        label_resultado = ctk.CTkLabel(frame,text="")
        label_resultado.grid(row=3,padx=10,pady=10)
    
    def crear_tabla(self):
        global entry_bd,entry_nombre_tabla,entry_nombre_columna,entry_tipo,entry_longitud,entry_autoincrement,entry_primary_key,entry_nulos
        #Función interna al agregar columna
        #Datos almacenables
        datos_columnas = list()
        def agregar_columna():
            # Obtiene los valores de cada campo
            nombre_columna = entry_nombre_columna.get()
            tipo_dato = entry_tipo.get()
            longitud = entry_longitud.get()
            autoincrement = entry_autoincrement.get().lower()
            primary_key = entry_primary_key.get().lower()
            acepta_nulos = entry_nulos.get().lower()
            # Agrega los datos de la columna a la lista de datos_columnas
            datos_columnas.append({
                "nombre": nombre_columna,
                "tipo_dato": tipo_dato,
                "longitud": longitud,
                "auto_increment": autoincrement,
                "primary_key": primary_key,
                "acepta_nulos": acepta_nulos
            })
            # Borra los campos de entrada después de agregar una columna
            entry_nombre_columna.delete(0, ctk.END)
            entry_tipo.delete(0, ctk.END)
            entry_longitud.delete(0, ctk.END)
            entry_autoincrement.delete(0, ctk.END)
            entry_primary_key.delete(0, ctk.END)
            entry_nulos.delete(0, ctk.END)
            label_resultado.configure(text="")
        
        #Funcion interna prepara el query y ejecuta la función de la clase bd
        def ejecucion():
            #Crea el query para crear la tabla
            base_de_datos_a_usar = entry_bd.get()
            nombre_tabla = entry_nombre_tabla.get()
            query = str(f"CREATE TABLE {nombre_tabla} (")
            for columna in datos_columnas:
                query += f"{columna['nombre']} {columna['tipo_dato']}({columna['longitud']})"
                if columna['auto_increment'] == "si":
                    query += " AUTO_INCREMENT"
                if columna['primary_key'] == "si":
                    query += " PRIMARY KEY"
                if columna['acepta_nulos'] == "no":
                    query += " NOT NULL"
                query += ","
            query = query[:-1]
            query += ");"
            #Elimina el contenido de los entry
            entry_bd.delete(0, ctk.END)
            entry_nombre_tabla.delete(0, ctk.END)
            entry_nombre_columna.delete(0, ctk.END)
            entry_tipo.delete(0, ctk.END)
            entry_longitud.delete(0, ctk.END)
            entry_autoincrement.delete(0, ctk.END)
            entry_primary_key.delete(0, ctk.END)
            entry_nulos.delete(0, ctk.END)
            #Emerge una etiqueta con el resultado
            resultado = base_datos.crear_tabla(base_de_datos_a_usar,nombre_tabla,query)
            label_resultado.configure(text=resultado)
        
        #Ventana 
        ventana = ctk.CTkToplevel()
        ventana.title("Crear Tabla")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (650,800)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=10,pady=10)
        #Label gral
        label_gral = ctk.CTkLabel(frame,text="CREAR TABLA",font=font_family)
        label_gral.grid(row=0,columnspan=2,padx=10,pady=25)
        #Label bd
        label_bd = ctk.CTkLabel(frame,text="Ingrese la base de datos que va a utilizar: ",font=font_family)
        label_bd.grid(row=1,column=0,padx=10,pady=10,sticky='e')
        #Entry bd
        entry_bd = ctk.CTkEntry(frame)
        entry_bd.grid(row=1,column=1,padx=10,pady=5)
        #Label nombre tabla
        label_nombre_tabla = ctk.CTkLabel(frame,text="Ingrese el nombre que desea para la tabla: ",font = font_family)
        label_nombre_tabla.grid(row=2,column=0,padx=10,pady=10,sticky='e')
        #Entry nombre tabla
        entry_nombre_tabla = ctk.CTkEntry(frame)
        entry_nombre_tabla.grid(row=2,column=1,padx=10,pady=5)
        #Label nombre columna
        label_nombre_columna = ctk.CTkLabel(frame,text="Ingrese el nombre de la columna:",font=font_family)
        label_nombre_columna.grid(row=3,column=0,padx=10,pady=10,sticky='e')
        #Entry nombre columna
        entry_nombre_columna = ctk.CTkEntry(frame)
        entry_nombre_columna.grid(row=3,column=1,padx=10,pady=5)
        #Label tipo de dato
        label_tipo = ctk.CTkLabel(frame,text="Tipo de dato de la columna:",font=font_family)
        label_tipo.grid(row=4,column=0,padx=10,pady=10,sticky='e')
        #Entry tipo de dato
        entry_tipo = ctk.CTkEntry(frame)
        entry_tipo.grid(row=4,column=1,padx=10,pady=5)
        #Label longitud
        label_longitud = ctk.CTkLabel(frame,text="Ingrese la longitud de los datos:",font=font_family)
        label_longitud.grid(row=5,column=0,padx=10,pady=10,sticky='e')
        #Entry longitud
        entry_longitud = ctk.CTkEntry(frame)
        entry_longitud.grid(row=5,column=1,padx=10,pady=5)
        #Label general si o no
        label_gral_2 = ctk.CTkLabel(frame,text="Ingrese respuestas únicas de SI o NO",font=font_family)
        label_gral_2.grid(row=6,columnspan=2,pady=25,padx=10)
        #Autoincrement
        label_autoincrement = ctk.CTkLabel(frame,text="Columna auto-incrementable? ",font=font_family)
        label_autoincrement.grid(row=7,column=0,padx=10,pady=10)
        #Entry autoincrement
        entry_autoincrement = ctk.CTkEntry(frame)
        entry_autoincrement.grid(row=7,column=1,padx=10,pady=5)
        #Label primarykey
        label_primary_key = ctk.CTkLabel(frame,text="Columna primary key? ",font=font_family)
        label_primary_key.grid(row=8,column=0,padx=10,pady=10)
        #Entry primary key
        entry_primary_key = ctk.CTkEntry(frame)
        entry_primary_key.grid(row=8,column=1,padx=10,pady=5)
        #Label nulos
        label_nulls = ctk.CTkLabel(frame,text="Acepta valores nulos? ",font=font_family)
        label_nulls.grid(row=9,column=0,padx=10,pady=10)
        #Entry nulos
        entry_nulos = ctk.CTkEntry(frame)
        entry_nulos.grid(row=9,column=1,padx=10,pady=5)
        #Botones
        #Boton agregar columna
        boton_agregar = ctk.CTkButton(frame,text="Agregar columna",command=agregar_columna)
        boton_agregar.grid(row=10,columnspan=2,padx=10,pady=20)
        #Label final
        label_final = ctk.CTkLabel(frame,text="Si ya terminó de agregar las columnas ",font=font_family)
        label_final.grid(row=11,columnspan=2,pady=10)
        #Boton crear columna
        boton_crear = ctk.CTkButton(frame,text="Crear Tabla",command=ejecucion)
        boton_crear.grid(row=12,columnspan=2,padx=10,pady=10)
        #Label resultado
        label_resultado = ctk.CTkLabel(frame,text="")
        label_resultado.grid(row=13,columnspan=2,pady=10,padx=10)
        
    def eliminar_tabla(self):
        #funcion interna eliminar
        def eliminar():
            nombre_bd = entry_bd.get()
            nombre_tabla = entry_tabla.get()
            entry_tabla.delete(0,ctk.END)
            entry_bd.delete(0,ctk.END)
            resultado = base_datos.eliminar_tabla(nombre_bd,nombre_tabla)
            label_resultado.configure(text=resultado)
        #Ventana
        ventana = ctk.CTkToplevel()
        ventana.title("Eliminar tabla")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (500,210)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=10,padx=10)
        #Label bd
        label_bd = ctk.CTkLabel(frame,text="Ingrese la base de datos a utilizar: ",font=font_family)
        label_bd.grid(column=0,row=0,padx=10,pady=10,sticky='e')
        #Entry bd
        entry_bd = ctk.CTkEntry(frame)
        entry_bd.grid(column=1,row=0,padx=10,pady=10)
        #Label tabla
        label_tabla = ctk.CTkLabel(frame,text="Tabla que desea eliminar: ", font=font_family)
        label_tabla.grid(column=0,row=1,padx=10,pady=10,sticky='e')
        #Entry tabla
        entry_tabla = ctk.CTkEntry(frame)
        entry_tabla.grid(column=1,row=1,padx=10,pady=10)
        #Boton 
        boton = ctk.CTkButton(frame,text="Eliminar",command=eliminar)
        boton.grid(columnspan=2,row=2,padx=10,pady=10)
        #Label resultado
        label_resultado = ctk.CTkLabel(frame,text="")
        label_resultado.grid(columnspan=2,row=3,padx=10,pady=15)
        
    def mostrar_tablas(self):
        #Funcion interna buscar
        def buscar():
            #Si hay resultados de una busqueda anterior los borra
            text_box.delete("1.0","end")
            #Obtiene el valor de la base de datos ingresada
            base_de_datos = entry_bd.get()
            #Almacena la lista de tuplas con los resultados
            resultado = base_datos.mostrar_tablas(base_de_datos)
            #Cuenta la cantidad de resultados
            cantidad_resultados = len(resultado)
            #Itera la lista de tablas y las va incorporando en el textbox
            for tabla in resultado:
                text_box.insert(index="end",text=tabla)
                text_box.insert(index="end", text="\n")
            #Si el entry esta vacío
            if base_de_datos == "":
                label_contador.configure(text="Ingrese el nombre de la base de datos.")
                text_box.delete("1.0","end")
            #Si la base de datos no existe
            elif resultado == f"'{base_de_datos}' no existe.":
                label_contador.configure(text=f"La base de datos '{base_de_datos}' no existe.")
                text_box.delete("1.0","end")
            #Si existe la bd pero no tiene tablas
            elif cantidad_resultados == 0:
                label_contador.configure(text="")
                text_box.insert(index="end",text="Se encontró la base de datos pero no posee ninguna tabla.")
            #Si solo hay un resultado
            elif cantidad_resultados == 1:
                label_contador.configure(text=f"{cantidad_resultados} coincidencia.")
            #Si hay +1 de un resultado
            else:
                label_contador.configure(text=f"{cantidad_resultados} coincidencias.")
        #Funcion interna borrar
        def borrar():
            #Si hay algún contenido borra todo
            entry_bd.delete("0","end")
            text_box.delete("1.0","end")
            label_contador.configure(text="")
        #Ventana
        ventana = ctk.CTkToplevel()
        ventana.title("Tablas existentes")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (410,450)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=5,pady=20)
        #Label 1
        label_1 = ctk.CTkLabel(frame,text="Ingrese base de datos: ", font=font_family)
        label_1.grid(column=0,row=0,padx=10,pady=10)
        #Entry bd
        entry_bd = ctk.CTkEntry(frame)
        entry_bd.grid(column=1,row=0,padx=10,pady=10)
        #Label 2
        label_2 = ctk.CTkLabel(frame,text="Resultados", font=font_family)
        label_2.grid(columnspan=2,row=1,padx=10,pady=10)
        #TextBox
        text_box = ctk.CTkTextbox(frame,width=380)
        text_box.grid(columnspan=2,row=2,padx=10,pady=10)
        #Label contador 
        label_contador = ctk.CTkLabel(frame,text="")
        label_contador.grid(columnspan=2,row=3,padx=10,pady=10)
        #Boton buscar
        boton_buscar = ctk.CTkButton(frame,text="Buscar",command=buscar)
        boton_buscar.grid(column=0,row=4,padx=10,pady=10)
        #Boton eliminar
        boton_eliminar = ctk.CTkButton(frame,text="Borrar",command=borrar)
        boton_eliminar.grid(column=1,row=4,padx=10,pady=10)
        
    def borrar_registro(self):
        #Funcion interna eliminar
        def eliminar():
            bd = entry_bd.get()
            tabla = entry_tabla.get()
            condicion = entry_condicion.get()
            resultado = base_datos.borrar_registro(bd,tabla,condicion)
            if condicion == "":
                label_resultado.configure(text="Ingrese la condición.")
            else:
                label_resultado.configure(text=resultado)
        #Funcion interta vaciar
        def vaciar():
            entry_bd.delete(0,ctk.END)
            entry_tabla.delete(0,ctk.END)
            entry_condicion.delete(0,ctk.END)
        #Ventana
        ventana = ctk.CTkToplevel()
        ventana.title("Borrar registro")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (575,250)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame
        frame = ctk.CTkFrame(ventana)
        frame.pack()
        #Label bd
        label_bd = ctk.CTkLabel(frame,text="Ingrese el nombre de la base de datos: ", font=font_family)
        label_bd.grid(column=0,row=0,padx=10,pady=10,sticky='w')
        #Label tabla
        label_tabla = ctk.CTkLabel(frame,text="Ingrese el nombre de la tabla: ", font=font_family)
        label_tabla.grid(column=0,row=1,padx=10,pady=10,sticky='w')
        #Label condicion
        label_condicion = ctk.CTkLabel(frame,text="Ingrese la condición para eliminar registros: ", font=font_family)
        label_condicion.grid(column=0,row=2,padx=10,pady=10,sticky='w')
        #Entry bd
        entry_bd = ctk.CTkEntry(frame)
        entry_bd.grid(column=1,row=0,padx=10,pady=10)
        #Entry tabla
        entry_tabla = ctk.CTkEntry(frame)
        entry_tabla.grid(column=1,row=1,padx=10,pady=10)
        #Entry condicion
        entry_condicion = ctk.CTkEntry(frame)
        entry_condicion.grid(column=1,row=2,padx=10,pady=10)
        #Boton eliminar
        boton_eliminar = ctk.CTkButton(frame,text="Eliminar registros",command=eliminar)
        boton_eliminar.grid(column=1,row=3,padx=10,pady=10)
        #Boton vaciar
        boton_vaciar = ctk.CTkButton(frame,text="Vaciar inputs", command=vaciar)
        boton_vaciar.grid(column=0,row=3,padx=10,pady=10)
        #Label resultado
        label_resultado = ctk.CTkLabel(frame,text="")
        label_resultado.grid(columnspan=2,row=4,padx=10,pady=10)
    
    def borrar_todos_los_registros(self):
        #Funcion interna vaciar inputs
        def borrar():
            entry_tabla.delete(0, ctk.END)
            entry_bd.delete(0, ctk.END)
        #Funcion interna eliminar todos los registros
        def eliminar_registros():
            bd = entry_bd.get()
            tabla = entry_tabla.get()
            resultado = base_datos.borrar_todos_los_registros(bd,tabla)
            if bd == "":
                label_resultado.configure(text="Ingrese la base de datos.")
            elif tabla == "":
                label_resultado.configure(text="Ingrese la tabla.")
            else: 
                label_resultado.configure(text=resultado)
        #Ventana
        ventana = ctk.CTkToplevel()
        ventana.title("Vaciar tabla")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (500,250)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame 
        frame = ctk.CTkFrame(ventana,width=480)
        frame.pack(padx=10,pady=10)
        #Label general
        label_gral = ctk.CTkLabel(frame, text="ELIMINAR TODOS LOS REGISTROS", font=font_family)
        label_gral.grid(columnspan=2,row=0,padx=10,pady=10)
        #Label bd
        label_bd = ctk.CTkLabel(frame,text="Ingrese base de datos: ", font=font_family)
        label_bd.grid(column=0,row=1,padx=10,pady=10,sticky='w')
        #Entry bd
        entry_bd = ctk.CTkEntry(frame)
        entry_bd.grid(column=1,row=1,padx=10,pady=10)
        #Label tabla
        label_tabla = ctk.CTkLabel(frame,text="Ingrese la tabla: ", font=font_family)
        label_tabla.grid(column=0,row=2,padx=10,pady=10,sticky='w')
        #Entry tabla
        entry_tabla = ctk.CTkEntry(frame)
        entry_tabla.grid(column=1,row=2,padx=10,pady=10)
        #Boton borrar 
        boton_borrar = ctk.CTkButton(frame,text="Borrar inputs", command=borrar)
        boton_borrar.grid(column=0,row=3,padx=10,pady=10)
        #Boton eliminar
        boton_eliminar = ctk.CTkButton(frame,text="Borrar registros", command=eliminar_registros)
        boton_eliminar.grid(column=1,row=3,padx=10,pady=10)
        #Label final
        label_resultado = ctk.CTkLabel(frame,text="")
        label_resultado.grid(columnspan=2,row=4,padx=10,pady=10)
    
    def actualizar_registro(self):
        #Funcion interna vaciar inputs
        def vaciar():
            entry_bd.delete(0, ctk.END)
            entry_tabla.delete(0, ctk.END)
            entry_columna.delete(0, ctk.END)
            entry_condicion.delete(0, ctk.END)
            label_resultado.configure(text="")
        #Funcion interna actualizar registros
        def actualizar():
            bd = entry_bd.get()
            tabla = entry_tabla.get()
            columna = entry_columna.get()
            condicion = entry_condicion.get()
            resultado = base_datos.actualizar_registro(bd,tabla,columna,condicion)
            if bd == "":
                label_resultado.configure(text="Ingrese la base de datos.")
            elif tabla == "":
                label_resultado.configure(text="Ingrese la tabla.")
            elif columna == "":
                label_resultado.configure(text="Ingrese la columna/s a actualizar.")
            elif condicion == "":
                label_resultado.configure(text="Ingrese la condición.")
            else:
                label_resultado.configure(text=resultado)
        #Ventana
        ventana = ctk.CTkToplevel()
        ventana.title("Actualizar registro")
        #Pone la ventana emergente por encima
        ventana.grab_set()
        #Dimensiones (centrado automatico)
        dimesion = (600,300)
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        ventana.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        ventana.resizable(False,False)
        #Frame 
        frame = ctk.CTkFrame(ventana,width=480)
        frame.pack(padx=10,pady=10)
        #Label bd
        label_bd = ctk.CTkLabel(frame,text="Nombre base de datos: ", font=font_family)
        label_bd.grid(column=0,row=0,sticky='w',padx=10,pady=10)
        #Entry bd
        entry_bd = ctk.CTkEntry(frame)
        entry_bd.grid(column=1,row=0,padx=10,pady=10)
        #Label tabla
        label_tabla = ctk.CTkLabel(frame,text="Nombre tabla: ", font=font_family)
        label_tabla.grid(column=0,row=1,padx=10,pady=10,sticky='w')
        #Entry tabla 
        entry_tabla = ctk.CTkEntry(frame)
        entry_tabla.grid(column=1,row=1,padx=10,pady=10)
        #Label columna
        label_columna = ctk.CTkLabel(frame,text="Columnas a modificar (separadas por ' , '): ",font=font_family)
        label_columna.grid(column=0,row=2,sticky='w',padx=10,pady=10)
        #Entry columna
        entry_columna = ctk.CTkEntry(frame)
        entry_columna.grid(column=1,row=2,padx=10,pady=10)
        #Label condicion
        label_condicion = ctk.CTkLabel(frame,text="Condición: ", font=font_family)
        label_condicion.grid(column=0,row=3,padx=10,pady=10,sticky='w')
        #Entry condicion
        entry_condicion = ctk.CTkEntry(frame)
        entry_condicion.grid(column=1,row=3,padx=10,pady=10)
        #Boton vaciar
        boton_vaciar = ctk.CTkButton(frame,text="Vaciar inputs",command=vaciar)
        boton_vaciar.grid(column=0,row=4,sticky='w',padx=10,pady=10)
        #Boton actualizar
        boton_actualizar = ctk.CTkButton(frame,text="Actualizar",command=actualizar)
        boton_actualizar.grid(column=1,row=4,padx=10,pady=10)
        #Label resultado
        label_resultado = ctk.CTkLabel(frame,text="")
        label_resultado.grid(columnspan=2,row=5,padx=10,pady=10)

funciones = Funciones()

#Ventana opciones
class Opciones:
    #Datos de los botones
    botones = {
        "Consulta SQL" : funciones.consulta_sql,
        "Mostrar base de datos" : funciones.mostrar_bases_de_datos,
        "Crear base de datos" : funciones.crear_bases_de_datos,
        "Eliminar base de datos" : funciones.eliminar_base_de_datos,
        "Copia de seguridad" : funciones.copia_seguridad,
        "Crear tabla" : funciones.crear_tabla,
        "Eliminar tabla" : funciones.eliminar_tabla,
        "Mostrar tablas" : funciones.mostrar_tablas,
        "Borrar registro" : funciones.borrar_registro,
        "Actualizar registro" : funciones.actualizar_registro,
        "Borrar todos los registros" : funciones.borrar_todos_los_registros
    }
    
    def __init__(self):
        #Instanciación de la ventana
        self.root = ctk.CTk()
        self.root.title("Opciones de navegación")
        self.root.iconbitmap(icono)
        #Dimensión ventana (centrado automatico)
        dimesion = (600,550)
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        eje_x = (ancho_pantalla - dimesion[0]) // 2
        eje_y = (alto_pantalla - dimesion[1]) // 2
        self.root.geometry(f"{dimesion[0]}x{dimesion[1]}+{eje_x}+{eje_y}")
        #Bloqueo Pantalla
        self.root.resizable(False,False)
        #Actualiza la fila del botón
        contador_posicion = 0
        #Genera botones
        for text_boton in self.botones:
            boton = ctk.CTkButton(master=self.root, text=text_boton, height=30, width=580, command=self.botones[text_boton])
            boton.grid(row=contador_posicion, padx= 10, pady= 10)
            contador_posicion += 1
        #Mantiene la ventana abierta
        self.root.mainloop()