from flask import Blueprint, request, jsonify
from models.child_model import ChildModel
from models.smartwatches_models import SmartwatchModel
from flask_jwt_extended import jwt_required
import datetime

children_bp = Blueprint('children', __name__, url_prefix='/api')

@children_bp.route('/teachers/<int:teacher_id>/children', methods=['GET'])
# @jwt_required()
def get_children_by_teacher(teacher_id):
    """
    Listado de niños por cuidador
    ---
    tags:
      - Teachers
    summary: "Obtiene la lista de niños asignados a la guardería de un cuidador específico."
    parameters:
      - name: teacher_id
        in: path
        required: true
        description: "ID del cuidador (teacher)."
        schema:
          type: integer
    responses:
      '200':
        description: "Lista de niños obtenida exitosamente."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id_child: {type: integer}
                  first_name: {type: string}
                  last_name: {type: string}
                  birth_date: {type: string, format: date}
    """
    children = ChildModel.get_by_teacher_id(teacher_id)
    return jsonify(children)


@children_bp.route('/children/<int:child_id>', methods=['GET'])
# @jwt_required()
def get_child_full_details(child_id):
    """
    Datos completos de un niño
    ---
    tags:
      - Children
    summary: "Obtiene los detalles personales completos de un niño por su ID."
    parameters:
      - name: child_id
        in: path
        required: true
        description: "ID del niño."
        schema:
          type: integer
    responses:
      '200':
        description: "Detalles del niño obtenidos exitosamente."
        content:
          application/json:
            schema:
              type: object
              # Aquí defines las propiedades que devuelve tu ChildModel.get_details_by_id
              properties:
                id_child: {type: integer}
                first_name: {type: string}
                last_name: {type: string}
                birth_date: {type: string, format: date}
                id_daycare: {type: integer}
                id_tutor: {type: integer}
                id_smartwatch: {type: integer}
      '404':
        description: "Niño no encontrado."
    """
    child_info = ChildModel.get_details_by_id(child_id)
    if not child_info:
        return jsonify({"error": "Niño no encontrado"}), 404
    return jsonify(child_info)


@children_bp.route('/smartwatches/<int:smartwatch_id>/details', methods=['GET'])
# @jwt_required()
def get_smartwatch_child_details(smartwatch_id):
    """
    Búsqueda de niño y guardería por ID de Smartwatch
    ---
    tags:
      - Smartwatches
    summary: "Obtiene los detalles del smartwatch, del niño que lo usa y de su guardería."
    parameters:
      - name: smartwatch_id
        in: path
        required: true
        description: "ID del smartwatch."
        schema:
          type: integer
    responses:
      '200':
        description: "Detalles obtenidos exitosamente."
        content:
          application/json:
            schema:
              type: object
              properties:
                id_smartwatch: {type: integer}
                device_id: {type: string}
                model: {type: string}
                status: {type: string}
                child_first_name: {type: string}
                child_last_name: {type: string}
                birth_date: {type: string, format: date}
                daycare_name: {type: string}
      '404':
        description: "Smartwatch no encontrado o sin asignar."
    """
    details = SmartwatchModel.get_details_with_child(smartwatch_id)
    if details:
        return jsonify(details)
    return jsonify({"error": "Smartwatch no encontrado o sin asignar"}), 404


@children_bp.route('/children/<int:child_id>/tutor', methods=['GET'])
# @jwt_required()
def get_tutor_by_child(child_id):
    """
    Obtener datos del tutor por ID del niño
    ---
    tags:
      - Children
    summary: "Obtiene la información de contacto del padre o tutor de un niño."
    parameters:
      - name: child_id
        in: path
        required: true
        description: "ID del niño."
        schema:
          type: integer
    responses:
      '200':
        description: "Datos del tutor obtenidos exitosamente."
        content:
          application/json:
            schema:
              type: object
              properties:
                id_user: {type: integer}
                first_name: {type: string}
                last_name: {type: string}
                email: {type: string, format: email}
      '404':
        description: "Tutor no encontrado para este niño."
    """
    tutor = ChildModel.get_tutor_by_child_id(child_id)
    if tutor:
        return jsonify(tutor)
    return jsonify({"error": "Tutor no encontrado para este niño"}), 404


@children_bp.route('/children/<int:child_id>/teachers', methods=['GET'])
# @jwt_required()
def get_teachers_by_child(child_id):
    """
    Obtener datos de los cuidadores del niño
    ---
    tags:
      - Children
    summary: "Obtiene una lista de los cuidadores (teachers) de la guardería a la que asiste el niño."
    parameters:
      - name: child_id
        in: path
        required: true
        description: "ID del niño."
        schema:
          type: integer
    responses:
      '200':
        description: "Lista de cuidadores obtenida exitosamente."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  first_name: {type: string}
                  last_name: {type: string}
                  email: {type: string, format: email}
                  daycare_phone: {type: string}
    """
    teachers = ChildModel.get_teachers_by_child_id(child_id)
    return jsonify(teachers)


@children_bp.route('/children/<int:child_id>/sensors/average', methods=['GET'])
# @jwt_required()
def get_sensor_averages(child_id):
    """
    Promedio de sensores en un día específico
    ---
    tags:
      - Children
      - Sensors
    summary: "Calcula los promedios de las lecturas de los sensores para un niño en una fecha específica."
    parameters:
      - name: child_id
        in: path
        required: true
        description: "ID del niño."
        schema:
          type: integer
      - name: date
        in: query
        required: true
        description: "Fecha para el cálculo de promedios en formato YYYY-MM-DD."
        schema:
          type: string
          format: date
    responses:
      '200':
        description: "Promedios calculados exitosamente."
        content:
          application/json:
            schema:
              type: object
              properties:
                first_name: {type: string}
                last_name: {type: string}
                avg_temperature: {type: number, format: float}
                avg_heart_rate: {type: number, format: float}
                avg_spo2_level: {type: number, format: float}
      '400':
        description: "El parámetro 'date' es requerido o tiene un formato inválido."
      '404':
        description: "No se encontraron datos para este niño en la fecha especificada."
    """
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({"error": "El parámetro 'date' (YYYY-MM-DD) es requerido"}), 400

    try:
        datetime.date.fromisoformat(date_str)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    averages = ChildModel.get_sensor_averages(child_id, date_str)
    if averages:
        return jsonify(averages)
    return jsonify({"error": "No se encontraron datos para este niño en la fecha especificada"}), 404