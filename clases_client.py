# programa client_GO
import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, ttk, simpledialog
import sqlite3
import hashlib
from datetime import datetime
import pytz
import os
import sys

""""
Lo que vamos a crear el un programa que nos permita agregar productoa una base de datos
para llevar el control de stock de un negocio.

crear la clase para el usuario.
crear la clase para la interfaz.
crear la clase para la interfaz de el login.
registrar el usuario.
hacer el login
"""
conexion = sqlite3.connect("client_GO.db")
cursor = conexion.cursor()


class Iniciosesion:

    def __init__(self):

        self.root_sesion = None
        self.frame_inicio = None
        self.frame_registro = None
        self.entrada_nombre = None
        self.entrada_apellidos = None
        self.entrada_email = None
        self.entrada_contraseña = None
        self.entrada_email_inicio = None
        self.entrada_contraseña_inicio = None
        self.root_codigo = None
        self.boton_cancelar = None

    @staticmethod
    def resolver_ruta(ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

    # se esconde ell framee de registro y se muestra el de inicio de sesion
    def mostrar_inicio_sesion(self):

        self.frame_registro.place_forget()
        self.frame_inicio.place(x=0, y=0, width=350, height=400)
        self.root_sesion.title('Iniciar sesion')

    # este es el inicio de sesion
    def inicio(self):

        self.root_sesion = Tk()
        self.root_sesion.geometry("350x400+620+200")
        self.root_sesion.maxsize(350, 400)
        self.root_sesion.minsize(350, 400)
        self.root_sesion.title('Iniciar sesion')

        icono = self.resolver_ruta('assets/logotipo.ico')

        self.root_sesion.iconbitmap(icono)

        # frame para principal
        self.frame_inicio = Frame(self.root_sesion, bg='')
        self.frame_inicio.place(x=0, y=0, width=350, height=400, )

        # imagen para el fondo
        inicio_ruta = self.resolver_ruta('assets/inicio_sesion1.png')
        imagen = Image.open(inicio_ruta)
        imagen2 = imagen.resize((400, 400), Image.LANCZOS)
        img_final = ImageTk.PhotoImage(imagen2)

        # label para poner la imagen
        label_image = Label(self.frame_inicio, image=img_final)
        label_image.place(x=0, y=0, width=350, height=400)
        label_image.image = img_final

        # entrada email
        self.entrada_email_inicio = Entry(label_image, font="'console', 12", bd=6.2, relief=GROOVE, bg="white",
                                          fg='#575757')
        self.entrada_email_inicio.insert(0, 'Usuario')
        self.entrada_email_inicio.place(x=60, y=180, width=230, height=35)
        self.entrada_email_inicio.bind("<FocusIn>", lambda event: self.eliminar_texto(event, self.entrada_email_inicio,
                                                                                      'Usuario'))
        self.entrada_email_inicio.bind("<FocusOut>", lambda event: self.mostrar_texto(event, self.entrada_email_inicio,
                                                                                      'Usuario'))

        # entrada contraseña
        self.entrada_contraseña_inicio = Entry(label_image, font="'console', 12", bd=6.2, relief=GROOVE, bg="white",
                                               fg='#575757')
        self.entrada_contraseña_inicio.insert(0, 'Contraseña')
        self.entrada_contraseña_inicio.place(x=60, y=230, width=230, height=35)
        self.entrada_contraseña_inicio.bind("<FocusIn>",
                                            lambda event: self.eliminar_texto(event, self.entrada_contraseña_inicio))
        self.entrada_contraseña_inicio.bind("<FocusOut>",
                                            lambda event: self.mostrar_texto(event, self.entrada_contraseña_inicio,
                                                                             'Contraseña'))

        # imagen para el boton iniciar
        iniciar_ruta = self.resolver_ruta('assets/iniciar.png')
        imagen_boton = Image.open(iniciar_ruta)
        imagen_b = imagen_boton.resize((107, 32), Image.LANCZOS)
        img_final_boton = ImageTk.PhotoImage(imagen_b)

        # boton para iniciar sesion
        boton_iniciar = Button(label_image, image=img_final_boton, bg='#00BFFF', command=self.iniciar)
        boton_iniciar.place(x=125, y=285, width=100, height=35)

        # imagen para el boton registrar
        registrar_ruta = self.resolver_ruta('assets/registrarme.png')
        imagen_boton_reg = Image.open(registrar_ruta)
        imagen_r = imagen_boton_reg.resize((128, 32), Image.LANCZOS)
        img_final_boton_r = ImageTk.PhotoImage(imagen_r)

        # boton para ir a registro
        boton_registrar = Button(label_image, image=img_final_boton_r, bg='#00BFFF', command=self.registro)
        boton_registrar.place(x=109, y=330, width=130, height=35)

        # imagen ojo cerrado
        ojocerrado_ruta = self.resolver_ruta('assets/ojo_cerrado.png')
        imagen_ojo_cerrado = Image.open(ojocerrado_ruta)
        imagen_ojo_cerrado2 = imagen_ojo_cerrado.resize((30, 20), Image.LANCZOS)
        img_final_ojo_cerrado = ImageTk.PhotoImage(imagen_ojo_cerrado2)

        # boton ver y ocultar contraseña
        boton_ver_contr = Button(label_image, text='ocultar',
                                 command=lambda: self.ver_contraseña(self.entrada_contraseña_inicio,
                                                                     boton_ver_contr),
                                 image=img_final_ojo_cerrado)
        boton_ver_contr.place(x=248.5, y=235, width=35, height=22.5)
        boton_ver_contr.image = img_final_ojo_cerrado

        self.root_sesion.mainloop()

    @staticmethod
    def eliminar_texto(event, entrada, texto1=None):

        if entrada.get() == texto1:
            entrada.delete(0, tkinter.END)
            entrada.config(fg='black')
        if entrada.get() == 'Contraseña':
            entrada.delete(0, tkinter.END)
            entrada.config(fg='black', show='*')

    @staticmethod
    def mostrar_texto(event, entrada, texto):

        if not entrada.get():
            entrada.insert(0, texto)
            entrada.config(fg='#575757', show='')

    @staticmethod
    def ver_contraseña(entrada, boton):

        palabra = entrada.get()
        texto_boton = boton.cget('text')

        if palabra == 'Contraseña':
            entrada.delete(0, END)
            entrada.config(fg='#575757')
            entrada.insert(0, 'Contraseña')
        elif texto_boton == 'ocultar':

            # imagen ojo abierto
            ojoabierto_ruta = Iniciosesion.resolver_ruta('assets/ojo_abierto.png')
            imagen_ojo_abierto = Image.open(ojoabierto_ruta)
            imagen_ojo_abierto2 = imagen_ojo_abierto.resize((27, 17), Image.LANCZOS)
            img_final_ojo_abierto = ImageTk.PhotoImage(imagen_ojo_abierto2)

            entrada.delete(0, END)
            entrada.config(fg='black', show='')
            entrada.insert(0, palabra)
            boton.config(text='ver', image=img_final_ojo_abierto)
            boton.image = img_final_ojo_abierto
        elif texto_boton == 'ver':

            # imagen ojo cerrado
            ojocerrado_ruta = Iniciosesion.resolver_ruta('assets/ojo_cerrado.png')
            imagen_ojo_cerrado = Image.open(ojocerrado_ruta)
            imagen_ojo_cerrado2 = imagen_ojo_cerrado.resize((30, 20), Image.LANCZOS)
            img_final_ojo_cerrado = ImageTk.PhotoImage(imagen_ojo_cerrado2)

            entrada.delete(0, END)
            entrada.config(fg='black', show='*')
            entrada.insert(0, palabra)
            boton.config(text='ocultar', image=img_final_ojo_cerrado)
            boton.image = img_final_ojo_cerrado

    def registro(self):

        # renombremos el título de la ventana
        self.root_sesion.title('Registro')

        # frame principal en registro
        self.frame_registro = Frame(self.root_sesion, bg='green2')
        self.frame_registro.place(x=0, y=0, width=350, height=400)

        # imagen para el fondo del registro
        registro_ruta = Iniciosesion.resolver_ruta('assets/img_registro.png')
        imagen_reg = Image.open(registro_ruta)
        imagen_reg2 = imagen_reg.resize((400, 400), Image.LANCZOS)
        img_final_reg = ImageTk.PhotoImage(imagen_reg2)

        # label para poner la imagen registro
        label_registo = Label(self.frame_registro, image=img_final_reg, bg='red')
        label_registo.place(x=0, y=0, width=350, height=400)
        label_registo.image = img_final_reg

        # entrada nombre registro
        self.entrada_nombre = Entry(label_registo, font="'console', 12", bd=6.2, relief=GROOVE, bg="white",
                                    fg='#575757')
        self.entrada_nombre.insert(0, 'Nombres')
        self.entrada_nombre.place(x=60, y=170, width=230, height=35)
        self.entrada_nombre.bind("<FocusIn>", lambda event: self.eliminar_texto(event, self.entrada_nombre, 'Nombres'))
        self.entrada_nombre.bind("<FocusOut>", lambda event: self.mostrar_texto(event, self.entrada_nombre, 'Nombres'))

        # entrada apellidos registro
        self.entrada_apellidos = Entry(label_registo, font="'console', 12", bd=6.2, relief=GROOVE, bg="white",
                                       fg='#575757')
        self.entrada_apellidos.insert(0, 'Apellidos')
        self.entrada_apellidos.place(x=60, y=215, width=230, height=35)
        self.entrada_apellidos.bind("<FocusIn>", lambda event: self.eliminar_texto(event, self.entrada_apellidos,
                                                                                   'Apellidos'))
        self.entrada_apellidos.bind("<FocusOut>", lambda event: self.mostrar_texto(event, self.entrada_apellidos,
                                                                                   'Apellidos'))

        # entrada email registro
        self.entrada_email = Entry(label_registo, font="'console', 12", bd=6.2, relief=GROOVE, bg="white", fg='#575757')
        self.entrada_email.insert(0, 'Usuario')
        self.entrada_email.place(x=60, y=260, width=230, height=35)
        self.entrada_email.bind("<FocusIn>", lambda event: self.eliminar_texto(event, self.entrada_email, 'Usuario'))
        self.entrada_email.bind("<FocusOut>", lambda event: self.mostrar_texto(event, self.entrada_email, 'Usuario'))

        # entrada contraseña  registro
        self.entrada_contraseña = Entry(label_registo, font="'console', 12", bd=6.2, relief=GROOVE, bg="white",
                                        fg='#575757')
        self.entrada_contraseña.insert(0, 'Contraseña')
        self.entrada_contraseña.place(x=60, y=310, width=230, height=35)
        self.entrada_contraseña.bind("<FocusIn>", lambda event: self.eliminar_texto(event, self.entrada_contraseña))
        self.entrada_contraseña.bind("<FocusOut>", lambda event: self.mostrar_texto(event, self.entrada_contraseña,
                                                                                    'Contraseña'))

        # imagen boton  cancelar
        cancelar_ruta = Iniciosesion.resolver_ruta('assets/img_cancelar.png')
        imagen_cancelar = Image.open(cancelar_ruta)
        imagen_canc_2 = imagen_cancelar.resize((90, 25), Image.LANCZOS)
        img_final_cancelar = ImageTk.PhotoImage(imagen_canc_2)

        # imagen para boton registrar
        botonregistrar_ruta = Iniciosesion.resolver_ruta('assets/boton_resistro.png')
        imagen_registrarme = Image.open(botonregistrar_ruta)
        imagen_registrarme_2 = imagen_registrarme.resize((110, 27), Image.LANCZOS)
        img_final_registrarme = ImageTk.PhotoImage(imagen_registrarme_2)

        # boton cancelar
        self.boton_cancelar = Button(self.frame_registro, image=img_final_cancelar, bg='#1C1C1C',
                                     command=self.mostrar_inicio_sesion)
        self.boton_cancelar.place(x=63, y=357, width=90, height=25)
        self.boton_cancelar.image = img_final_cancelar

        # boton registrarme
        boton_registrarme = Button(self.frame_registro, image=img_final_registrarme, bg='green',
                                   command=self.guardar_registro)
        boton_registrarme.place(x=188, y=355, width=105, height=27)
        boton_registrarme.image = img_final_registrarme

        # imagen ojo cerrado
        ojocerado_ruta = Iniciosesion.resolver_ruta('assets/ojo_cerrado.png')
        imagen_ojo_cerrado = Image.open(ojocerado_ruta)
        imagen_ojo_cerrado2 = imagen_ojo_cerrado.resize((30, 19), Image.LANCZOS)
        img_final_ojo_cerrado = ImageTk.PhotoImage(imagen_ojo_cerrado2)

        # imagen volver de registro
        imgvolver_ruta = Iniciosesion.resolver_ruta('assets/img_volver.png')
        imagen_volver_reg = Image.open(imgvolver_ruta)
        imagen_volver_reg2 = imagen_volver_reg.resize((40, 23), Image.LANCZOS)
        img_final_volver_registro = ImageTk.PhotoImage(imagen_volver_reg2)

        # boton ver contraseña
        boton_ver_contr = Button(label_registo, text='ocultar',
                                 command=lambda: self.ver_contraseña(self.entrada_contraseña, boton_ver_contr),
                                 image=img_final_ojo_cerrado)
        boton_ver_contr.place(x=249, y=315, width=35, height=22.5)
        boton_ver_contr.image = img_final_ojo_cerrado

    # esta funccion cambia la imagen cuando nos registramos para que no diga
    # cancelar sino vovlver.
    def cambiar_img_volver(self):

        # cargamos la imagen de el boton
        imgvolver_ruta = Iniciosesion.resolver_ruta('assets/img_volver.png')
        imagen_volver = Image.open(imgvolver_ruta)
        imagen_volver2 = imagen_volver.resize((90, 25), Image.LANCZOS)
        imagen_volver_final = ImageTk.PhotoImage(imagen_volver2)

        # actualizamos la imagen de el boton para regresar
        self.boton_cancelar.configure(image=imagen_volver_final)
        self.boton_cancelar.image = imagen_volver_final

    # guardamos el registro
    def guardar_registro(self):

        try:
            # obtenemos las entradas
            nombres = self.entrada_nombre.get()
            apellidos = self.entrada_apellidos.get()
            email = self.entrada_email.get()
            contraseña = self.entrada_contraseña.get()
            contraseña_hash = hashlib.sha256(contraseña.encode()).hexdigest()
            lista = ['contraseña', '12345678', '123456789', '012345678', '0123456789']

            # condicional para si no se ingresa nada en los campos
            if nombres == 'Nombres' or apellidos == 'Apellidos' or email == 'Email' or contraseña == 'Contraseña' or \
                    len(nombres) <= 0 or len(apellidos) <= 0 or len(email) <= 0 or len(contraseña) <= 0:
                messagebox.showinfo("ALERTA", "ESPACIOS VACIOS")

            elif contraseña.lower() == 'contraseña':
                messagebox.showinfo("ALERTA", "CONTRASEÑA INUSUAL E INSEGURA")

            elif len(contraseña) < 8:
                messagebox.showinfo("ALERTA", "LA CONTRASEÑA DEBE TENER 8 O MAS DIGITO")

            # condicional para guardar el registro
            elif nombres and apellidos and email and contraseña != 'contraseña':

                # este codigo es para que se pueda registrar
                codigo = str(346643)
                codigo_hash = hashlib.sha256(codigo.encode()).hexdigest()
                try:
                    codigo_seguridad = simpledialog.askstring(title='CODIGO DE SEGURIDAD',
                                                              prompt="""         INGRESE EL CODIGO DE SEGURIDAD 
            PARA REALIZAR EL REGISTRO""")
                    codigo_seguridad2 = hashlib.sha256(codigo_seguridad.encode()).hexdigest()

                    # si el codigo que se ingresa esta bien se hacce el registro
                    if codigo_seguridad2 == codigo_hash:

                        objeto = Interfaz()
                        cursor.execute("INSERt INTO usuarios(nombres, apellidos, email, password) VALUES(?, ?, ?, ?)",
                                       (nombres, apellidos, email, contraseña_hash))
                        id_reciente = cursor.lastrowid
                        if id_reciente:

                            # imagen confirmacion registro
                            confirmacion_ruta = Iniciosesion.resolver_ruta('assets/confirmacion_registro.png')
                            imagen_confirmacion = Image.open(confirmacion_ruta)
                            imagen_confirmacion_r2 = imagen_confirmacion.resize((115, 145), Image.LANCZOS)
                            img_final_confirmacionr = ImageTk.PhotoImage(imagen_confirmacion_r2)

                            texto = "Guardado corretamente"
                            objeto.mensaje_temporal(self.root_sesion, texto, 2200, img_final_confirmacionr,
                                                    137, 185, 115, 145)
                            conexion.commit()

                            # se cambia la imagen
                            self.cambiar_img_volver()

                        elif id_reciente is None:
                            messagebox.showinfo("ALERTA", "USUARIO NO AGREGADO, INTENTE NUEVAMENTE")
                    elif codigo_seguridad2 != codigo_hash:
                        messagebox.showinfo("ALERTA", """               CODIGO INCORRECTO
                     INTENTE DE NUEVO""")
                except AttributeError:
                    messagebox.showinfo("ALERTA", """               CODIGO INCORRECTO
                   INTENTE DE NUEVO""")
        except sqlite3.IntegrityError:
            messagebox.showinfo('ALERTA', 'ESTE USUARIO YA EXISTE')

    def iniciar(self):

        # instanciamos un objeto de la clase Interfaz
        # inicio = Interfaz()

        email_inicio = self.entrada_email_inicio.get()
        contraseña_inicio = self.entrada_contraseña_inicio.get()
        contraseña_hash = hashlib.sha256(contraseña_inicio.encode()).hexdigest()

        cursor.execute("SELECT * FROM usuarios WHERE email=? AND password=?",
                       (email_inicio, contraseña_hash))
        dato = cursor.fetchone()

        if dato:
            self.root_sesion.destroy()

            inicio = Interfaz()
            inicio.app()
        elif dato is None:
            messagebox.showinfo("ALERTA", "EL USUARIO O LA CONTRASEÑA SON INCORRECTAS")
        conexion.commit()


class Interfaz:

    def __init__(self):

        self.entrada_nombre = None
        self.entrada_talla = None
        self.entrada_precio_CL = None
        self.entrada_descripcion = None
        self.ruta_imagen = None
        self.entrada_id = None
        self.entrada_unidades = None
        self.label_imagen = None
        self.root = None
        self.frame_secundario = None
        self.busqueda_var = None
        self.treeview = None
        self.treeview_ventas = None
        self.filas = []
        self.filas_ventas = []
        self.frame_stock = None
        self.frame_tabla_datos = None
        self.entrada_preciof = None
        self.frame_ventas = None
        self.entrada_ganancia = None
        self.entrada_prventas = None
        self.entrada_idproventas = None
        self.entrada_cantidadvent = None
        self.entrada_totalventa = None
        self.entrada_gananciaventas = None
        self.entrada_precioprod = None
        self.string_var_operacion = None
        self.stringvar_ventas = None
        self.stringvar_cantidad = None
        self.busquedavar_ventas = None
        self.entrada_busqueda_ventas = None
        self.valor_gasto = None
        self.nombre_gasto = None
        self.frame_contabilidad = None
        self.treeview_gastos = None
        self.busquedavar_gastos = None
        self.entrada_busqueda_gastos = None
        self.filas_gastos = []
        self.treeview_reporte = None
        self.igual_fecha = None
        self.label_venta_dia = None
        self.label_gastos = None
        self.label_ganancia_dia = None
        self.label_ganancia_final = None

    def app(self):

        self.root = Tk()

        # titulo del programa
        self.root.title("Client GO")

        # icono de el programa
        ico_pr = Iniciosesion.resolver_ruta('assets/logotipo.ico')
        self.root.wm_iconbitmap(ico_pr)

        # tamaño principal de la ventana
        self.root.geometry("1000x500+250+150")
        self.root.maxsize(1000, 500)
        self.root.minsize(1000, 500)

        self.frame_stock = Frame(self.root)
        self.frame_stock.place(x=0, y=0, width=1000, height=500)

        # imagen dnombre del programa
        nombreprogr_ruta = Iniciosesion.resolver_ruta("assets/El-texto-del-párrafo.jpg")
        imagen = Image.open(nombreprogr_ruta)
        img = imagen.resize((1000, 100), Image.LANCZOS)
        imagen1 = ImageTk.PhotoImage(img)

        # imagen para el boton menu
        botonmenu_ruta = Iniciosesion.resolver_ruta("assets/boton_menu.png")
        im_menu = Image.open(botonmenu_ruta)
        img_menu2 = im_menu.resize((29, 35), Image.LANCZOS)
        imagen_final = ImageTk.PhotoImage(img_menu2)

        # label para imagen logo
        label = Label(self.frame_stock, image=imagen1)
        label.place(x=0, y=0)
        label.image = imagen1

        self.string_var_operacion = StringVar()
        self.string_var_operacion.trace('w', self.operacion_ganancia_prod)

        # frame principal para todos los witgets
        frame_principal = Frame(self.frame_stock, bg="#458B74", bd=2, relief=RAISED)  # 7FFFD4
        frame_principal.place(x=10, y=110, width=980, height=380)

        # frame secundario para las imagenes
        self.frame_secundario = Frame(frame_principal, bg="white", bd=10, relief=GROOVE)
        self.frame_secundario.place(x=500, y=97, width=440, height=260)

        # label nombre
        label_nombre = Label(frame_principal, text="Nombre", bg="#458B74", font="'Robot', 16")
        label_nombre.place(x=70, y=5)

        # label talla
        label_talla = Label(frame_principal, text="Talla", bg="#458B74", font="'Robot', 16")
        label_talla.place(x=235, y=5)

        # label unidades
        label_unidades = Label(frame_principal, text="Unidades", bg="#458B74", font="'Robot', 16")
        label_unidades.place(x=372, y=5)

        # label precio fabrica
        label_precio_fabrica = Label(frame_principal, text="Precio compra", bg="#458B74", font="'Robot', 16")  # 7FFFD4
        label_precio_fabrica.place(x=502, y=5)

        # label precio cliente
        label_precio = Label(frame_principal, text="Precio venta", bg="#458B74", font="'Robot', 16")  # 7FFFD4
        label_precio.place(x=665, y=5)

        # label gananicia
        label_ganancia = Label(frame_principal, text="Ganancia", bg="#458B74", font="'Robot', 16")  # 7FFFD4
        label_ganancia.place(x=827, y=5)

        # label descripcion
        label_descripcion = Label(frame_principal, text="Descripcion:", bg="#458B74", font="'Robot', 16")
        label_descripcion.place(x=35, y=100)

        # label imagen producto
        self.label_imagen = Label(self.frame_secundario, bg="white")
        self.label_imagen.place(x=0, y=0)

        # label id
        label_id = Label(frame_principal, text="ID:", bg="#458B74", font="'Robot', 16")
        label_id.place(x=330, y=340)

        # entrada nombre
        self.entrada_nombre = Entry(frame_principal, font="'Robot', 14", bd=3)  # espacio de 35
        self.entrada_nombre.place(x=40, y=35, width=135, height=30)

        # entrada talla
        self.entrada_talla = Entry(frame_principal, font="'Robot', 14", bd=3)
        self.entrada_talla.place(x=205, y=35, width=120, height=30)

        # entrada unidades
        self.entrada_unidades = Entry(frame_principal, font="'Robot', 14", bd=3)
        self.entrada_unidades.place(x=359, y=35, width=120, height=30)

        # entrada precio fabrica
        self.entrada_preciof = Entry(frame_principal, font="'Robot', 14", bd=3)
        self.entrada_preciof.place(x=514, y=35, width=120, height=30)

        # entrada precio
        self.entrada_precio_CL = Entry(frame_principal, font="'Robot', 14", bd=3,
                                       textvariable=self.string_var_operacion)
        self.entrada_precio_CL.place(x=668, y=35, width=120, height=30)

        # entrada ganancia
        self.entrada_ganancia = Entry(frame_principal, font="'Robot', 14", bd=3, state='readonly')
        self.entrada_ganancia.place(x=817, y=35, width=120, height=30)

        # entrada desscripcion
        self.entrada_descripcion = Text(frame_principal, font="'console', 12", bd=3)
        self.entrada_descripcion.place(x=165, y=100, width=300, height=170)

        # entrada id
        self.entrada_id = Entry(frame_principal, font="'Robot', 14", bd=3, fg='#006400', justify='right',)
        self.entrada_id.place(x=363, y=340, width=100, height=30)

        # boton guardar
        boton_guardar = Button(frame_principal, text="Guardar", bg="gray", font="'console', 15", bd=5, relief=GROOVE,
                               command=self.guardar_producto)
        boton_guardar.config()
        boton_guardar.place(x=363, y=290, width=100, height=40, )

        # boton agregar imagen
        boton_agregar_img = Button(self.frame_secundario, text="Agregar img", bg="gray", font="'Robot, 12",
                                   command=lambda: self.cargar_img(self.label_imagen), bd=2.5, relief=GROOVE)
        boton_agregar_img.place(x=310, y=208, width=98, height=25)

        # boton buscar
        boton_buscar = Button(frame_principal, bg="gray", text="Buscar", font="'Robot', 15", bd=5, relief=GROOVE,
                              command=lambda: self.buscar_producto(self.label_imagen))
        boton_buscar.place(x=248, y=290, width=100, height=40)

        # boton borrar
        boton_borrar = Button(frame_principal, bg="gray", text="Borrar", font="'Robot', 15", bd=5, relief=GROOVE,
                              command=self.borra)
        boton_borrar.place(x=132, y=290, width=100, height=40)

        # boton limpiar espacios
        boton_limpiar = Button(frame_principal, text="Limpiar", bg='gray', font="'ROBOT', 15", bd=5, relief=GROOVE,
                               command=self.limpiar)
        boton_limpiar.place(x=17, y=290, width=100, height=40)

        # boton menu
        boton_menu = Menubutton(label, image=imagen_final, bg='#737373')  # 696969
        boton_menu.place(x=3, y=8, width=32, height=38)
        boton_menu.image = imagen_final

        # menuu dentro de el boton
        menu_dentro = Menu(boton_menu, tearoff=False)
        boton_menu.configure(menu=menu_dentro)

        # añadimos el menu desplegable que tendra el boton
        menu_dentro.add_cascade(label="Base de datos", font=('console', 8, 'bold'), background='white',
                                activebackground='#79CDCD', foreground='black', activeforeground='black',
                                command=self.ver_base_datos)
        menu_dentro.add_cascade(label="Ventas", font=('console', 8, 'bold'), background='white',
                                activebackground='#79CDCD', foreground='black', activeforeground='black',
                                command=self.mostrar_ventas)
        menu_dentro.add_cascade(label="Contabilidad", font=('console', 8, 'bold'), background='white',
                                activebackground='#79CDCD', foreground='black', activeforeground='black',
                                command=self.mostrar_contabilidad)
        menu_dentro.add_cascade(label="Cerrar sesion", font=('console', 8, 'bold'), background='white',
                                activebackground='#79CDCD', foreground='black', activeforeground='black',
                                command=self.opcion_cerrar_sesion)

        self.root.mainloop()

    def operacion_ganancia_prod(self, *args):

        try:
            # obtenemos las entradas de los valores de fabrica y cliente
            if self.entrada_preciof is not None:
                entrada_fabrica = self.entrada_preciof.get()
                obtener_str_vent = self.string_var_operacion.get()

                # si no se ingresa nada en la entrada de el precio cliente se elimina
                # el valor de la entrada de ganancia para que no quede ningun valor ahi
                if len(self.entrada_precio_CL.get()) <= 0:
                    self.entrada_ganancia.config(state='normal')
                    self.entrada_ganancia.delete(0, END)
                    self.entrada_ganancia.config(state='readonly')

                # condicion para verificar que se escribio algo en las entradas
                elif obtener_str_vent and entrada_fabrica:
                    # esta es la operacion para sacar la ganancia
                    operacion = int(obtener_str_vent) - int(entrada_fabrica)
                    operacion_formateada = f"{operacion:,}"

                    # se cambia el estado de solo lectura de el entry ganancia
                    # para poder insertar texto y luego ponerlo como estaba
                    self.entrada_ganancia.config(state='normal')
                    self.entrada_ganancia.delete(0, END)
                    self.entrada_ganancia.insert(0, operacion_formateada)
                    self.entrada_ganancia.config(state='readonly')
        except ValueError:

            # si se ingresan numeros con puntos o letras dara un error para ingresar bien los nuemeros
            messagebox.showinfo('ALERTA', 'SOLO SE ADMITEN NUMEROS SIN PUNTUACION EN LOS PRECIOS')
            self.entrada_preciof.delete(0, END)
            self.entrada_precio_CL.delete(0, END)
            self.entrada_ganancia.config(state='normal')
            self.entrada_ganancia.delete(0, END)
            self.entrada_ganancia.config(state='readonly')

    def cargar_img(self, label):

        self.ruta_imagen = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if self.ruta_imagen:
            imagen_1 = Image.open(self.ruta_imagen)
            imagen_2 = imagen_1.resize((413, 236), Image.LANCZOS)  # Redimensiona la imagen a 200x200 píxeles
            photo = ImageTk.PhotoImage(imagen_2)
            label.config(image=photo, bd=2, relief=RAISED)
            label.image = photo  # Mantén una referencia de la imagen

    def guardar_producto(self):

        nombre_prod = self.entrada_nombre.get()
        talla_prod = self.entrada_talla.get()
        precio_fab = self.entrada_preciof.get()
        precio_prod = self.entrada_precio_CL.get()
        unidades_prod = self.entrada_unidades.get()
        entrada_ganancia = self.entrada_ganancia.get()
        descripcion_prod = self.entrada_descripcion.get(1.0, END)
        verificar_imagen = self.label_imagen.cget('image')
        img = self.ruta_imagen
        count_desc = len(descripcion_prod)

        if nombre_prod and talla_prod and precio_fab and precio_prod and unidades_prod and entrada_ganancia and \
                descripcion_prod and img and count_desc > 3 and verificar_imagen:

            cursor.execute("""
            INSERT INTO productos(Nombre, Talla, Unidades, Precio_fabrica, Precio_cliente,Ganancia, Descripcion, Imagen)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", (nombre_prod, talla_prod, unidades_prod, precio_fab, precio_prod,
                                                entrada_ganancia, descripcion_prod, img))
            id_reciente = cursor.lastrowid
            if id_reciente:

                cursor.execute(f"SELECT unidades, Precio_fabrica FROM productos WHERE id=?", (id_reciente,))
                dato = cursor.fetchone()

                operacion = dato[0] * dato[1]
                cursor.execute("UPDATE productos SET Total_invertido=? WHERE Total_invertido IS NULL",
                               (f"{operacion:,}",))

                texto = "Guardado corretamente"
                self.mensaje_temporal_noimagen(self.root, texto, 3000)
                self.entrada_id.config(fg='#006400')
                self.entrada_id.insert(tkinter.END, id_reciente)
            conexion.commit()
        else:
            messagebox.showinfo("ALERTA", "ESPACIOS VACIOS")

    def buscar_producto(self, mostrar):

        id = self.entrada_id.get()
        cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
        dato = cursor.fetchone()

        if dato:

            self.entrada_nombre.delete(0, END)
            self.entrada_talla.delete(0, END)
            self.entrada_unidades.delete(0, END)
            self.entrada_preciof.delete(0, END)
            self.entrada_precio_CL.delete(0, END)
            self.entrada_ganancia.delete(0, END)
            self.entrada_descripcion.delete(1.0, END)

            self.entrada_nombre.insert(tkinter.END, dato[1])
            self.entrada_talla.insert(tkinter.END, dato[2])
            self.entrada_unidades.insert(tkinter.END, dato[3])
            self.entrada_preciof.insert(tkinter.END, dato[4])
            self.entrada_precio_CL.insert(tkinter.END, dato[5])
            self.entrada_ganancia.insert(tkinter.END, dato[4])
            self.entrada_descripcion.insert(tkinter.END, dato[7])

            imagen_1 = Image.open(dato[9])
            imagen_2 = imagen_1.resize((413, 236), Image.LANCZOS)  # Redimensiona la imagen a 200x200 píxeles
            photo = ImageTk.PhotoImage(imagen_2)
            mostrar.config(image=photo, bd=2, relief=RAISED)
            mostrar.image = photo  # Mantén una referencia de la imagen
        elif len(id) < 1:
            messagebox.showinfo("ALERTA", "ESPACIO ID VACIO")
        elif dato is None:
            messagebox.showinfo("ALERTA", "PRODUCTO NO ENCONTRADO")

    def limpiar(self):

        self.entrada_nombre.delete(0, END)
        self.entrada_talla.delete(0, END)
        self.entrada_unidades.delete(0, END)
        self.entrada_preciof.delete(0, END)
        self.entrada_precio_CL.delete(0, END)
        self.entrada_ganancia.config(state='normal')
        self.entrada_ganancia.delete(0, END)
        self.entrada_ganancia.config(state='readonly')
        self.entrada_descripcion.delete(1.0, END)
        self.label_imagen.config(image='')
        self.entrada_id.delete(0, END)

    def borra(self):

        dato_borrar = self.entrada_id.get()

        if len(dato_borrar) < 1:
            messagebox.showinfo("ALERTA", "ESPACIO ID VACIO")
        elif len(dato_borrar) >= 1:

            codigo = str(346643)
            clave = simpledialog.askstring(title='CODIGO DE SEGURIDAD0',
                                           prompt='INGRESE EL CODIGO DE SEGURIDAD PARA BORRAR UN ARTCULO')
            if clave == codigo:

                cursor.execute("DELETE FROM productos WHERE id=?", (dato_borrar,))
                conexion.commit()
                self.limpiar()

                cursor.execute("SELECT * FROM productos WHERE id=?", (dato_borrar,))
                dato_consulta = cursor.fetchone()

                if dato_consulta is None:
                    self.limpiar()
                    texto = "Eliminado corretamente"
                    self.mensaje_temporal_noimagen(self.root, texto, 3000)
            elif clave != codigo:
                messagebox.showinfo('ALERTA', 'CODIGO DE SEGURIDAD INCORRECTO')

    def opcion_cerrar_sesion(self):

        # instanciamos la clase inicio sesion para despues abrir el inicio de sesion
        volver_inicio = Iniciosesion()

        # cerramos la ventana de el programa principal
        self.root.destroy()

        volver_inicio.inicio()

    def mensaje_temporal(self, root1, mensaje, duracion, imagen=None, x=None, y=None, ancho=None, alto=None):

        # crear un label para mostrar
        label = Label(self.root, text=mensaje, image=imagen, bd=2, relief=GROOVE)
        label.config(bg="#CDC0B0", font="'console', 10")
        label.place(x=x, y=y, width=ancho, height=alto)
        label.image = imagen

        root1.after(duracion, label.destroy)

    def mensaje_temporal_noimagen(self, root1, mensaje, duracion, ):

        label = Label(self.root, text=mensaje, bd=3, relief=GROOVE)
        label.config(bg="green2", font="'console', 10")
        label.place(x=260, y=340, width=150, height=30)

        root1.after(duracion, label.destroy)

    def mostrar_tabla_stock(self):

        self.frame_stock.place_forget()
        self.frame_tabla_datos.place(x=0, y=0, width=1000, height=500)

    def mostrar_ventas(self):

        self.frame_stock.place_forget()
        self.ventana_ventas()

    def mostrar_frame_stock(self):

        self.frame_ventas.place_forget()
        self.frame_stock.place(x=0, y=0, width=1000, height=500)

    def mostrar_frame_contabilidad(self):

        self.frame_contabilidad.place_forget()
        self.frame_stock.place(x=0, y=0, width=1000, height=500)

    def boton_volver(self):

        self.frame_tabla_datos.place_forget()
        self.frame_stock.place(x=0, y=0, width=1000, height=500)

    # barra de busqueda en base de datos
    def update_list(self, *args):

        obtener_strvar = self.busqueda_var.get().lower()

        # eliminar todos los elementos del arbol que no coincidad
        for item in self.treeview.get_children():
            fila = self.treeview.item(item)['values']
            if obtener_strvar not in str(fila).lower():
                self.treeview.delete(item)

        if obtener_strvar:
            # agregar de nuevo solo los elementos que coinciden con la busqueda
            for item1 in self.filas:
                for valor in item1:
                    if obtener_strvar.lower() in str(valor).lower():
                        self.treeview.insert('', 'end', values=item1)
        elif not obtener_strvar:
            for i in self.treeview.get_children():
                self.treeview.delete(i)
            cursor.execute("SELECT * FROM productos")
            datos = cursor.fetchall()
            for dato in datos:
                self.treeview.insert('', 'end', values=dato)

    # obtener filas de los productos
    def obtener_filas(self):

        self.filas = []
        for item_filas in self.treeview.get_children():
            fila = self.treeview.item(item_filas)['values']
            self.filas.append(fila)

    # aqui estar la tabla de los productos
    def ver_base_datos(self):

        self.frame_tabla_datos = Frame(self.root)
        self.frame_tabla_datos.place(x=0, y=0, width=1000, height=500)

        # self.mostrar_tabla_stock()

        # Crea un estilo
        estilo = ttk.Style()

        # le damos el estilo de tema visual
        estilo.theme_use("clam")

        # Configura el estilo del Treeview
        estilo.configure("Treeview",
                         background="#458B74",  # Color de fondo
                         foreground="black",  # Color del texto
                         rowheight=24,  # Altura de las filas
                         fieldbackground="white",
                         font=('Console', 15))  # tipo de letra
        estilo.map('Treeview', background=[('selected', '#00FFFF')], foreground=[('selected', 'black')])

        # Configura el estilo del encabezado del Treeview
        estilo.configure("Treeview.Heading",
                         background="#708090",  # Color de fondo
                         foreground="black",  # Color del texto
                         font=("console", 14, "bold"))  # Tipo de letra

        # Crea un Treeview
        self.treeview = ttk.Treeview(self.frame_tabla_datos)

        # consulta para insertar los datos a la tabla
        cursor.execute("SELECT * FROM productos")
        datos = cursor.fetchall()

        # insertamos con un bucle los valores
        for dato in datos:
            self.treeview.insert('', 'end', values=dato)

        # creamos el scrollbar
        scrbar = ttk.Scrollbar(self.frame_tabla_datos, orient='vertical', command=self.treeview.yview)
        scrbar.place(relx=0.98, rely=0, relwidth=0.02, relheight=0.932)

        # actualizar el contenido cuando se deslace la barra
        self.treeview.configure(yscrollcommand=scrbar.set)

        # Define las columnas
        self.treeview['columns'] = ("ID", "Nombre", "Talla", "Unidades", "Precio_Compra", "Precio_venta",
                                    "Total_invertido", "Ganancia", "Descripcion")

        # Formatea cada columna
        self.treeview.column('#0', width=0, stretch=NO)
        self.treeview.column(column="ID", anchor=CENTER, width=2)
        self.treeview.column(column="Nombre", anchor=CENTER, width=25)
        self.treeview.column(column="Talla", anchor=CENTER, width=15)
        self.treeview.column(column="Unidades", anchor=CENTER, width=50)
        self.treeview.column(column="Precio_Compra", anchor=CENTER, width=78)
        self.treeview.column(column="Precio_venta", anchor=CENTER, width=35)
        self.treeview.column(column="Total_invertido", anchor=CENTER, width=35)
        self.treeview.column(column="Ganancia", anchor=CENTER, width=78)
        self.treeview.column(column="Descripcion", anchor=CENTER, width=78)
        # self.treeview.column(column="Imagen", anchor=CENTER, width=70)

        # Crea los encabezados
        self.treeview.heading("#0", text="", anchor=CENTER)
        self.treeview.heading("ID", text="ID", anchor=CENTER)
        self.treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        self.treeview.heading("Talla", text="Talla", anchor=CENTER)
        self.treeview.heading("Unidades", text="Unidades", anchor=CENTER)
        self.treeview.heading("Precio_Compra", text="Precio_Compra", anchor=CENTER)
        self.treeview.heading("Precio_venta", text="Precio_venta", anchor=CENTER)
        self.treeview.heading("Total_invertido", text="Total_invertido", anchor=CENTER)
        self.treeview.heading("Ganancia", text="Ganancia", anchor=CENTER)
        self.treeview.heading("Descripcion", text="Descripcion", anchor=CENTER)
        # self.treeview.heading("Imagen", text="Imagen", anchor=CENTER)

        # creamos un stringvar para poder hacer la busqueda
        self.busqueda_var = StringVar()
        self.busqueda_var.trace('w', self.update_list)

        # hacemos un label que diga buscar
        label_buscar = Label(self.frame_tabla_datos, text='Buscar', font="'console', 11", relief=GROOVE)
        label_buscar.place(x=5, y=2, width=70, height=27)

        # creamos el entry para escribir la busqueda
        entrada = Entry(self.frame_tabla_datos, textvariable=self.busqueda_var, bg='#CDC0B0')
        entrada.config(bd=3, font="'console', 13", relief=GROOVE)
        entrada.place(x=75, y=2, width=700, height=27)

        # ubicamos la tabla
        self.treeview.place(x=5, y=30, width=975, height=437)

        # imagen para el boton volver
        botonvolver = Iniciosesion.resolver_ruta('assets/flecha_volver.png')
        img_volver = Image.open(botonvolver)
        img_volver2 = img_volver.resize((62, 28), Image.LANCZOS)
        imagen_final = ImageTk.PhotoImage(img_volver2)

        # boton volver
        boton_regresar = Button(self.frame_tabla_datos, text='regresar', image=imagen_final, bg='white', relief=GROOVE,
                                bd=4, command=self.boton_volver)
        boton_regresar.place(x=5, y=469, width=80, height=31)
        boton_regresar.image = imagen_final

    # aqui estara la seccion de las ventas
    def ventana_ventas(self):

        # frame principal de ventas
        self.frame_ventas = Frame(self.root, bg='#ADADAD')
        self.frame_ventas.place(x=0, y=0, width=1000, height=500)

        # strinvar para id de la venta
        self.stringvar_ventas = StringVar()
        self.stringvar_ventas.trace('w', self.buscar_precio_prod)

        # stringvar para busqueda en ventas
        self.busquedavar_ventas = StringVar()
        self.busquedavar_ventas.trace('w', self.busqueda_ventas)

        # stringvar para la cantidad de la venta
        self.stringvar_cantidad = StringVar()
        self.stringvar_cantidad.trace('w', self.operacion_cantidad)

        # hacemos un label que diga buscar en ventas
        label_ventas_buscar = Label(self.frame_ventas, text='Buscar', font="'console', 11", relief=GROOVE)
        label_ventas_buscar.place(x=5, y=189, width=70, height=27)

        # creamos el entry para escribir la busqueda en ventas
        self.entrada_busqueda_ventas = Entry(self.frame_ventas, bg='#CDC0B0', textvariable=self.busquedavar_ventas)
        self.entrada_busqueda_ventas.config(bd=3, font="'console', 13", relief=GROOVE)
        self.entrada_busqueda_ventas.place(x=75, y=189, width=700, height=27)

        # creamos un estilo
        estilo_ventas = ttk.Style()

        estilo_ventas.theme_use('clam')

        # Configura el estilo del Treeview
        estilo_ventas.configure('Treeview',
                                background='#458B74',
                                foreground='black',  # color de fondo
                                rowheight=24,  # Altura de las filas
                                fildbackground='white',
                                font=('console', 15))  # tipo de letra
        estilo_ventas.map("Treeview", backgroud=[('selected', '#00FFFF')], foreground=[('selected', 'black')])

        # Configura el estilo del encabezado del Treeview
        estilo_ventas.configure("Treeview.Heading",
                                background="#708090",  # Color de fondo
                                foreground="black",  # Color del texto
                                font=("console", 14, "bold"))  # Tipo de letra

        self.treeview_ventas = ttk.Treeview(self.frame_ventas)

        # consulta a la base de datos
        cursor.execute("SELECT * FROM ventas")
        datos_ventas = cursor.fetchall()

        # insertamos los valores a la tabla
        for dato in datos_ventas:
            self.treeview_ventas.insert('', 0, values=dato)

        # creamos el scrollbar
        scrbar_ventas = ttk.Scrollbar(self.frame_ventas, orient='vertical', command=self.treeview_ventas.yview)
        scrbar_ventas.place(relx=0.974, rely=0.440, relwidth=0.02, relheight=0.491)

        # actualizar el contenido cuando se deslace la barra
        self.treeview_ventas.configure(yscrollcommand=scrbar_ventas.set)

        self.treeview_ventas['columns'] = ('ID', 'Producto', 'ID_prd', 'Cantidad', 'Valor unit', 'Total venta',
                                           'Ganancias', 'Fecha')

        # formateamos cada columna
        self.treeview_ventas.column('#0', width=0, stretch=NO)
        self.treeview_ventas.column(column="ID", anchor=CENTER, width=2)
        self.treeview_ventas.column(column="Producto", anchor=CENTER, width=2)
        self.treeview_ventas.column(column="ID_prd", anchor=CENTER, width=2)
        self.treeview_ventas.column(column="Cantidad", anchor=CENTER, width=2)
        self.treeview_ventas.column(column="Valor unit", anchor=CENTER, width=2)
        self.treeview_ventas.column(column="Total venta", anchor=CENTER, width=2)
        self.treeview_ventas.column(column="Ganancias", anchor=CENTER, width=2)
        self.treeview_ventas.column(column="Fecha", anchor=CENTER, width=2)

        # le damos nombre a los encabezados
        self.treeview_ventas.heading('#0', text="", anchor=CENTER)
        self.treeview_ventas.heading("ID", text="ID", anchor=CENTER)
        self.treeview_ventas.heading("Producto", text="Producto", anchor=CENTER)
        self.treeview_ventas.heading("ID_prd", text="ID_prd", anchor=CENTER)
        self.treeview_ventas.heading("Cantidad", text="Cantidad", anchor=CENTER)
        self.treeview_ventas.heading("Valor unit", text="Valor unit", anchor=CENTER)
        self.treeview_ventas.heading("Total venta", text="Total venta", anchor=CENTER)
        self.treeview_ventas.heading("Ganancias", text="Ganancias", anchor=CENTER)
        self.treeview_ventas.heading("Fecha", text="Fecha", anchor=CENTER)

        # ubicamos la tabla
        self.treeview_ventas.place(x=5, y=219, width=968, height=247)

        # frame para poner los widgets de la venta dentro
        frame_ventas2 = Frame(self.frame_ventas, bg='#458B74')
        frame_ventas2.place(x=5, y=5, width=990, height=181)

        # label prodcto en venta
        label_producto = Label(self.frame_ventas, text='Producto:', bg="#458B74", font="'Robot', 16")
        label_producto.place(x=50, y=10)

        # label para id de el producto
        label_id_pro = Label(self.frame_ventas, text='ID prod:', bg="#458B74", font="'Robot', 16")
        label_id_pro.place(x=413, y=10)

        # label para la cntidad de el producto a llevar
        label_cantidadventa = Label(self.frame_ventas, text='Cantidad:', bg="#458B74", font="'Robot', 16")
        label_cantidadventa.place(x=687, y=10)

        # label precio del producto
        label_precioprod = Label(self.frame_ventas, text='Precio producto:', bg="#458B74", font="'Robot', 16")
        label_precioprod.place(x=50, y=50)

        # label para la ganancia
        label_gananciavent = Label(self.frame_ventas, text='Ganancia:', bg="#458B74", font="'Robot', 16")
        label_gananciavent.place(x=50, y=90)

        # label total de la venta
        label_totalventa = Label(self.frame_ventas, text='Total venta:', bg="#00FF00", font="'Robot', 16", fg='black',
                                 relief=GROOVE, bd=3)
        label_totalventa.place(x=50, y=150)

        label_gasto = Label(self.frame_ventas, text='Gasto:', bg="#458B74", font="'Robot', 16")
        label_gasto.place(x=413, y=50)

        label_gasto = Label(self.frame_ventas, text='Valor G:', bg="#458B74", font="'Robot', 16")
        label_gasto.place(x=413, y=90)

        # entrada producto ventas
        self.entrada_prventas = Entry(self.frame_ventas, bg='white', font="'console', 14", relief=GROOVE, bd=4,
                                      state='readonly')
        self.entrada_prventas.place(x=155, y=10, width=200, height=30)

        # entrada id ventas
        self.entrada_idproventas = Entry(self.frame_ventas, bg='white', font="'console', 14", relief=GROOVE, bd=4,
                                         textvariable=self.stringvar_ventas)
        self.entrada_idproventas.place(x=500, y=10, width=140, height=30)

        # entrada cantidad
        self.entrada_cantidadvent = Entry(self.frame_ventas, bg='white', font="'console', 14", relief=GROOVE, bd=4,
                                          textvariable=self.stringvar_cantidad)
        self.entrada_cantidadvent.place(x=790, y=10, width=140, height=30)

        # precio del producto
        self.entrada_precioprod = Entry(self.frame_ventas, bg='white', font="'console', 14", relief=GROOVE, bd=4)
        self.entrada_precioprod.place(x=215, y=50, width=140, height=30)

        # entrada total de la ganancia
        self.entrada_gananciaventas = Entry(self.frame_ventas, bg='white', font="'console', 14", relief=GROOVE, bd=4,
                                            state='readonly')
        self.entrada_gananciaventas.place(x=215, y=90, width=140, height=30)

        # entrada total de la venta
        self.entrada_totalventa = Entry(self.frame_ventas, bg='white', font="'console', 14", relief=GROOVE, bd=4,
                                        state='readonly')
        self.entrada_totalventa.place(x=215, y=150, width=140, height=30)

        # entrada nnombre del gasto
        self.nombre_gasto = Entry(self.frame_ventas, bg='red', font="'console', 14", relief=GROOVE, bd=4)
        self.nombre_gasto.place(x=500, y=50, width=140, height=30)

        # entrada valor del gasto
        self.valor_gasto = Entry(self.frame_ventas, bg='red', font="'console', 14", relief=GROOVE, bd=4)
        self.valor_gasto.place(x=500, y=90, width=140, height=30)

        # imagen para boton regresar
        botonvolver = Iniciosesion.resolver_ruta('assets/flecha_volver.png')
        imagen_volver = Image.open(botonvolver)
        imagen_volver2 = imagen_volver.resize((63, 28), Image.LANCZOS)
        imagen_volver_final = ImageTk.PhotoImage(imagen_volver2)

        # imagen actualizar ventas
        ventana_ruta = Iniciosesion.resolver_ruta('assets/refrescar.png')
        imagen_act_ventas = Image.open(ventana_ruta)
        imagen_act_ventas2 = imagen_act_ventas.resize((22, 22), Image.LANCZOS)
        img_act_final = ImageTk.PhotoImage(imagen_act_ventas2)

        # boton para realizar la compra
        boton_vender = Button(self.frame_ventas, text='Vender', bg='green2', relief=GROOVE, font="'console, 14",
                              bd=4, command=self.guardar_venta)
        boton_vender.place(x=830, y=70, width=100, height=40)

        # bboton para limpiar los espacios
        boton_limpiar = Button(self.frame_ventas, text='Limpiar', bg='#9AC0CD', relief=GROOVE, font="'console, 14",
                               bd=4, command=self.boton_limpiar_venta)
        boton_limpiar.place(x=830, y=130, width=100, height=40)

        # boton para regresar a la seccion principal
        boton_regresar = Button(self.frame_ventas, image=imagen_volver_final, text='regresar', bg='white',
                                relief=GROOVE, font="'console, 14",
                                bd=4, command=self.mostrar_frame_stock)
        boton_regresar.place(x=5, y=465, width=78, height=33)
        boton_regresar.Image = imagen_volver_final

        # boton para actualizar la tabla de las ventas
        boton_actualizar_ventas = Button(self.frame_ventas, image=img_act_final, command=self.boton_actualizar_ventas)
        boton_actualizar_ventas.place(x=776.5, y=190, width=25, height=25.5)
        boton_actualizar_ventas.Image = img_act_final

        # boton borrar venta
        boton_borrar_venta = Button(self.frame_ventas, text='Borrar venta', bg='#9AC0CD', relief=GROOVE,
                                    font="'console, 13", bd=4, command=self.borrar_venta)
        boton_borrar_venta.place(x=715, y=130, width=100, height=40)

        # boton para guardar los gastos
        boton_guardar_gasto = Button(self.frame_ventas, text='Gastar', bg='red', relief=GROOVE,
                                     font="'console, 14", bd=4, command=self.guardar_gasto)
        boton_guardar_gasto.place(x=715, y=70, width=100, height=40)

        boton_reporte = Menubutton(self.frame_ventas, text='REPORTE', bg='#00EEEE', relief=GROOVE,
                                   font="'console, 12", bd=4)
        boton_reporte.place(x=820, y=189, width=148, height=27)

        menu_reporte = Menu(boton_reporte, tearoff=False)
        boton_reporte.configure(menu=menu_reporte)

        menu_reporte.add_cascade(label="DIA", font=('console', 10, 'bold'), background='white',
                                 activebackground='#79CDCD', foreground='black', activeforeground='black',
                                 command=self.reporte_dia)

        menu_reporte.add_cascade(label="MES", font=('console', 10, 'bold'), background='white',
                                 activebackground='#79CDCD', foreground='black', activeforeground='black',
                                 command=self.operacion_mes)

    # obtener filas de las ventas
    # def obtener_filas_ventas(self):

        self.filas_ventas = []
        for item_filas in self.treeview_ventas.get_children():
            fila = self.treeview_ventas.item(item_filas)["values"]
            self.filas_ventas.append(fila)

    # esta es la busqueeda para la barra de busqueda en ventas
    def busqueda_ventas(self, *args):

        stringvar = self.busquedavar_ventas.get().lower()

        for item in self.treeview_ventas.get_children():
            fila = self.treeview_ventas.item(item)['values']
            if stringvar not in str(fila):
                self.treeview_ventas.delete(item)

        if stringvar:
            for i in self.filas_ventas:
                for palabra in i:
                    if stringvar in str(i):
                        self.treeview_ventas.insert(i)

        elif not stringvar:
            for i in self.treeview_ventas.get_children():
                self.treeview_ventas.delete(i)
            cursor.execute("SELECT * FROM ventas")
            datos = cursor.fetchall()
            for dato in datos:
                self.treeview_ventas.insert('', 0, values=dato)

    # funcion para limpiar los espacios en vetas
    def boton_limpiar_venta(self):
        self.entrada_idproventas.delete(0, END)
        self.entrada_cantidadvent.delete(0, END)

        # limpiar entry  precio
        self.entrada_precioprod.delete(0, END)

        # limpiar entrada producto
        self.entrada_prventas.config(state='normal')
        self.entrada_prventas.delete(0, END)
        self.entrada_prventas.config(state='readonly')

        # limpiar
        self.entrada_gananciaventas.config(state='normal')
        self.entrada_gananciaventas.delete(0, END)
        self.entrada_gananciaventas.config(state='readonly')

    # esta funcioa es para cuando no se escriba nada en la barra de busqeda de las venta
    def limpiar_con_id(self, entrada):

        if entrada.get() == '':
            # limpiar entry precio
            self.entrada_precioprod.delete(0, END)

            # limpiar entrada producto
            self.entrada_prventas.config(state='normal')
            self.entrada_prventas.delete(0, END)
            self.entrada_prventas.config(state='readonly')

            # limpiar
            self.entrada_gananciaventas.config(state='normal')
            self.entrada_gananciaventas.delete(0, END)
            self.entrada_gananciaventas.config(state='readonly')

    # funcion para cuando se escriba el id de el producto a vender se muestre el nombre y el precio
    def buscar_precio_prod(self, *args):

        if self.entrada_precioprod is not None:
            stringvar = self.stringvar_ventas.get()

            cursor.execute("SELECT * FROM productos WHERE id=?", (stringvar,))
            dato = cursor.fetchall()

            # self.limpiar_con_id(self.entrada_idproventas)

            if dato:
                for palabra in dato:
                    # id para venta
                    self.entrada_precioprod.delete(0, END)
                    self.entrada_precioprod.insert(0, f"{palabra[5]:,}")

                    # nombre para venta
                    self.entrada_prventas.config(state='normal')
                    self.entrada_prventas.delete(0, END)
                    self.entrada_prventas.insert(0, palabra[1])
                    self.entrada_prventas.config(state='readonly')

            elif stringvar == '':
                self.limpiar_con_id(self.entrada_idproventas)

            elif dato != stringvar:
                # messagebox.showinfo('ALERTA', 'PRODUCTO NO ENCONTRADO')
                self.entrada_precioprod.delete(0, END)
                self.entrada_prventas.config(state='normal')
                self.entrada_prventas.delete(0, END)
                self.entrada_prventas.config(state='readonly')

    # funcion para la operacion segun la cantidad de productos  para el tota de la venta
    def operacion_cantidad(self, *args):

        try:
            if self.entrada_precioprod is not None:

                stringvar_cantidad = self.stringvar_cantidad.get()
                precio_cantidad = self.entrada_precioprod.get()
                cadena = precio_cantidad.replace(',', '')
                entero = int(cadena)
                strinvar_entero = int(float(stringvar_cantidad))
                operacion = strinvar_entero * entero

                if stringvar_cantidad:

                    self.entrada_totalventa.config(state='normal')
                    self.entrada_totalventa.delete(0, END)
                    self.entrada_totalventa.insert(0, f"{operacion:,}")
                    self.entrada_totalventa.config(state='readonly')

                    cursor.execute("SELECT Precio_fabrica FROM productos WHERE id=?",
                                   (int(self.entrada_idproventas.get()),))
                    dato = cursor.fetchone()

                    if dato:
                        operacion_1 = entero - dato[int(0)]
                        operacion_final = strinvar_entero * operacion_1

                        self.entrada_gananciaventas.config(state='normal')
                        self.entrada_gananciaventas.delete(0, END)
                        self.entrada_gananciaventas.insert(0, f"{operacion_final:,}")
                        self.entrada_gananciaventas.config(state='readonly')

        except ValueError:
            self.entrada_totalventa.config(state='normal')
            self.entrada_totalventa.delete(0, END)
            self.entrada_totalventa.config(state='readonly')

            self.entrada_gananciaventas.config(state='normal')
            self.entrada_gananciaventas.delete(0, END)
            self.entrada_gananciaventas.config(state='readonly')

    # mensaje temporar para los botones en la eccion ventas
    def mensaje_temporal_venta(self, root2, mensaje, duracion):

        label = Label(self.root, text=mensaje, bd=3.5, relief=GROOVE)
        label.config(bg="green2", font="'console', 10")
        label.place(x=490, y=140, width=150, height=30)

        root2.after(duracion, label.destroy)

    # aqui se guardara la venta
    def guardar_venta(self):

        zona_horaria = datetime.now(pytz.timezone('UTC'))
        fecha_local = zona_horaria.astimezone(pytz.timezone('America/Bogota'))

        nombre_por = self.entrada_prventas.get()
        id = self.entrada_idproventas.get()
        cantidad = self.entrada_cantidadvent.get()
        precio_prod = self.entrada_precioprod.get()
        total = self.entrada_totalventa.get()
        ganancia = self.entrada_gananciaventas.get()
        fecha_ahora = fecha_local.strftime('%Y-%m-%d %H:%M:%S')

        funcion_descontar = self.descontar_stock()

        if funcion_descontar:

            if nombre_por and id and cantidad and precio_prod and total and ganancia and fecha_ahora:
                cursor.execute("INSERT INTO ventas(producto, id_prd, cantidad, valor_uni, total_vent, ganancia, fecha) "
                               "VALUES(?, ?, ?, ?, ?, ?, ?)", (nombre_por, id, cantidad, precio_prod, total, ganancia,
                                                               fecha_ahora))

                dato = cursor.lastrowid
                conexion.commit()

                if dato:

                    self.mensaje_temporal_venta(self.root, 'VENTA REALIZADA', 2000)
                else:
                    messagebox.showinfo('ALERTA', 'NO SE GUARDO LA VENTA INTENTE NUEVAMENTE')
            else:
                pass
        elif not funcion_descontar:
            pass

    # cada que se haga una venta aqui se esta guardando
    def boton_actualizar_ventas(self):

        for i in self.treeview_ventas.get_children():
            self.treeview_ventas.delete(i)
        cursor.execute("SELECT * FROM ventas")
        datos = cursor.fetchall()
        for dato in datos:
            self.treeview_ventas.insert('', 0, values=dato)

    # funcion para borrar una venta
    def borrar_venta(self):

        num_codigo = str(346643)

        num_id = simpledialog.askstring(title='ID VENTA',
                                        prompt='INGRESE EL ID DE LA VENTA A ELIMINAR')

        if not num_id:
            messagebox.showinfo('ALERTA', 'ESPACIO VACIO')

        elif num_id:

            cursor.execute('SELECT EXISTS (SELECT id FROM ventas WHERE id=?)', (num_id,))
            existe = cursor.fetchone()[0]

            if existe:

                cursor.execute("SELECT * FROM ventas WHERE id=?", (num_id,))
                dato = cursor.fetchone()

                if dato[0]:
                    codigo = simpledialog.askstring(title='CODIGO DE SEGURIDAD',
                                                    prompt='INGRESE EL CODIGO DE SEGURIDAD '
                                                           'PARA ELIMINAR UNA VENTA', parent=self.frame_ventas)

                    if codigo == num_codigo:

                        cursor.execute("SELECT Unidades FROM productos WHERE id=?", (dato[2],))
                        unidades_reciente = cursor.fetchone()
                        suma_cantidades = dato[3] + unidades_reciente[0]

                        cursor.execute("DELETE FROM ventas WHERE id=?", (dato[0],))
                        dato2 = cursor.fetchone()

                        cursor.execute("UPDATE productos SET unidades=? WHERE id=?", (suma_cantidades, dato[2]),)

                        if not dato2:
                            self.mensaje_temporal_venta(self.root, 'ELIMINADO', 2000)

                            conexion.commit()
                        else:
                            self.mensaje_temporal_venta(self.root, 'ERROR AL ELIMINAR', 2000)
                    elif codigo != num_codigo:
                        messagebox.showinfo('ALERTA', 'CODIGO INCORRECTO')

            elif not existe:
                messagebox.showinfo('ALERTA', 'EL ID INGRESADO NO EXISTE ')

    # funcion para  guardar los gastos
    def guardar_gasto(self):

        try:

            nombre_gasto = self.nombre_gasto.get()
            valor_gasto = self.valor_gasto.get()
            valor_gasto_fin = f"{int(valor_gasto):,}"
            fecha = datetime.now(pytz.timezone('UTC'))
            fecha_local = fecha.astimezone(pytz.timezone('America/Bogota'))
            fecha_final = fecha_local.strftime('%Y-%m-%d %H:%M:%S')

            if nombre_gasto and valor_gasto:

                cursor.execute('INSERT INTO gastos(Nombre_gasto, Valor_gasto, Fecha) VALUES(?, ?, ?)',
                               (nombre_gasto, valor_gasto_fin, fecha_final))
                dato = cursor.lastrowid

                if dato:
                    conexion.commit()
                    self.mensaje_temporal_venta(self.root, 'HECHO', 2000)
                elif dato is None:
                    messagebox.showinfo('ALERTA', 'NO SE PUDO GUARDAR INTENTE DE NUEVO')
            elif not nombre_gasto and not valor_gasto:
                messagebox.showinfo('ALERTA', "ESPACIOS VACIOS 'GASTO Y VALOR GASTO'")
        except ValueError:
            messagebox.showinfo('ALERTA', "INGRESE VALORES ENTEROS (NUMEROS) Y "
                                          "SIN SIGNOS DE PUNTUACION EN EL ESPACIO 'VALOR G'")

    # funcion para mostrar la seccioon o frame de contabilidad
    def mostrar_contabilidad(self):

        self.frame_stock.place_forget()
        self.ventana_contabilidad()

    # esta es la seccion para la contaabilidad
    def ventana_contabilidad(self):

        self.frame_contabilidad = Frame(self.root)
        self.frame_contabilidad.place(x=0, y=0, width=1000, height=500)

        # creamos un estilo
        estilo_gastos = ttk.Style()

        estilo_gastos.theme_use('clam')

        # Configura el estilo del Treeview
        estilo_gastos.configure('Treeview',
                                background='#458B74',
                                foreground='black',  # color de fondo
                                rowheight=24,  # Altura de las filas
                                fildbackground='white',
                                font=('console', 15))  # tipo de letra
        estilo_gastos.map("Treeview", backgroud=[('selected', '#00FFFF')], foreground=[('selected', 'black')])

        # Configura el estilo del encabezado del Treeview
        estilo_gastos.configure("Treeview.Heading",
                                background="#708090",  # Color de fondo
                                foreground="black",  # Color del texto
                                font=("console", 14, "bold"))  # Tipo de letra

        self.treeview_gastos = ttk.Treeview(self.frame_contabilidad)

        cursor.execute("SELECT * FROM gastos")
        datos_gastos = cursor.fetchall()

        for dato in datos_gastos:
            self.treeview_gastos.insert('', 0, values=dato)

        # creamos el scrollbar
        scrbar_gastos = ttk.Scrollbar(self.frame_contabilidad, orient='vertical', command=self.treeview_gastos.yview)
        scrbar_gastos.place(relx=0.974, rely=0.560, relwidth=0.02, relheight=0.370)

        # actualizar el contenido cuando se deslace la barra
        self.treeview_gastos.configure(yscrollcommand=scrbar_gastos.set)

        self.treeview_gastos['columns'] = ('ID GASTOS', 'Nombre gasto', 'Valor gasto', 'Fecha')

        self.treeview_gastos.column('#0', width=0, stretch=NO)
        self.treeview_gastos.column(column="ID GASTOS", anchor=CENTER, width=2)
        self.treeview_gastos.column(column="Nombre gasto", anchor=CENTER, width=2)
        self.treeview_gastos.column(column="Valor gasto", anchor=CENTER, width=2)
        self.treeview_gastos.column(column="Fecha", anchor=CENTER, width=2)

        self.treeview_gastos.heading('#0', text="", anchor=CENTER)
        self.treeview_gastos.heading("ID GASTOS", text="ID GASTOS", anchor=CENTER)
        self.treeview_gastos.heading("Nombre gasto", text="Nombre gasto", anchor=CENTER)
        self.treeview_gastos.heading("Valor gasto", text="Valor gasto", anchor=CENTER)
        self.treeview_gastos.heading("Fecha", text="Fecha", anchor=CENTER)

        # ubicamos la tabla
        self.treeview_gastos.place(x=5, y=280, width=968, height=185)

        # frame para poner los widgets de los gasto dentro
        # frame_gastos2 = Frame(self.frame_contabilidad, bg='#458B74')
        # frame_gastos2.place(x=5, y=5, width=990, height=181)

        # stringvar para busqueda en gastos
        self.busquedavar_gastos = StringVar()
        self.busquedavar_gastos.trace('w', self.busqueda_gastos)

        # hacemos un label que diga buscar en gastos
        label_gastos = Label(self.frame_contabilidad, text='Buscar', font="'console', 11", relief=GROOVE)
        label_gastos.place(x=5, y=252, width=70, height=27)

        # creamos el entry para escribir la busqueda en gastos
        self.entrada_busqueda_gastos = Entry(self.frame_contabilidad, bg='#CDC0B0',
                                             textvariable=self.busquedavar_gastos)
        self.entrada_busqueda_gastos.config(bd=3, font="'console', 13", relief=GROOVE)
        self.entrada_busqueda_gastos.place(x=75, y=252, width=700, height=27)

        # imagen para boton regresar
        volver_ruta = Iniciosesion.resolver_ruta('assets/flecha_volver.png')
        imagen_volver = Image.open(volver_ruta)
        imagen_volver2 = imagen_volver.resize((63, 28), Image.LANCZOS)
        imagen_volver_final = ImageTk.PhotoImage(imagen_volver2)

        # boton regresar
        boton_regresar = Button(self.frame_contabilidad, image=imagen_volver_final, text='regresar', bg='white',
                                relief=GROOVE, font="'console, 14",
                                bd=4, command=self.mostrar_frame_contabilidad)
        boton_regresar.place(x=5, y=467, width=78, height=33)
        boton_regresar.Image = imagen_volver_final

        # insertamos la tabla de los reportes en el label 2
        # creamos un estilo
        estilo_reporte = ttk.Style()

        estilo_reporte.theme_use('clam')

        # Configura el estilo del Treeview
        estilo_reporte.configure('Treeview',
                                 background='#458B74',
                                 foreground='black',  # color de fondo
                                 rowheight=24,  # Altura de las filas
                                 fildbackground='white',
                                 font=('console', 15))  # tipo de letra
        estilo_reporte.map("Treeview", backgroud=[('selected', '#00FFFF')], foreground=[('selected', 'black')])

        # Configura el estilo del encabezado del Treeview
        estilo_reporte.configure("Treeview.Heading",
                                 background="#708090",  # Color de fondo
                                 foreground="black",  # Color del texto
                                 font=("console", 14, "bold"))  # Tipo de letra

        self.treeview_reporte = ttk.Treeview(self.frame_contabilidad)

        cursor.execute("SELECT * FROM reportes")
        datos_reporte = cursor.fetchall()

        for dato in datos_reporte:
            self.treeview_reporte.insert('', 0, values=dato)

        # creamos el scrollbar
        scrbar_reporte = ttk.Scrollbar(self.frame_contabilidad, orient='vertical', command=self.treeview_reporte.yview)
        scrbar_reporte.place(relx=0.974, rely=0.01, relwidth=0.02, relheight=0.490)

        # actualizar el contenido cuando se deslace la barra
        self.treeview_reporte.configure(yscrollcommand=scrbar_reporte.set)

        self.treeview_reporte['columns'] = ('ID REPORTE', 'Mes', 'Gastos', 'Total vendido', 'Ganancia mes',
                                            'Ganancia final', 'Fecha')

        self.treeview_reporte.column('#0', width=0, stretch=NO)
        self.treeview_reporte.column(column="ID REPORTE", anchor=CENTER, width=2)
        self.treeview_reporte.column(column="Mes", anchor=CENTER, width=2)
        self.treeview_reporte.column(column="Gastos", anchor=CENTER, width=2)
        self.treeview_reporte.column(column="Total vendido", anchor=CENTER, width=2)
        self.treeview_reporte.column(column="Ganancia mes", anchor=CENTER, width=2)
        self.treeview_reporte.column(column="Ganancia final", anchor=CENTER, width=2)
        self.treeview_reporte.column(column="Fecha", anchor=CENTER, width=2)

        self.treeview_reporte.heading('#0', text="", anchor=CENTER)
        self.treeview_reporte.heading("ID REPORTE", text="ID REPORTE", anchor=CENTER)
        self.treeview_reporte.heading("Mes", text="Mes", anchor=CENTER)
        self.treeview_reporte.heading("Gastos", text="Gastos", anchor=CENTER)
        self.treeview_reporte.heading("Total vendido", text="Total vendido", anchor=CENTER)
        self.treeview_reporte.heading("Ganancia mes", text="Ganancia mes", anchor=CENTER)
        self.treeview_reporte.heading("Ganancia final", text="Ganancia final", anchor=CENTER)
        self.treeview_reporte.heading("Fecha", text="Fecha", anchor=CENTER)

        # ubicamos la tabla
        self.treeview_reporte.place(x=5, y=5, width=968, height=245)

    # obtenems las filas de la tabla gastos
    def obtener_filas_gastos(self):

        self.filas_gastos = []
        for item_filas in self.treeview_gastos.get_children():
            fila = self.treeview_gastos.item(item_filas)["values"]
            self.filas_gastos.append(fila)

    # funcion para buscar en gastos
    def busqueda_gastos(self, *args):

        stringvar = self.busquedavar_gastos.get().lower()

        for item in self.treeview_gastos.get_children():
            fila = self.treeview_gastos.item(item)['values']
            if stringvar not in str(fila):
                self.treeview_gastos.delete(item)

        if stringvar:
            for i in self.filas_gastos:
                for palabra in i:
                    if stringvar in str(i):
                        self.treeview_gastos.insert(i)

        elif not stringvar:
            for i in self.treeview_gastos.get_children():
                self.treeview_gastos.delete(i)
            cursor.execute("SELECT * FROM gastos")
            datos = cursor.fetchall()
            for dato in datos:
                self.treeview_gastos.insert('', 0, values=dato)

    # esta es la funcion que tendra las operaciones para la tabla de reporte mensual
    def operacion_mes(self):

        # fecha de cuando se hace el reporte
        fecha = datetime.now(pytz.timezone('UTC'))
        fecha_local = fecha.astimezone(pytz.timezone('America/Bogota'))
        fecha_final = fecha_local.strftime('%Y-%m-%d %H:%M:%S')
        fecha_final2 = fecha_local.strftime('%Y-%m')

        # entrada de la fecha
        entrada_busqueda = self.entrada_busqueda_ventas.get()

        if entrada_busqueda:

            if len(entrada_busqueda) >= 8:
                messagebox.showinfo('ALERTA', 'PARA REPORTE MENSUAL INGRESAR SOLO AÑO Y MES')
            elif len(entrada_busqueda) > 0 and len(entrada_busqueda) <= 7:
                fecha_mes = datetime.strptime(entrada_busqueda, '%Y-%m')

                codigo = str(346643)

                clave = simpledialog.askstring(title='CODIGO DE SEGURIDAD',
                                               prompt='INGRESE EL CODIGO DE SEGURIDAD PARA HACER EL REPORTE')

                # esta variables es para poder usar el total de los gastos en cualquier lado
                tgasto2 = 0
                tgasto1 = 0

                if clave == codigo:

                    try:
                        # consulta de el total vendido
                        cursor.execute("SELECT SUM(CAST(REPLACE(total_vent, ',', '') AS INTEGER)) FROM ventas WHERE "
                                       "strftime('%Y-%m', fecha) =?", (entrada_busqueda,))
                        tvendido = cursor.fetchone()
                        tvendido1 = int(''.join(map(str, tvendido)))
                        tvendido2 = f'{tvendido1:,}'

                        # consulta de el total de los gastos
                        cursor.execute("SELECT SUM(CAST(REPLACE(Valor_gasto, ',', '') AS INTEGER)) FROM gastos WHERE "
                                       "strftime('%Y-%m', fecha) =?", (entrada_busqueda,))
                        tgasto = cursor.fetchone()
                        tgasto1 = int(''.join(map(str, tgasto)))
                        tgasto2 = f'{tgasto1:,}'

                        # consulta de el total de la ganancia de el mes
                        cursor.execute("SELECT SUM(CAST(REPLACE(ganancia, ',', '') AS INTEGER)) FROM VENTAS WHERE "
                                       "strftime('%Y-%m', fecha) =?", (entrada_busqueda,))
                        tganancia = cursor.fetchone()
                        tganancia1 = int(''.join(map(str, tganancia)))
                        tganancia2 = f'{tganancia1:,}'

                        ganancia_final = tganancia1 - tgasto1
                        ganancia_final1 = f'{ganancia_final:,}'
                    except ValueError:

                        # consulta de el total vendido
                        cursor.execute("SELECT SUM(CAST(REPLACE(total_vent, ',', '') AS INTEGER)) FROM ventas WHERE "
                                       "strftime('%Y-%m', fecha) =?", (entrada_busqueda,))
                        tvendido = cursor.fetchone()
                        tvendido1 = int(''.join(map(str, tvendido)))
                        tvendido2 = f'{tvendido1:,}'

                        # ponemos el valor de los gasts en o porque nos devolvio None
                        tgasto2 = 0

                        # consulta de el total de la ganancia de el mes
                        cursor.execute("SELECT SUM(CAST(REPLACE(ganancia, ',', '') AS INTEGER)) FROM VENTAS WHERE "
                                       "strftime('%Y-%m', fecha) =?", (entrada_busqueda,))
                        tganancia = cursor.fetchone()
                        tganancia1 = int(''.join(map(str, tganancia)))
                        tganancia2 = f'{tganancia1:,}'

                        ganancia_final = tganancia1 - tgasto1
                        ganancia_final1 = f'{ganancia_final:,}'

                    cursor.execute("SELECT Fecha_reporte FROM reportes")
                    reporte = cursor.fetchall()

                    try:
                        lista_fechas = []

                        for fecha_x in reporte:
                            lista_fechas.append(fecha_x[0][:7])
                        if fecha_final2 in lista_fechas:
                            messagebox.showinfo("ALERTA", "ESTE REPORTE YA SE REALIZO")

                        elif fecha_final2 not in lista_fechas:
                            # insertamos los valores en la tabla reporte
                            cursor.execute("INSERT INTO reportes (Mes, Gastos, Total_vendido, Ganancia_mes, "
                                           "Ganancia_final,"
                                           "Fecha_reporte) VALUES(?, ?, ?, ?, ?, ?)",
                                           (fecha_mes.strftime('%b'), tgasto2,
                                            tvendido2, tganancia2,
                                            ganancia_final1, fecha_final))
                            dato = cursor.lastrowid
                            if dato:
                                conexion.commit()
                                self.mensaje_temporal_venta(self.root, 'REPORTE GUARDADO', 2000)
                    except TypeError:
                        # insertamos los valores en la tabla reporte
                        cursor.execute("INSERT INTO reportes (Mes, Gastos, Total_vendido, Ganancia_mes, "
                                       "Ganancia_final,"
                                       "Fecha_reporte) VALUES(?, ?, ?, ?, ?, ?)",
                                       (fecha_mes.strftime('%b'), tgasto2,
                                        tvendido2, tganancia2,
                                        ganancia_final1, fecha_final))
                        dato = cursor.lastrowid
                        if dato:
                            conexion.commit()
                            self.mensaje_temporal_venta(self.root, 'REPORTE GUARDADO', 2000)
                elif clave != codigo:
                    messagebox.showinfo('ALERTA', 'CODIGO INCORRECTO')
        else:
            messagebox.showinfo('ALERTA', 'ESPACIO VACIO, INGRESE LA FECHA PARA EL REPORTE')

    # esta funcion hace el descuento de el stock segun lla cantidad que se venda
    def descontar_stock(self):

        try:
            # cargamos el texto de las entradas
            if self.entrada_cantidadvent and self.entrada_idproventas:
                cantidad = self.entrada_cantidadvent.get()

                id = self.entrada_idproventas.get()

                # hacemos la consulta para saber si el producto esta disponiblle y es mayor a cero
                cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
                numero = cursor.fetchone()

                # si la cantidad ingresaddaa es mayor que la cantidad disponible no se puede restar
                if numero[3] < int(cantidad):
                    messagebox.showinfo('ALERTA', 'CANTIDAD NO DISPONIBLE')
                    return False
                # si es menor nos da un mensaje
                if numero[3] == 0:
                    messagebox.showinfo('ALERTA', 'ESTE PRODUCTO NO ESTA DISPONIBLE')
                    return False
                # verificamos que la cantidad sea mayor a cero
                elif numero[3] > 0 or numero[3] > int(cantidad) or numero[3] == cantidad:

                    # hacemos la consulta para descontar las unidaddes vendidas
                    cursor.execute("UPDATE productos SET Unidades = Unidades -? WHERE id =?", (cantidad, id,))
                    dato = cursor.fetchone()
                    return True
                conexion.commit()

        except (TypeError, ValueError):
            messagebox.showinfo('ALERTA', 'ESPACIOS VACIOS')

    # grafica de la ventana que se mostrara para el reporte de el dia
    def reporte_dia(self):

        if len(self.entrada_busqueda_ventas.get()) == 10:

            dia = Tk()
            dia.title('REPORTE DIA')
            dia.geometry('235x235+630+200')
            dia.minsize(235, 235)
            dia.maxsize(235, 235)

            frame = Frame(dia, bg='#458B74', relief=GROOVE, bd=3)
            frame.place(x=5, y=5, width=225, height=227)

            label_fecha = Label(frame, bg='#458B74', text='Fecha:', font="'consle', 11", fg='black')
            label_fecha.place(x=5, y=10)

            label_venta_dia = Label(frame, bg='#458B74', text='Venta dia:', font="'consle', 13", fg='black')
            label_venta_dia.place(x=5, y=60)

            label_gastos = Label(frame, bg='#458B74', text='Gastos dia:', font="'consle', 13", fg='black')
            label_gastos.place(x=5, y=90)

            label_ganancia_dia = Label(frame, bg='#458B74', text='Ganancia dia:', font="'consle', 13", fg='black')
            label_ganancia_dia.place(x=5, y=120)

            label_ganancia_final = Label(frame, bg='#458B74', text='Ganancia final:', font="'consle', 13",
                                         fg='black')
            label_ganancia_final.place(x=5, y=180)

            # aqui estaran los labels donde estaran los resultados
            self.igual_fecha = Label(frame, bg='#458B74', text='2023-10-10 02:30:50', font="'consle', 11",
                                     fg='black')
            self.igual_fecha.place(x=75, y=10)

            self.label_venta_dia = Label(frame, bg='#458B74', text='0', font="'consle', 12", fg='black')
            self.label_venta_dia.place(x=120, y=60)

            self.label_gastos = Label(frame, bg='#458B74', text='', font="'consle', 12", fg='black')
            self.label_gastos.place(x=120, y=90)

            self.label_ganancia_dia = Label(frame, bg='#458B74', text='', font="'consle', 12", fg='black')
            self.label_ganancia_dia.place(x=120, y=120)

            self.label_ganancia_final = Label(frame, bg='#458B74', text='', font="'consle', 12", fg='black')
            self.label_ganancia_final.place(x=120, y=180)

            self.operaciones_dia()

            dia.mainloop()
        else:
            messagebox.showinfo('ALERTA', 'PARA REPORTE DEL DIA INGRESAR SOLO AÑO/MES/DIA (AAAA-MM-DD)222')

    # funcion para hacer la operacion reporte de el dia
    def operaciones_dia(self):

        # obtenemos la entrada de la fecha para hacer las consultas
        fecha_dia = self.entrada_busqueda_ventas.get()

        # fecha de cuando se hace el reporte
        fecha = datetime.now(pytz.timezone('UTC'))  # America/Bogota
        fecha_local = fecha.astimezone(pytz.timezone('America/Bogota'))
        fecha_final = fecha_local.strftime('%Y-%m-%d %H:%M:%S')
        self.igual_fecha.config(text=fecha_final)

        # hacemos la consulta para sacar los valores
        if fecha_dia:

            # verificamos que se haya escrito algo
            if len(fecha_dia) > 0 and len(fecha_dia) < 11:

                # consulta para el total vendido del dia
                cursor.execute("SELECT SUM(CAST(REPLACE(total_vent, ',', '') AS INTEGER)) FROM ventas WHERE "
                               "strftime('%Y-%m-%d', fecha) =?", (fecha_dia,))

                # obtenemos lo que nos da la consulta para pasarlo a cadena
                # y luego a entero y luego ponerlo con comas
                venta_dia = cursor.fetchone()

                # consulta para los gastos
                cursor.execute("SELECT SUM(CAST(REPLACE(Valor_gasto, ',', '') AS INTEGER)) FROM gastos WHERE "
                               "strftime('%Y-%m-%d', Fecha) =?", (fecha_dia,))
                gasto = cursor.fetchone()

                # consulta para la ganancia del dia
                cursor.execute("SELECT SUM(CAST(REPLACE(ganancia, ',', '') AS INTEGER)) FROM ventas WHERE "
                               "strftime('%Y-%m-%d', fecha) =?", (fecha_dia,))
                ganancia_dia = cursor.fetchone()

                try:

                    if venta_dia is not None and gasto is not None and ganancia_dia is not None:

                        # aqui insertamos los valores en la venta de el dia
                        venta_str = int(''.join(map(str, venta_dia)))
                        venta_int = f'{venta_str:,}'
                        self.label_venta_dia.config(text=venta_int)

                        # aqui insertamos los valores en los gastos
                        gasto_entero = int(''.join(map(str, gasto)))
                        gasto_final = f'{gasto_entero:,}'
                        self.label_gastos.config(text=gasto_final)

                        # aqui insetamos las ganancias de el dia
                        gananica_entero = int(''.join(map(str, ganancia_dia)))
                        gananica_total = f'{gananica_entero:,}'
                        self.label_ganancia_dia.config(text=gananica_total)

                        # operacion para la gananica final
                        ganancia_final = gananica_entero - gasto_entero
                        ganancia_final_decimal = f'{ganancia_final:,}'
                        self.label_ganancia_final.config(text=ganancia_final_decimal)

                # con el error podemos manejar cuando un valor de la consulta esta en None
                except ValueError:

                    # insertamos en el label de las ventas
                    venta_str = int(''.join(map(str, venta_dia)))
                    venta_int = f'{venta_str:,}'
                    self.label_venta_dia.config(text=venta_int)

                    # el label de gastos lo dejamos en cero
                    self.label_gastos.config(text='0')

                    # insertamos en el lavel
                    gananica_entero = int(''.join(map(str, ganancia_dia)))
                    gananica_total = f'{gananica_entero:,}'
                    self.label_ganancia_dia.config(text=gananica_total)

                    # y hacemos la operacion para la gananica final
                    ganancia_final = gananica_entero - 0
                    ganancia_final_decimal = f'{ganancia_final:,}'
                    self.label_ganancia_final.config(text=ganancia_final_decimal)

        else:
            pass
