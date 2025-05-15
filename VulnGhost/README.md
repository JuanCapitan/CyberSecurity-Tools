# VulnGhost

VulnGhost es una herramienta de análisis de vulnerabilidades automatizado, escrita en Python, que recolecta información del sistema, escanea software instalado contra la base de datos NVD y genera un informe detallado.

## Estructura de archivos

```text
VulnGhost/
├── README.md
├── requirements.txt
├── .gitignore
├── config_example.yaml
└── VulnGhost.py
```

* **VulnGhost.py**: Script principal para escaneo de vulnerabilidades.
* **config\_example.yaml**: Plantilla de configuración para la API Key y parámetros.

## Uso

1. Clona o sitúa la carpeta `VulnGhost` en tu máquina:

   ```bash
   git clone https://github.com/<tu-usuario>/cybersecurity-tools.git
   cd cybersecurity-tools/VulnGhost
   ```

2. Instala las dependencias:

   ```bash
   # Usando pip directamente
   pip install -r requirements.txt
   # O, si tienes varias versiones de Python instaladas:
   python -m pip install -r requirements.txt
   ```

## Archivos del proyecto

* **README.md**: Documentación de instalación y uso.

* **requirements.txt**: Dependencias necesarias.

  ```text
  psutil
  requests
  PyYAML
  ```

* **.gitignore**: Patrones de archivos a ignorar por Git:

  ```text
  __pycache__/
  *.pyc
  config.yaml
  informe_vulnerabilidades.txt
  .env
  ```

* **config\_example.yaml**: Ejemplo de configuración:

  ```yaml
  # config_example.yaml
  nvd_api_key: TU_API_KEY_AQUI
  max_software: 10
  output_file: informe_vulnerabilidades.txt
  ```

## Futuras mejoras

* Exportar informe a PDF (reportlab / WeasyPrint).
* Envío de notificaciones (Telegram, email).
* Dashboard web con Flask para visualización en tiempo real.

---

*VulnGhost: tu asistente de ciberdefensa para identificar vulnerabilidades de forma sencilla y eficaz.*
