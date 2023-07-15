from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import letter
from tabulate import tabulate
from reportlab.platypus import Table, TableStyle
import  tempfile
from reportlab.lib import colors
import pandas as pd
def generar_graficaHumedad(arr_sorted):
    # Crear la gráfica utilizando Matplotlib
    x_labels = range(0, len(arr_sorted), 5)  # Etiquetas del eje x
    plt.plot(arr_sorted)
    plt.xlabel('Tiempo')
    plt.ylabel('Humedad')
    plt.title('Gráfica de Humedad')
    plt.xticks(x_labels)  # Establecer las etiquetas del eje x
    plt.grid(True)

    temp_filename = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
    plt.savefig(temp_filename)
    plt.close()

    return temp_filename

def generar_graficaTemperature(arr_sorted):
    # Crear la gráfica utilizando Matplotlib
    x_labels = range(0, len(arr_sorted), 5)  # Etiquetas del eje x
    plt.plot(arr_sorted)
    plt.xlabel('Tiempo')
    plt.ylabel('Temperatura')
    plt.title('Gráfica de Temperatura')
    plt.xticks(x_labels)  # Establecer las etiquetas del eje x
    plt.grid(True)

    temp_filename = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
    plt.savefig(temp_filename)
    plt.close()

    return temp_filename


def generar_pdf(table_frecuency_campo2,arr_sorted_campo2, desviacion_media_campo2,varianza_campo2,
                media_campo2,desviacion_estandar_campo2,arr_sorted_campo1,arr_ordenate_campo2, arr_ordenate_campo1,
                    desviacion_media_campo1, media_campo1, varianza_campo1, desviacion_estandar_campo1,pdf_filename):
    table_str = table_frecuency_campo2.to_string(index=False)
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(70, 700, "Datos de Humedad:")
    # Ajustar la posición de los datos de humedad en forma horizontal con salto de línea
    x_pos = 70
    y_pos = 680
    max_width = 550  # Ancho máximo disponible para los datos
    for dato in arr_sorted_campo2:
        text_width = c.stringWidth(str(dato), "Helvetica", 12)
        if x_pos + text_width > max_width:
            x_pos = 70  # Volver al inicio de la línea
            y_pos -= 20  # Saltar a la siguiente línea
        c.drawString(x_pos, y_pos, str(dato))
        x_pos += text_width + 20  # Dejar un espacio entre los datos
        # Espacio adicional antes de la desviación media
    x_pos = 70
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, 600, "Datos ordenados de Humedad:")
    for dato in arr_ordenate_campo2:
        text_width = c.stringWidth(str(dato), "Helvetica", 12)
        if x_pos + text_width > max_width:
            x_pos = 70  # Volver al inicio de la línea
            y_pos -= 20  # Saltar a la siguiente línea
        c.drawString(x_pos, y_pos, str(dato))
        x_pos += text_width + 20  # Dejar un espacio entre los datos

    # Ajustar la posición vertical después de mostrar los datos de humedad
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, y_pos, "Desviación Media de Humedad:")
    c.drawString(70, y_pos - 20, str(desviacion_media_campo2))
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, y_pos, "Varianza de Humedad:")
    c.drawString(70, y_pos - 20, str(varianza_campo2))
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, y_pos, "Media de Humedad:")
    c.drawString(70, y_pos - 20, str(media_campo2))
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, y_pos, "Desviacion estandar humedad:")
    c.drawString(70, y_pos - 20, str(round(desviacion_estandar_campo2,2)))
    c.showPage()
    temp_filename = generar_graficaHumedad(arr_sorted_campo2)
    c.drawImage(temp_filename, 80, 400, width=500, height=400)
    c.showPage()
    width, height = letter

    # Configurar la posición de la tabla en el PDF
    x_start = 50
    y_start = height - 100
    line_height = 20

    # Ajustar el espacio entre columnas
    x_offset = 80

    # Ajustar el tamaño de la letra para que quepa la tabla en una página
    font_size = 10

    # Agregar el título de la tabla
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_start, y_start, "Tabla de frecuencias")
    y_start -= line_height

    column_headers = table_frecuency_campo2.columns.tolist()
    c.setFont("Helvetica-Bold", font_size)
    x = x_start
    for header in column_headers:
        c.drawString(x, y_start, header)
        x += x_offset  # Ajustar el espacio entre columnas
    y_start -= line_height
    # Agregar los datos de la tabla
    c.setFont("Helvetica", font_size)
    for _, row in table_frecuency_campo2.iterrows():
        x = x_start
        for header in column_headers:
            value = str(row[header])
            if header == "Marca de clase":
                # Alinear a la izquierda y ajustar la longitud a 10 caracteres
                c.drawString(x, y_start, value.ljust(10))
            else:
                c.drawString(x, y_start, value)
            x += x_offset  # Ajustar el espacio entre columnas
        y_start -= line_height

    c.showPage()

    c.drawString(70, 700, "Datos de Temperatura:")
    # Ajustar la posición de los datos de humedad en forma horizontal con salto de línea
    x_pos = 70
    y_pos = 680
    max_width = 550  # Ancho máximo disponible para los datos
    for dato in arr_sorted_campo1:
        text_width = c.stringWidth(str(dato), "Helvetica", 12)
        if x_pos + text_width > max_width:
            x_pos = 70  # Volver al inicio de la línea
            y_pos -= 20  # Saltar a la siguiente línea
        c.drawString(x_pos, y_pos, str(dato))
        x_pos += text_width + 20  # Dejar un espacio entre los datos
    x_pos = 70
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, 535, "Datos ordenados de Temperatura:")
    for dato in arr_ordenate_campo1:
        text_width = c.stringWidth(str(dato), "Helvetica", 12)
        if x_pos + text_width > max_width:
            x_pos = 70  # Volver al inicio de la línea
            y_pos -= 20  # Saltar a la siguiente línea
        c.drawString(x_pos, y_pos, str(dato))
        x_pos += text_width + 20  # Dejar un espacio entre los datos
    # Ajustar la posición vertical después de mostrar los datos de humedad
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, y_pos, "Desviación Media de Temperatura:")
    c.drawString(70, y_pos - 20, str(desviacion_media_campo1))
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, y_pos, "Varianza de Temperatura:")
    c.drawString(70, y_pos - 20, str(varianza_campo1))
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, y_pos, "Media de Temperatura:")
    c.drawString(70, y_pos - 20, str(media_campo1))
    y_pos -= 40  # Espacio adicional antes de la desviación media
    c.drawString(70, y_pos, "Desviacion estandar Temperatura:")
    c.drawString(70, y_pos - 20, str(round(desviacion_estandar_campo1, 2)))
    c.showPage()
    temp_filename = generar_graficaTemperature(arr_sorted_campo1)
    c.drawImage(temp_filename, 80, 400, width=500, height=400)
    os.remove(temp_filename)

    c.save()