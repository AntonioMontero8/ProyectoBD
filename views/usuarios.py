import customtkinter as ctk
from DataBase.usuario_bd import usuario_bd
import utils.entidades as entidades
from utils.helpers import limpiar_ventana


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


def LimpiarDatos(entry_buscar, entries):
    if entry_buscar:
        entry_buscar.delete(0, "end")

    for entry in entries:
        if isinstance(entry, ctk.CTkComboBox):
            entry.set("")
        else:
            entry.delete(0, "end")


def Cancelar(boton_guardar, boton_eliminar, boton_editar, boton_nuevo, entry_buscar, entries):
    global edi_nuevo
    boton_eliminar.configure(state="normal")
    boton_editar.configure(state="normal")
    boton_nuevo.configure(state="normal")
    boton_guardar.configure(state="disabled")
    LimpiarDatos(entry_buscar, entries)
    edi_nuevo = None


def Buscar(entry_buscar, entries):
    id_text = entry_buscar.get().strip()
    if not id_text.isdigit():
        MostrarPopUp("Error", "Por favor ingresa un ID válido")
        return

    usuario = entidades.Usuario()
    usuario.set_usuario_id(int(id_text))

    db = usuario_bd()
    resultado = db.Buscar(usuario)

    if resultado:
        LimpiarDatos(None, entries)
        entries[0].insert(0, resultado.get_nombre())
        entries[1].insert(0, resultado.get_username())
        entries[2].insert(0, resultado.get_password())
        entries[3].set(resultado.get_tipo_usuario())
        MostrarPopUp("Usuario encontrado", "Datos cargados correctamente")
    else:
        MostrarPopUp("Error", "Usuario no encontrado")


def NuevoUsuario(boton_guardar, boton_eliminar, boton_editar, entry_buscar, entries):
    global edi_nuevo
    boton_eliminar.configure(state="disabled")
    boton_editar.configure(state="disabled")
    boton_guardar.configure(state="normal")
    LimpiarDatos(entry_buscar, entries)
    edi_nuevo = False


def Guardar(entry_buscar, entries, boton_guardar, boton_eliminar, boton_editar, boton_nuevo):
    global edi_nuevo
    valores = [entry.get().strip() for entry in entries]
    if any(not valor for valor in valores):
        MostrarPopUp("Atención", "Todos los campos del formulario son obligatorios.")
        return

    usuario = entidades.Usuario()
    usuario.set_nombre(valores[0])
    usuario.set_username(valores[1])
    usuario.set_password(valores[2])
    usuario.set_tipo_usuario(valores[3])

    db = usuario_bd()
    if edi_nuevo is True:
        id_text = entry_buscar.get().strip()
        if not id_text.isdigit():
            MostrarPopUp("Error", "Debes buscar un usuario antes de editar.")
            return
        usuario.set_usuario_id(int(id_text))
        db.Editar(usuario)
        MostrarPopUp("Éxito", "Usuario editado exitosamente.")
    elif edi_nuevo is False:
        db.Guardar(usuario)
        MostrarPopUp("Éxito", "Usuario guardado exitosamente.")
    else:
        MostrarPopUp("Atención", "Selecciona 'Nuevo' o 'Editar' para guardar cambios.")
        return

    LimpiarDatos(entry_buscar, entries)
    boton_guardar.configure(state="disabled")
    boton_eliminar.configure(state="normal")
    boton_editar.configure(state="normal")
    boton_nuevo.configure(state="normal")
    edi_nuevo = None


def Borrar(entry_buscar, entries):
    id_text = entry_buscar.get().strip()
    if not id_text.isdigit():
        MostrarPopUp("Error", "Por favor ingresa un ID válido para eliminar")
        return

    usuario = entidades.Usuario()
    usuario.set_usuario_id(int(id_text))

    db = usuario_bd()
    db.Borrar(usuario)
    MostrarPopUp("Éxito", "Usuario borrado exitosamente.")
    LimpiarDatos(entry_buscar, entries)


