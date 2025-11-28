from flask import Blueprint, request, jsonify
from models.child_model import ChildModel
from models.smartwatches_models import SmartwatchModel
from flask_jwt_extended import jwt_required
import datetime

children_bp = Blueprint('children', __name__, url_prefix='/api')

@children_bp.route('/children', methods=['GET'])
def get_all_children():
    """
    Obtener todos los niños con relaciones
    ---
    tags:
      - Children
    summary: "Obtiene todos los niños con información de guardería, tutor, cuidador y smartwatch."
    description: "Retorna un arreglo de niños con datos enriquecidos provenientes de las tablas relacionadas (daycares, users y smartwatches)."
    responses:
      '200':
        description: "Lista de niños con relaciones."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id_child:
                    type: integer
                    description: "ID del niño"
                    example: 7
                  child_first_name:
                    type: string
                    description: "Nombre del niño"
                    example: "Sofía"
                  child_last_name:
                    type: string
                    description: "Apellido del niño"
                    example: "López"
                  birth_date:
                    type: string
                    format: date
                    description: "Fecha de nacimiento"
                    example: "2020-06-15"
                  daycare_name:
                    type: string
                    description: "Nombre de la guardería"
                    example: "Pequeños Gigantes"
                  tutor_first_name:
                    type: string
                    description: "Nombre del tutor"
                    example: "María"
                  tutor_last_name:
                    type: string
                    description: "Apellido del tutor"
                    example: "García"
                  caregiver_first_name:
                    type: string
                    nullable: true
                    description: "Nombre del cuidador (puede ser nulo)"
                    example: "Carlos"
                  caregiver_last_name:
                    type: string
                    nullable: true
                    description: "Apellido del cuidador (puede ser nulo)"
                    example: "Ramírez"
                  device_id:
                    type: string
                    description: "Identificador del smartwatch asignado"
                    example: "SW-ABC123"
                  smartwatch_model:
                    type: string
                    description: "Modelo del smartwatch"
                    example: "KidsSafe v2"
            examples:
              ejemplo:
                summary: "Ejemplo de respuesta"
                value:
                  - id_child: 7
                    child_first_name: "Sofía"
                    child_last_name: "López"
                    birth_date: "2020-06-15"
                    daycare_name: "Pequeños Gigantes"
                    tutor_first_name: "María"
                    tutor_last_name: "García"
                    caregiver_first_name: "Carlos"
                    caregiver_last_name: "Ramírez"
                    device_id: "SW-ABC123"
                    smartwatch_model: "KidsSafe v2"
                  - id_child: 8
                    child_first_name: "Diego"
                    child_last_name: "Pérez"
                    birth_date: "2019-11-02"
                    daycare_name: "Pequeños Gigantes"
                    tutor_first_name: "Luis"
                    tutor_last_name: "Pérez"
                    caregiver_first_name: null
                    caregiver_last_name: null
                    device_id: "SW-XYZ789"
                    smartwatch_model: "AngelCare Band"
    """
    data = ChildModel.get_all_with_relations()
    return jsonify(data)

@children_bp.route('/children/with-tutor-caregiver', methods=['GET'])
def get_children_with_tutor_caregiver_daycare():
    """
    Niños con guardería, tutor y cuidador (consulta específica)
    ---
    tags:
      - Children
    summary: "Obtiene los niños con datos de guardería, tutor y cuidador usando la consulta solicitada."
    description: |
      Ejecuta exactamente la siguiente consulta SQL para devolver la información solicitada:

      SELECT
          c.id_child,
          c.first_name AS child_first_name,
          c.last_name AS child_last_name,
          c.birth_date,
          d.name AS daycare_name,
          t.first_name AS tutor_first_name,
          t.last_name AS tutor_last_name,
          ca.first_name AS caregiver_first_name,
          ca.last_name AS caregiver_last_name

      FROM
          children c
      JOIN
          daycares d ON c.id_daycare = d.id_daycare
      JOIN
          users t ON c.id_tutor = t.id_user
      JOIN
          users ca ON c.id_caregiver = ca.id_user;
    responses:
      '200':
        description: "Lista de niños con los campos pedidos."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id_child:
                    type: integer
                    example: 5
                  child_first_name:
                    type: string
                    example: "Ana"
                  child_last_name:
                    type: string
                    example: "Gómez"
                  birth_date:
                    type: string
                    format: date
                    example: "2020-01-20"
                  daycare_name:
                    type: string
                    example: "Peques House"
                  tutor_first_name:
                    type: string
                    example: "Luis"
                  tutor_last_name:
                    type: string
                    example: "Gómez"
                  caregiver_first_name:
                    type: string
                    example: "Carla"
                  caregiver_last_name:
                    type: string
                    example: "Rojas"
            examples:
              ejemplo:
                summary: "Ejemplo de respuesta"
                value:
                  - id_child: 5
                    child_first_name: "Ana"
                    child_last_name: "Gómez"
                    birth_date: "2020-01-20"
                    daycare_name: "Peques House"
                    tutor_first_name: "Luis"
                    tutor_last_name: "Gómez"
                    caregiver_first_name: "Carla"
                    caregiver_last_name: "Rojas"
                  - id_child: 6
                    child_first_name: "Mario"
                    child_last_name: "Paz"
                    birth_date: "2019-10-11"
                    daycare_name: "Peques House"
                    tutor_first_name: "Elena"
                    tutor_last_name: "Paz"
                    caregiver_first_name: "Hugo"
                    caregiver_last_name: "Luna"
    """
    data = ChildModel.get_children_with_tutor_caregiver_daycare()
    return jsonify(data)

