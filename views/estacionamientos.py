import customtkinter as ctk
from utils.helpers import limpiar_ventana
import utils.entidades as entidades
from views.clientes import Buscar
from DataBase.estacionamiento_bd import estacionamiento_bd

# PopUp para mostrar mensajes de aviso al usuario
def MostrarPopUp(titulo, mensaje):
    popup = ctk.CTkToplevel()
    popup.title(titulo)
    popup.geometry("350x150")
    popup.grab_set() 
    popup.attributes("-topmost", True)
    etiqueta = ctk.CTkLabel(popup, text=mensaje, font=("Roboto", 16, "bold"))
    etiqueta.pack(pady=(30, 20))
    boton_aceptar = ctk.CTkButton(popup, text="Aceptar", command=popup.destroy)
    boton_aceptar.pack()

def LimpiarDatos(entry_id, entries, txt_direccion):
    if entry_id:
        entry_id.delete(0, "end")
    for entry in entries:
        entry.delete(0, "end")
    txt_direccion.delete("1.0", "end")

def Cancelar(btn_guardar, btn_eliminar, btn_editar, btn_nuevo, entry_id, entries, txt_direccion):
    global edi_nuevo
    btn_eliminar.configure(state="normal")
    btn_editar.configure(state="normal")
    btn_nuevo.configure(state="normal")
    btn_guardar.configure(state="disabled")
    LimpiarDatos(entry_id, entries, txt_direccion)
    edi_nuevo = None

def Nuevo(btn_guardar, btn_eliminar, btn_editar, entry_id, entries, txt_direccion):
    global edi_nuevo
    btn_eliminar.configure(state="disabled")
    btn_editar.configure(state="disabled")
    LimpiarDatos(entry_id, entries, txt_direccion)
    btn_guardar.configure(state="normal")
    edi_nuevo = False

def Editar(btn_eliminar, btn_nuevo, btn_guardar, entries):
    global edi_nuevo
    if not entries[0].get().strip():
        MostrarPopUp("Atención", "Primero busca un estacionamiento para editarlo")
        return
    edi_nuevo = True
    btn_eliminar.configure(state="disabled")
    btn_nuevo.configure(state="disabled")
    btn_guardar.configure(state="normal")

def Guardar(entry_id, entries, txt_direccion, btn_guardar, btn_eliminar, btn_editar, btn_nuevo):
    global edi_nuevo
    for entry in entries:
        if not entry.get().strip():
            MostrarPopUp("Atención", "Todos los campos son obligatorios.")
            return
    estacionamiento = entidades.Estacionamiento()
    db = estacionamiento_bd()
    estacionamiento.set_nombre(entries[0].get().strip())
    estacionamiento.set_cantidad_cajones(int(entries[1].get().strip()))
    estacionamiento.set_direccion(txt_direccion.get("1.0", "end").strip())
    if edi_nuevo == True: #Editar un estacionamiento
        estacionamiento.set_estacionamiento_id(int(entry_id.get().strip()))
        db.Editar(estacionamiento)
        MostrarPopUp("Éxito", "Estacionamiento editado correctamente.")
    elif edi_nuevo == False: #Guardar un nuevo estacionamiento      
        db.Guardar(estacionamiento)
        MostrarPopUp("Éxito", "Estacionamiento guardado correctamente.")
    Cancelar(btn_guardar, btn_eliminar, btn_editar, btn_nuevo, entry_id, entries, txt_direccion)

def Borrar(entry_id, entries, txt_direccion):
    if not entry_id.get().strip():
        MostrarPopUp("Atención", "Primero busca un estacionamiento para borrarlo")
        return    
    db = estacionamiento_bd()
    estacionamiento = entidades.Estacionamiento()
    estacionamiento.set_estacionamiento_id(int(entry_id.get()))
    db.Borrar(estacionamiento)
    
    MostrarPopUp("Éxito", "Estacionamiento borrado exitosamente.")
    LimpiarDatos(entry_id, entries, txt_direccion)

def Buscar(entry_id, entries, txt_direccion):
    global edi_nuevo
    id = entry_id.get().strip()
    if not id.isdigit():
        MostrarPopUp("Atención", "Ingresa un ID para buscar un estacionamiento")
        return
    estacionamiento = entidades.Estacionamiento()
    estacionamiento.set_estacionamiento_id(int(id))
    db = estacionamiento_bd()
    estacionamiento = db.Buscar(estacionamiento)
    edi_nuevo = None
    if estacionamiento:
        LimpiarDatos(None, entries, txt_direccion)
        entries[0].insert(0, estacionamiento.get_nombre())
        entries[1].insert(0, str(estacionamiento.get_cantidad_cajones()))
        txt_direccion.insert("1.0", estacionamiento.get_direccion())
    else:
        MostrarPopUp("Atención", "Estacionamiento no encontrado")


