from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel:

    @staticmethod
    def get_all():
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            # SE AGREGA 'phone'
            query = "SELECT id_user, id_daycare, username, first_name, last_name, email, phone, role, created_at FROM users"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_id(id_user):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            # SE AGREGA 'phone'
            query = "SELECT id_user, id_daycare, username, first_name, last_name, email, phone, role, created_at FROM users WHERE id_user = %s"
            cursor.execute(query, (id_user,))
            return cursor.fetchone()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def create(data):
        conn = None
        try:
            hashed_password = generate_password_hash(data['password'])
            conn = get_db_connection()
            cursor = conn.cursor()
            # SE AGREGA 'phone'
            query = """
                INSERT INTO users (id_daycare, username, password, first_name, last_name, email, phone, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data.get('id_daycare'), data['username'], hashed_password,
                data['first_name'], data['last_name'], data['email'], data.get('phone'), data['role']
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def update(id_user, data):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # SE AGREGA 'phone' EN EL UPDATE
            query = """
                UPDATE users SET id_daycare = %s, username = %s, first_name = %s, last_name = %s, email = %s, phone = %s, role = %s
                WHERE id_user = %s
            """
            cursor.execute(query, (
                data.get('id_daycare'), data['username'], data['first_name'],
                data['last_name'], data['email'], data.get('phone'), data['role'], id_user
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def delete(id_user):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id_user = %s", (id_user,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_username(username):
        """Obtiene un usuario por su username, incluyendo la contraseña."""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            # SE SELECCIONA TODO, ASÍ QUE 'phone' YA ESTÁ INCLUIDO
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()