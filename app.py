from flask import Flask, jsonify
from flasgger import Swagger
from dotenv import load_dotenv
import mysql.connector
import os # <--- Importa os
from flask_jwt_extended import JWTManager

from routes.smartwatch import smartwatches_bp

# Cargar variables de entorno
load_dotenv()

# Importar Blueprints
from routes.daycares import daycares_bp
from routes.users import users_bp
from routes.auth import auth_bp
from routes.smartwatch import smartwatches_bp
from routes.reading import readings_bp
from routes.children_routes import children_bp

# Crear la instancia de la aplicación
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") # Carga la clave
jwt = JWTManager(app) # Inicializa JWT


# Configuración de Swagger
app.config['SWAGGER'] = {
    'title': 'API Angel Care',
    'uiversion': 3,
    'openapi': '3.0.2',
    'version': '2.0',
    'description': 'API con capas separadas para gestionar guarderías y usuarios.'
}
swagger = Swagger(app)

# --- Manejadores de Errores Globales ---
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, mysql.connector.Error):
        if e.errno == 1062:
            return jsonify({"error": "Conflicto: El registro ya existe."}), 409
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500

    print(f"Error no controlado: {e}")  # Para depuración
    return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500


# Registrar Blueprints
app.register_blueprint(daycares_bp)
app.register_blueprint(users_bp)
app.register_blueprint(smartwatches_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(readings_bp)
app.register_blueprint(children_bp)

# Ruta de bienvenida
@app.route('/')
def index():
    return "<h1>API v2 Angel Care</h1><p>Visita <a href='/apidocs'>/apidocs</a> para la documentación.</p>"


# Punto de entrada
if __name__ == '__main__':
    app.run(debug=True, port=5000)