@children_bp.route('/caregiver/<int:caregiver_id>/children', methods=['GET'])
# @jwt_required()
def get_children_by_caregiver(caregiver_id):
    """
    Listado de niños por cuidador
    ---
    tags:
      - caregiver
    summary: "Obtiene la lista de niños asignados a la guardería de un cuidador específico."
    parameters:
      - name: caregiver_id
        in: path
        required: true
        description: "ID del cuidador (caregiver)."
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
    children = ChildModel.get_by_caregiver_id(caregiver_id)
    return jsonify(children)


@children_bp.route('/tutor/<int:tutor_id>/children', methods=['GET'])
# @jwt_required()
def get_children_by_tutor(tutor_id):
    """
    Listado de niños por tutor (Padre)
    ---
    tags:
      - Children
    summary: "Obtiene los niños asociados a un tutor específico."
    parameters:
      - name: tutor_id
        in: path
        required: true
        description: "ID del tutor (usuario con rol tutor)."
        schema:
          type: integer
    responses:
      '200':
        description: "Lista de niños encontrada."
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
                  daycare_name: {type: string}
                  device_id: {type: string}
    """
    children = ChildModel.get_by_tutor_id(tutor_id)
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


@children_bp.route('/children/<int:child_id>/caregiver', methods=['GET'])
# @jwt_required()
def get_caregiver_by_child(child_id):
    """
    Obtener datos de los cuidadores del niño
    ---
    tags:
      - Children
    summary: "Obtiene una lista de los cuidadores (caregiver) de la guardería a la que asiste el niño."
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
    caregiver = ChildModel.get_caregivers_by_child_id(child_id)
    return jsonify(caregiver)


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


@children_bp.route('/children', methods=['POST'])
# @jwt_required()
def create_child():
    """
    Crear un nuevo niño y asignar tutor (y opcionalmente cuidador y smartwatch)
    ---
    tags:
      - Children
    summary: "Crea un nuevo niño y lo asocia con un tutor."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [first_name, last_name, birth_date, id_daycare, id_tutor]
            properties:
              first_name: {type: string}
              last_name: {type: string}
              birth_date: {type: string, format: date}
              id_daycare: {type: integer}
              id_tutor: {type: integer}
              id_smartwatch: {type: integer, nullable: true}
              id_caregiver: {type: integer, nullable: true}
    responses:
      '201':
        description: "Niño creado exitosamente."
      '400':
        description: "Datos inválidos o faltantes."
    """
    body = request.get_json(silent=True) or {}
    required = ["first_name", "last_name", "birth_date", "id_daycare", "id_tutor"]
    missing = [k for k in required if not body.get(k)]
    if missing:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing)}"}), 400
    # validar fecha
    try:
        datetime.date.fromisoformat(body["birth_date"])
    except Exception:
        return jsonify({"error": "Formato de fecha inválido en 'birth_date'. Use YYYY-MM-DD."}), 400

    child = ChildModel.create_child(
        first_name=body["first_name"],
        last_name=body["last_name"],
        birth_date=body["birth_date"],
        id_daycare=body["id_daycare"],
        id_tutor=body["id_tutor"],
        id_smartwatch=body.get("id_smartwatch"),
        id_caregiver=body.get("id_caregiver"),
    )
    if not child:
        return jsonify({"error": "No se pudo crear el niño."}), 400
    return jsonify(child), 201


