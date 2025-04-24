# 🔍 Escáner de Red Local en Python

Este script realiza un escaneo de red en una subred del tipo `/24` (ej: `192.168.1.0/24`) utilizando múltiples hilos (`threading`) y comandos `ping` para detectar dispositivos activos en la red local. 

## ⚙️ Características

- Escaneo multihilo para mayor velocidad.
- Detección de dispositivos activos mediante `ping`.
- Progreso dinámico del escaneo.
- Compatible con Windows, Linux y macOS.
- Manejo de errores y entrada del usuario robusta.

---

## 🖥️ ¿Cómo funciona?

1. El usuario ingresa la subred base (ejemplo: `192.168.0`).
2. Se inicia un escaneo a las direcciones IP desde `.1` hasta `.254`.
3. Se crea un hilo por IP, enviando un `ping` para verificar si está activa.
4. Los dispositivos activos son guardados y mostrados al finalizar el escaneo.

---

## 🚀 Uso

### Requisitos
- Python 3.x
- Sistema operativo con soporte para el comando `ping`

### Ejecutar desde consola:

```bash
python escaner_red.py
