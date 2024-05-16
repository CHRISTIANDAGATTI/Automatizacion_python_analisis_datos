import pandas

def funcion_string_a_fecha(dataFrame: pandas.DataFrame, Lista_errores: list, column_name: str ):
    """
    Convierte una columna de cadenas a datetime en un DataFrame de pandas y cambia el formato de la fecha a 'dd/mm/yyyy'.

    La columna puede tener fechas en diferentes formatos, como 'yyyy-mm-dd hh:mm:ss.s', 'yyyy-mm-dd', 'dd-mm-yyyy', 'yyyy/mm/dd hh:mm:ss.s', 'yyyy/mm/dd' o 'dd/mm/yyyy'.

    Args:
        dataFrame (pandas.DataFrame): El DataFrame que contiene los datos.
        Lista_errores (list): Una lista para almacenar cualquier error encontrado durante la conversión.
        column_name (str): El nombre de la columna a convertir.

    Returns:
        pandas.DataFrame: El DataFrame con la columna especificada convertida a datetime y formateada.

    Raises:
        Exception: Si ocurre un error durante la conversión, se agrega el mensaje de error a la lista `Lista_errores`.
    """
    # Obtener el nombre de la función
    function_name = funcion_string_a_fecha.__name__

    try:
        if dataFrame[column_name].dtype != 'datetime64[ns]':
            dataFrame[column_name] = pandas.to_datetime(dataFrame[column_name], errors='coerce')
            dataFrame[column_name] = dataFrame[column_name].dt.strftime('%d/%m/%Y')
            
    except Exception as e:
        Lista_errores.append(f"{function_name}: {str(e)} en la columna '{column_name}'.")
    
    return dataFrame




def funcion_string_a_float(dataFrame: pandas.DataFrame, Lista_errores: list, column_name: str ):
    """
    Convierte una columna de cadenas a float en un DataFrame de pandas.

    Args:
        dataFrame (pandas.DataFrame): El DataFrame que contiene los datos.
        Lista_errores (list): Una lista para almacenar cualquier error encontrado durante la conversión.
        column_name (str): El nombre de la columna a convertir.

    Returns:
        pandas.DataFrame: El DataFrame con la columna especificada convertida a float.

    Raises:
        Exception: Si ocurre un error durante la conversión, se agrega el mensaje de error a la lista `errores`.
    """
    # Obtener el nombre de la función
    function_name = funcion_string_a_float.__name__

    try:
        if dataFrame[column_name].dtype != 'object':
            dataFrame[column_name] = dataFrame[column_name].astype(str)

            # Realiza la operación de reemplazo y convierte a float
            dataFrame[column_name] = dataFrame[column_name].str.replace(',','.')
            dataFrame[column_name] = dataFrame[column_name].astype(float)
    except Exception as e:
        Lista_errores.append(f"{function_name}: {str(e)} en la columna '{column_name}'.")
    
    return dataFrame



def funcion_str_to_int(df: pandas.DataFrame, error_list: list, column_name: str):
    """
    Convierte una columna de cadenas a enteros en un DataFrame de pandas.

    Args:
        df (pandas.DataFrame): El DataFrame que contiene los datos.
        error_list (list): Una lista para almacenar cualquier error encontrado durante la conversión.
        column_name (str): El nombre de la columna a convertir.

    Returns:
        pandas.DataFrame: El DataFrame con la columna especificada convertida a enteros.

    Raises:
        Exception: Si ocurre un error durante la conversión, se agrega el mensaje de error a la lista `error_list`.
    """
    # Obtener el nombre de la función
    function_name = funcion_str_to_int.__name__

    try:
        df[column_name] = pandas.to_numeric(df[column_name], errors='coerce').astype('Int64')
    except Exception as e:
        error_list.append(f"{function_name}: {str(e)} en la columna '{column_name}'.")
    
    return df



def funcion_float_to_str(df: pandas.DataFrame, error_list: list, column_name: str):
    """
    Convierte una columna de numeros decimales a cadenas en un DataFrame de pandas.

    Args:
        df (pandas.DataFrame): El DataFrame que contiene los datos.
        error_list (list): Una lista para almacenar cualquier error encontrado durante la conversión.
        column_name (str): El nombre de la columna a convertir.

    Returns:
        pandas.DataFrame: El DataFrame con la columna especificada convertida a cadena.

    Raises:
        Exception: Si ocurre un error durante la conversión, se agrega el mensaje de error a la lista `error_list`.
    """
    # Obtener el nombre de la función
    function_name = funcion_str_to_int.__name__

    try:
        df[column_name] = pandas.to_numeric(df[column_name], errors='coerce').astype(str)
    except Exception as e:
        error_list.append(f"{function_name}: {str(e)} en la columna '{column_name}'.")
    
    return df


def convertir_tipos_datos(df: pandas.DataFrame, dtype_dict: dict, error: list):
    """
    Convierte los tipos de datos de las columnas en un DataFrame de acuerdo a un diccionario dado.

    Parámetros:
    df (pandas.DataFrame): El DataFrame cuyos tipos de datos se van a convertir.
    dtype_dict (dict): Un diccionario donde las claves son nombres de columnas y los valores son los tipos de datos deseados.
    error (list): Una lista para almacenar los mensajes de error.

    Returns:
    df (pandas.DataFrame): El DataFrame con los tipos de datos convertidos.
    """
    # Obtener el nombre de la función
    function_name = convertir_tipos_datos.__name__

    for columna, dtype in dtype_dict.items():
        if columna in df.columns:
            try:
                df[columna] = df[columna].astype(dtype)
            except ValueError:
                error_message = f"{function_name}: Error al convertir la columna '{columna}' a {dtype}"
                error.append(error_message)
        else:
            error_message = f"{function_name}: La columna '{columna}' no existe en el DataFrame."
            error.append(error_message)
    return df