@children_bp.route('/children/<int:child_id>', methods=['PATCH'])
# @jwt_required()
def update_child(child_id):
    """
    Actualizar datos de un niño
    ---
    tags:
      - Children
    summary: "Actualiza datos del niño (parcial o completo)."
    parameters:
      - name: child_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              first_name: {type: string}
              last_name: {type: string}
              birth_date: {type: string, format: date}
              id_daycare: {type: integer}
              id_tutor: {type: integer}
              id_smartwatch: {type: integer}
              id_caregiver: {type: integer}
    responses:
      '200':
        description: "Datos actualizados."
      '400':
        description: "Solicitud inválida."
      '404':
        description: "Niño no encontrado."
    """
    body = request.get_json(silent=True) or {}

    if "birth_date" in body:
        try:
            datetime.date.fromisoformat(body["birth_date"])
        except Exception:
            return jsonify({"error": "Formato de fecha inválido en 'birth_date'. Use YYYY-MM-DD."}), 400

    updated = ChildModel.update_child(child_id, body)
    if not updated:
        # comprobar si el niño existe
        exists = ChildModel.get_details_by_id(child_id)
        if not exists:
            return jsonify({"error": "Niño no encontrado"}), 404
        return jsonify({"error": "No hay cambios aplicables o datos inválidos"}), 400
    return jsonify(updated)


# --- RUTAS PARA NOTAS (CRUD COMPLETO) ---

@children_bp.route('/children/<int:child_id>/notes', methods=['GET'])
# @jwt_required()
def get_child_notes(child_id):
    """
    Obtener las notas/reportes de un niño
    ---
    tags:
      - Children Notes
    summary: "Obtiene el historial de notas, incidentes o reportes de un niño."
    parameters:
      - name: child_id
        in: path
        required: true
        description: "ID del niño."
        schema:
          type: integer
    responses:
      '200':
        description: "Lista de notas obtenida exitosamente."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id_note: {type: integer}
                  title: {type: string}
                  content: {type: string}
                  priority: {type: string, enum: [low, medium, high]}
                  created_at: {type: string, format: date-time}
                  author_first_name: {type: string}
                  author_last_name: {type: string}
                  author_role: {type: string}
    """
    notes = ChildModel.get_notes(child_id)
    return jsonify(notes)


@children_bp.route('/children/<int:child_id>/notes', methods=['POST'])
# @jwt_required()
def create_child_note(child_id):
    """
    Crear una nota para un niño
    ---
    tags:
      - Children Notes
    summary: "Agrega una nota, reporte o incidente al historial del niño."
    parameters:
      - name: child_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [id_author, title, content, priority]
            properties:
              id_author:
                type: integer
                description: "ID del usuario que escribe la nota (profesor o admin)"
              title:
                type: string
                example: "No quiso comer"
              content:
                type: string
                example: "El niño rechazó las verduras durante el almuerzo."
              priority:
                type: string
                enum: [low, medium, high]
                example: "medium"
    responses:
      '201':
        description: "Nota creada exitosamente."
      '400':
        description: "Datos faltantes o prioridad inválida."
    """
    body = request.get_json(silent=True) or {}
    
    required = ["id_author", "title", "content", "priority"]
    missing = [k for k in required if not body.get(k)]
    if missing:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing)}"}), 400

    valid_priorities = ["low", "medium", "high"]
    if body["priority"] not in valid_priorities:
        return jsonify({"error": f"Prioridad inválida. Use: {', '.join(valid_priorities)}"}), 400

    note_id = ChildModel.create_note(
        child_id=child_id,
        id_author=body["id_author"],
        title=body["title"],
        content=body["content"],
        priority=body["priority"]
    )

    if note_id:
        return jsonify({"message": "Nota creada exitosamente", "id_note": note_id}), 201
    
    return jsonify({"error": "No se pudo crear la nota. Verifique que el autor y el niño existan."}), 400


