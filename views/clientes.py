import customtkinter as ctk
from CTkTable import CTkTable
import utils.entidades as entidades
from DataBase.cliente_bd import cliente_bd
from DataBase.vehiculos_bd import vehiculos_bd
from utils.helpers import limpiar_ventana


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

def LimpiarDatos(entry_id, entries, tabla):
    if entry_id:
        entry_id.delete(0, "end")
    else:
        pass

    for entry in entries:
        entry.delete(0, "end")

    datos_vacios = [["Matricula", "Marca", "Modelo", "Color"]] + [["", "", "", ""] for _ in range(5)]
    tabla.update_values(datos_vacios)
    
# Limpia todos los campos y regresa los botones a "Habilitados"
def Cancelar(boton_guardar ,boton_eliminar, boton_editar, boton_nuevo, entry_id, entries, tabla):
    global edi_nuevo
    boton_eliminar.configure(state="normal")
    boton_editar.configure(state="normal")
    boton_nuevo.configure(state="normal")
    boton_guardar.configure(state="disabled")
    LimpiarDatos(entry_id, entries, tabla)
    edi_nuevo = None

def Buscar(entry_id, entries, tabla):
    global edi_nuevo
    id = entry_id.get().strip()
    if not id.isdigit():
        MostrarPopUp("Error", "Porfavor ingresa un ID valido")
        return
    cliente = entidades.Cliente()
    cliente.set_cliente_id(int(id))
    db = cliente_bd()
    cliente = db.Buscar(cliente)
    edi_nuevo = None # Resetear estado al buscar uno nuevo
    if cliente:
        print(f"Cliente obtenido: {cliente.get_nombre()}")  # Debug
        # -- Limpieza de campos --
        LimpiarDatos(None, entries, tabla)
        
        # -- Impresion del cliente --
        entries[0].insert(0, cliente.get_nombre())
        entries[1].insert(0, cliente.get_telefono())
        entries[2].insert(0, cliente.get_email())
        entries[3].insert(0, cliente.get_rfc())
        entries[4].insert(0, cliente.get_CP_domicilio_fiscal())
        entries[5].insert(0, cliente.get_regimen_fiscal())
        
        # -- Cargar vehículos asociados --
        db_v = vehiculos_bd()
        coches = db_v.BuscarPorCliente(cliente)
        
        header = ["Matricula", "Marca", "Modelo", "Color"]
        filas_vehiculos = []
        for v in coches:
            filas_vehiculos.append([v.get_matricula(), v.get_marca(), v.get_modelo(), v.get_color()])
        
        # Mantenemos un mínimo de 5 filas por estética, la tabla se expandirá automáticamente si hay más
        while len(filas_vehiculos) < 5:
            filas_vehiculos.append(["", "", "", ""])
            
        tabla.update_values([header] + filas_vehiculos)
    else:
        MostrarPopUp("Error", "Cliente no encontrado")
        
#Deshabilita los botones de eliminar y editar para evitar problemaas
#También limpia los campos del formulario y la tabla
def NuevoCliente(btn_guardar ,btn_eliminar, btn_editar, entry_id, entries, tabla):
    global edi_nuevo
    btn_eliminar.configure(state="disabled")
    btn_editar.configure(state="disabled")
    entry_id.delete(0, "end")
    LimpiarDatos(entry_id, entries, tabla)
    btn_guardar.configure(state="normal")
    edi_nuevo = False
    
    
def Guardar(entry_id, entries, tabla, btn_guardar, btn_eliminar, btn_editar, btn_nuevo):
    global edi_nuevo
    # Verificar que todos los campos tengan información
    for entry in entries:
        if not entry.get().strip():
            MostrarPopUp("Atención", "Todos los campos del formulario son obligatorios.")
            return

    cliente = entidades.Cliente()
    db = cliente_bd()
    cliente.set_nombre(entries[0].get())
    cliente.set_telefono(entries[1].get())
    cliente.set_email(entries[2].get())
    cliente.set_rfc(entries[3].get())
    cliente.set_CP_domicilio_fiscal(entries[4].get())
    cliente.set_regimen_fiscal(entries[5].get())

    if edi_nuevo == True: #Si es para editar un cliente
        cliente.set_cliente_id(int(entry_id.get()))
        db.Editar(cliente)
        MostrarPopUp("Éxito", "Cliente editado exitosamente.")
    elif edi_nuevo == False: #Si es para guardar un nuevo cliente
        db.Guardar(cliente)
        MostrarPopUp("Éxito", "Cliente guardado exitosamente.")

    # Restaurar interfaz
    LimpiarDatos(entry_id, entries, tabla)
    btn_guardar.configure(state="disabled")
    btn_eliminar.configure(state="normal")
    btn_editar.configure(state="normal")
    btn_nuevo.configure(state="normal")
    edi_nuevo = None

#Borra un cliente luego de buscarlo
def Borrar(entry_id, entries, tabla):
    for entry in entries:
            if not entry.get().strip():
                MostrarPopUp("Atención", "Primero busca un cliente para borrarlo")
                return
    db = cliente_bd()
    cliente = entidades.Cliente()
    cliente.set_cliente_id(int(entry_id.get()))
    db.Borrar(cliente)
    MostrarPopUp("Éxito", "Cliente borrado exitosamente.")
    LimpiarDatos(entry_id, entries, tabla)

