import customtkinter as ctk
from utils.helpers import limpiar_ventana

def pantalla_registro_estacionamientos(ventana):
    limpiar_ventana(ventana)
    
    ctk.CTkLabel(ventana, text="Configuración de Estacionamiento", font=("Arial", 24, "bold")).pack(pady=20)
    
    frame_form = ctk.CTkFrame(ventana)
    frame_form.pack(pady=10, padx=20, fill="both", expand=True)

    # Nombre del Local
    ctk.CTkLabel(frame_form, text="Nombre del Local:", font=("Arial", 13, "bold")).pack(pady=(20, 5))
    ctk.CTkEntry(frame_form, width=400, placeholder_text="Ej. Estacionamiento Central").pack(pady=5)

    # Cantidad de Cajones (Campo nuevo)
    ctk.CTkLabel(frame_form, text="Capacidad Total (Cajones):", font=("Arial", 13, "bold")).pack(pady=(15, 5))
    # Usamos un Entry pero podrías validar que solo acepte números después
    ctk.CTkEntry(frame_form, width=150, placeholder_text="Ej. 50").pack(pady=5)

    # Dirección
    ctk.CTkLabel(frame_form, text="Dirección Completa:", font=("Arial", 13, "bold")).pack(pady=(15, 5))
    ctk.CTkTextbox(frame_form, width=400, height=80).pack(pady=5)

    # Botón de Acción
    ctk.CTkButton(ventana, text="Actualizar Datos de Sucursal", 
                  fg_color="#5cb85c", 
                  hover_color="#4cae4c",
                  font=("Arial", 14, "bold"),
                  height=40).pack(pady=30)

def pantalla_login(ventana):
    limpiar_ventana(ventana)
    
    ctk.CTkLabel(ventana, text="Acceso al Sistema", font=("Arial", 28, "bold")).pack(pady=(50, 20))
    
    frame_form = ctk.CTkFrame(ventana, width=400, height=300)
    frame_form.pack(pady=20, padx=60)
    frame_form.pack_propagate(False)
    
    ctk.CTkLabel(frame_form, text="Usuario:", font=("Arial", 14)).pack(pady=(30, 5))
    ctk.CTkEntry(frame_form, placeholder_text="Admin / Cobrador", width=250).pack(pady=5)
    
    ctk.CTkLabel(frame_form, text="Contraseña:", font=("Arial", 14)).pack(pady=(15, 5))
    #ctk.CTkEntry(frame_form, placeholder_text="********", show="*", width=250).pack(pady=5)
    mctk.PasswordEntry(frame_form, placeholder_text="********", width=250).pack(pady=5)
    
    ctk.CTkButton(frame_form, text="Iniciar Sesión", width=200, fg_color="#1f6aa5").pack(pady=30)
