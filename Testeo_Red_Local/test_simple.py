import socket
import platform
import subprocess
import os

def escribir_en_archivo(contenido):
    print(contenido)  # Mostrar el contenido en la terminal
    with open("resultados_red.txt", "a", encoding="utf-8") as archivo:
        archivo.write(contenido + "\n")

def test_red():
    escribir_en_archivo("Iniciando prueba de red...")
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    escribir_en_archivo(f"Tu IP local es: {ip_local}")

    ip_router = '.'.join(ip_local.split('.')[:-1] + ['1'])
    escribir_en_archivo(f"Probando conexión con router ({ip_router})...")

    param = '-n' if platform.system().lower() == 'windows' else '-c'
    resultado = subprocess.call(['ping', param, '1', ip_router], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if resultado == 0:
        escribir_en_archivo(f"Conexión con el router ({ip_router}) exitosa.")
    else:
        escribir_en_archivo(f"No se pudo conectar al router ({ip_router}).")

def probar_conexion_externa():
    try:
        ip_google = '8.8.8.8'
        escribir_en_archivo(f"Probando conexión a {ip_google}...")
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        resultado = subprocess.call(['ping', param, '1', ip_google], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if resultado == 0:
            escribir_en_archivo(f"Conexión a {ip_google} exitosa.")
        else:
            escribir_en_archivo(f"No se pudo conectar a {ip_google}.")
    except Exception as e:
        escribir_en_archivo(f"Error al probar conexión externa: {e}")

def probar_resolucion_DNS():
    try:
        dominio = 'www.google.com'
        escribir_en_archivo(f"Resolviendo {dominio}...")
        ip_dominio = socket.gethostbyname(dominio)
        escribir_en_archivo(f"La IP de {dominio} es: {ip_dominio}")
    except socket.gaierror:
        escribir_en_archivo(f"No se pudo resolver el dominio {dominio}.")

def escanear_puertos_locales():
    escribir_en_archivo("Escaneando puertos locales (1-1024)...")
    ip_local = socket.gethostbyname(socket.gethostname())
    for puerto in range(1, 1025):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.1)
            resultado = sock.connect_ex((ip_local, puerto))
            if resultado == 0:
                escribir_en_archivo(f"Puerto abierto encontrado: {puerto}")

def mostrar_informacion_red():
    escribir_en_archivo("Obteniendo información de la red local...")
    try:
        import psutil
        interfaces = psutil.net_if_addrs()
        for interfaz, direcciones in interfaces.items():
            escribir_en_archivo(f"Interfaz: {interfaz}")
            for direccion in direcciones:
                if direccion.family == socket.AF_INET:
                    escribir_en_archivo(f"  Dirección IP: {direccion.address}")
                    escribir_en_archivo(f"  Máscara de Subred: {direccion.netmask}")
                    escribir_en_archivo(f"  Broadcast: {direccion.broadcast}")
    except ImportError:
        escribir_en_archivo("El módulo 'psutil' no está instalado. Instálalo con 'pip install psutil'.")

if __name__ == "__main__":
    # Limpiar archivo anterior si existe
    if os.path.exists("resultados_red.txt"):
        os.remove("resultados_red.txt")

    test_red()
    probar_conexion_externa()
    probar_resolucion_DNS()
    mostrar_informacion_red()
    escanear_puertos_locales()
    escribir_en_archivo("Escaneo de puertos locales completado.")
