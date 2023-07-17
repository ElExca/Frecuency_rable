from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo import DESCENDING

from pdf_generator import generar_pdf
from calculator import statistical_calculator
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://angel:angel1205@bd1.5gebju1.mongodb.net/Esp32?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = 'b99878292951aa53e17598417a4a0a0121fcd0808ef8ae13f76a786a09bdaa4f'
mongo = PyMongo(app)



@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Buscar al usuario en la base de datos MongoDB
    user = mongo.db.users.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        # Generar el token JWT
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Credenciales inválidas'}), 401

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # Verificar si el usuario ya existe en la base de datos
    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'El nombre de usuario ya está en uso'}), 400

    # Generar un hash de la contraseña
    password_hash = generate_password_hash(password)

    # Crear un nuevo usuario en la base de datos
    new_user = {'username': username, 'password': password_hash}
    mongo.db.users.insert_one(new_user)

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201
@app.route('/api/calcular', methods=['GET'])
def obtener_documentos():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token faltante'}), 401

    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload['username']
        documentos = mongo.db.Datos.find().sort("_id", DESCENDING).limit(50)
        campo1_output = []
        campo2_output = []
        campo3_output = []
        campo4_output = []
        campo5_output = []
        for documento in documentos:
            campo1_output.append(documento['Temperature'])
            campo2_output.append(documento['Humidity'])
            campo3_output.append(documento['Pressure'])
            campo4_output.append(documento['CO2'])
            campo5_output.append(documento['Altitude'])
        pdf_filename = 'ReporteSensores.pdf'
        # Realizar la operación
        arr_sorted_campo1 = campo1_output[:50] if len(campo1_output) >= 50 else campo1_output
        arr_sorted_campo2 = campo2_output[:50] if len(campo2_output) >= 50 else campo2_output
        arr_sorted_campo3 = campo3_output[:50] if len(campo3_output) >= 50 else campo3_output
        arr_sorted_campo4 = campo4_output[:50] if len(campo4_output) >= 50 else campo4_output
        arr_sorted_campo5 = campo5_output[:50] if len(campo5_output) >= 50 else campo5_output
        #Temperatura
        desviacion_media_campo1, media_campo1, varianza_campo1, desviacion_estandar_campo1, arr_ordenate_campo1,table_frecuency_campo1 = statistical_calculator(
            arr_sorted_campo1)
        #Humedad
        desviacion_media_campo2, media_campo2, varianza_campo2, desviacion_estandar_campo2, arr_ordenate_campo2, table_frecuency_campo2= statistical_calculator(
            arr_sorted_campo2)
        #Presion
        desviacion_media_campo3, media_campo3, varianza_campo3, desviacion_estandar_campo3, arr_ordenate_campo3, table_frecuency_campo3= statistical_calculator(
            arr_sorted_campo3)
        #CO2
        desviacion_media_campo4, media_campo4, varianza_campo4, desviacion_estandar_campo4, arr_ordenate_campo4, table_frecuency_campo4= statistical_calculator(
            arr_sorted_campo4)
        #Altitud
        desviacion_media_campo5, media_campo5, varianza_campo5, desviacion_estandar_campo5, arr_ordenate_campo5, table_frecuency_campo5= statistical_calculator(
            arr_sorted_campo5)

        #Generar pdf
        generar_pdf(pd.DataFrame(table_frecuency_campo2),pd.DataFrame(table_frecuency_campo1),pd.DataFrame(table_frecuency_campo3),
        pd.DataFrame(table_frecuency_campo4),pd.DataFrame(table_frecuency_campo5),arr_sorted_campo2, desviacion_media_campo2, varianza_campo2, media_campo2,
        desviacion_estandar_campo2,arr_sorted_campo1, arr_ordenate_campo2, arr_ordenate_campo1,
        desviacion_media_campo1, media_campo1, varianza_campo1, desviacion_estandar_campo1,pdf_filename,
        desviacion_media_campo3, media_campo3, varianza_campo3, desviacion_estandar_campo3, arr_ordenate_campo3,
        arr_sorted_campo3,desviacion_media_campo4, media_campo4, varianza_campo4, desviacion_estandar_campo4, arr_ordenate_campo4,
        arr_sorted_campo4,desviacion_media_campo5, media_campo5, varianza_campo5, desviacion_estandar_campo5,arr_ordenate_campo5,arr_sorted_campo5)


        return jsonify({
            'Humedad': campo2_output,
            'Temperature': campo1_output

        })


    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido'}), 401



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
