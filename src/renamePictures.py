import os
import time

def rename_pictures_in_dir(path):
    if not path:
        raise ValueError("Ruta no especificada")

    if not os.path.isdir(path):
        raise FileNotFoundError(f"La ruta especificada no es válida: {path}")

    extensiones = ('.jpg', '.jpeg', '.bmp', '.png', '.gif', '.tiff')
    archivos = [f for f in os.listdir(path) if f.lower().endswith(extensiones)]
    archivos.sort()

    if not archivos:
        raise FileNotFoundError("No se encontraron imágenes en la carpeta seleccionada.")

    renamed_files = []
    
    for archivo in archivos:
        try:
            extension = os.path.splitext(archivo)[1]
            timestamp = int(time.time() * 1000)
            nuevo_nombre = f"{timestamp}{extension}"
            ruta_original = os.path.join(path, archivo)
            ruta_nueva = os.path.join(path, nuevo_nombre)

            # Intentar renombrar varias veces con un retraso
            success = False
            for _ in range(3):
                try:
                    os.rename(ruta_original, ruta_nueva)
                    renamed_files.append((archivo, nuevo_nombre))
                    success = True
                    break  # Renombrado exitoso, salir del bucle
                except OSError:
                    time.sleep(0.1)  # Esperar un poco antes de intentar de nuevo
            
            if not success:
               # Optamos por no romper todo el proceso si uno falla, pero podríamos loguearlo
               # O en este diseño, podríamos levantar una warning.
               # Para mantener simplicidad, solo reportamos los que sí se lograron.
               pass

        except Exception as ex:
             # Igual que arriba, un fallo en un archivo no debería detener todo necesariamente,
             # pero si es crítico, raise. Aquí dejaremos que continue.
             pass

    return renamed_files