from flask import Blueprint, request, jsonify
from models.reading_model import ReadingModel
from models.smartwatches_models import SmartwatchModel
from flask_jwt_extended import jwt_required

# Creamos un nuevo Blueprint para estas rutas
readings_bp = Blueprint('api', __name__, url_prefix='/api')

# --- Rutas para Lecturas de Sensores ---

@readings_bp.route('/readings', methods=['POST'])
#@jwt_required()
def save_readings():
    """
    Guardar lecturas de sensores de un smartwatch
    ---
    tags:
      - Readings
    summary: "Recibe y guarda un lote de lecturas de sensores de un smartwatch."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id_smartwatch:
                type: integer
                description: "ID del smartwatch que envía los datos (requerido)."
              temperature:
                type: number
                format: float
                description: "Lectura de temperatura."
              heart_rate:
                type: integer
                description: "Lectura de ritmo cardíaco (BPM)."
              spo2:
                type: number
                format: float
                description: "Nivel de saturación de oxígeno (SpO2)."
              accelerometer:
                type: object
                properties:
                  x: {type: number, format: float}
                  y: {type: number, format: float}
                  z: {type: number, format: float}
                  is_fall: {type: boolean}
            required:
              - id_smartwatch
    responses:
      '201':
        description: "Lecturas guardadas exitosamente."
      '400':
        description: "Datos incompletos, falta 'id_smartwatch'."
      '500':
        description: "Error interno al guardar las lecturas."
    """
    data = request.get_json()
    if not data or not data.get('id_smartwatch'):
        return jsonify({"error": "El campo 'id_smartwatch' es requerido"}), 400

    if ReadingModel.save_readings(data):
        return jsonify({"message": "Lecturas guardadas exitosamente"}), 201
    return jsonify({"error": "No se pudieron guardar las lecturas"}), 500


@readings_bp.route('/readings/smartwatch/<int:smartwatch_id>/latest', methods=['GET'])
#@jwt_required()
def get_latest_readings(smartwatch_id):
    """
    Obtener la última lectura de todos los sensores
    ---
    tags:
      - Readings
    summary: "Obtiene la lectura más reciente de cada sensor para un smartwatch específico."
    parameters:
      - name: smartwatch_id
        in: path
        required: true
        description: "ID del smartwatch a consultar."
        schema:
          type: integer
    responses:
      '200':
        description: "Últimas lecturas obtenidas."
      '404':
        description: "No se encontraron lecturas para el smartwatch."
    """
    readings = ReadingModel.get_all_last_readings(smartwatch_id)
    if readings:
        return jsonify(readings)
    return jsonify({"error": "No se encontraron lecturas"}), 404


@readings_bp.route('/readings/smartwatch/<int:smartwatch_id>/heart_rate', methods=['GET'])
#@jwt_required()
def get_heart_rate_history(smartwatch_id):
    """
    Obtener últimas 10 lecturas de ritmo cardíaco
    ---
    tags:
      - Readings
    summary: "Obtiene las últimas 10 lecturas de ritmo cardíaco (BPM) para una gráfica."
    parameters:
      - name: smartwatch_id
        in: path
        required: true
        description: "ID del smartwatch a consultar."
        schema:
          type: integer
    responses:
      '200':
        description: "Lista de las últimas 10 lecturas de ritmo cardíaco."
    """
    history = ReadingModel.get_last_10_heart_rate(smartwatch_id)
    return jsonify(history)


@readings_bp.route('/readings/smartwatch/<int:smartwatch_id>/oxygen', methods=['GET'])
#@jwt_required()
def get_oxygen_history(smartwatch_id):
    """
    Obtener últimas 10 lecturas de oxigenación
    ---
    tags:
      - Readings
    summary: "Obtiene las últimas 10 lecturas de oxigenación (SpO2) para una gráfica."
    parameters:
      - name: smartwatch_id
        in: path
        required: true
        description: "ID del smartwatch a consultar."
        schema:
          type: integer
    responses:
      '200':
        description: "Lista de las últimas 10 lecturas de oxigenación."
    """
    history = ReadingModel.get_last_10_oxygenation(smartwatch_id)
    return jsonify(history)


# --- Rutas para Acciones de Smartwatches ---

@readings_bp.route('/smartwatches/activate', methods=['POST'])
#@jwt_required()
def activate_band():
    """
    Activar y asignar un smartwatch
    ---
    tags:
      - Smartwatches Actions
    summary: "Activa el estado de un smartwatch y lo asigna a un niño."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id_smartwatch:
                type: integer
                description: "ID del smartwatch a activar."
              id_child:
                type: integer
                description: "ID del niño al que se le asignará."
            required:
              - id_smartwatch
              - id_child
    responses:
      '200':
        description: "Smartwatch activado y asignado exitosamente."
      '400':
        description: "Faltan los IDs de smartwatch o niño."
      '500':
        description: "Error en la transacción."
    """
    data = request.get_json()
    smartwatch_id = data.get('id_smartwatch')
    child_id = data.get('id_child')

    if not smartwatch_id or not child_id:
        return jsonify({"error": "Los campos 'id_smartwatch' y 'id_child' son requeridos"}), 400

    if SmartwatchModel.activate_and_assign(smartwatch_id, child_id):
        return jsonify({"message": "Smartwatch activado y asignado"})
    return jsonify({"error": "Error al activar y asignar el smartwatch"}), 500


@readings_bp.route('/smartwatches/<int:smartwatch_id>/deactivate', methods=['PUT'])
#@jwt_required()
def deactivate_band(smartwatch_id):
    """
    Desactivar y desasignar un smartwatch
    ---
    tags:
      - Smartwatches Actions
    summary: "Desactiva el estado de un smartwatch y lo desvincula de cualquier niño."
    parameters:
      - name: smartwatch_id
        in: path
        required: true
        description: "ID del smartwatch a desactivar."
        schema:
          type: integer
    responses:
      '200':
        description: "Smartwatch desactivado y desasignado exitosamente."
      '500':
        description: "Error en la transacción."
    """
    if SmartwatchModel.deactivate_and_unassign(smartwatch_id):
        return jsonify({"message": "Smartwatch desactivado y desasignado"})
    return jsonify({"error": "Error al desactivar el smartwatch"}), 500