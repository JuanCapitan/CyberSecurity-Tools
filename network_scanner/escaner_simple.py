import socket
import platform
import subprocess
import threading
from datetime import datetime
import time

class EscaneadorRed:
    def __init__(self):
        self.dispositivos = []
        self.total_escaneados = 0
        self.lock = threading.Lock()

    def escanear_ip(self, ip):
        try:
            # Intenta hacer ping
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            resultado = subprocess.call(
                ['ping', param, '1', ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ) == 0

            if resultado:
                with self.lock:
                    self.dispositivos.append({
                        'ip': ip,
                        'estado': 'Activo'
                    })
                    print(f"Dispositivo encontrado: {ip}")

            with self.lock:
                self.total_escaneados += 1
                self.mostrar_progreso()

        except:
            with self.lock:
                self.total_escaneados += 1
                self.mostrar_progreso()

    def mostrar_progreso(self):
        porcentaje = (self.total_escaneados / 254) * 100
        print(f"\rProgreso: {porcentaje:.1f}% completado", end='')
        if self.total_escaneados == 254:
            print("\nEscaneo finalizado.")


    def Definir_base(self):
        # Solicitar al usuario la IP base
        try:
            ip_base = input('Ingrese sub-red correspondiente, ejemplo "192.168.0": ')
            return ip_base
        except ValueError:
            print("Error: Formato de IP no válido. Asegúrese de usar el formato correcto.")
        return self.Definir_base()
    

    def escanear_red(self, ip_base) -> int:
        # Validar la IP base
        print(f"Iniciando escaneo de red {ip_base}.0/24")
        print("Esto puede tomar unos minutos...")
        print("Presione Ctrl+C para cancelar el escaneo.")
        print("-" * 30) 
        
    
        hilos = []
        for ultimo_octeto in range(1, 255):
            ip = f"{ip_base}.{ultimo_octeto}"
            hilo = threading.Thread(target=self.escanear_ip, args=(ip,))
            hilo.daemon = True  # Permite que el hilo se cierre al finalizar el programa
            hilos.append(hilo)
            hilo.start()
            # Pequeña pausa para no sobrecargar
            time.sleep(0.1)

        for hilo in hilos:
            hilo.join(timeout=1)  # Timeout de 1 segundo por hilo

        print("\n\nEscaneo completado!")
        self.mostrar_resultados()

    def mostrar_resultados(self):
        print("\nDispositivos encontrados:")
        print("-" * 30)
        for dispositivo in self.dispositivos:
            print(f"IP: {dispositivo['ip']}")
        print(f"\nTotal dispositivos encontrados: {len(self.dispositivos)}")

def main():
    escaner = EscaneadorRed()
    ip_base = escaner.Definir_base()
    escaner.escanear_red(ip_base)
    
if __name__ == "__main__":
    main()
    
