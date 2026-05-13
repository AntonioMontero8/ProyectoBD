import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import font
import re
from PIL import Image

class DatePicker(ctk.CTkFrame):
    _calendario_abierto = None

    def __init__(self, master, date_format="dd/mm/yyyy", width=140, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.placeholder = date_format
        self.popup = None
        self.cal = None

        self.entry = ctk.CTkEntry(self, width=width - 35)
        self.entry.grid(row=0, column=0, padx=(0, 2))

        self.after(100, lambda: self.entry.configure(placeholder_text=self.placeholder))

        self.btn = ctk.CTkButton(
            self, text="📅", width=30, command=self.toggle_calendario
        )
        self.btn.grid(row=0, column=1)

        self.meses = [
            "Enero","Febrero","Marzo","Abril","Mayo","Junio",
            "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
        ]

    def toggle_calendario(self):
        if self.popup and self.popup.winfo_exists():
            self.ocultar_calendario()
            return

        if DatePicker._calendario_abierto and DatePicker._calendario_abierto != self:
            DatePicker._calendario_abierto.ocultar_calendario()

        self.mostrar_calendario()
        DatePicker._calendario_abierto = self

    def mostrar_calendario(self):
        root = self.winfo_toplevel()

        self.popup = ctk.CTkToplevel(root)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        fg = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        border = ctk.ThemeManager.theme["CTkFrame"]["border_color"]
        text = ctk.ThemeManager.theme["CTkLabel"]["text_color"]

        width, height = 230, 250

        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()

        self.popup.geometry(f"{width}x{height}+{x}+{y}")

        outer = ctk.CTkFrame(
            self.popup,
            fg_color=fg,
            border_width=1,
            border_color=border,
            corner_radius=10
        )
        outer.pack(fill="both", expand=True)

        container = ctk.CTkFrame(outer, fg_color=fg, corner_radius=10)
        container.pack(fill="both", expand=True, padx=2, pady=2)

        self.popup.after(10, self.popup.focus_force)
        self.popup.bind("<FocusOut>", lambda e: self.ocultar_calendario())

        hoy = datetime.today()
        self.mes_var = tk.StringVar(value=self.meses[hoy.month - 1])
        self.anio_var = tk.StringVar(value=str(hoy.year))

        top = ctk.CTkFrame(container, fg_color="transparent")
        top.pack(fill="x", pady=(4, 2), padx=4)

        mes_menu = ctk.CTkOptionMenu(
            top,
            values=self.meses,
            variable=self.mes_var,
            width=120,
            command=lambda _: self.actualizar_calendario()
        )
        mes_menu.pack(side="left")

        anio_entry = ctk.CTkEntry(
            top,
            textvariable=self.anio_var,
            width=60,
            justify="center"
        )
        anio_entry.pack(side="right")
        anio_entry.bind("<Return>", lambda e: self.actualizar_calendario())

        bg_color = fg[1] if isinstance(fg, tuple) else fg
        text_color = text[1] if isinstance(text, tuple) else text

        self.cal = Calendar(
            container,
            selectmode="day",
            date_pattern=self.placeholder,
            locale="es_ES",
            font=("Arial", 9),
            background=bg_color,
            foreground=text_color,
            headersbackground=bg_color,
            headersforeground=text_color,
            normalbackground=bg_color,
            normalforeground=text_color,
            weekendbackground=bg_color,
            weekendforeground=text_color,
            selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1],
            selectforeground="white",
            bordercolor=border
        )

        self.cal.pack(fill="both", expand=True, padx=6, pady=6)
        self.cal.bind("<<CalendarSelected>>", self.seleccionar_fecha)

    def _click_fuera(self, event):
        if not (self.popup and self.popup.winfo_exists()):
            return

        widget = event.widget
        while widget:
            if widget == self.popup or widget == self:
                return
            widget = getattr(widget, "master", None)

        self.ocultar_calendario()

    def ocultar_calendario(self):
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()

        self.popup = None
        self.winfo_toplevel().unbind("<Button-1>")
        DatePicker._calendario_abierto = None

    def actualizar_calendario(self):
        try:
            mes = self.meses.index(self.mes_var.get()) + 1
            anio = int(self.anio_var.get())
            self.cal.selection_set(datetime(anio, mes, 1))
            self.cal._display_calendar(anio, mes)
        except:
            pass

    def seleccionar_fecha(self, event=None):
        try:
            fecha = self.cal.selection_get().strftime("%d/%m/%Y")
            self.entry.delete(0, tk.END)
            self.entry.insert(0, fecha)
        finally:
            self.ocultar_calendario()

    def get(self):
        return self.entry.get()