@children_bp.route('/notes/<int:note_id>', methods=['PATCH'])
# @jwt_required()
def update_child_note(note_id):
    """
    Actualizar una nota existente
    ---
    tags:
      - Children Notes
    summary: "Edita el título, contenido o prioridad de una nota."
    parameters:
      - name: note_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title: {type: string}
              content: {type: string}
              priority: {type: string, enum: [low, medium, high]}
    responses:
      '200':
        description: "Nota actualizada correctamente."
      '400':
        description: "Datos inválidos o sin cambios."
      '404':
        description: "Nota no encontrada."
    """
    body = request.get_json(silent=True) or {}
    
    if "priority" in body:
        valid_priorities = ["low", "medium", "high"]
        if body["priority"] not in valid_priorities:
             return jsonify({"error": f"Prioridad inválida. Use: {', '.join(valid_priorities)}"}), 400

    existing_note = ChildModel.get_note_by_id(note_id)
    if not existing_note:
        return jsonify({"error": "Nota no encontrada"}), 404

    success = ChildModel.update_note(note_id, body)
    
    if success:
        updated_note = ChildModel.get_note_by_id(note_id)
        return jsonify({"message": "Nota actualizada", "note": updated_note})
    
    return jsonify({"error": "No se pudieron aplicar los cambios"}), 400


@children_bp.route('/notes/<int:note_id>', methods=['DELETE'])
# @jwt_required()
def delete_child_note(note_id):
    """
    Eliminar una nota
    ---
    tags:
      - Children Notes
    summary: "Elimina una nota del historial del niño."
    parameters:
      - name: note_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      '200':
        description: "Nota eliminada correctamente."
      '404':
        description: "Nota no encontrada."
    """
    existing_note = ChildModel.get_note_by_id(note_id)
    if not existing_note:
        return jsonify({"error": "Nota no encontrada"}), 404

    success = ChildModel.delete_note(note_id)
    
    if success:
        return jsonify({"message": "Nota eliminada correctamente"}), 200
    
    return jsonify({"error": "Error al eliminar la nota"}), 500


# --- RUTAS PARA SCHEDULES (HORARIOS) ---

@children_bp.route('/children/<int:child_id>/schedule', methods=['GET'])
# @jwt_required()
def get_child_schedule(child_id):
    """
    Obtener el horario semanal del niño
    ---
    tags:
      - Children Schedule
    summary: "Obtiene las actividades programadas en el horario semanal del niño."
    parameters:
      - name: child_id
        in: path
        required: true
        description: "ID del niño."
        schema:
          type: integer
    responses:
      '200':
        description: "Lista de actividades obtenida exitosamente."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id_schedule: {type: integer}
                  day_of_week: {type: string, enum: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]}
                  start_time: {type: string, format: time, example: "09:00"}
                  end_time: {type: string, format: time, example: "10:00"}
                  activity_name: {type: string}
                  description: {type: string}
    """
    schedule = ChildModel.get_schedules(child_id)
    return jsonify(schedule)


@children_bp.route('/children/<int:child_id>/schedule', methods=['POST'])
# @jwt_required()
def create_child_schedule(child_id):
    """
    Agregar actividad al horario
    ---
    tags:
      - Children Schedule
    summary: "Agrega una nueva actividad al horario semanal." 
    parameters:
      - name: child_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [day_of_week, start_time, end_time, activity_name]
            properties:
              day_of_week: 
                type: string
                enum: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
              start_time: 
                type: string
                example: "09:00"
              end_time: 
                type: string
                example: "10:00"
              activity_name: 
                type: string
              description: 
                type: string
    responses:
      '201':
        description: "Actividad creada."
      '400':
        description: "Datos faltantes."
    """
    body = request.get_json(silent=True) or {}
    
    required = ["day_of_week", "start_time", "end_time", "activity_name"]
    missing = [k for k in required if not body.get(k)]
    if missing:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing)}"}), 400

    schedule_id = ChildModel.create_schedule(
        child_id=child_id,
        day_of_week=body["day_of_week"],
        start_time=body["start_time"],
        end_time=body["end_time"],
        activity_name=body["activity_name"],
        description=body.get("description", "")
    )

    if schedule_id:
        return jsonify({"message": "Actividad agregada al horario", "id_schedule": schedule_id}), 201
    
    return jsonify({"error": "No se pudo crear la actividad."}), 400


@children_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
# @jwt_required()
def delete_child_schedule(schedule_id):
    """
    Eliminar actividad del horario
    ---
    tags:
      - Children Schedule
    summary: "Elimina una actividad del horario por su ID."
    parameters:
      - name: schedule_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      '200':
        description: "Actividad eliminada correctamente."
      '404':
        description: "Actividad no encontrada."
    """
    existing_schedule = ChildModel.get_schedule_by_id(schedule_id)
    if not existing_schedule:
        return jsonify({"error": "Actividad no encontrada"}), 404

    success = ChildModel.delete_schedule(schedule_id)
    
    if success:
        return jsonify({"message": "Actividad eliminada correctamente"}), 200
    
    return jsonify({"error": "Error al eliminar la actividad"}), 500  