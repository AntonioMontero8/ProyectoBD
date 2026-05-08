# Guía de Instalación y Configuración - Sistema de Estacionamiento

## Instalación de Librerías (Consola)

Abre tu terminal y ejecuta el siguiente comando para instalar todas las dependencias de una sola vez:

```bash
pip install customtkinter tkcalendar Pillow opencv-python pyzbar qrcode CTkTable mysql-connector-python
```

### Detalles de las herramientas instaladas:
*   `customtkinter`: El framework principal para la interfaz moderna.
*   `tkcalendar`: Requerido por el componente personalizado `DatePicker`.
*   `Pillow`: Necesario para el procesamiento de imágenes y logos.
*   `opencv-python` (CV2): Utilizado para el acceso y control de la cámara.
*   `pyzbar`: El motor encargado de decodificar y leer los códigos QR.
*   `qrcode`: Utilizado para generar los códigos QR de los servicios.
*   `CTkTable`: Componente para mostrar las tablas de clientes, vehículos y reportes.
*   `mysql-connector-python`: El driver oficial para comunicar Python con tu base de datos en XAMPP.

### Escáner QR (Windows)
La librería `pyzbar` requiere las DLLs de ZBar. Generalmente, al instalarla vía `pip` en Windows, estas se incluyen. Si recibes un error de "zbar shared library not found", podrías necesitar instalar el Visual C++ Redistributable.

## Ejecución

Hay que correr el programa desde el archivo main.py
