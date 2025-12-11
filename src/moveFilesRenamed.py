import os
import re
import shutil

def move_files_renamed(carpeta, progress_callback=None):
    if carpeta is None:
        raise ValueError("No se seleccionó ninguna carpeta.")

    archivos = os.listdir(carpeta)
    total_archivos = len(archivos)
    archivos_validos = 0

    # Primero validamos si hay archivos para mover
    for archivo in archivos:
        if archivo.lower().endswith(('.xml', '.pdf')):
            match = re.match(r"(\d{2})\.(\d{2})\.(\d{4})_([A-Z0-9]+)_([A-Z0-9]+)_FACTURA\.(xml|pdf)", archivo, re.I)
            if match:
                archivos_validos += 1

    if archivos_validos == 0:
        raise ValueError("No se encontraron archivos con el formato de nombre correcto. Renombre los archivos primero.")

    for i, archivo in enumerate(archivos):
        if archivo.lower().endswith(('.xml', '.pdf')):
            match = re.match(r"(\d{2})\.(\d{2})\.(\d{4})_([A-Z0-9]+)_([A-Z0-9]+)_FACTURA\.(xml|pdf)", archivo, re.I)
            if match:
                try:
                    dia, mes, anio, emisor, uuid, extension = match.groups()
                except ValueError as ve:
                    print(f"Error al desempaquetar valores del archivo {archivo}: {str(ve)}")
                    continue
                
                ruta_final = os.path.join(carpeta, anio, name_month(mes), emisor)
                if not os.path.exists(ruta_final):
                    os.makedirs(ruta_final)
                
                archivo_origen = os.path.join(carpeta, archivo)
                archivo_destino = os.path.join(ruta_final, archivo)
                
                if os.path.exists(archivo_destino):
                    archivo_destino = os.path.join(ruta_final, f"_dup{archivo}")
                
                try:
                    shutil.move(archivo_origen, archivo_destino)
                except Exception as e:
                    print(f"No se pudo mover {archivo_origen} a {archivo_destino}: {str(e)}")
            else:
                pass # Archivo no coincide, lo ignoramos

        # Actualizar barra de progreso usando el callback si existe
        if progress_callback:
            porcentaje_avance = (i + 1) / total_archivos
            progress_callback(porcentaje_avance)

    return True

def name_month(mes):
    meses = {
        "01": "01. Enero", "02": "02. Febrero", "03": "03. Marzo", "04": "04. Abril",
        "05": "05. Mayo", "06": "06. Junio", "07": "07. Julio", "08": "08. Agosto",
        "09": "09. Septiembre", "10": "10. Octubre", "11": "11. Noviembre", "12": "12. Diciembre"
    }
    return meses.get(mes, "Mes no encontrado")