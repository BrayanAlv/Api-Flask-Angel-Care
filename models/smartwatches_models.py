from db import get_db_connection

        ### ----- ###     QUERYS     ### ----- ###
QUERY_GET_ALL = "SELECT * FROM smartwatches ORDER BY id_smartwatch"
QUERY_GET_BY_ID = "SELECT * FROM smartwatches WHERE id_smartwatch = %s"
QUERY_GET_BY_CHILD_ID = "SELECT * FROM smartwatches WHERE id_child = %s"
QUERY_INSERT = "INSERT INTO smartwatches (device_id, model, status) VALUES (%s, %s, %s)"
QUERY_DEACTIVATE = "UPDATE smartwatches SET status = 'inactive' WHERE id_smartwatch = %s"
QUERY_DELETE = "DELETE FROM smartwatches WHERE id_smartwatch = %s"
QUERY_UPDATE = "UPDATE smartwatches SET status = %s, model = %s WHERE id_smartwatch = %s"
QUERY_UNLINK_FROM_CHILDREN = "UPDATE children SET id_smartwatch = NULL WHERE id_smartwatch = %s"


class SmartwatchModel:
    @staticmethod
    def get_all():
        """Obtiene todos los smartwatches."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(QUERY_GET_ALL)
                    return cursor.fetchall()
        except Exception as e:
            # Opcional: Manejar el error de forma más específica
            print(f"Error en get_all: {e}")
            return []

    @staticmethod
    def get_by_id(smartwatch_id):
        """Obtiene un smartwatch por su ID."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # Siempre pasa los parámetros como una tupla para evitar inyección SQL
                    cursor.execute(QUERY_GET_BY_ID, (smartwatch_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None

    @staticmethod
    def get_by_child_id(child_id):
        """Obtiene todos los smartwatches asociados a un niño."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(QUERY_GET_BY_CHILD_ID, (child_id,))
                    # Cambiado a fetchall() por si un niño puede tener más de un reloj
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_by_child_id: {e}")
            return []

    @staticmethod
    def create(data):
        """Crea un nuevo smartwatch."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Extrae los valores del diccionario 'data' en el orden correcto
                    values = (data['device_id'], data['model'], data.get('status', 'active'))
                    cursor.execute(QUERY_INSERT, values)
                    conn.commit()
                    return cursor.lastrowid # Devuelve el ID del nuevo registro
        except Exception as e:
            print(f"Error en create: {e}")
            return None

    @staticmethod
    def deactivate(smartwatch_id):
        """Desactiva un smartwatch cambiando su estado a 'inactive'."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(QUERY_DEACTIVATE, (smartwatch_id,))
                    conn.commit()
                    # rowcount devuelve el número de filas afectadas (debería ser 1)
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en deactivate: {e}")
            return False

    @staticmethod
    def get_details_with_child(smartwatch_id):
        """Obtiene detalles del smartwatch, el niño que lo usa y la guardería."""
        query = """
            SELECT s.id_smartwatch, s.device_id, s.model, s.status,
                   c.first_name AS child_first_name, c.last_name AS child_last_name, c.birth_date,
                   d.name AS daycare_name
            FROM smartwatches s
            JOIN children c ON s.id_smartwatch = c.id_smartwatch
            JOIN daycares d ON c.id_daycare = d.id_daycare
            WHERE s.id_smartwatch = %s;
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (smartwatch_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_details_with_child: {e}")
            return None

    @staticmethod
    def delete(smartwatch_id):
        """Elimina un smartwatch y sus detalles asociados."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(QUERY_DELETE, (smartwatch_id,))
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en delete: {e}")
            return False

    @staticmethod
    def safe_delete(smartwatch_id):
        """Desasigna el smartwatch de cualquier niño y luego elimina el registro."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Primero quitar la referencia en children
                    cursor.execute(QUERY_UNLINK_FROM_CHILDREN, (smartwatch_id,))
                    # Luego eliminar el smartwatch
                    cursor.execute(QUERY_DELETE, (smartwatch_id,))
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en safe_delete: {e}")
            return False

    @staticmethod
    def update(smartwatch_id, status=None, model=None):
        """Actualiza los campos status y model de un smartwatch."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Si no se proporcionan ambos campos, obtener los actuales para mantenerlos
                    if status is None or model is None:
                        cursor.execute(QUERY_GET_BY_ID, (smartwatch_id,))
                        current = cursor.fetchone()
                        if not current:
                            return False
                        if status is None:
                            status = current[3] if not isinstance(current, dict) else current.get('status')
                        if model is None:
                            model = current[2] if not isinstance(current, dict) else current.get('model')
                    cursor.execute(QUERY_UPDATE, (status, model, smartwatch_id))
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en update: {e}")
            return False

