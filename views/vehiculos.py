import customtkinter as ctk
from utils.helpers import limpiar_ventana
from utils.entidades import Vehiculo
from DataBase.vehiculos_bd import vehiculos_bd
from myCustomTkinter import mostrar_mensaje, confirmar_mensaje

import re

veh_bd = vehiculos_bd()
modo = ""
def pantalla_vehiculos(ventana, dueno_id= None, callback_guardar=None):
    #region validaciones
    def validar_matricula(texto):
        if texto == "":
            return True

        patron = r"^[A-Za-z]{0,2}[0-9]{0,4}$"
        return re.match(patron, texto) is not None

    # CONVERTIR A MAYÚSCULAS
    def convertir_mayusculas(event):
        entry = event.widget

        posicion = entry.index("insert")

        texto = entry.get().upper()

        entry.delete(0, "end")
        entry.insert(0, texto)

        entry.icursor(posicion)

    v_matricula = ventana.register(validar_matricula)

    def validar_numero(texto):
        return texto.isdigit() or texto == ""

    v_numero = ventana.register(validar_numero)

    def validar_letras(texto):
        return all(c.isalpha() or c.isspace() for c in texto)
    
    v_letras = ventana.register(validar_letras)
    #endregion

    global modo
    modo = ""
    try:
        limpiar_ventana(ventana)
    except:
        # En caso de que ventana sea un CTkToplevel, usamos esto:
        for widget in ventana.winfo_children():
            widget.destroy()

    # ---------------- CONFIGURACIÓN GRID PRINCIPAL ----------------
    # Se mantiene exactamente igual a tu diseño original
    ventana.grid_rowconfigure(0, weight=1)  # espacio arriba
    ventana.grid_rowconfigure(1, weight=0)  # titulo + búsqueda
    ventana.grid_rowconfigure(2, weight=3)  # centro (form)
    ventana.grid_rowconfigure(3, weight=1)  # espacio abajo
    ventana.grid_columnconfigure(0, weight=1)

    # ---------------- CONTENEDOR SUPERIOR ----------------
    frame_top = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_top.grid(row=0, column=0, sticky="ns")
    frame_top.grid_columnconfigure((0, 1, 2), weight=1)

    # Título (Cambia ligeramente según el modo)
    texto_titulo = "vehículos" if callback_guardar else "nuevo vehículo"
    titulo = ctk.CTkLabel(
        frame_top,
        text=texto_titulo,
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.grid(row=0, column=0, columnspan=3, pady=(10, 15), sticky="n")

    # Barra de búsqueda (SOLO SE MUESTRA EN MODO COMPLETO)
    if not callback_guardar:
        lbl_buscar = ctk.CTkLabel(frame_top, text="matricula:")
        lbl_buscar.grid(row=1, column=0, sticky="e", padx=5)

        entry_buscar = ctk.CTkEntry(frame_top, width=200)
        entry_buscar.grid(row=1, column=1, padx=5)
        entry_buscar.configure(validate="key",validatecommand=(v_matricula, "%P"))
        entry_buscar.bind("<KeyRelease>", convertir_mayusculas)

        btn_buscar = ctk.CTkButton(frame_top, text="buscar", width=100)
        btn_buscar.grid(row=1, column=2, padx=5)

    # ---------------- FORMULARIO CENTRAL ----------------
    frame_form = ctk.CTkFrame(ventana)
    frame_form.grid(row=2, column=0)

    for i in range(5):
        frame_form.grid_rowconfigure(i, weight=1)
    frame_form.grid_columnconfigure(1, weight=1)

    campos = ["matricula:", "marca:", "modelo:", "color:", "ID del dueño:"]
    entries = {} # Usamos diccionario para extraer datos fácilmente luego

    for i, texto in enumerate(campos):
        lbl = ctk.CTkLabel(frame_form, text=texto)
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        entry = ctk.CTkEntry(frame_form, width=250)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[texto] = entry

    entries["matricula:"].configure(validate="key",validatecommand=(v_matricula, "%P"))
    entries["matricula:"].bind("<KeyRelease>", convertir_mayusculas)
    entries["marca:"].configure(validate="key",validatecommand=(v_letras, "%P"))
    entries["modelo:"].configure(validate="key",validatecommand=(v_numero, "%P"))
    entries["color:"].configure(validate="key",validatecommand=(v_letras, "%P"))
    entries["ID del dueño:"].configure(validate="key",validatecommand=(v_numero, "%P"))

    if callback_guardar:
        entries["ID del dueño:"].insert(0,dueno_id)
        entries["ID del dueño:"].configure(state="readonly",fg_color="#242424",   border_color="#242424")
        
    # Botones del form (SOLO EN MODO COMPLETO)
    if not callback_guardar:
        frame_botones = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_botones.grid(row=5, column=0, columnspan=2, pady=15)

        btn_eliminar = ctk.CTkButton(frame_botones, text="eliminar", width=100)
        btn_eliminar.pack(side="left", padx=10)
        btn_eliminar.configure(state="disabled")

        btn_editar = ctk.CTkButton(frame_botones, text="editar", width=100)
        btn_editar.pack(side="left", padx=10)
        btn_editar.configure(state="disabled")

        btn_nuevo = ctk.CTkButton(frame_botones, text="nuevo", width=100)
        btn_nuevo.pack(side="left", padx=10)

    # ---------------- BOTONES INFERIORES (ESQUINA) ----------------
    frame_bottom = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_bottom.grid(row=3, column=0, sticky="se", padx=20, pady=20)

    def clean_entries():
        for entry in entries.values():
            entry.configure(state="normal")
            entry.delete(0,"end")

    def buscar():
        veh = vehiculos_bd()
        res = veh.buscar(entry_buscar.get())
        if res is False:
            mostrar_mensaje("", "vehiculo no encontrado")
            btn_cancelar.configure(state="disabled")
        else:
            clean_entries()
            entries["matricula:"].insert(0, res[0])
            entries["marca:"].insert(0, res[2])
            entries["modelo:"].insert(0, res[1])
            entries["color:"].insert(0, res[3])
            entries["ID del dueño:"].insert(0, res[4])

            btn_editar.configure(state="normal")
            btn_eliminar.configure(state="normal")
            btn_nuevo.configure(state="disabled")

            btn_cancelar.configure(state="normal")

        btn_guardar.configure(state="disabled")

    if not callback_guardar:
        btn_buscar.configure(command=buscar)

    def eliminar():
        matricula = entries["matricula:"].get()
        if confirmar_mensaje("",f"¿Quiere eliminiar el vehiculo\n '{matricula}' permanentemente?"):
            veh_bd.eliminar(matricula)
            btn_editar.configure(state="disabled")
            btn_eliminar.configure(state="disabled")
            cancelar()

    if not callback_guardar:
        btn_eliminar.configure(command=eliminar)

    def editar():
        global modo
        for entry in entries.values():
            entry.configure(state="normal")
        entries["matricula:"].configure(state="disabled")
        btn_eliminar.configure(state="disabled")
        btn_nuevo.configure(state="disabled")

        btn_guardar.configure(state="normal")
        btn_cancelar.configure(state="normal")

        modo = "editar"
    
    if not callback_guardar:
        btn_editar.configure(command = editar)

    def nuevo():
        global modo
        clean_entries()
        btn_eliminar.configure(state="disabled")
        btn_editar.configure(state="disabled")

        btn_guardar.configure(state="normal")
        btn_cancelar.configure(state="normal")

        modo = "nuevo"

    if not callback_guardar:
        btn_nuevo.configure(command=nuevo)

    # Lógica para cancelar
    def cancelar():
        if callback_guardar:
            print(entries["ID del dueño:"].get())
            ventana.destroy()
        else:
            global modo
            clean_entries()
            for entry in entries.values():
                entry.configure(state = "disabled")

            btn_editar.configure(state="disabled")
            btn_eliminar.configure(state="disabled")

            btn_editar.configure(state="disabled")
            btn_eliminar.configure(state="disabled")
            btn_nuevo.configure(state="normal")

            btn_guardar.configure(state="disabled")
            btn_cancelar.configure(state="disabled")

            modo = ""

    btn_cancelar = ctk.CTkButton(frame_bottom, text="cancelar", width=120, command=cancelar)
    btn_cancelar.pack(side="left", padx=10)

    # Lógica para guardar
    def guardar():
        global modo
        for entry in entries.values():
            if entry.get() == "":
                mostrar_mensaje("","Es nesesario llenar\ntodos los campos")
                return

        patron = r"^[A-Z]{2}\d{4}$"
        if not re.match(patron, entries["matricula:"].get()) :
            mostrar_mensaje("","la matricula debe tener\nel formato 'AA0000'")
            return
        print("M BIEN")
        veh = Vehiculo()
        veh.set_matricula(entries["matricula:"].get())
        veh.set_modelo(entries["modelo:"].get())
        veh.set_marca(entries["marca:"].get())
        veh.set_color(entries["color:"].get())
        veh.set_cliente_id(entries["ID del dueño:"].get())

        if modo == "nuevo":
            res = veh_bd.guardar(veh)

            mostrar_mensaje("",res[1])

            if res[0]:
                if callback_guardar and res:
                    callback_guardar(veh.get_matricula())
                    ventana.destroy()
                else:
                    btn_guardar.configure(state="disabled")
                    btn_cancelar.configure(state="disabled")

        elif modo == "editar":
            res = veh_bd.editar(veh)
            mostrar_mensaje("",res[1])
            if res[0]:
                entry_buscar.delete(0,"end")
                entry_buscar.insert(0,entries["matricula:"].get())
                btn_nuevo.configure(state="disabled")
                #btn_cancelar.configure(state="disabled")
                buscar()
                btn_guardar.configure(state="disabled")
                btn_cancelar.configure(state="disabled")
                
                modo = ""
        
    btn_guardar = ctk.CTkButton(frame_bottom, text="guardar", width=120, command=guardar)
    btn_guardar.pack(side="left", padx=10)

    
    if callback_guardar:
        modo = "nuevo"
    else:
        cancelar()

if __name__ == "__main__":
    app = ctk.CTk()
    pantalla_vehiculos(app)
    app.mainloop()