def Editar(boton_eliminar, boton_nuevo, boton_guardar, entries):
    global edi_nuevo
    if not any(entry.get().strip() for entry in entries):
        MostrarPopUp("Atención", "Primero busca un usuario para editarlo")
        return

    edi_nuevo = True
    boton_eliminar.configure(state="disabled")
    boton_nuevo.configure(state="disabled")
    boton_guardar.configure(state="normal")


def pantalla_usuarios(ventana):
    global edi_nuevo
    edi_nuevo = None

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
    frame_top.grid(row=0, column=0, sticky="ns")
    frame_top.grid_columnconfigure((0, 1, 2), weight=1)

    # Título
    titulo = ctk.CTkLabel(
        frame_top,
        text="usuarios",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.grid(row=0, column=0, columnspan=3, pady=(10, 15), sticky="n")

    # Búsqueda
    lbl_buscar = ctk.CTkLabel(frame_top, text="Id:")
    lbl_buscar.grid(row=1, column=0, sticky="e", padx=5)

    entry_buscar = ctk.CTkEntry(frame_top, width=200)
    entry_buscar.grid(row=1, column=1, padx=5)

    btn_buscar = ctk.CTkButton(
        frame_top,
        text="buscar",
        width=100,
        command=lambda: Buscar(entry_buscar, entries)
    )
    btn_buscar.grid(row=1, column=2, padx=5)

    # ---------------- FORMULARIO CENTRAL ----------------
    frame_form = ctk.CTkFrame(ventana)
    frame_form.grid(row=2, column=0)

    for i in range(4):
        frame_form.grid_rowconfigure(i, weight=1)
    frame_form.grid_columnconfigure(1, weight=1)

    campos = ["Nombre:", "Usuario:", "contraseña:", "Tipo Usuario:"]

    entries = []

    for i, texto in enumerate(campos):
        lbl = ctk.CTkLabel(frame_form, text=texto)
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        if i == 3:  # Tipo Usuario
            combo_tipos = ctk.CTkComboBox(
                frame_form, 
                values=["admin", "cobrador"],
                width=250,
                state="readonly"
            )
            combo_tipos.grid(row=i, column=1, padx=10, pady=5)
            entries.append(combo_tipos)
        else:
            entry = ctk.CTkEntry(frame_form, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

    # Botones del formulario
    frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botones.grid(row=4, column=0, columnspan=2, pady=15)

    btn_eliminar = ctk.CTkButton(
        frame_botones,
        text="eliminar",
        width=100,
        command=lambda: Borrar(entry_buscar, entries)
    )
    btn_eliminar.pack(side="left", padx=10)

    btn_editar = ctk.CTkButton(
        frame_botones,
        text="editar",
        width=100,
        command=lambda: Editar(btn_eliminar, btn_nuevo, btn_guardar, entries)
    )
    btn_editar.pack(side="left", padx=10)

    btn_nuevo = ctk.CTkButton(
        frame_botones,
        text="nuevo",
        width=100,
        command=lambda: NuevoUsuario(btn_guardar, btn_eliminar, btn_editar, entry_buscar, entries)
    )
    btn_nuevo.pack(side="left", padx=10)

    # ---------------- BOTONES INFERIORES ----------------
    frame_bottom = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_bottom.grid(row=3, column=0, sticky="se", padx=20, pady=20)

    btn_cancelar = ctk.CTkButton(
        frame_bottom,
        text="cancelar",
        width=120,
        command=lambda: Cancelar(btn_guardar, btn_eliminar, btn_editar, btn_nuevo, entry_buscar, entries)
    )
    btn_cancelar.pack(side="left", padx=10)

    btn_guardar = ctk.CTkButton(
        frame_bottom,
        text="guardar",
        width=120,
        command=lambda: Guardar(entry_buscar, entries, btn_guardar, btn_eliminar, btn_editar, btn_nuevo)
    )
    btn_guardar.pack(side="left", padx=10)
    btn_guardar.configure(state="disabled")
