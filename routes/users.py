from flask import Blueprint, request, jsonify
from models.user_model import UserModel

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['GET'])
def get_users():
    """
    Obtener todos los usuarios
    ---
    tags:
      - Users
    summary: "Obtiene una lista de todos los usuarios."
    description: "Devuelve una lista de objetos de usuario, sin incluir la contraseña."
    responses:
      '200':
        description: "Lista de usuarios obtenida exitosamente."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id_user: {type: integer}
                  id_daycare: {type: integer, nullable: true}
                  username: {type: string}
                  first_name: {type: string}
                  last_name: {type: string}
                  email: {type: string}
                  role: {type: string, enum: ['admin', 'teacher', 'tutor']}
                  created_at: {type: string, format: date-time}
    """
    users = UserModel.get_all()
    return jsonify(users)


@users_bp.route('/<int:id_user>', methods=['GET'])
def get_user(id_user):
    """
    Obtener un usuario por ID
    ---
    tags:
      - Users
    summary: "Obtiene los detalles de un usuario específico por su ID."
    parameters:
      - name: id_user
        in: path
        required: true
        description: "ID del usuario a obtener."
        schema:
          type: integer
    responses:
      '200':
        description: "Detalles del usuario."
      '404':
        description: "Usuario no encontrado."
    """
    user = UserModel.get_by_id(id_user)
    if user:
        return jsonify(user)
    return jsonify({"error": "Usuario no encontrado"}), 404


@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Crear un nuevo usuario
    ---
    tags:
      - Users
    summary: "Registra un nuevo usuario en el sistema."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id_daycare:
                type: integer
                description: "ID de la guardería a la que pertenece (opcional)."
                example: 1
              username:
                type: string
                example: "j.perez"
              password:
                type: string
                format: password
                example: "supersecret123"
              first_name:
                type: string
                example: "Juan"
              last_name:
                type: string
                example: "Perez"
              email:
                type: string
                format: email
                example: "juan.perez@example.com"
              role:
                type: string
                enum: ['admin', 'teacher', 'tutor']
                example: "tutor"
            required:
              - username
              - password
              - first_name
              - last_name
              - email
              - role
    responses:
      '201':
        description: "Usuario creado exitosamente."
      '400':
        description: "Error en la solicitud, faltan campos requeridos."
      '409':
        description: "Conflicto, el username o email ya existen."
    """
    data = request.get_json()
    required_fields = ['username', 'password', 'first_name', 'last_name', 'email', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    user_id = UserModel.create(data)
    return jsonify({"message": "Usuario creado", "id": user_id}), 201


@users_bp.route('/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    """
    Actualizar un usuario
    ---
    tags:
      - Users
    summary: "Actualiza los datos de un usuario existente."
    description: "Este endpoint no actualiza la contraseña."
    parameters:
      - name: id_user
        in: path
        required: true
        description: "ID del usuario a actualizar."
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id_daycare: {type: integer, nullable: true}
              username: {type: string}
              first_name: {type: string}
              last_name: {type: string}
              email: {type: string, format: email}
              role: {type: string, enum: ['admin', 'teacher', 'tutor']}
            required:
              - username
              - first_name
              - last_name
              - email
              - role
    responses:
      '200':
        description: "Usuario actualizado exitosamente."
      '400':
        description: "Datos inválidos o campos faltantes."
      '404':
        description: "Usuario no encontrado."
    """
    data = request.get_json()
    required_fields = ['username', 'first_name', 'last_name', 'email', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    if UserModel.update(id_user, data):
        return jsonify({"message": "Usuario actualizado"})
    return jsonify({"error": "Usuario no encontrado"}), 404


@users_bp.route('/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    """
    Eliminar un usuario
    ---
    tags:
      - Users
    summary: "Elimina un usuario de la base de datos por su ID."
    parameters:
      - name: id_user
        in: path
        required: true
        description: "ID del usuario a eliminar."
        schema:
          type: integer
    responses:
      '200':
        description: "Usuario eliminado exitosamente."
      '404':
        description: "Usuario no encontrado."
    """
    if UserModel.delete(id_user):
        return jsonify({"message": "Usuario eliminado"})
    return jsonify({"error": "Usuario no encontrado"}), 404

