# Network Scanner – Proyecto de Comprobación de Conectividad

Este proyecto es una utilidad sencilla en Python para:

- Comprobar la conectividad con el router local.  
- Verificar acceso a Internet (ping a 8.8.8.8).  
- Resolver nombres de dominio (DNS lookup).  
- Recopilar información de interfaces de red (usando `psutil`).  
- Escanear puertos locales abiertos (1–1024).  
- Registrar todo el flujo de trabajo en un archivo de texto.

---

## Estructura de archivos

- **`network_scanner.py`**  
  Script principal con todas las funciones de escaneo y registro.  
- **`test_simple.py`**  
  Test básico con `unittest` para validar la función de escritura en archivo.  
- **`resultados_red.txt`**  
  Archivo de salida donde se van acumulando los resultados de cada prueba.  
- **`.gitignore`**  
  Para excluir `__pycache__/`, logs temporales y otros archivos generados.

---

## Requisitos

- **Python 3.x**  
- **Dependencias**  
  ```bash
  pip install psutil
