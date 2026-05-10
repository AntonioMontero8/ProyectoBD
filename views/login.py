import customtkinter as ctk
import myCustomTkinter as mctk
import utils.entidades as entidades
from DataBase.usuario_bd import usuario_bd
from utils.helpers import limpiar_ventana
from views.servicios import pantalla_servicios

# Definición de variables globales para evitar advertencias de alcance (scope)
id_usuario_logueado = None
perfil = None

def revisar_credenciales(entry_u, entry_p, app):
    global id_usuario_logueado, perfil
    nombre_usuario = entry_u.get()
    password = entry_p.get()
    usuario = entidades.Usuario()
    usuario.set_username(nombre_usuario)
    usuario.set_password(password)
    db = usuario_bd()
    resultado = db.HacerLogin(usuario)
    if resultado:
        id_usuario_logueado, perfil = resultado
        mostrar_popup(nombre_usuario, True, app)
        print(f"Intento de login - ID_Usuario: {id_usuario_logueado}, Perfil: {perfil}, Usuario: {nombre_usuario}, Password: {password}")
    else:
        mostrar_popup(None, False, app)
    
def mostrar_popup(nombre_usuario, ingresado, app):
    if ingresado:
        mensaje = f"Sesión iniciada: {nombre_usuario}"
    else:
        mensaje = "No se pudo autenticar este usuario"
    popup = ctk.CTkToplevel()
    popup.title("Inicio de Sesión")

    popup.geometry("350x150")

    popup.grab_set() #No puede interactuar con el fondo  hasta cerrar el pop-up
    popup.attributes("-topmost", True)

    etiqueta = ctk.CTkLabel(popup, text=mensaje, font=("Roboto", 16, "bold"))
    etiqueta.pack(pady=(30, 20))

    if ingresado:
        # Si el login fue exitoso, configurar el menú lateral
        app.login_exitoso(id_usuario_logueado, perfil)
        # Cargar la pantalla principal (por ejemplo, servicios)
        pantalla_servicios(app.contenedor, None)

    boton_aceptar = ctk.CTkButton(popup, text="Aceptar", command=popup.destroy)
    boton_aceptar.pack()    
    

def pantalla_login(ventana, app):

    limpiar_ventana(ventana)

    ctk.CTkLabel(
        ventana,
        text="Acceso al Sistema",
        font=("Arial", 28, "bold")
    ).pack(pady=(50, 20))

    frame_form = ctk.CTkFrame(
        ventana,
        width=400,
        height=300
    )

    frame_form.pack(pady=20, padx=60)
    frame_form.pack_propagate(False)

    ctk.CTkLabel(
        frame_form,
        text="Usuario:",
        font=("Arial", 14)
    ).pack(pady=(30, 5))

    # Asignamos el Entry a una variable
    entry_usuario = ctk.CTkEntry(
        frame_form,
        placeholder_text="Admin / Cobrador",
        width=250
    )
    entry_usuario.pack(pady=5)

    ctk.CTkLabel(
        frame_form,
        text="Contraseña:",
        font=("Arial", 14)
    ).pack(pady=(15, 5))

    entry_password = mctk.PasswordEntry(
        frame_form,
        placeholder_text="********",
        width=250
    )
    entry_password.pack(pady=5)

    ctk.CTkButton(
        frame_form,
        text="Iniciar Sesión",
        width=200,
        command=lambda: revisar_credenciales(entry_usuario, entry_password, app)
    ).pack(pady=30)
