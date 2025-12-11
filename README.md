# Factura Tools

Herramienta de escritorio desarrollada en Python con Flet para renombrar y organizar facturas XML/PDF.

## Estructura del Proyecto

El proyecto sigue una estructura moderna de paquetes Python:

```
factura-tools/
├── src/
│   ├── main.py            # Punto de entrada de la aplicación
│   ├── ui/                # Lógica de Interfaz de Usuario (Flet)
│   │   ├── __init__.py
│   │   └── app_window.py  # Ventana principal
│   ├── processFiles.py    # Lógica de procesamiento de facturas
│   ├── renamePictures.py  # Lógica de renombardo de imágenes
│   └── ...                # Otros módulos de lógica backend
├── pyproject.toml         # Configuración del proyecto y dependencias
├── requirements.txt       # Lista de dependencias (legacy)
└── README.md
```

## Instalación

Se recomienda instalar el proyecto en modo editable dentro de un entorno virtual:

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv .venv
# Activar entorno (Windows)
.venv\Scripts\activate

# Instalar dependencias y el proyecto
pip install -e .
```

## Ejecución

Para iniciar la aplicación, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python -m src.main
```

## Funcionalidades

1.  **Renombrar Imágenes**: Renombra masivamente imágenes con timestamp para evitar duplicados.
2.  **Renombrar Facturas**: Escanea una carpeta en busca de XML/PDF, extrae datos del XML (Fecha, Emisor, UUID) y renombra ambos archivos siguiendo un formato estandarizado. Genera un reporte en Excel.
3.  **Organizar Facturas**: Mueve las facturas renombradas a una estructura de carpetas `Año/Mes/Emisor`.

## Tecnologías

-   **Python 3.x**
-   **Flet**: Framework de UI.
-   **Pandas & OpenPyXL**: Generación de reportes Excel.
-   **PyMuPDF**: Procesamiento de PDFs.
-   **Unidecode**: Manejo de caracteres especiales.
