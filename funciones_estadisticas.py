import pandas
import numpy as np

def calcular_estadisticas(df: pandas.DataFrame , estadisticas : dict):
    """
    Calcula estadísticas para cada columna numérica en un DataFrame de pandas.

    Parámetros:
    df (pandas.DataFrame): El DataFrame para el cual calcular las estadísticas.
    estadisticas (dict): El diccionario donde se almacenarán las estadísticas.

    Returns:
    None

    """
    # Obtener las columnas numéricas del DataFrame
    columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

    # Inicializar las listas en el diccionario de estadísticas
    estadisticas['columna'] = []
    estadisticas['maximo'] = []
    estadisticas['minimo'] = []
    estadisticas['media'] = []
    estadisticas['desviacion_estandar'] = []
    estadisticas['mediana'] = []
    estadisticas['moda'] = []
    estadisticas['cantidad_total'] = []  # Cambiado a 'cantidad_total'
    estadisticas['nulos'] = []  # Nueva lista para la cantidad de valores nulos
    estadisticas['repetidos'] = []  # Nueva lista para la cantidad de valores repetidos
    estadisticas['unicos'] = []  # Nueva lista para la cantidad de valores únicos

    # Calcular las estadísticas para cada columna numérica
    for columna in columnas_numericas:
        maximo = round(df[columna].max(), 2) if not pandas.isna(df[columna].max()) else np.nan
        minimo = round(df[columna].min(), 2) if not pandas.isna(df[columna].min()) else np.nan
        
        # Si la columna tiene valores y no todos son NaN, entonces se calcula la media
        if df[columna].count() > 0 and not df[columna].isna().all():
            media = round(df[columna].mean(), 2)
        else:
            media = np.nan
        
        desviacion_estandar = round(df[columna].std(), 2) if not pandas.isna(df[columna].std()) else np.nan
        mediana = round(df[columna].median(), 2) if not pandas.isna(df[columna].median()) else np.nan
        moda = round(df[columna].mode()[0], 2) if not df[columna].mode().empty and not pandas.isna(df[columna].mode()[0]) else np.nan
        cantidad_total = df[columna].count()  # Cantidad de valores no nulos
        nulos = df[columna].isnull().sum()  # Cantidad de valores nulos
        repetidos = df[columna].duplicated().sum()  # Cantidad de valores repetidos
        unicos = df[columna].nunique()  # Cantidad de valores únicos

        # Agregar las estadísticas al diccionario
        estadisticas['columna'].append(columna)
        estadisticas['maximo'].append(maximo)
        estadisticas['minimo'].append(minimo)
        estadisticas['media'].append(media)
        estadisticas['desviacion_estandar'].append(desviacion_estandar)
        estadisticas['mediana'].append(mediana)
        estadisticas['moda'].append(moda)
        estadisticas['cantidad_total'].append(cantidad_total)  # Agregar la cantidad_total al diccionario
        estadisticas['nulos'].append(nulos)  # Agregar la cantidad de nulos al diccionario
        estadisticas['repetidos'].append(repetidos)  # Agregar la cantidad de repetidos al diccionario
        estadisticas['unicos'].append(unicos)  # Agregar la cantidad de únicos al diccionario