import shutil
import os
import sys
import pandas
from datetime import datetime
from tqdm import tqdm



def leer_csv(nombre_archivo : str, separador: str):
    """
    Lee un archivo CSV y devuelve un DataFrame.

    Parámetros:
    nombre_archivo (str): El nombre del archivo CSV a leer.
    separador (str): El separador de campos en el archivo CSV.

    Returns:
    df (pd.DataFrame): El DataFrame resultante.
    """
    # Obtén el número total de líneas del archivo
    num_lines = sum(1 for l in open(nombre_archivo, 'r', encoding='utf-8'))

    # Define el tamaño del chunk
    chunk_size = 10000

    # Crea un objeto tqdm para mostrar la barra de progreso
    progress_bar = tqdm(total=num_lines, desc="Leyendo CSV", bar_format='{l_bar}{bar:30}{r_bar}', colour='yellow')

    # Lee el archivo CSV en chunks y actualiza la barra de progreso
    chunks = []
    for chunk in pandas.read_csv(nombre_archivo, chunksize=chunk_size, sep=separador, encoding='utf-8'):
        chunks.append(chunk)
        progress_bar.update(chunk_size)

    # Cierra la barra de progreso
    progress_bar.close()

    # Combina los chunks en un solo DataFrame
    df = pandas.concat(chunks, axis=0)

    return df



#   mover_archivos('entrada.csv'          , 'salida.csv'               , 'paraBackup'            , 'paraDW')
def mover_archivos(nombre_archivo_entrada, nombre_archivo_salida, nueva_ubicacion_original, nueva_ubicacion_transformado):
    try:
        
        # ------------------------ DEFINICIONES DE NOMBRES ARCHIVOS Y DIRECTORIOS ------------------------------------
  
        # print("Ubicación del ejecutable: ", sys.executable)
        # cuando se va a generar un ejectuable hay que usar sys.executable ya que el ejecutable genera un directorio temporal y 
        # se pierde la ubicacion del archivo por lo que hay que descomentar la siguiente linea para generar el ejecutable
        #base_dir = os.path.dirname(sys.executable)  ## esto sirve para hacer el ejecutable
        
        # cuando no se usa un archivo ejecutable se debe usar la siguiente linea, si se va generar el ejecutable
        # base_dir = os.path.dirname(os.path.abspath(__file__))


        #  ESTO LO QUE HACE EN ASIGNAR DINAMICA EL BASE_DIR, SI SE ESTA EJECUTANDO UN SCRIPT ENTONCES USA LA SEGUNDA LINEA DEL IF SI SE ESTA EJECUTNADO
        # UN JECUTABLE ENTONCES USA LA PRIMER LINEA DEL IF
        if getattr(sys, 'frozen', False):
            # El programa se está ejecutando como un ejecutable empaquetado con PyInstaller
            base_dir = os.path.dirname(sys.executable)
        else:
            # El programa se está ejecutando como un script
            base_dir = os.path.dirname(os.path.abspath(__file__))


        # './entrada.csv'
        # directorio_original_y_nombre_entrada = os.path.normpath(nombre_archivo_entrada)
        # print("nombre archivo entrada", directorio_original_y_nombre_entrada)
        directorio_original_y_nombre_entrada = os.path.normpath(os.path.join(base_dir, nombre_archivo_entrada))
        
        # './salida.csv' 
        # directorio_original_y_nombre_salida = os.path.normpath(nombre_archivo_salida)  
        # print("nombre archivo salida", directorio_original_y_nombre_salida)      
        directorio_original_y_nombre_salida = os.path.normpath(os.path.join(base_dir, nombre_archivo_salida))

        # './paraBackup' 
        # directorio_paraBackup = os.path.normpath(nueva_ubicacion_original)  
        # print("directorio para backup ", directorio_paraBackup)     
        directorio_paraBackup = os.path.normpath(os.path.join(base_dir, nueva_ubicacion_original))
        
        # './paraDW'
        # directorio_paraDW = os.path.normpath(nueva_ubicacion_transformado)
        # print("directorio para DW ", directorio_paraDW)        
        directorio_paraDW = os.path.normpath(os.path.join(base_dir, nueva_ubicacion_transformado))


        # ---------------------- CREACION DIRECTORIOS DESTINO y COPIA ARCHIVOS ORIGINALES-------------------------------------------
        # './paraBackup' 
        os.makedirs(directorio_paraBackup, exist_ok=True)
        
        # './paraAnalisis'
        os.makedirs(directorio_paraDW, exist_ok=True)


        # print("inicio copia archivos originales")
        # copia './entrada.csv'  en la ruta './paraBackup' 
        # shutil.copy2(directorio_original_y_nombre_entrada, directorio_paraBackup)
        
        # copia './salida.csv'  en la ruta './paraDW'
        # shutil.copy2(directorio_original_y_nombre_salida, directorio_paraDW)
        
        # print("fin copia archivos originales")
        # input("presione enter para continuar")
        
        
        # ---------------------- RENOMBRADO ARCHIVOS-------------------------------------------

        # obtengo la fecha actual por ej 2024-05-13
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # genero una variable con el nombre:   2024-05-13_entrada.csv
        nombre_archivo_fecha_entrada_csv = f"{fecha_actual}_{os.path.basename(nombre_archivo_entrada)}"
       
        
        # genero una variable con el nombre:  2024-05-13_salida.csv
        nombre_archivo_fecha_salida_csv = f"{fecha_actual}_{os.path.basename(nombre_archivo_salida)}"
       


        # genero una variable con el nombre: ./paraBackup/2024-05-13_entrada.csv
        directorio_paraBackup_fecha_entrada_csv = os.path.join(directorio_paraBackup, nombre_archivo_fecha_entrada_csv)
        
        
        # genero una varialbe con el nombre ./paraAnalisis/2024-05-13_salida.csv
        directorio_paraDW_fecha_salida_csv = os.path.join(directorio_paraDW, nombre_archivo_fecha_salida_csv)
        
        

        # Si el archivo de destino ya existe, se borra
        # ./paraBackup/2024-05-13_entrada.csv
        if os.path.exists(directorio_paraBackup_fecha_entrada_csv):
            os.remove(directorio_paraBackup_fecha_entrada_csv)    
   

       
        #     ./entrada.csv    , ./paraBackup/2024-05-13_entrada.csv
        shutil.copy2(directorio_original_y_nombre_entrada, directorio_paraBackup_fecha_entrada_csv)
        os.remove(directorio_original_y_nombre_entrada)  
        
        
            

        # Si el archivo de destino ya existe, se borra 
        # ./paraAnalisis/2024-05-13_salida.csv
        if os.path.exists(directorio_paraDW_fecha_salida_csv):
            os.remove(directorio_paraDW_fecha_salida_csv)
            

        #            './entrada.csv'                    , 
        shutil.copy2(directorio_original_y_nombre_salida, directorio_paraDW_fecha_salida_csv )        
        os.remove(directorio_original_y_nombre_salida)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    


