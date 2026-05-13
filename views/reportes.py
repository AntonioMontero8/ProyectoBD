import customtkinter as ctk
from CTkTable import CTkTable
from utils.helpers import limpiar_ventana
from DataBase.reportes_bd import reportes_bd

def MostrarPopUp(titulo, mensaje):
    popup = ctk.CTkToplevel()
    popup.title(titulo)
    popup.geometry("350x150")
    popup.grab_set() 
    popup.attributes("-topmost", True)
    etiqueta = ctk.CTkLabel(popup, text=mensaje, font=("Roboto", 16, "bold"), justify="center")
    etiqueta.pack(pady=(30, 20))
    boton_aceptar = ctk.CTkButton(popup, text="Aceptar", command=popup.destroy)
    boton_aceptar.pack()

def pantalla_reportes(ventana):
    try:
        limpiar_ventana(ventana)
    except:
        for widget in ventana.winfo_children():
            widget.destroy()

    theme = ctk.ThemeManager.theme
    header_color = theme["CTkOptionMenu"]["fg_color"]
    
    # ---------------- CONFIG GRID PRINCIPAL ----------------
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(2, weight=0) # KPIs
    ventana.grid_rowconfigure(3, weight=1) # Tablas

    # ---------------- BARRA SUPERIOR ----------------
    frame_top = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_top.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

    titulo = ctk.CTkLabel(frame_top, text="DASHBOARD GERENCIAL", font=ctk.CTkFont(size=26, weight="bold"))
    titulo.pack(side="left")

    # Controles derechos
    btn_historico = ctk.CTkButton(frame_top, text="Ver Histórico Anual (Top)", fg_color="#b8860b", hover_color="#8b6508", command=lambda: mostrar_historico())
    btn_historico.pack(side="right", padx=10)

    btn_generar = ctk.CTkButton(frame_top, text="Generar Reporte", width=120, command=lambda: generar_reporte(entry_anio.get()))
    btn_generar.pack(side="right", padx=10)

    entry_anio = ctk.CTkEntry(frame_top, width=100, justify="center", placeholder_text="Ej. 2026")
    entry_anio.pack(side="right", padx=5)

    lbl_anio = ctk.CTkLabel(frame_top, text="Año a consultar:")
    lbl_anio.pack(side="right", padx=(0, 5))

    # ---------------- TARJETAS KPI (Resumen Rápido) ----------------
    frame_kpis = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_kpis.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
    frame_kpis.grid_columnconfigure((0,1,2), weight=1)

    # Función creadora de KPIs
    def crear_kpi(master, col, titulo_texto, valor_inicial, color_txt):
        f = ctk.CTkFrame(master, corner_radius=10)
        f.grid(row=0, column=col, sticky="ew", padx=10)
        ctk.CTkLabel(f, text=titulo_texto, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 0))
        lbl_valor = ctk.CTkLabel(f, text=valor_inicial, font=ctk.CTkFont(size=24, weight="bold"), text_color=color_txt)
        lbl_valor.pack(pady=(5, 10))
        return lbl_valor

    lbl_kpi_ingreso = crear_kpi(frame_kpis, 0, "Ingreso Total del Año", "$0.00", "#28a745")
    lbl_kpi_mes = crear_kpi(frame_kpis, 1, "Mes con Mayor Demanda", "---", "#ffc107")
    lbl_kpi_vehiculos = crear_kpi(frame_kpis, 2, "Vehículos Atendidos", "0", "#17a2b8")

    # ---------------- CONTENEDOR CENTRAL ----------------
    frame_centro = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_centro.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
    frame_centro.grid_columnconfigure(0, weight=1)
    frame_centro.grid_columnconfigure(1, weight=1)
    frame_centro.grid_rowconfigure(0, weight=1)

    # ---- IZQUIERDA: TABLA MESES ----
    frame_izq = ctk.CTkFrame(frame_centro)
    frame_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    
    ctk.CTkLabel(frame_izq, text="Flujo Vehicular Mensual", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
    
    # Preparamos tabla vacía
    meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    datos_meses = [["Mes", "Entradas", "Salidas"]] + [[m, "0", "0"] for m in meses_nombres]
    
    tabla_meses = CTkTable(master=frame_izq, values=datos_meses, header_color=header_color, corner_radius=5)
    tabla_meses.pack(padx=10, pady=10, expand=True, fill="both")

    # ---- DERECHA: FINANZAS Y HORARIOS ----
    frame_der = ctk.CTkFrame(frame_centro, fg_color="transparent")
    frame_der.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    frame_der.grid_rowconfigure(0, weight=1)
    frame_der.grid_rowconfigure(1, weight=1)
    frame_der.grid_columnconfigure(0, weight=1)

    # Finanzas
    frame_finanzas = ctk.CTkFrame(frame_der)
    frame_finanzas.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
    ctk.CTkLabel(frame_finanzas, text="Ingresos por Tipo de Servicio", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
    
    datos_finanzas = [["Servicio", "Ingresos ($)"], ["Estacionamiento (Hora)", "$0.00"], ["Pensión", "$0.00"]]
    tabla_finanzas = CTkTable(master=frame_finanzas, values=datos_finanzas, header_color=header_color, corner_radius=5)
    tabla_finanzas.pack(padx=20, pady=10, fill="x")

    # Horarios (Barras)
    frame_horarios = ctk.CTkFrame(frame_der)
    frame_horarios.grid(row=1, column=0, sticky="nsew")
    ctk.CTkLabel(frame_horarios, text="Demanda por Horario", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

    frame_barras = ctk.CTkFrame(frame_horarios, fg_color="transparent")
    frame_barras.pack(fill="both", expand=True, padx=20, pady=10)

    # Función para crear barras de progreso
    def crear_barra(master, texto_rango):
        f = ctk.CTkFrame(master, fg_color="transparent")
        f.pack(fill="x", pady=5)
        ctk.CTkLabel(f, text=texto_rango, width=120, anchor="w").pack(side="left")
        pb = ctk.CTkProgressBar(f, height=15)
        pb.pack(side="left", fill="x", expand=True, padx=10)
        pb.set(0)
        lbl_pct = ctk.CTkLabel(f, text="0%", width=40, anchor="e")
        lbl_pct.pack(side="right")
        return pb, lbl_pct

    barras = {
        "Madrugada (00-05)": crear_barra(frame_barras, "🌙 Madrugada (00-05)"),
        "Mañana (06-11)": crear_barra(frame_barras, "☀️ Mañana (06-11)"),
        "Tarde (12-17)": crear_barra(frame_barras, "🌤️ Tarde (12-17)"),
        "Noche (18-23)": crear_barra(frame_barras, "🌒 Noche (18-23)")
    }

    # ==========================================
    # LÓGICA DE REPORTE Y SP
    # ==========================================
    bd = reportes_bd()

    def generar_reporte(anio_str):
        if not anio_str.isdigit() or len(anio_str) != 4:
            MostrarPopUp("Error", "Ingrese un año válido (Ej. 2026).")
            return
        
        # 1. Traer datos
        entradas, salidas = bd.obtener_datos_meses(anio_str)
        ingresos = bd.obtener_ingresos(anio_str)
        horarios = bd.obtener_horarios(anio_str)

        # 2. Llenar Tabla Meses y buscar el mes top
        matriz_meses = [["Mes", "Entradas", "Salidas"]]
        max_entradas = -1
        mes_top = "Ninguno"
        total_vehiculos = 0

        for i, nombre in enumerate(meses_nombres):
            num_mes = f"{(i+1):02d}"
            ent = entradas.get(num_mes, 0)
            sal = salidas.get(num_mes, 0)
            matriz_meses.append([nombre, str(ent), str(sal)])
            
            total_vehiculos += ent
            if ent > max_entradas:
                max_entradas = ent
                mes_top = nombre
        
        tabla_meses.update_values(matriz_meses)
        
        if total_vehiculos == 0:
            mes_top = "Sin registros"

        # 3. Llenar Ingresos
        ingreso_park = ingresos.get('estacionamiento', 0.0)
        ingreso_pens = ingresos.get('pension', 0.0)
        ingreso_total = ingreso_park + ingreso_pens
        
        tabla_finanzas.update_values([
            ["Servicio", "Ingresos ($)"], 
            ["Estacionamiento (Hora)", f"${ingreso_park:,.2f}"], 
            ["Pensión", f"${ingreso_pens:,.2f}"]
        ])

        # 4. Actualizar KPIs
        lbl_kpi_ingreso.configure(text=f"${ingreso_total:,.2f}")
        lbl_kpi_mes.configure(text=mes_top)
        lbl_kpi_vehiculos.configure(text=str(total_vehiculos))

        # 5. Llenar Horarios
        conteo_horarios = {"Madrugada (00-05)": 0, "Mañana (06-11)": 0, "Tarde (12-17)": 0, "Noche (18-23)": 0}
        
        for hora_str, cantidad in horarios.items():
            h = int(hora_str)
            if 0 <= h <= 5: conteo_horarios["Madrugada (00-05)"] += cantidad
            elif 6 <= h <= 11: conteo_horarios["Mañana (06-11)"] += cantidad
            elif 12 <= h <= 17: conteo_horarios["Tarde (12-17)"] += cantidad
            else: conteo_horarios["Noche (18-23)"] += cantidad

        for clave, (pb, lbl) in barras.items():
            cantidad = conteo_horarios[clave]
            pct = (cantidad / total_vehiculos * 100) if total_vehiculos > 0 else 0
            pb.set(pct / 100)
            lbl.configure(text=f"{int(pct)}%")

    # LÓGICA DEL PROCEDIMIENTO ALMACENADO
    def mostrar_historico():
        res = bd.llamar_sp_historico()
        
        pop = ctk.CTkToplevel()
        pop.title("Top de Ingresos Anuales (Histórico)")
        pop.geometry("450x350")
        pop.grab_set() 
        pop.attributes("-topmost", True)
        
        ctk.CTkLabel(pop, text="Ranking Histórico de Ingresos", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        if not res:
            ctk.CTkLabel(pop, text="No hay registros en la base de datos.").pack(pady=20)
        else:
            datos_sp = [["Año", "Servicios Atendidos", "Total Generado ($)"]]
            for row in res:
                datos_sp.append([row[0], str(row[1]), f"${float(row[2]):,.2f}"])
                
            tabla_sp = CTkTable(master=pop, values=datos_sp, header_color="#b8860b", corner_radius=5)
            tabla_sp.pack(padx=20, pady=10, fill="both", expand=True)

        ctk.CTkButton(pop, text="Cerrar", fg_color="gray", command=pop.destroy).pack(pady=15)