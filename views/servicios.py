import customtkinter as ctk
from CTkTable import CTkTable
import utils.entidades as entidades
from DataBase.servicios_bd import servicios_bd
from DataBase.precios_bd import precio_bd
from DataBase.cliente_bd import cliente_bd
from DataBase.vehiculos_bd import vehiculos_bd
from DataBase.estacionamientos_bd import estacionamiento_bd
from DataBase.cobros_bd import cobro_bd
from datetime import datetime
from views.vehiculos import pantalla_vehiculos
from myCustomTkinter import mostrar_mensaje

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
        text="SERVICIOS",
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
        text="Nuevo",
        width=100
    )
    btn_nuevo.pack(side="left", padx=5)

    # LABEL ID

    lbl_id = ctk.CTkLabel(
        frame_top,
        text="ID del servicio:"
    )
    lbl_id.pack(side="left", padx=(20, 5))

    # ENTRY BUSQUEDA
    entry_id = ctk.CTkEntry(
        frame_top,
        width=180
    )
    entry_id.pack(side="left", padx=5)

    if scaner is not None:
        scaner.set_widget_output(entry_id)
    # BOTON BUSCAR

    btn_buscar = ctk.CTkButton(
        frame_top,
        text="Buscar",
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

    
    # =========================================================
    # VISTA IZQUIERDA
    # DETALLES DEL SERVICIO (Base de Datos)
    # =========================================================

    def vista_detalles_servicio(frame, servicio_encontrado):
        limpiar_ventana(frame)

        # ---------------- GRID ----------------
        # Fila 0 (Título): No se estira
        frame.grid_rowconfigure(0, weight=0)
        # Fila 1 (Datos): SE ESTIRA (weight=1) para ocupar el espacio central
        frame.grid_rowconfigure(1, weight=1)
        # Fila 2 (Botones): No se estira, se queda abajo
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------
        titulo = ctk.CTkLabel(
            frame,
            text="Detalles del Servicio",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        # Cambiamos sticky a "n" para que siempre esté arriba
        titulo.grid(row=0, column=0, pady=(20, 10), sticky="n")

        # ---------------- DATOS DE LA BD ----------------
        # Cambiamos CTkFrame por CTkScrollableFrame para que si crece, ruede.
        frame_datos = ctk.CTkScrollableFrame(frame, width=400, height=350) 
        frame_datos.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        frame_datos.grid_columnconfigure(1, weight=1)

        # Preparamos los datos de la bd iniciales
        datos_mostrar = [
            ("Folio:", servicio_encontrado.get_folio_servicio()),
            ("Matrícula:", servicio_encontrado.get_matricula()),
            ("Tipo Servicio:", servicio_encontrado.get_tipo_servicio()),
            ("Fecha Entrada:", servicio_encontrado.get_fecha_entrada()),
            ("Hora Entrada:", servicio_encontrado.get_hora_entrada()),
            ("ID Estacionamiento:", servicio_encontrado.get_estacionamiento_id())
        ]

        # Validamos si ya tiene fecha y hora de salida
        fecha_salida = servicio_encontrado.get_fecha_salida()
        hora_salida = servicio_encontrado.get_hora_salida()
        
        servicio_pagado = False
        
        # LÓGICA DE SALIDA Y COBROS
        if fecha_salida and hora_salida: 
            datos_mostrar.append(("Fecha Salida:", fecha_salida))
            datos_mostrar.append(("Hora Salida:", hora_salida))
            
            # --- Buscar los detalles del cobro ---
            cobro_temp = entidades.Cobro()
            cobro_temp.set_folio_servicio(servicio_encontrado.get_folio_servicio())
            
            db_cobro = cobro_bd() 
            cobro_encontrado = db_cobro.BuscarCobro(cobro_temp)
            
            if cobro_encontrado:
                # Quitamos toda la lógica de unidad_tiempo y concatenación
                # porque tu base de datos ya trae la unidad incluida
                tiempo_estancia_db = cobro_encontrado.get_tiempo_estancia()
                
                datos_mostrar.append(("Tiempo de estancia:", tiempo_estancia_db))
                datos_mostrar.append(("Usuario que cobró:", cobro_encontrado.get_usuario_id()))
                datos_mostrar.append(("Monto:", f"${float(cobro_encontrado.get_monto_total()):.2f}"))
            
            # Se añade el estado al final de la lista
            datos_mostrar.append(("Estado:", "Pagado"))
            servicio_pagado = True
        else:
            # Si no hay fecha de salida, solo añadimos el estado al final
            datos_mostrar.append(("Estado:", "Sin pagar"))

        # Imprimimos cada dato en el frame
        for i, (label_text, valor) in enumerate(datos_mostrar):
            lbl_campo = ctk.CTkLabel(frame_datos, text=label_text, font=ctk.CTkFont(weight="bold"))
            lbl_campo.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            # Si el estado es "Sin pagar", podemos ponerle color rojo, y verde si es "Pagado"
            color_texto = ["default_theme"]
            if label_text == "Estado:":
                color_texto = "red" if valor == "Sin pagar" else "green"
                lbl_valor = ctk.CTkLabel(frame_datos, text=str(valor), text_color=color_texto, font=ctk.CTkFont(weight="bold"))
            else:
                lbl_valor = ctk.CTkLabel(frame_datos, text=str(valor))
                
            lbl_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # ---------------- BOTONES ----------------
        frame_bottom = ctk.CTkFrame(frame, fg_color="transparent")
        frame_bottom.grid(row=2, column=0, sticky="se", padx=20, pady=20)

        btn_cancelar = ctk.CTkButton(
            frame_bottom, 
            text="Cancelar", 
            width=120, 
            command=estado_inicial
        )
        btn_cancelar.pack(side="left", padx=10)

        # Aquí definimos el estado del boton para verificar si el servicio ya se pago o no
        estado_boton = "disabled" if servicio_pagado else "normal"

        btn_proceder_pago = ctk.CTkButton(
            frame_bottom,
            text="Proceder a pago",
            width=120,
            # DEBES CAMBIAR ESTA LÍNEA ASÍ:
            command=lambda: vista_pagar_servicio(frame, servicio_encontrado),
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
            encontrado = False
            id_ingresado = entry_id_cliente.get()
            
            if not id_ingresado.isdigit():
                lbl_estado_cliente.configure(text="ID inválido", text_color="red")
                return
            
            cliente_temp = entidades.Cliente()
            cliente_temp.set_cliente_id(int(id_ingresado))
            
            db_cliente = cliente_bd()
            cliente_encontrado = db_cliente.Buscar(cliente_temp)

            if cliente_encontrado:
                encontrado = True
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
            return encontrado

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

            # Llamamos al método para guardar entradas en la base de datos
            db_servicio = servicios_bd()
            exito = db_servicio.Guardar_Servicio(nuevo_servicio)

            if exito:
                folio_generado = nuevo_servicio.get_folio_servicio()
                lbl_mensaje_guardar.configure(text=f"Servicio guardado exitosamente. Folio: {folio_generado}", text_color="green")
                
                # =========================================================
                # MAGIA AQUÍ: Mandamos llamar a la vista QR en el panel derecho
                # =========================================================
                vista_qr(frame_derecho, str(folio_generado))
                btn_guardar.configure(state="disabled")
                btn_cancelar.configure(text="Regresar")
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

        # CALLBACK QUE SE EJECUTA AL GUARDAR VEHÍCULO
        def callback_guardar_vehiculo(matricula):
            verificar_cliente()
            option_vehiculo.set(matricula)

        # ABRIR POPUP DE VEHÍCULOS
        def abrir_popup_vehiculo(ventana_padre):

            cliente_id = entry_id_cliente.get()

            if not verificar_cliente():
                mostrar_mensaje("", "Primero debe seleccionar\nun cliente valido")
                return

            popup = ctk.CTkToplevel(ventana_padre)

            popup.title("Nuevo vehículo")
            popup.geometry("700x500")

            popup.transient(ventana_padre)
            popup.grab_set()

            pantalla_vehiculos(
                ventana=popup,
                dueno_id=cliente_id,
                callback_guardar= callback_guardar_vehiculo
            )

        btn_nuevo_vehiculo.configure(command=lambda :abrir_popup_vehiculo(ventana))
    # =========================================================
    # VISTA IZQUIERDA
    # PAGAR SERVICIO
    # =========================================================

    # =========================================================
    # VISTA IZQUIERDA
    # PAGAR SERVICIO
    # =========================================================

    def vista_pagar_servicio(frame, servicio_encontrado):
        limpiar_ventana(frame)

        # ---------------- GRID ----------------
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_columnconfigure(0, weight=1)

        # ---------------- TITULO ----------------
        titulo = ctk.CTkLabel(
            frame,
            text="Pagar servicio",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(20, 10), sticky="n")

        # ---------------- CONTENEDOR PRINCIPAL (Scroll) ----------------
        frame_form = ctk.CTkScrollableFrame(frame, width=450, height=450)
        frame_form.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        frame_form.grid_columnconfigure(1, weight=1)

        # ---------------- DATOS FIJOS (Solo lectura) ----------------
        datos_fijos = [
            ("Folio del servicio:", servicio_encontrado.get_folio_servicio()),
            ("Matrícula:", servicio_encontrado.get_matricula()),
            ("Tipo de servicio:", servicio_encontrado.get_tipo_servicio().capitalize()),
            ("Fecha de Entrada:", servicio_encontrado.get_fecha_entrada()),
            ("Hora de Entrada:", servicio_encontrado.get_hora_entrada()),
            ("ID Estacionamiento:", servicio_encontrado.get_estacionamiento_id())
        ]

        for i, (label_text, valor) in enumerate(datos_fijos):
            lbl_campo = ctk.CTkLabel(frame_form, text=label_text, font=ctk.CTkFont(weight="bold"))
            lbl_campo.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            lbl_valor = ctk.CTkLabel(frame_form, text=str(valor))
            lbl_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        fila_actual = len(datos_fijos)

        # Separador visual
        separador = ctk.CTkFrame(frame_form, height=2, fg_color="gray")
        separador.grid(row=fila_actual, column=0, columnspan=2, sticky="we", padx=10, pady=15)
        fila_actual += 1

        # ---------------- ENTRADAS DEL OPERADOR ----------------
        
        # 1. Usuario
        lbl_usuario = ctk.CTkLabel(frame_form, text="ID Usuario:", font=ctk.CTkFont(weight="bold"))
        lbl_usuario.grid(row=fila_actual, column=0, padx=10, pady=8, sticky="e")
        entry_usuario = ctk.CTkEntry(frame_form, width=200)
        entry_usuario.grid(row=fila_actual, column=1, padx=10, pady=8, sticky="w")
        fila_actual += 1

        # 2. Fecha Salida
        lbl_fsalida = ctk.CTkLabel(frame_form, text="Fecha de salida:", font=ctk.CTkFont(weight="bold"))
        lbl_fsalida.grid(row=fila_actual, column=0, padx=10, pady=8, sticky="e")
        entry_fsalida = ctk.CTkEntry(frame_form, width=200, placeholder_text="AAAA-MM-DD")
        entry_fsalida.grid(row=fila_actual, column=1, padx=10, pady=8, sticky="w")
        fila_actual += 1

        # 3. Hora Salida
        lbl_hsalida = ctk.CTkLabel(frame_form, text="Hora de salida:", font=ctk.CTkFont(weight="bold"))
        lbl_hsalida.grid(row=fila_actual, column=0, padx=10, pady=8, sticky="e")
        entry_hsalida = ctk.CTkEntry(frame_form, width=200, placeholder_text="HH:MM")
        entry_hsalida.grid(row=fila_actual, column=1, padx=10, pady=8, sticky="w")
        fila_actual += 1

        # Label para mensajes de error de los cálculos
        lbl_mensaje_calculo = ctk.CTkLabel(frame_form, text="", font=ctk.CTkFont(size=12))
        lbl_mensaje_calculo.grid(row=fila_actual, column=0, columnspan=2, pady=5)
        fila_actual += 1

        # ---------------- BOTÓN CALCULAR ----------------
        btn_calcular = ctk.CTkButton(frame_form, text="Calcular", width=120)
        btn_calcular.grid(row=fila_actual, column=0, columnspan=2, pady=10)
        fila_actual += 1

        # ---------------- RESULTADOS ----------------
        lbl_tiempo_text = ctk.CTkLabel(frame_form, text="Tiempo de estancia:", font=ctk.CTkFont(weight="bold"))
        lbl_tiempo_text.grid(row=fila_actual, column=0, padx=10, pady=5, sticky="e")
        lbl_tiempo_valor = ctk.CTkLabel(frame_form, text="--")
        lbl_tiempo_valor.grid(row=fila_actual, column=1, padx=10, pady=5, sticky="w")
        fila_actual += 1

        lbl_monto_text = ctk.CTkLabel(frame_form, text="Monto a pagar:", font=ctk.CTkFont(weight="bold"))
        lbl_monto_text.grid(row=fila_actual, column=0, padx=10, pady=5, sticky="e")
        lbl_monto_valor = ctk.CTkLabel(frame_form, text="$0.00", text_color="green", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_monto_valor.grid(row=fila_actual, column=1, padx=10, pady=5, sticky="w")

        # ---------------- BOTONES INFERIORES ----------------
        frame_bottom = ctk.CTkFrame(frame, fg_color="transparent")
        frame_bottom.grid(row=2, column=0, sticky="se", padx=20, pady=20)

        btn_cancelar = ctk.CTkButton(
            frame_bottom,
            text="Cancelar",
            width=120,
            command=estado_inicial
        )
        btn_cancelar.pack(side="left", padx=10)

        # Botón bloqueado por defecto
        btn_pagar = ctk.CTkButton(
            frame_bottom,
            text="Pagar",
            width=120,
            state="disabled" 
        )
        btn_pagar.pack(side="left", padx=10)

        # =========================================================
        # LÓGICA MATEMÁTICA Y BD
        # =========================================================
        
        # Esta es la memoria temporal para compartir datos entre los dos botones
        datos_pago = {
            "folio_precio": 0,
            "tiempo_str": "",
            "monto_total": 0.0,
            "cliente_id": 0,
            "cantidad_sumar": 0, # Visitas (1) o Días (X)
            "f_salida": "",
            "h_salida": "",
            "id_usuario": 0
        }

        def ejecutar_calculo():
            btn_pagar.configure(state="disabled")
            lbl_tiempo_valor.configure(text="--")
            lbl_monto_valor.configure(text="$0.00")
            
            f_salida = entry_fsalida.get().strip()
            h_salida = entry_hsalida.get().strip()
            id_usuario = entry_usuario.get().strip()

            if not f_salida or not h_salida or not id_usuario:
                lbl_mensaje_calculo.configure(text="Error: Ingrese Usuario, Fecha y Hora.", text_color="red")
                return

            if not id_usuario.isdigit():
                lbl_mensaje_calculo.configure(text="Error: El ID de Usuario debe ser numérico.", text_color="red")
                return

            try:
                dt_salida = datetime.strptime(f"{f_salida} {h_salida}", "%Y-%m-%d %H:%M")
            except ValueError:
                lbl_mensaje_calculo.configure(text="Error: Formato de Fecha (AAAA-MM-DD) u Hora (HH:MM) inválido.", text_color="red")
                return

            f_entrada = servicio_encontrado.get_fecha_entrada()
            h_entrada = servicio_encontrado.get_hora_entrada()
            dt_entrada = datetime.strptime(f"{f_entrada} {h_entrada}", "%Y-%m-%d %H:%M")

            if dt_salida < dt_entrada:
                lbl_mensaje_calculo.configure(text="Error: La Fecha/Hora de salida no puede ser menor a la entrada.", text_color="red")
                return

            db_vehiculo = vehiculos_bd()
            datos_vehiculo = db_vehiculo.buscar(servicio_encontrado.get_matricula())
            
            if not datos_vehiculo:
                lbl_mensaje_calculo.configure(text="Error: El vehículo no existe en la BD.", text_color="red")
                return
            
            cliente_temp = entidades.Cliente()
            cliente_temp.set_cliente_id(datos_vehiculo[4])
            
            db_cliente = cliente_bd()
            cliente_obj = db_cliente.Buscar(cliente_temp)
            
            if not cliente_obj:
                lbl_mensaje_calculo.configure(text="Error: No se encontró al propietario.", text_color="red")
                return

            db_precios = precio_bd()
            lista_precios = db_precios.obtener_todos()
            # Guardamos tanto el monto como el folio_precio: { "parking": (30.0, 1) }
            diccionario_precios = {p.get_tipo(): (float(p.get_monto()), p.get_folio_precio()) for p in lista_precios}

            tipo_servicio = servicio_encontrado.get_tipo_servicio().lower()
            monto_total = 0.0
            tiempo_str = ""
            folio_precio_aplicado = 0
            cantidad_a_sumar = 0

            if "estacionamiento" in tipo_servicio or "parking" in tipo_servicio:
                diferencia = dt_salida - dt_entrada
                segundos_totales = diferencia.total_seconds()
                
                horas = int(segundos_totales // 3600)
                minutos = int((segundos_totales % 3600) // 60)

                if horas == 0 and minutos > 0:
                    horas_a_cobrar = 1
                elif minutos >= 46:
                    horas_a_cobrar = horas + 1
                else:
                    horas_a_cobrar = horas

                if horas_a_cobrar == 0: horas_a_cobrar = 1
                
                tiempo_str = f"{horas_a_cobrar} hrs"
                cantidad_a_sumar = 1 # Sumar 1 visita

                tipo_cl_park = str(cliente_obj.get_tipo_cliente_park()).lower()
                clave_precio = "parking_frecuente" if tipo_cl_park == "frecuente" else "parking"
                tarifa_base, folio_precio_aplicado = diccionario_precios.get(clave_precio, (30.0, 0))

                if horas_a_cobrar <= 4:
                    monto_total = horas_a_cobrar * tarifa_base
                else:
                    monto_total = (4 * tarifa_base) + ((horas_a_cobrar - 4) * (tarifa_base - 4))

            else:
                dias_diferencia = (dt_salida.date() - dt_entrada.date()).days
                dias_a_cobrar = 1 if dias_diferencia == 0 else dias_diferencia
                
                tiempo_str = f"{dias_a_cobrar} dias"
                cantidad_a_sumar = dias_a_cobrar # Sumar los días a tiempo_pension

                tipo_cl_pens = str(cliente_obj.get_tipo_cliente_pens()).lower()
                clave_precio = "pension_frecuente" if tipo_cl_pens == "frecuente" else "pension"
                tarifa_base, folio_precio_aplicado = diccionario_precios.get(clave_precio, (200.0, 0))
                
                monto_total = dias_a_cobrar * tarifa_base

            # Guardamos todo en la memoria temporal
            datos_pago["folio_precio"] = folio_precio_aplicado
            datos_pago["tiempo_str"] = tiempo_str
            datos_pago["monto_total"] = monto_total
            datos_pago["cliente_id"] = cliente_obj.get_cliente_id()
            datos_pago["cantidad_sumar"] = cantidad_a_sumar
            datos_pago["f_salida"] = f_salida
            datos_pago["h_salida"] = h_salida
            datos_pago["id_usuario"] = int(id_usuario)

            lbl_tiempo_valor.configure(text=tiempo_str)
            lbl_monto_valor.configure(text=f"${monto_total:.2f}")
            lbl_mensaje_calculo.configure(text="Cálculo realizado. Listo para procesar.", text_color="green")
            btn_pagar.configure(state="normal")

        def ejecutar_pago():
            # 1. Actualizar Servicio
            servicio_actualizado = entidades.Servicio()
            servicio_actualizado.set_folio_servicio(servicio_encontrado.get_folio_servicio())
            servicio_actualizado.set_fecha_salida(datos_pago["f_salida"])
            servicio_actualizado.set_hora_salida(datos_pago["h_salida"])
            servicio_actualizado.set_folio_precio(datos_pago["folio_precio"])
            
            db_serv = servicios_bd()
            if not db_serv.Actualizar_Salida(servicio_actualizado):
                MostrarPopUp("Error", "No se pudo actualizar el servicio.")
                return

            # 2. Actualizar Cliente (Suma visitas o días, el Trigger hace el resto)
            db_cli = cliente_bd()
            tipo_serv = servicio_encontrado.get_tipo_servicio().lower()
            db_cli.Actualizar_Visitas_Dias(datos_pago["cliente_id"], datos_pago["cantidad_sumar"], tipo_serv)

            # 3. Insertar Cobro
            nuevo_cobro = entidades.Cobro()
            # Creamos el formato C00001
            folio_formateado = f"C{servicio_encontrado.get_folio_servicio():05d}"
            nuevo_cobro.set_folio_cobro(folio_formateado)
            nuevo_cobro.set_folio_servicio(servicio_encontrado.get_folio_servicio())
            nuevo_cobro.set_tiempo_estancia(datos_pago["tiempo_str"])
            nuevo_cobro.set_usuario_id(datos_pago["id_usuario"])
            nuevo_cobro.set_monto_total(datos_pago["monto_total"])

            db_cobro = cobro_bd()
            if not db_cobro.Guardar(nuevo_cobro):
                MostrarPopUp("Error", "El servicio se cerró, pero hubo un error al guardar el ticket de cobro.")
                return

            # 4. Éxito y limpieza
            frame.focus_set()  # <--- MAGIA AQUÍ: Le quitamos el foco a las casillas de texto
            MostrarPopUp("Éxito", f"Cobro registrado correctamente.\nFolio: {folio_formateado}")
            estado_inicial()

        btn_calcular.configure(command=ejecutar_calculo)
        btn_pagar.configure(command=ejecutar_pago)


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
            text="" if scaner is not None else "QR no disponible",
            image= scaner.generar_qr(id_servicio) if scaner is not None else None
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
        if scaner is not None:
            scaner.set_label_video(lbl_camara)
            scaner.iniciar_escaneo()
        else:
            lbl_camara.configure(text="Escáner no disponible")

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

    if scaner is not None:
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