from flask import Flask, jsonify, request
from flasgger import Swagger
from dotenv import load_dotenv
import mysql.connector
import os
import joblib
import pandas as pd
import numpy as np
from flask_jwt_extended import JWTManager
from flask_cors import CORS 

# Importar Blueprints
from routes.daycares import daycares_bp
from routes.users import users_bp
from routes.auth import auth_bp
from routes.smartwatch import smartwatches_bp
from routes.reading import readings_bp
from routes.children_routes import children_bp

# Cargar variables de entorno
load_dotenv()

# Crear la instancia de la aplicación
app = Flask(__name__)

# --- CONFIGURACIÓN CORS ---
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# --- CARGAR MODELO DE IA ---
MODEL_PATH = 'health_classifier.pkl'
risk_model = None

if os.path.exists(MODEL_PATH):
    try:
        risk_model = joblib.load(MODEL_PATH)
        print(f"✅ IA SYSTEM: Modelo cargado exitosamente desde {MODEL_PATH}")
    except Exception as e:
        print(f"❌ IA ERROR: No se pudo cargar el modelo: {e}")
else:
    print(f"⚠️ IA WARNING: No se encontró el archivo {MODEL_PATH}. La predicción no funcionará.")

# --- CONFIGURACIÓN DE SWAGGER (CORREGIDA) ---
# Quitamos 'openapi': '3.0.2' para que use Swagger 2.0 por defecto.
# Esto hace que el botón 'Try it out' funcione con 'parameters: in: body'.
app.config['SWAGGER'] = {
    'title': 'API Angel Care',
    'uiversion': 3,
    'version': '2.0',
    'description': 'API con capas separadas, gestión de guarderías y Módulo de Inteligencia Artificial.',
    'specs_route': '/apidocs/'
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

    print(f"Error no controlado: {e}")
    return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

# Registrar Blueprints
app.register_blueprint(daycares_bp)
app.register_blueprint(users_bp)
app.register_blueprint(smartwatches_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(readings_bp)
app.register_blueprint(children_bp)

# --- ENDPOINT DE INTELIGENCIA ARTIFICIAL ---
@app.route('/api/analyze-reading', methods=['POST'])
def analyze_reading():
    """
    Analiza signos vitales en tiempo real para detectar riesgos de salud.
    ---
    tags:
      - Modelo entrenado
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos vitales para el análisis.
        required: true
        schema:
          id: AnalysisInput
          type: object
          required:
            - bpm
            - temperature
            - oxygen_level
          properties:
            bpm:
              type: integer
              description: Latidos por minuto
              default: 150
            temperature:
              type: number
              description: Temperatura corporal en Celsius
              default: 39.5
            oxygen_level:
              type: integer
              description: Nivel de saturación de oxígeno
              default: 96
    responses:
      200:
        description: Análisis completado
        schema:
          type: object
          properties:
            status:
              type: string
            analysis:
              type: object
      400:
        description: Error - Datos faltantes o vacíos
      503:
        description: Modelo IA no cargado
    """
    # 1. Verificar modelo
    if not risk_model:
        return jsonify({"error": "Modelo no cargado", "is_critical": False}), 503

    # 2. DEBUG: Ver qué llega realmente
    print(f"\n--- DEBUG SWAGGER ---")
    print(f"Content-Type: {request.content_type}")
    raw_data = request.get_data(as_text=True)
    print(f"Data recibida: '{raw_data}'")
    print(f"---------------------\n")

    # 3. Intentar obtener JSON
    # Si raw_data está vacío, es porque Swagger no envió nada
    if not raw_data:
         return jsonify({"error": "El cuerpo de la petición está vacío. Swagger no envió datos."}), 400

    data = request.get_json(force=True, silent=True)
    
    if not data:
        return jsonify({"error": "El formato no es JSON válido."}), 400
    
    # 4. Validar variables
    bpm = data.get('bpm')
    temp = data.get('temperature')
    oxy = data.get('oxygen_level')

    if None in [bpm, temp, oxy]:
        return jsonify({"error": "Faltan datos (bpm, temperature, oxygen_level)"}), 400

    try:
        # 5. Predicción
        features = pd.DataFrame([[bpm, temp, oxy]], columns=['bpm', 'temperature', 'oxygen_level'])
        prediction = risk_model.predict(features)[0]
        probability = risk_model.predict_proba(features)[0][1]
        is_risk = bool(prediction == 1)
        
        return jsonify({
            "status": "success",
            "data_received": {"bpm": bpm, "temperature": temp, "oxygen_level": oxy},
            "analysis": {
                "is_critical": is_risk,
                "risk_probability": round(probability * 100, 2),
                "message": "ANOMALÍA DETECTADA" if is_risk else " Signos Normales"
            }
        }), 200

    except Exception as e:
        print(f"Error IA: {e}")
        return jsonify({"error": str(e)}), 500


# Ruta de bienvenida
@app.route('/')
def index():
    ai_status = "<span style='color:green'>ONLINE</span>" if risk_model else "<span style='color:red'>OFFLINE</span>"
    return f"<h1>API v2 Angel Care</h1><p>IA System: {ai_status}</p><p>Visita <a href='/apidocs'>/apidocs</a> para la documentación.</p>"


# Punto de entrada
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)