def pantalla_registro_estacionamientos(ventana):
    global edi_nuevo
    edi_nuevo = None
    limpiar_ventana(ventana)
    
    # Configuración de Grid Principal
    ventana.grid_rowconfigure(0, weight=1) # Titulo
    ventana.grid_rowconfigure(1, weight=3) # Formulario
    ventana.grid_rowconfigure(2, weight=1) # Botones
    ventana.grid_columnconfigure(0, weight=1)

    # --- Título ---
    ctk.CTkLabel(ventana, text="Registro de Estacionamientos", font=("Arial", 26, "bold")).grid(row=0, column=0, pady=20)
    
    # --- Frame Central (Formulario) ---
    frame_form = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_form.grid(row=1, column=0, sticky="nsew", padx=40)
    frame_form.grid_columnconfigure(1, weight=1)

    # ID y Búsqueda
    lbl_id = ctk.CTkLabel(frame_form, text="ID Estacionamiento:", font=("Arial", 13, "bold"))
    lbl_id.grid(row=0, column=0, sticky="e", padx=10, pady=10)
    
    frame_search = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_search.grid(row=0, column=1, sticky="w")
    
    entry_id = ctk.CTkEntry(frame_search, width=120)
    entry_id.pack(side="left", padx=(0, 10))
    
    btn_buscar = ctk.CTkButton(frame_search, text="Buscar", width=100, command=lambda: Buscar(entry_id, entries, txt_direccion))
    btn_buscar.pack(side="left")

    # Campos de tabla
    ctk.CTkLabel(frame_form, text="Nombre del Local:", font=("Arial", 13, "bold")).grid(row=1, column=0, sticky="e", padx=10, pady=10)
    entry_nombre = ctk.CTkEntry(frame_form, width=350, placeholder_text="Ej. Sucursal Centro")
    entry_nombre.grid(row=1, column=1, sticky="w", padx=10)

    ctk.CTkLabel(frame_form, text="Capacidad (Cajones):", font=("Arial", 13, "bold")).grid(row=2, column=0, sticky="e", padx=10, pady=10)
    entry_capacidad = ctk.CTkEntry(frame_form, width=120, placeholder_text="Ej. 50")
    entry_capacidad.grid(row=2, column=1, sticky="w", padx=10)

    ctk.CTkLabel(frame_form, text="Dirección Completa:", font=("Arial", 13, "bold")).grid(row=3, column=0, sticky="ne", padx=10, pady=10)
    txt_direccion = ctk.CTkTextbox(frame_form, width=350, height=80)
    txt_direccion.grid(row=3, column=1, sticky="w", padx=10, pady=10)

    entries = [entry_nombre, entry_capacidad] #Para facilitar el paso de parámetros

    # --- Botones inferiores ---
    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.grid(row=2, column=0, sticky="ew", padx=40, pady=20)

    btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", width=120, state="disabled", fg_color="#28a745", hover_color="#218838")

    # Botones agrupados a la izquierda
    btn_eliminar = ctk.CTkButton(frame_botones, text="Borrar", width=90, fg_color="#dc3545", hover_color="#c82333",
                                 command=lambda: Borrar(entry_id, entries, txt_direccion))
    btn_eliminar.pack(side="left", padx=5)

    btn_editar = ctk.CTkButton(frame_botones, text="Editar", width=90,
                               command=lambda: Editar(btn_eliminar, btn_nuevo, btn_guardar, entries))
    btn_editar.pack(side="left", padx=5)

    btn_nuevo = ctk.CTkButton(frame_botones, text="Nuevo", width=90,
                              command=lambda: Nuevo(btn_guardar, btn_eliminar, btn_editar, entry_id, entries, txt_direccion))
    btn_nuevo.pack(side="left", padx=5)

    # Botones agrupados a la derecha
    btn_guardar.configure(command=lambda: Guardar(entry_id, entries, txt_direccion, btn_guardar, btn_eliminar, btn_editar, btn_nuevo))
    btn_guardar.pack(side="right", padx=5)

    btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", width=120,
                                 command=lambda: Cancelar(btn_guardar, btn_eliminar, btn_editar, btn_nuevo, entry_id, entries, txt_direccion))
    btn_cancelar.pack(side="right", padx=5)
