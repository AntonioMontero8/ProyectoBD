import customtkinter as ctk
from utils.helpers import limpiar_ventana
from DataBase.vehiculos_bd import vehiculos_bd
from myCustomTkinter import mostrar_mensaje

def pantalla_vehiculos(ventana, dueno_id= None, callback_guardar=None):
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

        btn_buscar = ctk.CTkButton(frame_top, text="buscar", width=100)
        btn_buscar.grid(row=1, column=2, padx=5)

    # ---------------- FORMULARIO CENTRAL ----------------
    frame_form = ctk.CTkFrame(ventana)
    frame_form.grid(row=2, column=0)

    for i in range(5):
        frame_form.grid_rowconfigure(i, weight=1)
    frame_form.grid_columnconfigure(1, weight=1)

    campos = ["matricula:", "marca:", "modelo:", "Color:", "ID del dueño:"]
    entries = {} # Usamos diccionario para extraer datos fácilmente luego

    for i, texto in enumerate(campos):
        lbl = ctk.CTkLabel(frame_form, text=texto)
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        entry = ctk.CTkEntry(frame_form, width=250)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[texto] = entry

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

    # Lógica para cancelar
    def cancelar():
        if callback_guardar:
            print(entries["ID del dueño:"].get())
            ventana.destroy()
        else:
            clean_entries()
            btn_editar.configure(state="disabled")
            btn_eliminar.configure(state="disabled")

    def buscar():
        veh = vehiculos_bd()
        res = veh.buscar(entry_buscar.get())
        if res is False:
            mostrar_mensaje("", "vehiculo no encontrado")
        else:
            clean_entries()
            for i, entry in enumerate(entries.values()):
                entry.insert(0,res[i])
                entry.configure(state="disabled")

            btn_editar.configure(state="normal")
            btn_eliminar.configure(state="normal")
    btn_buscar.configure(command=buscar)

    btn_cancelar = ctk.CTkButton(frame_bottom, text="cancelar", width=120, command=cancelar)
    btn_cancelar.pack(side="left", padx=10)

    # Lógica para guardar
    def accion_guardar():
        # Obtenemos la matrícula para el OptionMenu
        id_registrado = entries["matricula:"].get()
        
        if callback_guardar:
            callback_guardar(id_registrado)
        
        # Si es un popup, cerramos al guardar
        if callback_guardar:
            ventana.destroy()
        

    btn_guardar = ctk.CTkButton(frame_bottom, text="guardar", width=120, command=accion_guardar)
    btn_guardar.pack(side="left", padx=10)

if __name__ == "__main__":
    app = ctk.CTk()
    pantalla_vehiculos(app)
    app.mainloop()