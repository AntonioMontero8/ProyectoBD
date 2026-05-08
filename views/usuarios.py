import customtkinter as ctk
from CTkTable import CTkTable

from utils.helpers import limpiar_ventana

def pantalla_usuarios(ventana):
    try:
        limpiar_ventana(ventana)
    except:
        pass

    # ---------------- CONFIG GRID PRINCIPAL ----------------
    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_rowconfigure(1, weight=0)
    ventana.grid_rowconfigure(2, weight=3)
    ventana.grid_rowconfigure(3, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    # ---------------- CONTENEDOR SUPERIOR ----------------
    frame_top = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_top.grid(row=0, column=0,sticky="ns")

    frame_top.grid_columnconfigure((0, 1, 2), weight=1)

    # Título
    titulo = ctk.CTkLabel(
        frame_top,
        text="usuarios",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.grid(row=0, column=0, columnspan=3, pady=(10, 15),sticky="n")

    # Búsqueda
    lbl_buscar = ctk.CTkLabel(frame_top, text="Id:")
    lbl_buscar.grid(row=1, column=0, sticky="e", padx=5)

    entry_buscar = ctk.CTkEntry(frame_top, width=200)
    entry_buscar.grid(row=1, column=1, padx=5)

    btn_buscar = ctk.CTkButton(frame_top, text="buscar", width=100)
    btn_buscar.grid(row=1, column=2, padx=5)

    # ---------------- FORMULARIO CENTRAL ----------------
    frame_form = ctk.CTkFrame(ventana)
    frame_form.grid(row=2, column=0)

    for i in range(5):
        frame_form.grid_rowconfigure(i, weight=1)
    frame_form.grid_columnconfigure(1, weight=1)

    campos = ["Nombre:", "Email:", "Usuario:", "contraseña:", "perfil:"]

    entries = []

    for i, texto in enumerate(campos):
        lbl = ctk.CTkLabel(frame_form, text=texto)
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        entry = ctk.CTkEntry(frame_form, width=250)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    # Botones del formulario
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.grid(row=5, column=0, columnspan=2, pady=15)

    btn_eliminar = ctk.CTkButton(frame_botones, text="eliminar", width=100)
    btn_eliminar.pack(side="left", padx=10)

    btn_editar = ctk.CTkButton(frame_botones, text="editar", width=100)
    btn_editar.pack(side="left", padx=10)

    btn_nuevo = ctk.CTkButton(frame_botones, text="nuevo", width=100)
    btn_nuevo.pack(side="left", padx=10)

    # ---------------- BOTONES INFERIORES ----------------
    frame_bottom = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_bottom.grid(row=3, column=0, sticky="se", padx=20, pady=20)

    btn_cancelar = ctk.CTkButton(frame_bottom, text="cancelar", width=120)
    btn_cancelar.pack(side="left", padx=10)

    btn_guardar = ctk.CTkButton(frame_bottom, text="guardar", width=120)
    btn_guardar.pack(side="left", padx=10)
