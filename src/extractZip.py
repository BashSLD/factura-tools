import os
import zipfile

def process_zip_files(path: str):
    try:
        if not os.path.isdir(path):
            raise FileNotFoundError(f"La ruta especificada no existe: {path}")

        archivos_zip = [f for f in os.listdir(path) if f.lower().endswith('.zip')]
        if not archivos_zip:
            return  # No se encontraron archivos zip, no hacemos nada (pero no es error)

        extracted_count = 0
        for zip_file in archivos_zip:
            ruta_zip = os.path.join(path, zip_file)
            try:
                with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                    zip_ref.extractall(path)
                    extracted_count += 1
            except zipfile.BadZipFile:
                raise ValueError(f"El archivo {zip_file} no es un archivo ZIP válido.")
            except Exception as e:
                raise Exception(f"Error al extraer {zip_file}: {str(e)}")
        
        return extracted_count

    except Exception:
        raise