#Habilita la edicion de un cliente luego de buscarlo
def Editar(boton_eliminar, boton_nuevo, boton_guardar, entries):
    global edi_nuevo
    for entry in entries:
            if not entry.get().strip():
                MostrarPopUp("Atención", "Primero busca un cliente para editarlo")
                return
    edi_nuevo = True
    boton_eliminar.configure(state="disabled")
    boton_nuevo.configure(state="disabled")
    boton_guardar.configure(state="normal")


def pantalla_clientes(ventana):
    global edi_nuevo
    edi_nuevo = None #Boton para comprobar si al dar click en guardar aplicará para un nuevo cliente o para editar un cliente (True = Editar, False = Nuevo)
    try:
        limpiar_ventana(ventana)
    except:
        pass

    # ---------------- GRID PRINCIPAL ----------------
    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_rowconfigure(1, weight=0)
    ventana.grid_rowconfigure(2, weight=3)
    ventana.grid_rowconfigure(3, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    # ---------------- TOP (TITULO + BUSQUEDA) ----------------
    frame_top = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_top.grid(row=0, column=0,sticky="ns")

    frame_top.grid_columnconfigure((0,1,2), weight=1)

    titulo = ctk.CTkLabel(
        frame_top,
        text="Clientes",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.grid(row=0, column=0, columnspan=3, pady=(10, 15), sticky="n")

    lbl_id = ctk.CTkLabel(frame_top, text="Id:")
    lbl_id.grid(row=1, column=0, sticky="e", padx=5)

    entry_id = ctk.CTkEntry(frame_top, width=200)
    entry_id.grid(row=1, column=1, padx=5)

    btn_buscar = ctk.CTkButton(frame_top, text="Buscar", width=100, command = lambda: Buscar(entry_id, entries, tabla))
    btn_buscar.grid(row=1, column=2, padx=5)

    # ---------------- BLOQUE CENTRAL (FORM + TABLA) ----------------
    frame_centro = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_centro.grid(row=2, column=0)

    frame_centro.grid_columnconfigure(0, weight=1)
    frame_centro.grid_columnconfigure(1, weight=1)

    # -------- FORMULARIO --------
    frame_form = ctk.CTkFrame(frame_centro)
    frame_form.grid(row=0, column=0, padx=20, pady=10)

    campos = [
        "Nombre:",
        "Teléfono:",
        "Email:",
        "RFC:",
        "CP domicilio fiscal:",
        "Régimen fiscal:"
    ]

    for i in range(len(campos)):
        frame_form.grid_rowconfigure(i, weight=1)

    frame_form.grid_columnconfigure(1, weight=1)

    entries = []

    for i, texto in enumerate(campos):
        lbl = ctk.CTkLabel(frame_form, text=texto)
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        entry = ctk.CTkEntry(frame_form, width=250)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    # Botones del formulario
    frame_btn_form = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_btn_form.grid(row=len(campos), column=0, columnspan=2, pady=15)

    # --- Boton eliminar cliente ---
    boton_eliminar = ctk.CTkButton(frame_btn_form, text="Eliminar", width=80, command = lambda: Borrar(entry_id, entries, tabla))
    boton_eliminar.pack(side="left", padx=10)
    
    # --- Boton editar cliente ----
    boton_editar = ctk.CTkButton(frame_btn_form, text="Editar", width=80, command = lambda: Editar(boton_eliminar, boton_nuevo, boton_guardar, entries))
    boton_editar.pack(side="left", padx=10)
    
    # --- Boton nuevo cliente ---
    boton_nuevo = ctk.CTkButton(frame_btn_form, text="Nuevo", width=80,
                  command=lambda: NuevoCliente(boton_guardar, boton_eliminar, boton_editar, entry_id, entries, tabla)
                  )
    boton_nuevo.pack(side="left", padx=10)

    # -------- TABLA VEHICULOS --------
    frame_tabla = ctk.CTkFrame(frame_centro)
    frame_tabla.grid(row=0, column=1, padx=20, pady=10, sticky="n")

    lbl_tabla = ctk.CTkLabel(frame_tabla, text="Vehículos")
    lbl_tabla.pack(anchor="w", padx=10, pady=(5, 0))

    datos_tabla = [
        ["Matricula", "Marca", "Modelo", "Color"]
    ] + [["", "", "", ""] for _ in range(5)]

    tabla = CTkTable(
        master=frame_tabla,
        values=datos_tabla
    )
    tabla.pack(padx=10, pady=10)

    # ---------------- BOTONES INFERIORES ----------------
    frame_bottom = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_bottom.grid(row=3, column=0, sticky="se", padx=20, pady=20)

    # Definimos el botón primero para que la referencia exista al crear el botón de Cancelar
    boton_guardar = ctk.CTkButton(frame_bottom, text="Guardar", width=120, state="disabled", command=lambda: Guardar(entry_id, entries, tabla, boton_guardar, boton_eliminar, boton_editar, boton_nuevo))

    ctk.CTkButton(frame_bottom, text="Cancelar", width=120, 
                  command=lambda: Cancelar(boton_guardar ,boton_eliminar, boton_editar, boton_nuevo, entry_id, entries, tabla)
                  ).pack(side="left", padx=10)

    boton_guardar.pack(side="left", padx=10)