import customtkinter as ctk
import myCustomTkinter as mctk
import utils.entidades as entidades
from DataBase.usuario_bd import usuario_bd
from utils.helpers import limpiar_ventana
from views.servicios import pantalla_servicios

# Definición de variables globales
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
    
    # Truco UI: Quitamos el foco a los inputs para evitar el TclError al destruirlos
    app.focus_set() 
    
    if resultado:
        id_usuario_logueado, perfil = resultado
        mostrar_popup(nombre_usuario, True, app)
    else:
        mostrar_popup(None, False, app)
    
def mostrar_popup(nombre_usuario, ingresado, app):
    if ingresado:
        mensaje = f"Sesión iniciada: {nombre_usuario}"
    else:
        mensaje = "No se pudo autenticar este usuario"
        
    popup = ctk.CTkToplevel()
    popup.title("Estado de Login")
    popup.geometry("350x150")
    popup.grab_set()
    popup.attributes("-topmost", True)
    
    ctk.CTkLabel(popup, text=mensaje, font=("Roboto", 16, "bold")).pack(pady=(30, 20))
    
    def cerrar_y_continuar(event=None):
        popup.destroy()
        if ingresado:
            app.login_exitoso(id_usuario_logueado, perfil)
            # =========================================================
            # CORRECCIÓN VITAL: Pasamos app.scaner en lugar de None
            # =========================================================
            pantalla_servicios(app.contenedor, app.scaner)

    boton_aceptar = ctk.CTkButton(popup, text="Aceptar", command=cerrar_y_continuar)
    boton_aceptar.pack()
    
    # Permitir que el PopUp se cierre con Enter
    popup.bind("<Return>", cerrar_y_continuar)

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
        height=320
    )

    frame_form.pack(pady=20, padx=60)
    frame_form.pack_propagate(False)

    ctk.CTkLabel(
        frame_form,
        text="Usuario:",
        font=("Arial", 14)
    ).pack(pady=(30, 5))

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
    ).pack(pady=(20, 5))

    entry_password = mctk.PasswordEntry(
        frame_form,
        placeholder_text="********",
        width=250
    )
    entry_password.pack(pady=5)

    def ejecutar_login(event=None):
        revisar_credenciales(entry_usuario, entry_password, app)
        return 'break' # Detiene la propagación del evento en Tkinter para evitar el TclError

    btn_login = ctk.CTkButton(
        frame_form,
        text="Ingresar",
        width=200,
        command=ejecutar_login
    )
    btn_login.pack(pady=(30, 10))

    # Enlazar la tecla Enter a las cajas de texto
    entry_usuario.bind("<Return>", ejecutar_login)
    entry_password.entry.bind("<Return>", ejecutar_login)