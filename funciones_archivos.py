import shutil
import os
from datetime import datetime

def mover_archivos(nombre_archivo_original, nombre_archivo_transformado, nueva_ubicacion_original, nueva_ubicacion_transformado):
    """
    Mueve el archivo original a una nueva ubicación y luego mueve el archivo transformado a otra ubicación.
    Agrega la fecha actual al nombre del archivo en el formato 'yyyy-mm-dd' después de moverlos.

    Parámetros:
    nombre_archivo_original (str): El nombre del archivo original.
    nombre_archivo_transformado (str): El nombre del archivo transformado.
    nueva_ubicacion_original (str): La nueva ubicación para el archivo original.
    nueva_ubicacion_transformado (str): La nueva ubicación para el archivo transformado.

    Returns:
    bool: True si la operación fue exitosa, False si hubo un error.

    """
    try:
        # Obtener la ruta al directorio del script
        base_dir = os.path.dirname(__file__)

        # Construir las rutas completas de los archivos
        ruta_original = os.path.normpath(os.path.join(base_dir, nombre_archivo_original))
        ruta_nueva_original = os.path.normpath(os.path.join(base_dir, nueva_ubicacion_original, nombre_archivo_original))
        ruta_transformado = os.path.normpath(os.path.join(base_dir, nombre_archivo_transformado))
        ruta_nueva_transformado = os.path.normpath(os.path.join(base_dir, nueva_ubicacion_transformado, nombre_archivo_transformado))

        # Crear los directorios si no existen
        os.makedirs(os.path.dirname(ruta_nueva_original), exist_ok=True)
        os.makedirs(os.path.dirname(ruta_nueva_transformado), exist_ok=True)

        # Mover el archivo original a la nueva ubicación
        shutil.move(ruta_original, ruta_nueva_original)

        # Mover el archivo transformado a la nueva ubicación
        shutil.move(ruta_transformado, ruta_nueva_transformado)

        # Obtener la fecha actual en el formato 'yyyy-mm-dd'
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # Agregar la fecha actual al nombre del archivo
        nombre_archivo_original_con_fecha = f"{fecha_actual}_{nombre_archivo_original}"
        nombre_archivo_transformado_con_fecha = f"{fecha_actual}_{nombre_archivo_transformado}"

        # Construir las rutas completas de los archivos con la fecha
        ruta_nueva_original_con_fecha = os.path.normpath(os.path.join(base_dir, nueva_ubicacion_original, nombre_archivo_original_con_fecha))
        ruta_nueva_transformado_con_fecha = os.path.normpath(os.path.join(base_dir, nueva_ubicacion_transformado, nombre_archivo_transformado_con_fecha))

        # Renombrar los archivos para agregar la fecha
        os.rename(ruta_nueva_original, ruta_nueva_original_con_fecha)
        os.rename(ruta_nueva_transformado, ruta_nueva_transformado_con_fecha)

        # Si todo salió bien, devolver True
        return True
    except Exception as e:
        # Si hubo un error, devolver False
        print(f"Error: {e}")
        return False