from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Esp32'
mongo = PyMongo(app)


@app.route('/api/calcular', methods=['GET'])
def obtener_documentos():
    documentos = mongo.db.Datos.find()
    campo1_output = []
    campo2_output = []
    for documento in documentos:
        campo1_output.append(documento['Temperatura'])
        campo2_output.append(documento['Humedad'])

    # Realizar la operación
    arr_sorted_campo2 = campo2_output[:50] if len(campo2_output) >= 50 else campo2_output
    desviacion_media_campo2, resultado_campo2 = calcular_desviacion_media(arr_sorted_campo2)
    pdf_filename = 'Reporte.pdf'
    generar_pdf(arr_sorted_campo2,desviacion_media_campo2,pdf_filename)


    return jsonify({
        'Humedad': campo2_output,
        'Desviacion_Media': desviacion_media_campo2
    })

def calcular_desviacion_media(arr_sorted):
    media = sum(arr_sorted) / len(arr_sorted)

    desviacion = 0
    for elemento in arr_sorted:
        desviacion += abs(elemento - media)
    desviacion_media = round(desviacion / len(arr_sorted), 2)
    return desviacion_media, media

def generar_pdf(arr_sorted_campo2, desviacion_media_campo2,pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "Datos de Humedad:")

    # Ajustar la posición de los datos de humedad en forma horizontal con salto de línea
    x_pos = 100
    y_pos = 680
    max_width = 550  # Ancho máximo disponible para los datos
    for dato in arr_sorted_campo2:
        text_width = c.stringWidth(str(dato), "Helvetica", 12)
        if x_pos + text_width > max_width:
            x_pos = 100  # Volver al inicio de la línea
            y_pos -= 20  # Saltar a la siguiente línea
        c.drawString(x_pos, y_pos, str(dato))
        x_pos += text_width + 20  # Dejar un espacio entre los datos

    # Ajustar la posición vertical después de mostrar los datos de humedad
    y_pos -= 40  # Espacio adicional antes de la desviación media

    c.drawString(100, y_pos, "Desviación Media de Humedad:")
    c.drawString(100, y_pos - 20, str(desviacion_media_campo2))
    c.save()
@app.route('/api/documentos', methods=['POST'])
def agregar_documento():
    nuevo_documento = {
        'campo1': request.json['campo1'],
        'campo2': request.json['campo2']
    }
    mongo.db.datos.insert_one(nuevo_documento)
    return jsonify({'mensaje': 'Documento agregado correctamente'})

@app.route('/api/documentos/<id>', methods=['GET'])
def obtener_documento(id):
    documento = mongo.db.nombre_de_la_coleccion.find_one({'_id': id})
    if documento:
        output = {'campo1': documento['campo1'], 'campo2': documento['campo2']}
    else:
        output = 'Documento no encontrado'
    return jsonify({'documento': output})

@app.route('/api/documentos/<id>', methods=['PUT'])
def actualizar_documento(id):
    documento = mongo.db.nombre_de_la_coleccion.find_one({'_id': id})
    if documento:
        documento_actualizado = {
            'campo1': request.json['campo1'],
            'campo2': request.json['campo2']
        }
        mongo.db.Datos.update_one({'_id': id}, {'$set': documento_actualizado})
        return jsonify({'mensaje': 'Documento actualizado correctamente'})
    else:
        return jsonify({'mensaje': 'Documento no encontrado'})

@app.route('/api/documentos/<id>', methods=['DELETE'])
def eliminar_documento(id):
    documento = mongo.db.Datos.find_one({'_id': id})
    if documento:
        mongo.db.Datos.delete_one({'_id': id})
        return jsonify({'mensaje': 'Documento eliminado correctamente'})
    else:
        return jsonify({'mensaje': 'Documento no encontrado'})

if __name__ == '__main__':
    app.run()
