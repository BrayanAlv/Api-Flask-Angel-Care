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

# --- CARGAR MODELO ENTRENADO---
MODEL_PATH = 'health_classifier.pkl'
risk_model = None

if os.path.exists(MODEL_PATH):
    try:
        risk_model = joblib.load(MODEL_PATH)
        print(f" SYSTEM: Modelo cargado exitosamente desde {MODEL_PATH}")
    except Exception as e:
        print(f" ERROR: No se pudo cargar el modelo: {e}")
else:
    print(f" WARNING: No se encontró el archivo {MODEL_PATH}. La predicción no funcionará.")

# Configuración de Swagger
app.config['SWAGGER'] = {
    'title': 'API Angel Care',
    'uiversion': 3,
    'openapi': '3.0.2',
    'version': '2.0',
    'description': 'API con capas separadas, gestión de guarderías y Módulo de Inteligencia Artificial.'
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

# --- Modelo para florecnio entrenado ---
@app.route('/api/analyze-reading', methods=['POST'])
def analyze_reading():
    """
    Analiza signos vitales para detectar riesgos de salud.
    Usa un modelo de Regresión Logística entrenado con datos pediátricos.
    ---
    tags:
      - Modelo entrenado
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - bpm
            - temperature
            - oxygen_level
          properties:
            bpm:
              type: integer
              description: Latidos por minuto
              example: 150
            temperature:
              type: number
              description: Temperatura corporal en Celsius
              example: 39.5
            oxygen_level:
              type: integer
              description: Nivel de saturación de oxígeno (SpO2)
              example: 96
    responses:
      200:
        description: Análisis completado exitosamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            analysis:
              type: object
              properties:
                is_critical:
                  type: boolean
                  description: True si se detecta una anomalía de salud
                risk_probability:
                  type: number
                  description: Porcentaje de confianza del modelo (0-100)
                message:
                  type: string
                  description: Mensaje legible para el usuario
      400:
        description: Datos faltantes o incorrectos
      503:
        description: Modelo de IA no cargado en el servidor
    """
    # Aqui se checa si esta cargado
    if not risk_model:
        return jsonify({
            "error": "El servicio de IA no está disponible (Modelo no cargado)", 
            "is_critical": False
        }), 503

    data = request.get_json()
    
    # Validadores
    bpm = data.get('bpm')
    temp = data.get('temperature')
    oxy = data.get('oxygen_level')

    if None in [bpm, temp, oxy]:
        return jsonify({"error": "Faltan datos vitales (bpm, temperature, oxygen_level)"}), 400

    try:
        # Esto ignora los warnings
        features = pd.DataFrame(
            [[bpm, temp, oxy]], 
            columns=['bpm', 'temperature', 'oxygen_level']
        )
        
        # Realizar la predicción
        prediction = risk_model.predict(features)[0] # 0 = Normal, 1 = Riesgo
        probability = risk_model.predict_proba(features)[0][1] # Probabilidad de ser clase 1
        
        is_risk = bool(prediction == 1)
        
        # Retornar 
        return jsonify({
            "status": "success",
            "data_received": {
                "bpm": bpm,
                "temperature": temp,
                "oxygen_level": oxy
            },
            "analysis": {
                "is_critical": is_risk,
                "risk_probability": round(probability * 100, 2),
                "message": "⚠️ ANOMALÍA DETECTADA: Signos vitales fuera de rango." if is_risk else "✅ Signos vitales normales."
            }
        }), 200

    except Exception as e:
        print(f"Error en predicción IA: {str(e)}")
        return jsonify({"error": "Error interno procesando la predicción"}), 500


# Ruta de bienvenida
@app.route('/')
def index():
    ai_status = "<span style='color:green'>ONLINE</span>" if risk_model else "<span style='color:red'>OFFLINE</span>"
    return f"<h1>API v2 Angel Care</h1><p>IA System: {ai_status}</p><p>Visita <a href='/apidocs'>/apidocs</a> para la documentación.</p>"


# Punto de entrada
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)