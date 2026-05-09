import customtkinter as ctk
from CTkTable import CTkTable
import utils.entidades as entidades
from DataBase.servicios_bd import servicios_bd
from DataBase.precios_bd import precio_bd
from DataBase.cliente_bd import cliente_bd
from DataBase.vehiculos_bd import vehiculos_bd
from DataBase.estacionamientos_bd import estacionamiento_bd
from datetime import datetime

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

    # =====================================================
    # ESTADO INICIAL
    # =====================================================
    def estado_inicial():
        #Vaciamos el contenido de ambos frames para dejarlos como al inicio
        limpiar_ventana(frame_izquierdo)
        limpiar_ventana(frame_derecho)

    #region vistas frame
    
    # =========================================================
    # VISTA IZQUIERDA
    # DETALLES DEL SERVICIO (Base de Datos)
    # =========================================================

    def vista_detalles_servicio(frame, servicio_encontrado):
        limpiar_ventana(frame)

        # ---------------- GRID ----------------
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------
        titulo = ctk.CTkLabel(
            frame,
            text="Detalles del Servicio",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(20, 10), sticky="s")

        # ---------------- DATOS DE LA BD ----------------
        #Aquí conseguimos toda la información de la BD para consultar servicios
        frame_datos = ctk.CTkFrame(frame)
        frame_datos.grid(row=1, column=0, padx=20, pady=10)
        frame_datos.grid_columnconfigure(1, weight=1)

        #Preparamos los datos de la bd
        datos_mostrar = [
            ("Folio:", servicio_encontrado.get_folio_servicio()),
            ("Matrícula:", servicio_encontrado.get_matricula()),
            ("Tipo Servicio:", servicio_encontrado.get_tipo_servicio()),
            ("Fecha Entrada:", servicio_encontrado.get_fecha_entrada()),
            ("Hora Entrada:", servicio_encontrado.get_hora_entrada()),
            ("ID Estacionamiento:", servicio_encontrado.get_estacionamiento_id())
        ]

        #Validamos si ya tiene fecha y hora de salida
        fecha_salida = servicio_encontrado.get_fecha_salida()
        hora_salida = servicio_encontrado.get_hora_salida()
        
        servicio_pagado = False
        
        #Aquí es para mostrar Fecha y Hora de Salida en caso de que no esten vacios
        if fecha_salida and hora_salida: 
            datos_mostrar.append(("Fecha Salida:", fecha_salida))
            datos_mostrar.append(("Hora Salida:", hora_salida))
            servicio_pagado = True

        #Imprimimos cada dato en el frame
        for i, (label_text, valor) in enumerate(datos_mostrar):
            lbl_campo = ctk.CTkLabel(frame_datos, text=label_text, font=ctk.CTkFont(weight="bold"))
            lbl_campo.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            lbl_valor = ctk.CTkLabel(frame_datos, text=str(valor))
            lbl_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # ---------------- BOTONES ----------------
        frame_bottom = ctk.CTkFrame(frame, fg_color="transparent")
        frame_bottom.grid(row=2, column=0, sticky="se", padx=20, pady=20)

        btn_cancelar = ctk.CTkButton(
            frame_bottom, 
            text="cerrar", 
            width=120, 
            command=estado_inicial
        )
        btn_cancelar.pack(side="left", padx=10)

        #Aquí definimos el estado del boton para verificar si el servicio ya se pago o no
        estado_boton = "disabled" if servicio_pagado else "normal"

        btn_proceder_pago = ctk.CTkButton(
            frame_bottom,
            text="Proceder a pago",
            width=120,
            command=lambda: vista_pagar_servicio(frame),
            state=estado_boton
        )
        btn_proceder_pago.pack(side="left", padx=10)
    
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
        titulo.grid(row=0, column=0, pady=(20, 10), sticky="s")

        # ---------------- FORMULARIO ----------------
        frame_form = ctk.CTkFrame(frame)
        frame_form.grid(row=1, column=0, padx=20, pady=10)
        frame_form.grid_columnconfigure(1, weight=1)

        # 1. ID CLIENTE
        lbl_id_cliente = ctk.CTkLabel(frame_form, text="ID cliente:")
        lbl_id_cliente.grid(row=0, column=0, padx=10, pady=8, sticky="e")

        frame_cliente = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_cliente.grid(row=0, column=1, padx=10, pady=8, sticky="we")

        entry_id_cliente = ctk.CTkEntry(frame_cliente, width=100)
        entry_id_cliente.pack(side="left", padx=(0, 10))

        btn_verificar = ctk.CTkButton(frame_cliente, text="Verificar", width=80)
        btn_verificar.pack(side="left")

        lbl_estado_cliente = ctk.CTkLabel(frame_cliente, text="", font=ctk.CTkFont(size=12))
        lbl_estado_cliente.pack(side="left", padx=10)

        # 2. VEHICULO
        lbl_vehiculo = ctk.CTkLabel(frame_form, text="Vehículo:")
        lbl_vehiculo.grid(row=1, column=0, padx=10, pady=8, sticky="e")

        frame_vehiculo = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_vehiculo.grid(row=1, column=1, padx=10, pady=8, sticky="we")

        option_vehiculo = ctk.CTkOptionMenu(frame_vehiculo, values=["---"])
        option_vehiculo.pack(side="left", expand=True, fill="x", padx=(0, 10))

        btn_nuevo_vehiculo = ctk.CTkButton(frame_vehiculo, text="nuevo", width=100)
        btn_nuevo_vehiculo.pack(side="right")

        # 3. FECHA ENTRADA
        lbl_fecha = ctk.CTkLabel(frame_form, text="Fecha entrada:")
        lbl_fecha.grid(row=2, column=0, padx=10, pady=8, sticky="e")
        
        entry_fecha = ctk.CTkEntry(frame_form, width=300, placeholder_text="AAAA-MM-DD")
        entry_fecha.grid(row=2, column=1, padx=10, pady=8)

        # 4. HORA ENTRADA (Ajustado a HH:MM)
        lbl_hora = ctk.CTkLabel(frame_form, text="Hora entrada:")
        lbl_hora.grid(row=3, column=0, padx=10, pady=8, sticky="e")
        
        entry_hora = ctk.CTkEntry(frame_form, width=300, placeholder_text="HH:MM")
        entry_hora.grid(row=3, column=1, padx=10, pady=8)

        # 5. TIPO SERVICIO
        lbl_servicio = ctk.CTkLabel(frame_form, text="Tipo de servicio:")
        lbl_servicio.grid(row=4, column=0, padx=10, pady=8, sticky="e")

        option_servicio = ctk.CTkOptionMenu(frame_form, values=["Estacionamiento", "Pensión"])
        option_servicio.grid(row=4, column=1, padx=10, pady=8, sticky="we")

        # 6. ESTABLECIMIENTO
        lbl_estacionamiento = ctk.CTkLabel(frame_form, text="ID Establecimiento:")
        lbl_estacionamiento.grid(row=5, column=0, padx=10, pady=8, sticky="e")
        
        entry_estacionamiento = ctk.CTkEntry(frame_form, width=300)
        entry_estacionamiento.grid(row=5, column=1, padx=10, pady=8)

        #Label para mostrar errores de guardado
        lbl_mensaje_guardar = ctk.CTkLabel(frame_form, text="", font=ctk.CTkFont(size=12))
        lbl_mensaje_guardar.grid(row=6, column=0, columnspan=2, pady=5)

        # ---------------- LÓGICA DE VERIFICACIÓN ----------------
        #En esta función, verificamos si el cliente existe o no, en caso de que si, se buscan los vehiculos que tenga registrado a su nombre
        def verificar_cliente():
            id_ingresado = entry_id_cliente.get()
            
            if not id_ingresado.isdigit():
                lbl_estado_cliente.configure(text="ID inválido", text_color="red")
                return
            
            cliente_temp = entidades.Cliente()
            cliente_temp.set_cliente_id(int(id_ingresado))
            
            db_cliente = cliente_bd()
            cliente_encontrado = db_cliente.Buscar(cliente_temp)

            if cliente_encontrado:
                lbl_estado_cliente.configure(text=f"Ok: {cliente_encontrado.get_nombre()}", text_color="green")
                
                db_vehiculo = vehiculos_bd()
                lista_vehiculos = db_vehiculo.BuscarPorCliente(cliente_temp)
                
                if lista_vehiculos:
                    matriculas = [v.get_matricula() for v in lista_vehiculos]
                    option_vehiculo.configure(values=matriculas)
                    option_vehiculo.set(matriculas[0]) 
                else:
                    option_vehiculo.configure(values=["Sin vehículos"])
                    option_vehiculo.set("Sin vehículos")
            else:
                lbl_estado_cliente.configure(text="El cliente no existe", text_color="red")
                option_vehiculo.configure(values=["---"])
                option_vehiculo.set("---")

        btn_verificar.configure(command=verificar_cliente)

        # ---------------- LÓGICA DE GUARDADO ----------------
        def guardar_servicio():
            #Usamos datetime para comprobar que los formatos de fecha y hora introducidos sean correctos
            id_cliente = entry_id_cliente.get().strip()
            fecha = entry_fecha.get().strip()
            hora = entry_hora.get().strip()
            id_est = entry_estacionamiento.get().strip()
            vehiculo = option_vehiculo.get()
            
            # 1. Validar que no haya campos vacíos
            if not id_cliente or not id_est or not fecha or not hora or vehiculo in ["---", "Sin vehículos"]:
                lbl_mensaje_guardar.configure(text="Error: Todos los campos son obligatorios.", text_color="red")
                return

            # 2. Validar formato de Fecha (AAAA-MM-DD)
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                lbl_mensaje_guardar.configure(text="Error: La fecha debe tener el formato AAAA-MM-DD.", text_color="red")
                return

            # 3. Validar formato de Hora (HH:MM)
            try:
                # El formato %H:%M acepta desde 00:00 hasta 23:59
                datetime.strptime(hora, "%H:%M")
            except ValueError:
                lbl_mensaje_guardar.configure(text="Error: La hora debe tener el formato HH:MM.", text_color="red")
                return
            
            # 4. Validar que el ID del establecimiento sea numérico
            if not id_est.isdigit():
                lbl_mensaje_guardar.configure(text="Error: ID de establecimiento inválido.", text_color="red")
                return

            # 5. Validar existencia del establecimiento en la BD
            est_temp = entidades.Estacionamiento()
            est_temp.set_estacionamiento_id(int(id_est))
            
            db_est = estacionamiento_bd()
            est_encontrado = db_est.Buscar(est_temp)

            if not est_encontrado:
                lbl_mensaje_guardar.configure(text="Error: El establecimiento no existe en la BD.", text_color="red")
                return
            
           #Preparamos la entidad Servicio (en singular)
            nuevo_servicio = entidades.Servicio()
            nuevo_servicio.set_estacionamiento_id(int(id_est))
            nuevo_servicio.set_matricula(vehiculo)
            nuevo_servicio.set_fecha_entrada(fecha)
            nuevo_servicio.set_hora_entrada(hora)
            nuevo_servicio.set_tipo_servicio(option_servicio.get().lower())
            nuevo_servicio.set_fecha_salida("")
            nuevo_servicio.set_hora_salida("")
            nuevo_servicio.set_folio_precio(0)

            #Llamamos al método para guardar entradas en la base de datos
            db_servicio = servicios_bd()
            exito = db_servicio.Guardar_Servicio(nuevo_servicio)

            if exito:
                folio_generado = nuevo_servicio.get_folio_servicio()
                lbl_mensaje_guardar.configure(text=f"Servicio guardado exitosamente. Folio: {folio_generado}", text_color="green")
            else:
                lbl_mensaje_guardar.configure(text="Error al intentar guardar el servicio.", text_color="red")


        # ---------------- BOTONES INFERIORES ----------------
        frame_bottom = ctk.CTkFrame(frame, fg_color="transparent")
        frame_bottom.grid(row=2, column=0, sticky="se", padx=20, pady=20)

        btn_cancelar = ctk.CTkButton(
            frame_bottom,
            text="cancelar",
            width=120,
            command=estado_inicial
        )
        btn_cancelar.pack(side="left", padx=10)

        btn_guardar = ctk.CTkButton(
            frame_bottom,
            text="guardar",
            width=120,
            command=guardar_servicio
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
            width=120,
            command=estado_inicial
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
        frame.grid_rowconfigure(0, weight=0) # Título
        frame.grid_rowconfigure(1, weight=1) # Tabla (ocupa el centro)
        frame.grid_rowconfigure(2, weight=0) # Texto de condiciones (abajo)

        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------
        titulo = ctk.CTkLabel(
            frame,
            text="Precios",
            font=ctk.CTkFont(size=28, weight="bold")
        )

        titulo.grid(row=0, column=0, pady=(20, 10), sticky="n")

        # ---------------- OBTENER DATOS BD ----------------
        bd_precio = precio_bd()
        lista_precios = bd_precio.obtener_todos()

        # ---------------- TABLA (3 Columnas) ----------------
        # Cabecera
        datos = [
            ["Servicio", "Precio", "Precio con\ndescuento"]
        ]

        # Llenado dinámico
        if lista_precios:
            # Convertimos la lista en un diccionario para buscar por el nombre exacto de la BD
            # Almacenamos el monto asegurándonos de que sea entero
            diccionario_precios = {precio.get_tipo(): int(precio.get_monto()) for precio in lista_precios}

            # 1. Lógica para Estacionamiento Normal (parking)
            if "parking" in diccionario_precios:
                monto = diccionario_precios["parking"]
                datos.append([
                    "Estacionamiento",
                    f"${monto:.2f}",       # El :.2f lo muestra como float (ej. $30.00)
                    f"${monto - 4:.2f}"    # Restamos 4 como descuento después de 5 horas
                ])

            # 2. Lógica para Estacionamiento Frecuente (parking_frecuente)
            if "parking_frecuente" in diccionario_precios:
                monto = diccionario_precios["parking_frecuente"]
                datos.append([
                    "Estacionamiento\n(Cliente Frecuente)",
                    f"${monto:.2f}",
                    f"${monto - 4:.2f}"
                ])

            # 3. Lógica para Pensión (pension) y su descuento (pension_frecuente)
            if "pension" in diccionario_precios:
                monto_pension = diccionario_precios["pension"]
                
                # Buscamos 'pension_frecuente' para el descuento. Si no existe, repite el precio normal.
                monto_descuento = diccionario_precios.get("pension_frecuente", monto_pension)
                
                datos.append([
                    "Pensión",
                    f"${monto_pension:.2f}",
                    f"${monto_descuento:.2f}"
                ])
        else:
            datos.append(["Sin registros", "$0.00", "$0.00"])

        tabla = CTkTable(
            master=frame,
            values=datos,
            width=130 
        )

        tabla.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        # ---------------- CONDICIONES (Texto Inferior) ----------------
        texto_condiciones = (
            "Condiciones de descuento:\n\n"
            "• Estacionamiento: Después de 5 horas.\n"
            "• Pensión: Después de 1 año."
        )

        lbl_condiciones = ctk.CTkLabel(
            frame,
            text=texto_condiciones,
            font=ctk.CTkFont(size=14),
            justify="left"
        )

        lbl_condiciones.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")


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
            estado_inicial()
        
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
        # 1. Obtener el texto del entry
        folio_ingresado = entry_id.get()
        
        # Validar que no esté vacío y sea un número
        if not folio_ingresado or not folio_ingresado.isdigit():
            MostrarPopUp("Error", "Solo se aceptan folios con digitos")
            return

        # 2. Instanciar la entidad Servicio y pasarle el folio
        servicio_buscar = entidades.Servicio()
        servicio_buscar.set_folio_servicio(int(folio_ingresado))

        # 3. Realizar la búsqueda en la BD
        db = servicios_bd()
        servicio_encontrado = db.Buscar(servicio_buscar)

        # 4. Validar el resultado
        if servicio_encontrado:
            # Si se encontró, mostramos los detalles en la nueva vista
            vista_detalles_servicio(frame_izquierdo, servicio_encontrado)
            vista_qr(frame_derecho, str(servicio_encontrado.get_folio_servicio()))
        else:
            # Si no se encontró, limpiamos la vista y podemos mostrar error
            estado_inicial()
            MostrarPopUp("Error", "No se encontro ningún servicio con ese folio")

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