from flask import Flask, jsonify
from flasgger import Swagger
from dotenv import load_dotenv
import mysql.connector
import os # <--- Importa os
from flask_jwt_extended import JWTManager

# Cargar variables de entorno
load_dotenv()

# Importar Blueprints
from routes.daycares import daycares_bp
from routes.users import users_bp
from routes.auth import auth_bp

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
    # Manejar errores de MySQL de forma específica
    if isinstance(e, mysql.connector.Error):
        # Error 1062: Entrada duplicada (UNIQUE constraint)
        if e.errno == 1062:
            return jsonify({"error": "Conflicto: El registro ya existe."}), 409
        # Otros errores de base de datos
        return jsonify({"error": f"Error de base de datos: {e.msg}"}), 500

    # Manejar cualquier otra excepción no controlada
    # En un entorno de producción, es importante no exponer detalles del error.
    # Aquí se podría registrar el error en un archivo de logs.
    print(f"Error no controlado: {e}")  # Para depuración
    return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500


# Registrar Blueprints
app.register_blueprint(daycares_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)


# Ruta de bienvenida
@app.route('/')
def index():
    return "<h1>API v2 Angel Care</h1><p>Visita <a href='/apidocs'>/apidocs</a> para la documentación.</p>"


# Punto de entrada
if __name__ == '__main__':
    app.run(debug=True, port=5000)