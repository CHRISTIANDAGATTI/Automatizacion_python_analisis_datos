import pandas
import re

def control_cantidad_registros(archivo_csv, df: pandas.DataFrame, error:list):
    """
    Compara la cantidad de registros en un DataFrame dado y un archivo CSV.

    Parámetros:
    archivo_csv (str): La ruta al archivo CSV que se va a comparar.
    df (pandas.DataFrame): El DataFrame que se va a comparar.
    error (list): Una lista para almacenar los mensajes de error.

    Returns:
    None

    """
    # Obtener el nombre de la función
    function_name = control_cantidad_registros.__name__

    # Cargar el archivo CSV en un nuevo DataFrame
    csv_df = pandas.read_csv(archivo_csv, sep=';')

    # Comparar la cantidad de registros
    if len(df) != len(csv_df):
        error_message = f"{function_name}: La cantidad de registros no coincide: DataFrame tiene {len(df)} registros, CSV tiene {len(csv_df)} registros"
        error.append(error_message)
    # else:
    #     print("La cantidad de registros coincide")
    
    
def control_nombre_columnas(df, dtype_dict, error):
    """
    Verifica si todos los nombres de las columnas de un DataFrame están en un diccionario dado.

    Parámetros:
    df (pandas.DataFrame): El DataFrame cuyos nombres de columnas se van a verificar.
    dtype_dict (dict): Un diccionario donde las claves son nombres de columnas.
    error (list): Una lista para almacenar los mensajes de error.

    Returns:
    bool: True si todos los nombres de las columnas están en el diccionario, False de lo contrario.
    """
    columnas_df = set(df.columns)
    columnas_dict = set(dtype_dict.keys())
    
    if not columnas_df.issubset(columnas_dict):
        columnas_no_encontradas = columnas_df - columnas_dict
        for columna in columnas_no_encontradas:
            error_message = f"La columna '{columna}' no está en el diccionario."
            error.append(error_message)
        return False
    return True



def verificar_vacios_o_nulos(df, estaditicas: dict):
    """
    Verifica si hay valores nulos o vacíos en un DataFrame dado.

    Parámetros:
    df (pandas.DataFrame): El DataFrame a verificar.
    estaditicas (dict): Un diccionario para almacenar los mensajes de error.

    Returns:
    None

    """
    # Obtener el nombre de la función
    function_name = verificar_vacios_o_nulos.__name__

    # Verificar cada columna
    for columna in df.columns:
        # Contar valores nulos
        nulos = df[columna].isnull().sum()
        if nulos > 0:
            message = f"{function_name}: La columna '{columna}' contiene {nulos} valores nulos."
            estaditicas.setdefault('mensajes', []).append(message)

        # Contar valores vacíos
        vacios = df[columna].astype(str).str.strip().eq('').sum()
        if vacios > 0:
            message = f"{function_name}: La columna '{columna}' contiene {vacios} valores vacíos."
            estaditicas.setdefault('mensajes', []).append(message)
            
            
            

def comparar_tipo_datos_dataframe_csv(df: pandas.DataFrame, resultado: list, dtype_dict_esperado: dict):
    """
    Compara los tipos de datos en un DataFrame dado con un diccionario de tipos de datos esperados.
    Parámetros:
    df (pandas.DataFrame): El DataFrame cuyos tipos de datos se van a comparar.
    resultado (list): Una lista para almacenar los resultados.
    dtype_dict_esperado (dict): Un diccionario de tipos de datos esperados.
    Returns:
    None
    """
    # Obtener el nombre de la función
    function_name = comparar_tipo_datos_dataframe_csv.__name__
    # Comparar los tipos de datos
    for columna in df.columns:
        if columna in dtype_dict_esperado:
            # Obtener los tipos de datos únicos en la columna
            # unique_types es un array de numpy
            unique_types = df[columna].apply(type).unique()
            
            #conteo de nulos
            num_nulos = df[columna].isnull().sum()
            
            # Extraer el nombre del tipo de datos con una expresión regular
            # dtype_actual = re.search("'(.*)'", str(unique_types[0])).group(1)
            if (len(unique_types) > 1):
                dtype_actual = "multiples tipos"
            elif (num_nulos > 0):
                dtype_actual = "existen nulos"
            elif (len(unique_types) > 1 & num_nulos > 0):
                dtype_actual = "nulos / multiples tipos"
            elif (len(unique_types) == 1):
                dtype_actual = re.search("'(.*)'", str(unique_types[0])).group(1)
            else:
                dtype_actual ="controlar"
                
            # print (columna, dtype_actual, num_nulos)

            dtype_esperado = dtype_dict_esperado[columna]

            if dtype_actual == dtype_esperado:
                leyenda = "coincide"
            else:
                leyenda = "no coincide"
        else:
            dtype_actual = "No existe"
            dtype_esperado = "No existe"
            leyenda = "no coincide"
        
        resultado_dict = {
            "columna": columna,
            "dtype_esperado": dtype_esperado,
            "dtype_actual": dtype_actual,
            "leyenda": leyenda
        }

                
        resultado.append(resultado_dict)