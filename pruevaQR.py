import customtkinter as ctk
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode


class QRscaner():
    def __init__(self, root, label_video=None, do_at_scan = None):

        self.root = root
        self.label_video = label_video

        self.cap = None
        self.scanning = False
        self.do_at_scan = do_at_scan

        self.outputVar = ctk.StringVar(master=root, value="")

    def set_label_video(self, label):
        self.label_video = label

    def set_widget_output(self, widget):
        widget.configure(textvariable=self.outputVar)

    # =========================
    # GENERAR QR (VERSIÓN OPTIMIZADA EN MEMORIA)
    # =========================
    def generar_qr(self, texto):

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )

        qr.add_data(texto)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # MAGIA: Extraemos la imagen directamente a PIL sin guardarla en disco
        img_pil = img.get_image()

        ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(250, 250))

        return ctk_img

    # =========================
    # CÁMARA
    # =========================
    def iniciar_camara(self, index=0):
        if self.cap is None:
            self.cap = cv2.VideoCapture(index)

    def detener_camara(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    # =========================
    # ESCANEO
    # =========================
    def iniciar_escaneo(self):
        if self.scanning:
            return

        self.iniciar_camara()
        self.scanning = True
        self.actualizar_frame()

    def detener_escaneo(self):
        self.scanning = False

    def detectar_qr(self, frame):
        for code in decode(frame):
            return code.data.decode('utf-8')
        return None

    # =========================
    # MOSTRAR VIDEO
    # =========================
    def mostrar_frame(self, frame):

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        ctk_img = ctk.CTkImage(
            light_image=img,
            size=(400, 300)
        )

        self.label_video.configure(image=ctk_img)
        self.label_video.image = ctk_img

    def mostrar_resultado_final(self, texto):

        self.outputVar.set(texto)
        if self.do_at_scan is not None:
            self.do_at_scan()

        try:
            img = Image.open("check.png")

            ctk_img = ctk.CTkImage(
                light_image=img,
                size=(400, 300)
            )

            self.label_video.configure(image=ctk_img)
            self.label_video.image = ctk_img

        except:
            print("check.png no encontrada")

    # =========================
    # LOOP VIDEO
    # =========================
    def actualizar_frame(self):

        if not self.scanning or self.cap is None:
            return

        ret, frame = self.cap.read()

        if not ret:
            self.detener_escaneo()
            return

        info_qr = self.detectar_qr(frame)

        if info_qr:
            self.detener_escaneo()
            self.mostrar_resultado_final(info_qr)
            return

        self.mostrar_frame(frame)

        self.root.after(10, self.actualizar_frame)


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":

    app = ctk.CTk()

    app.title("Escáner QR")
    app.geometry("500x600")

    label_video = ctk.CTkLabel(app, text="")
    label_video.pack(pady=10)

    label_resultado = ctk.CTkEntry(app, width=300)
    label_resultado.pack(pady=10)

    scaner = QRscaner(app, label_video)

    scaner.set_widget_output(label_resultado)

    # Entrada para generar QR
    entry_qr = ctk.CTkEntry(app, width=300)
    entry_qr.pack(pady=10)

    # Botón escanear
    boton_scan = ctk.CTkButton(
        app,
        text="Iniciar escaneo",
        command=scaner.iniciar_escaneo
    )

    boton_scan.pack(pady=10)

    # Botón generar QR
    boton_generar = ctk.CTkButton(
        app,
        text="Generar QR",
        command=lambda: scaner.generar_qr(entry_qr.get())
    )

    boton_generar.pack(pady=10)

    app.mainloop()