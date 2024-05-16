import math
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import legal as GOV_LEGAL
from reportlab.lib.styles import getSampleStyleSheet

def generar_pdf_estadistico(estadisticas: list, nombre_archivo: str, max_columnas_por_hoja: int, titulo: str):
    """
    Genera un archivo PDF con las estadísticas proporcionadas.

    Parámetros:
    estadisticas (dict): El diccionario de estadísticas.
    nombre_archivo (str): El nombre del archivo PDF a generar.
    max_columnas_por_hoja (int): El número máximo de columnas por hoja.
    titulo (str): El título del PDF.

    Returns:
    None

    """
    # Crear el documento PDF
    pdf = SimpleDocTemplate(nombre_archivo, pagesize=landscape((40*cm , 20*cm)), leftMargin=2*cm, rightMargin=3*cm)  # Cambiar a orientación apaisada y establecer márgenes

    # Crear la tabla con las estadísticas
    data = [['Nombre Columna', 'Máximo', 'Mínimo', 'Media', 'Desviación Estándar', 'Mediana', 'Moda', 'Nulos', 'Repetidos', 'Unicos', 'Cantidad Total']]  # Agregar 'Cantidad' al encabezado
    styles = []
    for i in range(len(estadisticas['columna'])):
        fila = [estadisticas['columna'][i], estadisticas['maximo'][i], estadisticas['minimo'][i], estadisticas['media'][i], estadisticas['desviacion_estandar'][i], estadisticas['mediana'][i], estadisticas['moda'][i], estadisticas['nulos'][i], estadisticas['repetidos'][i], estadisticas['unicos'][i], estadisticas['cantidad_total'][i]]  # Agregar la cantidad a la fila
        data.append(fila)

        # Comprobar si la fila contiene un valor NaN, None o el número de nulos es mayor que cero
        if any(x is None or (isinstance(x, float) and math.isnan(x)) for x in fila) or estadisticas['nulos'][i] > 0:
            # Si es así, agregar un estilo para cambiar el color del texto a rojo
            styles.append(('TEXTCOLOR', (0, i+1), (-1, i+1), colors.red))
        else:
            styles.append(('TEXTCOLOR', (0, i+1), (-1, i+1), colors.black))

    # Dividir los datos en varias tablas si es necesario
    max_filas_por_pagina = 30  # Ajustar según sea necesario
    tablas = []
    for i in range(1, len(data), max_filas_por_pagina):
        tabla = [data[0]] + data[i:i + max_filas_por_pagina]
        tablas.append(tabla)

    # Dividir cada tabla en subtablas basadas en el número máximo de columnas por hoja
    subtablas = []
    for tabla in tablas:
        for i in range(0, len(tabla[0]), max_columnas_por_hoja):
            subtabla = [fila[i:i + max_columnas_por_hoja] for fila in tabla]
            subtablas.append(subtabla)

    # Construir el PDF
    elems = []
    for subtabla in subtablas:
        t = Table(subtabla)

        # Aplicar estilo a la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ] + styles)
        t.setStyle(style)

        elems.append(Spacer(1, 2*cm))  # Agregar espacio en blanco a la izquierda
        elems.append(t)
        elems.append(Spacer(1, 3*cm))  # Agregar espacio en blanco a la derecha
        elems.append(PageBreak())  # Agregar un salto de página después de cada tabla

    # Agregar el título al PDF
    styles = getSampleStyleSheet()
    title = Paragraph(titulo, styles['Title'])
    elems.insert(0, title)
    
    pdf.build(elems)
    

def generar_pdf_formatos(resultado_formato: list, nombre_pdf_salida:str, titulo: str):
    """
    Genera un PDF a partir de una lista de diccionarios.

    Parámetros:
    resultado_formato (list): La lista de diccionarios.
    nombre_pdf_salida (str): El nombre del archivo PDF a generar.
    titulo (str): El título del PDF.

    Returns:
    None

    """
    # Crear un documento PDF
    pdf = SimpleDocTemplate(nombre_pdf_salida, pagesize=letter)

    # Crear una tabla con los datos de resultado_formato
    data = [["Columna", "Tipo de dato esperado", "Tipo de dato actual", "Leyenda"]]  # Encabezados de la tabla
    for dic in resultado_formato:
        data.append([dic["columna"], dic["dtype_esperado"], dic["dtype_actual"], dic["leyenda"]])

    table = Table(data)

    # Agregar estilo a la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])

    # Cambiar el color de la letra a rojo si la leyenda es 'no coincide'
    for i, dic in enumerate(resultado_formato, start=1):
        if dic["leyenda"] == "no coincide":
            style.add('TEXTCOLOR', (0, i), (-1, i), colors.red)

    table.setStyle(style)

    # Construir el PDF
    elems = []
    elems.append(table)
    
    # Agregar el título al PDF
    styles = getSampleStyleSheet()
    title = Paragraph(titulo, styles['Title'])
    elems.insert(0, title)
    
    pdf.build(elems)
    
    
    
def generar_pdf_cant_filas_y_nombre_columnas(resultados_cant_filas_y_nombre_columnas: list, nombre_pdf_salida: str, titulo: str):
    """
    Genera un PDF a partir de una lista.

    Parámetros:
    resultados_cant_filas_y_nombre_columnas (list): La lista de resultados.
    nombre_pdf_salida (str): El nombre del archivo PDF a generar.
    titulo (str): El título del PDF.

    Returns:
    None

    """
    # Crear un documento PDF
    pdf = SimpleDocTemplate(nombre_pdf_salida, pagesize=letter)

    # Crear una tabla con los datos de resultados
    if resultados_cant_filas_y_nombre_columnas:
        data = [resultados_cant_filas_y_nombre_columnas]  # Datos de la tabla
        table = Table(data)

        # Agregar estilo a la tabla
        style = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.red),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])
        table.setStyle(style)
        elems = [table]
    else:
        styles = getSampleStyleSheet()
        text = 'No hubo problema de nombre de columnas ni cantidad de filas'
        para = Paragraph(text, styles['Normal'])
        elems = [para]

    # Agregar el título al PDF
    styles = getSampleStyleSheet()
    title = Paragraph(titulo, styles['Title'])
    elems.insert(0, title)

    # Construir el PDF
    pdf.build(elems)