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
    description: "Verifica las credenciales del usuario contra la base de datos y, si son correctas, retorna un token de acceso válido y los datos del perfil del usuario."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
                description: "Nombre de usuario para iniciar sesión."
                example: "caregiver_ana"
              password:
                type: string
                format: password
                description: "Contraseña del usuario."
                example: "password123"
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
                  description: "Token JWT para utilizar en endpoints protegidos."
                user:
                  type: object
                  description: "Información del usuario autenticado."
                  properties:
                    id_user:
                      type: integer
                      example: 3
                    id_daycare:
                      type: integer
                      nullable: true
                      example: 1
                    username:
                      type: string
                      example: "caregiver_ana"
                    first_name:
                      type: string
                      example: "Ana"
                    last_name:
                      type: string
                      example: "Martínez"
                    email:
                      type: string
                      example: "ana@email.com"
                    phone:
                      type: string
                      description: "Teléfono de contacto."
                      example: "664-555-0103"
                    role:
                      type: string
                      example: "caregiver"
      '400':
        description: "Solicitud incorrecta (faltan datos)."
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Username y password son requeridos"
      '401':
        description: "Credenciales inválidas."
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Credenciales inválidas"
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username y password son requeridos"}), 400

    # 1. Buscar al usuario (incluye password hash)
    user = UserModel.get_by_username(username)

    # 2. Verificar password
    if user and check_password_hash(user['password'], password):
        
        # 3. Crear token (Identity = id_user, claims = role)
        # Es buena práctica incluir el rol en el token para validaciones rápidas
        access_token = create_access_token(identity=user['id_user'], additional_claims={"role": user['role']})
        
        # 4. RETORNAR TOKEN + DATOS DEL USUARIO
        # Aquí agregamos el campo 'phone' a la respuesta
        return jsonify({
            "access_token": access_token,
            "user": {
                "id_user": user['id_user'],
                "id_daycare": user.get('id_daycare'),
                "username": user['username'],
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "email": user['email'],
                "phone": user.get('phone'),  # <--- NUEVO CAMPO
                "role": user['role']
            }
        }), 200

    return jsonify({"error": "Credenciales inválidas"}), 401