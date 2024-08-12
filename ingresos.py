import pandas as pd
import warnings
import time


from funciones_conversion import funcion_string_a_fecha, funcion_string_a_float, funcion_str_to_int, convertir_tipos_datos
from funciones_controles import control_cantidad_registros, control_nombre_columnas, verificar_vacios_o_nulos, comparar_tipo_datos_dataframe_csv
from funciones_archivos import mover_archivos, generar_archivo_csv, leer_csv, mover_pdfs
from salida_errores import generar_archivo_errores_o_csv
from funciones_estadisticas import calcular_estadisticas
from funciones_pdf import generar_pdf_estadistico, generar_pdf_formatos, generar_pdf_cant_filas_y_nombre_columnas

# Ignorar las advertencias de RuntimeWarning
warnings.filterwarnings("ignore", category=RuntimeWarning)

input("El archivo que se va a leer se debe llamar entrada.csv, presione Enter para continuar...")

# Guarda el tiempo de inicio
start_time = time.time()

#   ------------------------ INICIO DEFINICION VARIABLES ---------------------------------

# diccionario de tipo de datos que espera el DW

       
dtype_dict_esperado = {
    'Nombre Regional': 'str',
    'Numero Oficial': 'str',
    'Razon Social': 'str',
    'Tipo Documento': 'str',
    'Dte': 'str',
    'Productor': 'str',
    'Renspa':'str',
    'Cuit Productor':'str',
    'Tipo Movimiento':'str',
    'Fecha Ingreso': 'str',
    'Eliminada':'int',
    'Intervenida':'int',
    'Tropa': 'int', 
    'Id Tropa': 'int',
    'Periodo': 'int',
    'Apta_para': 'str', 
    'Especie': 'str',
    'Cantidad Ingresada': 'int',
    'Cantidad Amparada': 'int',
    'Ticket Pesada': 'str',
    'Cuit Usuario Faena': 'str',
    'Nombre Usuario Faena': 'str',
    'Matricula RUCA':'int',
    'Establecimiento RUCA':'int',
    'CUIT Titular':'str',
    'Patente Chasis': 'str',
    'Precintos Chasis': 'str',
    'Patente Acoplado': 'str',
    'Precinto Acoplado': 'str'
}

# Definicion nombre de archivos entrada y salida
nombre_archivo_csv_entrada = 'entrada.csv'
nombre_archivo_csv_salida = 'salida.csv'


#   ------------------------ FIN DEFINICION VARIABLES --------------------------------------------------

#   ------------------------ INICIO CREACION LISTAS PARA GUARDAR DATOS ---------------------------------

# Creo una lista vacía para almacenar los errores por la transformacion de datos
errores_transformacion_datos = []

# Creo una lista vacía para almacenar los resultados de formatos
resultados_formato = []

# Creo una lista vacía para almacenar los resultados de cantidad de columnas y el nombre de las columnas 
resultados_cant_columnas_y_nombre_columnas = []

# Inicializa estadisticas como un diccionario vacío
estadisticas = {}

#   ------------------------ FIN CREACION LISTAS PARA GUARDAR DATOS ---------------------------------

#   ------------------------ INICIO LECTURA ARCHIVOS ------------------------------------------------

#Leo el archivo csv del sistema de archivos
datos =  leer_csv(nombre_archivo_csv_entrada, ';')
#datos = pd.read_csv(nombre_archivo_csv_entrada, sep=';') 
print("Inicio de transformaciones y generacion de archivos Pdf")
# datos = datos.astype(str) Pasar todo a string

#   ------------------------ FIN LECTURA ARCHIVOS ----------------------------------------

#   ------------------------ INICIO TRANSFORMACION DATOS ---------------------------------
# Filtrar columnas
datos = datos[list(dtype_dict_esperado.keys())]
datos = funcion_string_a_fecha(datos, errores_transformacion_datos, 'Fecha Ingreso') 
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Eliminada')
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Intervenida')
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Tropa')
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Id Tropa')
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Periodo')
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Cantidad Ingresada')
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Cantidad Amparada')
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Matricula RUCA')  
datos = funcion_str_to_int(datos, errores_transformacion_datos, 'Establecimiento RUCA') 

#   ------------------------ FIN TRANSFORMACION DATOS ---------------------------------

#   ------------------------ INICIO CONTROLES -----------------------------------------

#comparacion de tipo de datos y los resultados los envia a --> resultados_formato
comparar_tipo_datos_dataframe_csv(datos, resultados_formato, dtype_dict_esperado)

#comparacion de cantidad de registros y los resultados los envia a --> errores
control_cantidad_registros(nombre_archivo_csv_entrada, datos, resultados_cant_columnas_y_nombre_columnas)

#control nombre columnas y los resultados los envia a --> errores
control_nombre_columnas(datos, dtype_dict_esperado, resultados_cant_columnas_y_nombre_columnas)

#control vacios nulos  y los resultados los envia a --> estadisticas
# verificar_vacios_o_nulos(datos, estadisticas)

#   ------------------------ FINAL CONTROLES -------------------------------------

#   ------------------------ INICIO ESTADISTICAS ---------------------------------


#calculos estadisticas
calcular_estadisticas(datos, estadisticas)


#   ------------------------ FIN ESTADISTICAS --------------------------------------

#   ------------------------ INICIO GENERAR PDF ------------------------------------

generar_pdf_estadistico(estadisticas, 'estadisticas.pdf', 15, 'Reporte de estadisticas')

# esta funcion se debe ejecutar despues de la funcion -->  comparar_tipo_datos_dataframe_csv
generar_pdf_formatos(resultados_formato, 'formatos.pdf', 'Reporte de formatos')


# esta funcion genera pdf donde muestra si hubo columnas que no existen o la cant de filas de entrada y salida son distintas
generar_pdf_cant_filas_y_nombre_columnas(resultados_cant_columnas_y_nombre_columnas, 'cant_filas_y_nombre_columnas.pdf', 'Reporte de cantidad de filas y nombre de columnas')


mover_pdfs("./", "paraReportes")

print("Fin de transformaciones y generacion de archivos Pdf")

#   ------------------------ FIN GENERAR PDF ---------------------------------------


#   ------------------------ INICIO CREAR CSV --------------------------------------

# en este punto tengo 2 archivos 1) entrada.csv 2) salida.csv (Este ultimo tiene todos los datos transformados)
generar_archivo_csv(datos, nombre_archivo_csv_salida)


#   ------------------------ FIN CREAR CSV -----------------------------------------

#   ------------------------ INICIO MOVER ARCHIVOS ---------------------------------


# TODO si existe algun error hacer la funcionalidad de no mover el archivo, consultar que error son los importantes

print("Inicio de movimiento de archivos")
# mover archivos, se almacena en una variable booleana
resultado_mover_archivos = mover_archivos(nombre_archivo_csv_entrada, nombre_archivo_csv_salida, 'paraBackup', 'paraDW')

print("Fin de movimiento de archivos")

# Guarda el tiempo de finalización
end_time = time.time()

duration = end_time - start_time
print(f"El script tardó {round(duration/60, 2)} minutos en completarse.")
input("Presione Enter para terminar...")

#   ------------------------ FIN MOVER ARCHIVOS ---------------------------------




