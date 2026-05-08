import customtkinter as ctk
from CTkTable import CTkTable

from utils.helpers import limpiar_ventana

def pantalla_reportes(ventana):
    try:
        limpiar_ventana(ventana)
    except:
        pass

    theme = ctk.ThemeManager.theme
    header_color = theme["CTkOptionMenu"]["fg_color"]
    # ---------------- CONFIG GRID ----------------
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=1)
    ventana.grid_rowconfigure(2, weight=1)

    # ---------------- TITULO ----------------
    titulo = ctk.CTkLabel(
        ventana, 
        text="REPORTES ANUALES", 
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    # ---------------- AÑO ----------------
    frame_anio = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_anio.grid(row=1, column=0, sticky="w", padx=20, pady=10)

    lbl_anio = ctk.CTkLabel(frame_anio, text="Año:")
    lbl_anio.pack(side="left", padx=(0, 10))

    entry_anio = ctk.CTkEntry(frame_anio, width=150)
    entry_anio.pack(side="left")

    # ---------------- TABLA IZQUIERDA ----------------
    frame_tabla_izq = ctk.CTkFrame(ventana)
    frame_tabla_izq.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    datos_mes = [["Mes", "entradas", "salidas"]] + [["", "", ""] for _ in range(12)]

    tabla_mes = CTkTable(master=frame_tabla_izq, values=datos_mes,header_color=header_color,corner_radius=7)
    tabla_mes.pack(expand=True, fill="both", padx=10, pady=10)

    # ---------------- LADO DERECHO ----------------
    frame_derecha = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_derecha.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=20, pady=10)

    frame_derecha.grid_rowconfigure(1, weight=1)
    frame_derecha.grid_rowconfigure(2, weight=1)
    frame_derecha.grid_columnconfigure(0, weight=1)

    # -------- TABLA SERVICIO --------
    datos_servicio = [
        ["servicio", "vehículos", "ingresos"],
        ["Por hora", "", ""],
        ["pensión", "", ""]
    ]

    tabla_servicio = CTkTable(master=frame_derecha, values=datos_servicio,header_color=header_color,corner_radius=7)
    tabla_servicio.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    # -------- BLOQUE GRAFICA HORARIO --------
    frame_grafico1 = ctk.CTkFrame(frame_derecha)
    frame_grafico1.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

    frame_grafico1.grid_rowconfigure(1, weight=1)
    frame_grafico1.grid_columnconfigure(0, weight=1)

    lbl_graf1 = ctk.CTkLabel(frame_grafico1, text="Demanda por horario:")
    lbl_graf1.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))

    graf1 = ctk.CTkFrame(frame_grafico1)
    graf1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # -------- BLOQUE GRAFICA MES --------
    frame_grafico2 = ctk.CTkFrame(frame_derecha)
    frame_grafico2.grid(row=2, column=0, sticky="nsew")

    frame_grafico2.grid_rowconfigure(1, weight=1)
    frame_grafico2.grid_columnconfigure(0, weight=1)

    lbl_graf2 = ctk.CTkLabel(frame_grafico2, text="Demanda por mes:")
    lbl_graf2.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))

    graf2 = ctk.CTkFrame(frame_grafico2)
    graf2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
