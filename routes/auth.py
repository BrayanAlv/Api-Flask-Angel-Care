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
    summary: "Autentica un usuario y devuelve un token JWT junto con su info."
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
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
                user:
                  type: object
                  properties:
                    id_user:
                      type: integer
                    role:
                      type: string
                    username:
                      type: string
      '401':
        description: "Credenciales inválidas."
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username y password son requeridos"}), 400

    # 1. Buscar al usuario
    user = UserModel.get_by_username(username)

    # 2. Verificar password
    if user and check_password_hash(user['password'], password):
        
        # 3. Crear token (puedes agregar claims adicionales si quieres)
        # Es útil guardar el rol dentro del token también para validaciones en el backend
        access_token = create_access_token(identity=user['id_user'], additional_claims={"role": user['role']})
        
        # 4. RETORNAR TOKEN + DATOS DEL USUARIO
        return jsonify({
            "access_token": access_token,
            "user": {
                "id_user": user['id_user'],
                "role": user['role'],
              
            }
        }), 200

    return jsonify({"error": "Credenciales inválidas"}), 401