class PasswordEntry(ctk.CTkFrame):
    def __init__(self, master, placeholder_text="Contraseña", width=220,
                 eye_closed="ojo_1.png", eye_open="ojo_2.png", **kwargs):

        super().__init__(master, fg_color="transparent", width=width, **kwargs)

        self.columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder_text,
            show="*",
            width=width
        )
        self.entry.grid(row=0, column=0, columnspan = 2,sticky="ew")

        self.image_closed = ctk.CTkImage(
            light_image=Image.open(eye_closed),
            dark_image=Image.open(eye_closed),
            size=(14, 14)
        )

        self.image_open = ctk.CTkImage(
            light_image=Image.open(eye_open),
            dark_image=Image.open(eye_open),
            size=(14, 14)
        )

        self.visible = False

        self.toggle_btn = ctk.CTkButton(
            self,
            text="",
            width=24,
            height=24,
            fg_color="#343638",
            hover_color="#343638",
            image=self.image_closed,
            command=self.toggle_password,
            corner_radius=0
        )
        self.toggle_btn.grid(row=0, column=1, padx=5)

    def toggle_password(self):
        if self.visible:
            self.entry.configure(show="*")
            self.toggle_btn.configure(image=self.image_closed)
        else:
            self.entry.configure(show="")
            self.toggle_btn.configure(image=self.image_open)

        self.visible = not self.visible

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def clear(self):
        self.entry.delete(0, "end")


def mostrar_mensaje(titulo, mensaje):
    ventana_msg = ctk.CTkToplevel()
    ventana_msg.title(titulo)
    ventana_msg.geometry("300x150")
    ventana_msg.grab_set()

    lbl = ctk.CTkLabel(
        ventana_msg,
        text=mensaje,
        wraplength=250
    )
    lbl.pack(pady=20)

    btn = ctk.CTkButton(
        ventana_msg,
        text="Aceptar",
        command=ventana_msg.destroy
    )
    btn.pack(pady=10)

    ventana_msg.bind("<Return>", lambda event: ventana_msg.destroy())


def confirmar_mensaje(titulo, mensaje):
    resultado = {"respuesta": False}

    ventana_msg = ctk.CTkToplevel()
    ventana_msg.title(titulo)
    ventana_msg.geometry("300x150")
    ventana_msg.grab_set()

    lbl = ctk.CTkLabel(
        ventana_msg,
        text=mensaje,
        wraplength=250
    )
    lbl.pack(pady=20)

    frame_botones = ctk.CTkFrame(ventana_msg, fg_color="transparent")
    frame_botones.pack(pady=10)

    def confirmar():
        resultado["respuesta"] = True
        ventana_msg.destroy()

    def cancelar():
        resultado["respuesta"] = False
        ventana_msg.destroy()

    btn_no = ctk.CTkButton(
        frame_botones,
        text="Cancelar",
        command=cancelar,
        width=80
    )
    btn_no.pack(side="left", padx=10)

    btn_si = ctk.CTkButton(
        frame_botones,
        text="Aceptar",
        command=confirmar,
        width=80
    )
    btn_si.pack(side="left", padx=10)

    # CORRECCIÓN: Agregar los paréntesis () a confirmar
    ventana_msg.bind("<Return>", lambda event: confirmar())

    ventana_msg.wait_window()

    return resultado["respuesta"]