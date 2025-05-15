# Keylogger007 – Registro de Teclas y Capturas de Pantalla

> ⚠️ **Uso autorizada y ética solamente.** Este script es para auditorías de seguridad con consentimiento. No nos hacemos responsables del uso indebido.

---

## 📖 Descripción

`Keylogger007` es un script en Python que:

1. **Registra pulsaciones de tecla** (alfanuméricas y espacios).  
2. **Toma capturas de pantalla** a intervalos regulares.  
3. **Envía** todos los registros y capturas por correo electrónico al finalizar el tiempo de ejecución.  
4. **Limpia** automáticamente los archivos locales tras el envío.

Ideal para pruebas de auditoría en entornos controlados.

---

## 🛠️ Características

- Captura de teclas usando `pynput`.  
- Capturas de pantalla con `PIL.ImageGrab`.  
- Configuración flexible por línea de comandos (`argparse`).  
- Hilos independientes para teclado y pantalla (`threading.Thread`).  
- Envío SMTP a través de Gmail.  
- Limpieza automática de archivos tras el envío.

---

## 📦 Requisitos

- **Python** 3.6+  
- Módulos Python:
  ```bash
  pip install pynput pillow
