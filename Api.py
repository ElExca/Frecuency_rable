from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pdf_generator import generar_pdf
from calculator import statistical_calculator

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
    desviacion_media_campo2,media_campo2, varianza_campo2 = statistical_calculator(arr_sorted_campo2)
    pdf_filename = 'Reporte.pdf'
    generar_pdf(arr_sorted_campo2,desviacion_media_campo2,varianza_campo2,media_campo2,pdf_filename)


    return jsonify({
        'Humedad': campo2_output,
        'Desviacion_Media': desviacion_media_campo2
    })


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
