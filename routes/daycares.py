from flask import Blueprint, request, jsonify
from models.daycare_model import DaycareModel
from flask_jwt_extended import jwt_required


daycares_bp = Blueprint('daycares', __name__, url_prefix='/api/daycares')


@daycares_bp.route('/', methods=['GET'])
def get_daycares():
    """
    Obtener todas las guarderías
    ---
    tags:
      - Daycares
    summary: "Obtiene una lista de todas las guarderías."
    responses:
      '200':
        description: "Lista de guarderías obtenida exitosamente."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id_daycare: {type: integer}
                  name: {type: string}
                  address: {type: string}
                  phone: {type: string}
    """
    daycares = DaycareModel.get_all()
    return jsonify(daycares)


@daycares_bp.route('/<int:id_daycare>', methods=['GET'])
def get_daycare(id_daycare):
    """
    Obtener una guardería por ID
    ---
    tags:
      - Daycares
    summary: "Obtiene los detalles de una guardería específica por su ID."
    parameters:
      - name: id_daycare
        in: path
        required: true
        description: "ID de la guardería a obtener."
        schema:
          type: integer
    responses:
      '200':
        description: "Detalles de la guardería."
      '404':
        description: "Guardería no encontrada."
    """
    daycare = DaycareModel.get_by_id(id_daycare)
    if daycare:
        return jsonify(daycare)
    return jsonify({"error": "Guardería no encontrada"}), 404

# --- Rutas Protegidas (requieren token) ---

@daycares_bp.route('/', methods=['POST'])
@jwt_required()
def create_daycare():
    """
    Crear una nueva guardería
    ---
    tags:
      - Daycares
    summary: "Registra una nueva guardería en la base de datos."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: "Nombre de la guardería (requerido)."
                example: "Estancia El Solecito"
              address:
                type: string
                description: "Dirección de la guardería."
                example: "Av. Revolución 123"
              phone:
                type: string
                description: "Teléfono de contacto."
                example: "664-555-0101"
            required:
              - name
    responses:
      '201':
        description: "Guardería creada exitosamente."
      '400':
        description: "Error en la solicitud, falta el campo 'name'."
    """
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "El campo 'name' es requerido"}), 400

    daycare_id = DaycareModel.create(data)
    return jsonify({"message": "Guardería creada", "id": daycare_id}), 201


@daycares_bp.route('/<int:id_daycare>', methods=['PUT'])
@jwt_required()
def update_daycare(id_daycare):
    """
    Actualizar una guardería
    ---
    tags:
      - Daycares
    summary: "Actualiza los datos de una guardería existente."
    parameters:
      - name: id_daycare
        in: path
        required: true
        description: "ID de la guardería a actualizar."
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name: {type: string, description: "Nuevo nombre de la guardería."}
              address: {type: string, description: "Nueva dirección."}
              phone: {type: string, description: "Nuevo teléfono."}
            required:
              - name
    responses:
      '200':
        description: "Guardería actualizada exitosamente."
      '400':
        description: "Datos inválidos, falta el campo 'name'."
      '404':
        description: "Guardería no encontrada."
    """
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "El campo 'name' es requerido"}), 400

    if DaycareModel.update(id_daycare, data):
        return jsonify({"message": "Guardería actualizada"})
    return jsonify({"error": "Guardería no encontrada"}), 404


@daycares_bp.route('/<int:id_daycare>', methods=['DELETE'])
@jwt_required()
def delete_daycare(id_daycare):
    """
    Eliminar una guardería
    ---
    tags:
      - Daycares
    summary: "Elimina una guardería de la base de datos por su ID."
    parameters:
      - name: id_daycare
        in: path
        required: true
        description: "ID de la guardería a eliminar."
        schema:
          type: integer
    responses:
      '200':
        description: "Guardería eliminada exitosamente."
      '404':
        description: "Guardería no encontrada."
    """
    if DaycareModel.delete(id_daycare):
        return jsonify({"message": "Guardería eliminada"})
    return jsonify({"error": "Guardería no encontrada"}), 404