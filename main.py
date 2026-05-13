import customtkinter as ctk
from views.login import pantalla_login
from views.clientes import pantalla_clientes
from views.servicios import pantalla_servicios
from views.reportes import pantalla_reportes
from views.vehiculos import pantalla_vehiculos
from views.usuarios import pantalla_usuarios
from views.estacionamientos import pantalla_registro_estacionamientos
from pruevaQR import QRscaner

# ¡NUEVO!: Importamos la función de confirmación que ya tenías
from myCustomTkinter import confirmar_mensaje 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Variable global para la instancia de la app
app_instance = None

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        global app_instance
        app_instance = self  # Guardar referencia global
        
        self.title("Sistema de Gestión de Estacionamiento v1.0")
        self.geometry("1100x700")

        # Variables de sesión
        self.usuario_logueado = None
        self.perfil_usuario = None

        # Layout principal: Menú lateral y Contenedor central
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra Lateral (Navegación) - inicialmente oculta
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.grid_remove()  # Ocultar inicialmente
        
        # Iniciamos el escáner global
        self.scaner = QRscaner(self)
        self.scaner.iniciar_camara()

        self.titulo_menu = ctk.CTkLabel(self.menu_lateral, text="PARKING APP", font=("Arial", 20, "bold"))
        self.titulo_menu.pack(pady=30)

        # Botones de Navegación (se crearán dinámicamente)
        self.botones_menu = []

        # Contenedor Central (donde se cargan las funciones)
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Cargar pantalla inicial por defecto
        self.pantalla_login(self.contenedor)

    def pantalla_login(self, ventana):
        """Método de la clase App que llama a la función pantalla_login"""
        from views.login import pantalla_login as login_func
        login_func(ventana, self)

    # =========================================================
    # NUEVA FUNCIÓN: Lógica para resaltar el botón presionado
    # =========================================================
    def seleccionar_boton(self, boton_presionado):
        # 1. Volver a poner todos los botones "transparentes"
        for btn in self.botones_menu:
            if "Cerrar Sesión" not in btn.cget("text"):
                btn.configure(fg_color="transparent")
        
        # 2. Pintar de azul solo el que acabas de presionar
        boton_presionado.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

    def configurar_menu_admin(self):
        """Configura el menú lateral para usuarios admin (acceso completo)"""
        self._limpiar_menu()
        
        # NUEVO ESTILO: Por defecto son transparentes
        btn_estilo = {
            "width": 180, 
            "height": 40, 
            "anchor": "w",
            "fg_color": "transparent", 
            "text_color": ("gray10", "gray90"),
            "hover_color": ("gray70", "gray30")
        }
        
        # Todos los botones para admin
        botones_admin = [
            ("🚗 Servicios", lambda: pantalla_servicios(app_instance.contenedor, app_instance.scaner)),
            ("👥 Clientes", lambda: pantalla_clientes(app_instance.contenedor)),
            ("🚙 Vehículos", lambda: pantalla_vehiculos(app_instance.contenedor)),
            ("📊 Reportes", lambda: pantalla_reportes(app_instance.contenedor)),
            ("👤 Usuarios", lambda: pantalla_usuarios(app_instance.contenedor)),
            ("🏢 Estacionamientos", lambda: pantalla_registro_estacionamientos(app_instance.contenedor)),
            ("🔑 Cerrar Sesión", lambda: app_instance._volver_a_login())
        ]
        
        for texto, comando in botones_admin:
            btn = ctk.CTkButton(self.menu_lateral, text=texto, **btn_estilo)
            
            # Si NO es el botón de cerrar sesión, aplicamos la magia de resaltarlo
            if "Cerrar Sesión" not in texto:
                def crear_comando(b=btn, cmd=comando):
                    def wrapper():
                        self.seleccionar_boton(b) # Lo pinta de azul
                        cmd()                     # Abre la pantalla
                    return wrapper
                btn.configure(command=crear_comando())
            else:
                # Al botón de cerrar sesión le damos un tono rojizo al pasar el mouse
                btn.configure(command=comando, hover_color="#8b0000")

            btn.pack(pady=5)
            self.botones_menu.append(btn)
            
        # Al iniciar, dejamos seleccionado el primer botón ("Servicios")
        if self.botones_menu:
            self.seleccionar_boton(self.botones_menu[0])

    def configurar_menu_cobrador(self):
        """Configura el menú lateral para usuarios cobrador (acceso limitado)"""
        self._limpiar_menu()
        
        btn_estilo = {
            "width": 180, 
            "height": 40, 
            "anchor": "w",
            "fg_color": "transparent",
            "text_color": ("gray10", "gray90"),
            "hover_color": ("gray70", "gray30")
        }
        
        botones_cobrador = [
            ("🚗 Servicios", lambda: pantalla_servicios(app_instance.contenedor, app_instance.scaner)),
            ("👥 Registro Clientes", lambda: pantalla_clientes(app_instance.contenedor)),
            ("🚙 Registro Vehículos", lambda: pantalla_vehiculos(app_instance.contenedor)),
            ("🔑 Cerrar Sesión", lambda: app_instance._volver_a_login())
        ]
        
        for texto, comando in botones_cobrador:
            btn = ctk.CTkButton(self.menu_lateral, text=texto, **btn_estilo)
            
            if "Cerrar Sesión" not in texto:
                def crear_comando(b=btn, cmd=comando):
                    def wrapper():
                        self.seleccionar_boton(b)
                        cmd()
                    return wrapper
                btn.configure(command=crear_comando())
            else:
                btn.configure(command=comando, hover_color="#8b0000")

            btn.pack(pady=5)
            self.botones_menu.append(btn)
            
        if self.botones_menu:
            self.seleccionar_boton(self.botones_menu[0])

    def _limpiar_menu(self):
        """Limpia todos los botones del menú lateral"""
        for btn in self.botones_menu:
            btn.destroy()
        self.botones_menu.clear()

    def mostrar_menu_lateral(self):
        """Muestra el menú lateral y configura los botones según el perfil"""
        app_instance.menu_lateral.grid(row=0, column=0, sticky="nsew")
        
        if app_instance.perfil_usuario == "admin":
            app_instance.configurar_menu_admin()
        elif app_instance.perfil_usuario == "cobrador":
            app_instance.configurar_menu_cobrador()

    def ocultar_menu_lateral(self):
        """Oculta el menú lateral"""
        app_instance.menu_lateral.grid_remove()

    def login_exitoso(self, usuario_id, perfil):
        """Método llamado después de login exitoso"""
        app_instance.usuario_logueado = usuario_id
        app_instance.perfil_usuario = perfil
        app_instance.mostrar_menu_lateral()

    def _volver_a_login(self):
        """Oculta el menú lateral y muestra la pantalla de login"""
        # =========================================================
        # CAMBIO AQUÍ: Agregamos la validación del PopUp
        # =========================================================
        if confirmar_mensaje("Cerrar Sesión", "¿Estás seguro de que deseas salir del sistema?"):
            app_instance.ocultar_menu_lateral()
            app_instance.pantalla_login(app_instance.contenedor)
            
            # Limpiamos los datos del usuario por seguridad
            self.usuario_logueado = None
            self.perfil_usuario = None

if __name__ == "__main__":
    app = App()
    app.mainloop()