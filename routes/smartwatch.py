from flask import Blueprint, request, jsonify
from models.smartwatches_models import SmartwatchModel
from flask_jwt_extended import jwt_required

smartwatches_bp = Blueprint('smartwatches', __name__, url_prefix='/api/smartwatches')


@smartwatches_bp.route('/', methods=['GET'])
def get_smartwatches():
    """
    Obtener todos los smartwatches
    ---
    tags:
      - Smartwatches
    summary: "Obtiene una lista de todos los smartwatches registrados."
    responses:
      '200':
        description: "Lista de smartwatches obtenida exitosamente."
    """
    smartwatches = SmartwatchModel.get_all()
    return jsonify(smartwatches)


@smartwatches_bp.route('/<int:smartwatch_id>', methods=['GET'])
def get_smartwatch(smartwatch_id):
    """
    Obtener un smartwatch por ID
    ---
    tags:
      - Smartwatches
    summary: "Obtiene los detalles de un smartwatch específico por su ID."
    parameters:
      - name: smartwatch_id
        in: path
        required: true
        description: "ID del smartwatch a obtener."
        schema:
          type: integer
    responses:
      '200':
        description: "Detalles del smartwatch."
      '404':
        description: "Smartwatch no encontrado."
    """
    smartwatch = SmartwatchModel.get_by_id(smartwatch_id)
    if smartwatch:
        return jsonify(smartwatch)
    return jsonify({"error": "Smartwatch no encontrado"}), 404


@smartwatches_bp.route('/child/<int:child_id>', methods=['GET'])
def get_smartwatches_by_child(child_id):
    """
    Obtener smartwatches por ID de niño
    ---
    tags:
      - Smartwatches
    summary: "Obtiene una lista de smartwatches asociados a un niño específico."
    parameters:
      - name: child_id
        in: path
        required: true
        description: "ID del niño para buscar sus smartwatches."
        schema:
          type: integer
    responses:
      '200':
        description: "Lista de smartwatches del niño (puede estar vacía)."
    """
    smartwatches = SmartwatchModel.get_by_child_id(child_id)
    return jsonify(smartwatches)


@smartwatches_bp.route('/', methods=['POST'])
#@jwt_required()
def create_smartwatch():
    """
    Crear un nuevo smartwatch
    ---
    tags:
      - Smartwatches
    summary: "Registra un nuevo smartwatch en la base de datos."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              device_id:
                type: string
                description: "Identificador único del dispositivo (requerido)."
                example: "sn-a1b2c3d4"
              model:
                type: string
                description: "Modelo del smartwatch (requerido)."
                example: "KidsSafe v2"
              status:
                type: string
                description: "Estado inicial del reloj (opcional, por defecto 'active')."
                example: "active"
            required:
              - device_id
              - model
    responses:
      '201':
        description: "Smartwatch creado exitosamente."
      '400':
        description: "Error en la solicitud, faltan campos requeridos."
    """
    data = request.get_json()
    if not data or not data.get('device_id') or not data.get('model'):
        return jsonify({"error": "Los campos 'device_id' y 'model' son requeridos"}), 400

    smartwatch_id = SmartwatchModel.create(data)
    if smartwatch_id:
        return jsonify({"message": "Smartwatch creado", "id": smartwatch_id}), 201
    return jsonify({"error": "No se pudo crear el smartwatch"}), 500


@smartwatches_bp.route('/<int:smartwatch_id>/deactivate', methods=['PUT'])
#@jwt_required()
def deactivate_smartwatch(smartwatch_id):
    """
    Desactivar un smartwatch
    ---
    tags:
      - Smartwatches
    summary: "Cambia el estado de un smartwatch a 'inactive'."
    parameters:
      - name: smartwatch_id
        in: path
        required: true
        description: "ID del smartwatch a desactivar."
        schema:
          type: integer
    responses:
      '200':
        description: "Smartwatch desactivado exitosamente."
      '404':
        description: "Smartwatch no encontrado."
    """
    if SmartwatchModel.deactivate(smartwatch_id):
        return jsonify({"message": "Smartwatch desactivado"})
    return jsonify({"error": "Smartwatch no encontrado o no se pudo actualizar"}), 404