import customtkinter as ctk
from CTkTable import CTkTable

from utils.helpers import limpiar_ventana

def pantalla_servicios(ventana,scaner):
    limpiar_ventana(ventana)

    #region configuracion de vista
    # =====================================================
    # CONFIGURACION GRID PRINCIPAL
    # =====================================================
    ventana.grid_rowconfigure(0, weight=0)  # titulo
    ventana.grid_rowconfigure(1, weight=0)  # barra superior
    ventana.grid_rowconfigure(2, weight=1)  # contenido principal

    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=1)

    # =====================================================
    # TITULO
    # =====================================================
    lbl_titulo = ctk.CTkLabel(
        ventana,
        text="servicios",
        font=ctk.CTkFont(size=32, weight="bold")
    )

    lbl_titulo.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=(20, 10)
    )

    # =====================================================
    # BARRA SUPERIOR
    # =====================================================
    frame_top = ctk.CTkFrame(
        ventana,
        fg_color="transparent"
    )

    frame_top.grid(
        row=1,
        column=0,
        columnspan=2,
        pady=(0, 15),
        sticky="w"
    )

    # BOTON NUEVO

    btn_nuevo = ctk.CTkButton(
        frame_top,
        text="nuevo",
        width=100
    )
    btn_nuevo.pack(side="left", padx=5)

    # LABEL ID

    lbl_id = ctk.CTkLabel(
        frame_top,
        text="ID servicio:"
    )
    lbl_id.pack(side="left", padx=(20, 5))

    # ENTRY BUSQUEDA
    entry_id = ctk.CTkEntry(
        frame_top,
        width=180
    )
    entry_id.pack(side="left", padx=5)

    scaner.set_widget_output(entry_id)
    # BOTON BUSCAR

    btn_buscar = ctk.CTkButton(
        frame_top,
        text="buscar",
        width=100
    )
    btn_buscar.pack(side="left", padx=5)

    # BOTON ESCANEAR

    btn_escanear = ctk.CTkButton(
        frame_top,
        text="Escanear",
        width=100
    )
    btn_escanear.pack(side="left", padx=5)

    # =====================================================
    # FRAMES PRINCIPALES
    # =====================================================

    frame_izquierdo = ctk.CTkFrame(ventana)

    frame_izquierdo.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=(20, 10),
        pady=(0, 20)
    )

    frame_derecho = ctk.CTkFrame(ventana)

    frame_derecho.grid(
        row=2,
        column=1,
        sticky="nsew",
        padx=(10, 20),
        pady=(0, 20)
    )
    #endregion

    #region vistas frame
    # =========================================================
    # VISTA IZQUIERDA
    # REGISTRAR SERVICIO
    # =========================================================

    def vista_registrar_servicio(frame):
        limpiar_ventana(frame)

        # ---------------- GRID ----------------
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=1)

        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------

        titulo = ctk.CTkLabel(
            frame,
            text="Registrar servicio",
            font=ctk.CTkFont(size=26, weight="bold")
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(20, 10),
            sticky="s"
        )

        # ---------------- FORMULARIO ----------------

        frame_form = ctk.CTkFrame(frame)

        frame_form.grid(
            row=1,
            column=0,
            padx=20,
            pady=10
        )

        frame_form.grid_columnconfigure(1, weight=1)

        # ID CLIENTE

        lbl_id = ctk.CTkLabel(frame_form, text="ID cliente:")
        lbl_id.grid(row=0, column=0, padx=10, pady=8, sticky="e")

        entry_id = ctk.CTkEntry(frame_form, width=300)
        entry_id.grid(row=0, column=1, padx=10, pady=8)

        # VEHICULO

        lbl_vehiculo = ctk.CTkLabel(frame_form, text="vehículo:")
        lbl_vehiculo.grid(row=1, column=0, padx=10, pady=8, sticky="e")

        frame_vehiculo = ctk.CTkFrame(
            frame_form,
            fg_color="transparent"
        )

        frame_vehiculo.grid(
            row=1,
            column=1,
            padx=10,
            pady=8,
            sticky="we"
        )

        option_vehiculo = ctk.CTkOptionMenu(
            frame_vehiculo,
            values=["Vehículo 1", "Vehículo 2"]
        )

        option_vehiculo.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 10)
        )

        btn_nuevo_vehiculo = ctk.CTkButton(
            frame_vehiculo,
            text="nuevo",
            width=100
        )

        btn_nuevo_vehiculo.pack(side="right")

        # SERVICIO

        lbl_servicio = ctk.CTkLabel(
            frame_form,
            text="servicio:"
        )

        lbl_servicio.grid(
            row=2,
            column=0,
            padx=10,
            pady=8,
            sticky="e"
        )

        option_servicio = ctk.CTkOptionMenu(
            frame_form,
            values=["Estacionamiento", "Pensión"]
        )

        option_servicio.grid(
            row=2,
            column=1,
            padx=10,
            pady=8,
            sticky="we"
        )

        # DURACION

        lbl_duracion = ctk.CTkLabel(
            frame_form,
            text="duración:"
        )

        lbl_duracion.grid(
            row=3,
            column=0,
            padx=10,
            pady=8,
            sticky="e"
        )

        entry_duracion = ctk.CTkEntry(
            frame_form,
            width=300
        )

        entry_duracion.grid(
            row=3,
            column=1,
            padx=10,
            pady=8
        )

        # ---------------- BOTONES ----------------

        frame_bottom = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        frame_bottom.grid(
            row=2,
            column=0,
            sticky="se",
            padx=20,
            pady=20
        )

        btn_cancelar = ctk.CTkButton(
            frame_bottom,
            text="cancelar",
            width=120
        )

        btn_cancelar.pack(side="left", padx=10)

        btn_guardar = ctk.CTkButton(
            frame_bottom,
            text="guardar",
            width=120
        )

        btn_guardar.pack(side="left", padx=10)

    # =========================================================
    # VISTA IZQUIERDA
    # PAGAR SERVICIO
    # =========================================================

    def vista_pagar_servicio(frame):
        limpiar_ventana(frame)

        # ---------------- GRID ----------------

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=1)

        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------

        titulo = ctk.CTkLabel(
            frame,
            text="Pagar servicio",
            font=ctk.CTkFont(size=26, weight="bold")
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(20, 10),
            sticky="s"
        )

        # ---------------- FORMULARIO ----------------

        frame_form = ctk.CTkFrame(frame)

        frame_form.grid(
            row=1,
            column=0,
            padx=20,
            pady=10
        )

        lbl_id_servicio = ctk.CTkLabel(frame_form, text="ID servicio:")
        lbl_id_servicio.grid(row=0, column=0, padx=10, pady=8, sticky="e")

        entry_id_servicio = ctk.CTkEntry(frame_form, width=300)
        entry_id_servicio.grid(row=0, column=1, padx=10, pady=8)
        entry_id_servicio.insert(0,entry_id.get())

        # ---------------------------------------------------

        lbl_vehiculo = ctk.CTkLabel(frame_form, text="vehículo:")
        lbl_vehiculo.grid(row=1, column=0, padx=10, pady=8, sticky="e")

        entry_vehiculo = ctk.CTkEntry(frame_form, width=300)
        entry_vehiculo.grid(row=1, column=1, padx=10, pady=8)

        # ---------------------------------------------------

        lbl_servicio = ctk.CTkLabel(frame_form, text="servicio:")
        lbl_servicio.grid(row=2, column=0, padx=10, pady=8, sticky="e")

        entry_servicio = ctk.CTkEntry(frame_form, width=300)
        entry_servicio.grid(row=2, column=1, padx=10, pady=8)

        # ---------------------------------------------------

        lbl_duracion = ctk.CTkLabel(frame_form, text="duración:")
        lbl_duracion.grid(row=3, column=0, padx=10, pady=8, sticky="e")

        entry_duracion = ctk.CTkEntry(frame_form, width=300)
        entry_duracion.grid(row=3, column=1, padx=10, pady=8)

        # ---------------------------------------------------

        lbl_total = ctk.CTkLabel(frame_form, text="Total a pagar:")
        lbl_total.grid(row=4, column=0, padx=10, pady=8, sticky="e")

        entry_total = ctk.CTkEntry(frame_form, width=300)
        entry_total.grid(row=4, column=1, padx=10, pady=8)

        # ---------------- BOTONES ----------------

        frame_bottom = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        frame_bottom.grid(
            row=2,
            column=0,
            sticky="se",
            padx=20,
            pady=20
        )

        btn_cancelar = ctk.CTkButton(
            frame_bottom,
            text="cancelar",
            width=120
        )

        btn_cancelar.pack(side="left", padx=10)

        btn_pagar = ctk.CTkButton(
            frame_bottom,
            text="pagar",
            width=120
        )

        btn_pagar.pack(side="left", padx=10)


    # =========================================================
    # VISTA DERECHA
    # PRECIOS
    # =========================================================

    def vista_precios(frame):
        limpiar_ventana(frame)

        # ---------------- GRID ----------------
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=3)

        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------
        titulo = ctk.CTkLabel(
            frame,
            text="precios",
            font=ctk.CTkFont(size=28)
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(30, 10),
            sticky="s"
        )

        # ---------------- TABLA ----------------
        datos = [
            [
                "Servicio",
                "Precio",
                "Precio con\ndescuento",
                "Condición de\ndescuento"
            ],
            [
                "Estacionamiento\n(Hora)",
                "$30",
                "$25",
                "Después de\n5 horas"
            ],
            [
                "Estacionamiento\ncliente frecuente\n(Hora)",
                "$26",
                "$22",
                "Después de\n5 horas"
            ],
            [
                "pensión",
                "$500",
                "$400",
                "Después de\n2 años"
            ]
        ]

        tabla = CTkTable(
            master=frame,
            values=datos
        )

        tabla.grid(
            row=1,
            column=0,
            padx=20,
            pady=20,
            sticky="n"
        )


    # =========================================================
    # VISTA DERECHA
    # MOSTRAR QR
    # =========================================================

    def vista_qr(frame, id_servicio="error"):
        limpiar_ventana(frame)

        # ---------------- GRID ----------------

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=3)
        frame.grid_rowconfigure(2, weight=1)

        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------

        titulo = ctk.CTkLabel(
            frame, 
            text="ID del servicio:",
            font=ctk.CTkFont(size=28)
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(20, 10),
            sticky="s"
        )

        # ---------------- QR ----------------

        frame_qr = ctk.CTkFrame(
            frame,
            width=300,
            height=300,
        )

        frame_qr.grid(
            row=1,
            column=0,
            padx=20,
            pady=20
        )

        frame_qr.grid_propagate(False)

        lbl_qr = ctk.CTkLabel(
            frame_qr,
            text="",
            image= scaner.generar_qr(id_servicio)
        )

        lbl_qr.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ---------------- ID ----------------

        lbl_id = ctk.CTkLabel(
            frame,
            text=id_servicio,
            font=ctk.CTkFont(size=26)
        )

        lbl_id.grid(
            row=2,
            column=0,
            pady=(10, 30),
            sticky="n"
        )


    # =========================================================
    # VISTA DERECHA
    # ESCANEAR
    # =========================================================

    def vista_escanear(frame):
        limpiar_ventana(frame)

        # ---------------- GRID ----------------

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=3)
        frame.grid_rowconfigure(2, weight=1)

        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------

        titulo = ctk.CTkLabel(
            frame,
            text="Coloca el QR frente a la camara",
            font=ctk.CTkFont(size=24)
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(20, 10),
            sticky="s"
        )

        # ---------------- CAMARA ----------------

        frame_camara = ctk.CTkFrame(
            frame,
            width=350,
            height=300
        )

        frame_camara.grid(
            row=1,
            column=0,
            padx=20,
            pady=20
        )

        frame_camara.grid_propagate(False)

        lbl_camara = ctk.CTkLabel(
            frame_camara,
            #text="CAMARA"
        )

        lbl_camara.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )
        scaner.set_label_video(lbl_camara)
        scaner.iniciar_escaneo()

        # ---------------- BOTON ----------------
        def cancelar():
            scaner.detener_escaneo()
            vista_registrar_servicio()
        
        btn_cancelar = ctk.CTkButton(
            frame,
            text="cancelar",
            width=120, 
            command = cancelar
        )

        btn_cancelar.grid(
            row=2,
            column=0,
            pady=(10, 30),
            sticky="n",
        )
    #endregion

    #region flujo 
    #btn_nuevo = ctk.CTkButton()
    def nuevo():
        vista_registrar_servicio(frame_izquierdo)
        vista_precios(frame_derecho)

    btn_nuevo.configure(command = nuevo)

    def escanear():
        vista_escanear(frame_derecho)

    btn_escanear.configure(command= escanear)
    
    def buscar():
        if True: #busqueda exitosa
            vista_pagar_servicio(frame_izquierdo)
            vista_qr(frame_derecho,entry_id.get())

    scaner.do_at_scan = buscar

    btn_buscar.configure(command = buscar)
    #endregion

if __name__ == "__main__":
    app = ctk.CTk()
    from pruevaQR import QRscaner
    scaner = QRscaner(app)
    scaner.iniciar_camara()
    
    pantalla_servicios(app,scaner)
    app.mainloop()