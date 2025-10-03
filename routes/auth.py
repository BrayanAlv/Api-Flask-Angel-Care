# routes/auth.py
from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de Login
    ---
    tags:
      - Auth
    summary: "Autentica un usuario y devuelve un token JWT."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
                example: "j.perez"
              password:
                type: string
                format: password
                example: "supersecret123"
            required:
              - username
              - password
    responses:
      '200':
        description: "Autenticación exitosa."
      '401':
        description: "Credenciales inválidas."
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username y password son requeridos"}), 400

    # 1. Buscar al usuario en la base de datos
    user = UserModel.get_by_username(username)

    # 2. Verificar si el usuario existe y la contraseña es correcta
    if user and check_password_hash(user['password'], password):
        # 3. Crear el token si las credenciales son válidas
        # La 'identity' es lo que se guardará dentro del token para identificar al usuario.
        # Usar el ID del usuario es una práctica común.
        access_token = create_access_token(identity=user['id_user'])
        return jsonify(access_token=access_token)

    return jsonify({"error": "Credenciales inválidas"}), 401