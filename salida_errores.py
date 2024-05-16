import pandas 

def generar_archivo_errores_o_csv(errores: list, datos: pandas.DataFrame, nombre_archivo: str):
    """
    Genera un archivo de texto con los errores si la lista de errores no está vacía.
    Si la lista de errores está vacía, genera un archivo CSV a partir del DataFrame datos.

    Parámetros:
    errores (list): Una lista de errores.
    datos (pandas.DataFrame): El DataFrame a convertir en CSV.
    nombre_archivo (str): El nombre del archivo a generar.

    Returns:
    None

    """
    if errores:
        with open('errores.txt', 'w') as f:
            for error in errores:
                f.write(f"{error}\n")
    else:
        datos.to_csv(nombre_archivo, index=False)