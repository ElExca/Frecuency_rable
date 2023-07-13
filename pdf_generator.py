from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
def generar_pdf(arr_sorted_campo2, desviacion_media_campo2,varianza_campo2,media_campo2,pdf_filename):
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
    c.save()