def generar_archivo_csv(df: pandas.DataFrame, nombre_archivo: str):
    """
    Genera un archivo CSV a partir de un DataFrame.

    Parámetros:
    dataframe (pd.DataFrame): El DataFrame a convertir en CSV.
    nombre_archivo (str): El nombre del archivo CSV a generar.

    Returns:
    None

    """
    try:
        # Crear una barra de progreso
        with tqdm(total=len(df), desc="Generando CSV", ncols=100, bar_format='{l_bar}{bar:30}{r_bar}', colour='yellow') as pbar:
            for index, row in df.iterrows():
                # Actualizar la barra de progreso
                pbar.update()
                # Aquí puedes hacer cualquier procesamiento que necesites con la fila

        # Guardar el DataFrame como CSV
        df.to_csv(nombre_archivo, index=False, sep=';')
        print(f"Archivo {nombre_archivo} generado con éxito.")
    except Exception as e:
        print(f"Error al generar el archivo CSV: {e}")

def mover_pdfs(directorio_origen, directorio_destino):
    """
    Mueve todos los archivos PDF de un directorio a otro.

    Parámetros:
    directorio_origen (str): El directorio de donde se moverán los archivos PDF.
    directorio_destino (str): El directorio a donde se moverán los archivos PDF.

    Devuelve:
    None
    """
    if getattr(sys, 'frozen', False):
    # El programa se está ejecutando como un ejecutable empaquetado con PyInstaller
        base_dir = os.path.dirname(sys.executable)
    else:
    # El programa se está ejecutando como un script
        base_dir = os.path.dirname(os.path.abspath(__file__))
    

    directorio_origen= os.path.normpath(os.path.join(base_dir, directorio_origen))
    directorio_destino = os.path.normpath(os.path.join(base_dir,directorio_destino))
    
    # Asegúrate de que el directorio de destino exista
    os.makedirs(directorio_destino, exist_ok=True)

    # Recorre todos los archivos en el directorio de origen
    for nombre_archivo in os.listdir(directorio_origen):
        # Si el archivo es un PDF
        if nombre_archivo.endswith('.pdf'):
            # Construye las rutas completas del archivo en el origen y el destino
            ruta_origen = os.path.join(directorio_origen, nombre_archivo)
            ruta_destino = os.path.join(directorio_destino, nombre_archivo)

            # Mueve el archivo
            shutil.move(ruta_origen, ruta_destino)