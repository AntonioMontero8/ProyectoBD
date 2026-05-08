import customtkinter as ctk
from views.login import pantalla_login
from views.clientes import pantalla_clientes
from views.servicios import pantalla_servicios
from views.reportes import pantalla_reportes
from views.vehiculos import pantalla_vehiculos
from views.usuarios import pantalla_usuarios
from views.estacionamientos import pantalla_registro_estacionamientos

from pruevaQR import QRscaner

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Estacionamiento v1.0")
        self.geometry("1100x700")

        # Layout principal: Menú lateral y Contenedor central
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra Lateral (Navegación)
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        
        scaner = QRscaner(self)
        #scaner.iniciar_camara()
        ctk.CTkLabel(self.menu_lateral, text="PARKING APP", font=("Arial", 20, "bold")).pack(pady=30)

        # Botones de Navegación
        btn_estilo = {"width": 180, "height": 40, "anchor": "w"}
        
        ctk.CTkButton(self.menu_lateral, text="🔑 Pantalla Login", command=lambda: pantalla_login(self.contenedor), **btn_estilo).pack(pady=5)
        ctk.CTkButton(self.menu_lateral, text="🚗 servicios", command=lambda: pantalla_servicios(self.contenedor,scaner), **btn_estilo).pack(pady=5)
        ctk.CTkButton(self.menu_lateral, text="📈 Reportes Admin", command=lambda: pantalla_reportes(self.contenedor), **btn_estilo).pack(pady=5)
        ctk.CTkButton(self.menu_lateral, text="📈 Registro clientes", command=lambda: pantalla_clientes(self.contenedor), **btn_estilo).pack(pady=5)
        ctk.CTkButton(self.menu_lateral, text="📈 Registro vehiculos", command=lambda: pantalla_vehiculos(self.contenedor), **btn_estilo).pack(pady=5)
        ctk.CTkButton(self.menu_lateral, text="📈 Registro usuarios", command=lambda: pantalla_usuarios(self.contenedor), **btn_estilo).pack(pady=5) 
        ctk.CTkButton(self.menu_lateral, text="📈 Registro estacionamientos", command=lambda: pantalla_registro_estacionamientos(self.contenedor), **btn_estilo).pack(pady=5)

        # Contenedor Central (donde se cargan las funciones)
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Cargar pantalla inicial por defecto
        pantalla_login(self.contenedor)

if __name__ == "__main__":
    app = App()
    app.mainloop()