from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pdf_generator import generar_pdf
from calculator import statistical_calculator
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config[
    "MONGO_URI"
] = "mongodb+srv://angel:angel1205@bd1.5gebju1.mongodb.net/Esp32?retryWrites=true&w=majority"
app.config[
    "SECRET_KEY"
] = "b99878292951aa53e17598417a4a0a0121fcd0808ef8ae13f76a786a09bdaa4f"
mongo = PyMongo(app)

CORS(app)


@app.route("/login", methods=["POST"])
@cross_origin(origin="http://localhost:3000", headers=["Content-Type"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    # Buscar al usuario en la base de datos MongoDB
    user = mongo.db.users.find_one({"username": username})

    if user and check_password_hash(user["password"], password):
        # Generar el token JWT
        token = jwt.encode(
            {"username": username}, app.config["SECRET_KEY"], algorithm="HS256"
        )
        return jsonify({"token": token})

    return jsonify({"message": "Credenciales inválidas"}), 401


@app.route("/register", methods=["POST", "OPTIONS"])
@cross_origin(origin="http://localhost:3000", headers=["Content-Type"])
def register():
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")

    # Verificar si el email ya existe en la base de datos
    existing_email = mongo.db.users.find_one({"email": email})
    if existing_email:
        return jsonify({"message": "El email ya está en uso"}), 400

    # Verificar si el usuario ya existe en la base de datos
    existing_user = mongo.db.users.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "El nombre de usuario ya está en uso"}), 400

    # Generar un hash de la contraseña
    password_hash = generate_password_hash(password)

    # Crear un nuevo usuario en la base de datos
    new_user = {"email": email, "username": username, "password": password_hash}
    mongo.db.users.insert_one(new_user)

    return jsonify({"message": "Usuario registrado exitosamente"}), 201


@app.route("/api/calcular", methods=["GET"])
def obtener_documentos():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"message": "Token faltante"}), 401

    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        username = payload["username"]
        documentos = mongo.db.Datos.find()
        campo1_output = []
        campo2_output = []
        for documento in documentos:
            campo1_output.append(documento["Temperatura"])
            campo2_output.append(documento["Humedad"])

        # Realizar la operación
        arr_sorted_campo2 = (
            campo2_output[:50] if len(campo2_output) >= 50 else campo2_output
        )
        (
            desviacion_media_campo2,
            media_campo2,
            varianza_campo2,
            desviacion_estandar_campo2,
        ) = statistical_calculator(arr_sorted_campo2)
        pdf_filename = "Reporte.pdf"
        generar_pdf(
            arr_sorted_campo2,
            desviacion_media_campo2,
            varianza_campo2,
            media_campo2,
            desviacion_estandar_campo2,
            pdf_filename,
        )

        return jsonify(
            {"Humedad": campo2_output, "Desviacion_Media": desviacion_media_campo2}
        )

    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 401


@app.route("/api/documentos/<id>", methods=["DELETE"])
def eliminar_documento(id):
    documento = mongo.db.Datos.find_one({"_id": id})
    if documento:
        mongo.db.Datos.delete_one({"_id": id})
        return jsonify({"mensaje": "Documento eliminado correctamente"})
    else:
        return jsonify({"mensaje": "Documento no encontrado"})


if __name__ == "__main__":
    app.run()
