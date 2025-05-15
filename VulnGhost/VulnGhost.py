import os
import platform
import subprocess
import socket
import psutil
import requests
import time
import json

# Configuración de la API de NVD
NVD_API_KEY = input("Introduce tu API Key de NVD: ")
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
HEADERS = {"apiKey": NVD_API_KEY}

if not NVD_API_KEY or NVD_API_KEY == "TU_API_KEY_ACÁ":
    raise ValueError("Por favor, configura una API Key válida para NVD.")

# Funciones para recolectar información del sistema
def get_os_info():
    return {
        "Sistema": platform.system(),
        "Versión": platform.version(),
        "Plataforma": platform.platform(),
        "Nombre del nodo": platform.node(),
    }

def get_installed_software(limit=None):
    sistema = platform.system()
    programas = []

    if sistema == "Windows":
        try:
            command = [
                "powershell", "-Command",
                "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | "
                "Select-Object DisplayName, DisplayVersion"
            ]
            output = subprocess.check_output(command, stderr=subprocess.DEVNULL, text=True)
            lines = output.split('\n')
            for line in lines:
                if line.strip() and "DisplayName" not in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        nombre = " ".join(parts[:-1])
                        version = parts[-1]
                        programas.append({'Nombre': nombre.strip(), 'Versión': version.strip()})
        except Exception as e:
            programas.append({'Error': f'No se pudo obtener lista de software: {str(e)}'})

    elif sistema == "Linux":
        try:
            output = subprocess.check_output(['dpkg', '-l'], text=True)
            for line in output.split('\n')[5:]:
                parts = line.split()
                if len(parts) >= 3:
                    programas.append({'Nombre': parts[1], 'Versión': parts[2]})
        except Exception as e:
            programas.append({'Error': f'No se pudo obtener lista de paquetes: {str(e)}'})

    return programas[:limit] if limit else programas

def get_running_services():
    services = []
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                services.append({
                    'PID': proc.info['pid'],
                    'Nombre': proc.info['name'] or "Nombre no disponible"
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        services.append({'Error': f'No se pudo obtener lista de servicios: {str(e)}'})
    return services

def get_open_ports():
    open_ports = []
    try:
        connections = psutil.net_connections()
        for conn in connections:
            if conn.status == 'LISTEN':
                ip, port = conn.laddr
                open_ports.append({'IP': ip, 'Puerto': port})
    except Exception as e:
        open_ports.append({'Error': f'No se pudo obtener lista de puertos: {str(e)}'})
    return open_ports

# Función para buscar CVEs en la API de NVD
def buscar_cves(nombre_software, version=None):
    print(f"\n[+] Buscando CVEs para: {nombre_software} {version if version else ''}")
    params = {
        "keywordSearch": nombre_software,
        "resultsPerPage": 5,
        "startIndex": 0
    }

    if version:
        params["keywordSearch"] = f"{nombre_software} {version}"

    vulnerabilidades = []
    while True:
        try:
            respuesta = requests.get(NVD_API_URL, headers=HEADERS, params=params)
            datos = respuesta.json()
            cves = datos.get("vulnerabilities", [])
            if not cves:
                break
            for cve in cves:
                info = cve["cve"]
                cve_id = info["id"]
                desc = info["descriptions"][0]["value"]
                score = info.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", "N/A")
                vulnerabilidades.append({
                    "cve_id": cve_id,
                    "descripcion": desc,
                    "cvss": score
                })
            params["startIndex"] += len(cves)
            time.sleep(1)  # Para evitar sobrecargar la API
        except requests.exceptions.RequestException as e:
            vulnerabilidades.append({"error": f"Problema de red: {e}"})
            break
        except KeyError as e:
            vulnerabilidades.append({"error": f"Respuesta inesperada de la API: {e}"})
            break
        except Exception as e:
            vulnerabilidades.append({"error": f"No se pudo buscar: {e}"})
            break

    return vulnerabilidades

# Función principal para analizar vulnerabilidades
def analizar_vulnerabilidades(limit_software=20):
    software_list = get_installed_software(limit=limit_software)
    informe = []

    for sw in software_list:
        nombre = sw.get('Nombre')
        version = sw.get('Versión')
        if not nombre or nombre.strip() == "----------- --------------":
            print(f"[!] Software con nombre inválido detectado, omitiendo...")
            continue

        print(f"[+] Analizando {nombre} {version}")
        vulns = buscar_cves(nombre, version)
        informe.append({
            'software': nombre,
            'version': version,
            'vulnerabilidades': vulns
        })

    return informe

# Generar informe completo
def generar_informe(exportar_a_archivo=False):
    info = get_os_info()
    informe = []

    # Información del sistema
    informe.append("[+] Información del sistema:")
    for k, v in info.items():
        informe.append(f"   {k}: {v}")

    # Resumen
    software_vulnerabilidades = analizar_vulnerabilidades(limit_software=10)
    total_softwares = len(software_vulnerabilidades)
    softwares_con_vulnerabilidades = sum(1 for item in software_vulnerabilidades if item['vulnerabilidades'])
    softwares_sin_vulnerabilidades = total_softwares - softwares_con_vulnerabilidades

    informe.append("\n[+] Resumen:")
    informe.append(f"   Total de softwares analizados: {total_softwares}")
    informe.append(f"   Softwares con vulnerabilidades: {softwares_con_vulnerabilidades}")
    informe.append(f"   Softwares sin vulnerabilidades: {softwares_sin_vulnerabilidades}")

    # Detalle de vulnerabilidades
    informe.append("\n[+] Detalle de vulnerabilidades:")
    for item in software_vulnerabilidades:
        informe.append(f"\n== {item['software']} {item['version']} ==")
        if item['vulnerabilidades']:
            for v in item['vulnerabilidades']:
                if 'error' in v:
                    informe.append(f"  ERROR: {v['error']}")
                else:
                    descripcion = v['descripcion'][:200]  # Limitar a 200 caracteres
                    cvss = v['cvss'] if v['cvss'] != "N/A" else "No asignado"
                    informe.append(f"  - {v['cve_id']} (CVSS {cvss}): {descripcion}...")
        else:
            informe.append("  → Sin vulnerabilidades encontradas.")

    # Servicios activos
    informe.append("\n[+] Servicios activos:")
    for s in get_running_services()[:10]:
        informe.append(f"   {s['Nombre']} (PID {s['PID']})")

    # Puertos abiertos
    informe.append("\n[+] Puertos abiertos:")
    for p in get_open_ports():
        informe.append(f"   {p['IP']}:{p['Puerto']}")

    # Imprimir en consola
    for linea in informe:
        print(linea)

    # Exportar a archivo si es necesario
    if exportar_a_archivo:
        with open("info_vulner.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(informe))
        print("\n[+] Informe exportado a 'info_vulner.txt'")

# Punto de entrada principal
if __name__ == "__main__":
    generar_informe(exportar_a_archivo=True)

