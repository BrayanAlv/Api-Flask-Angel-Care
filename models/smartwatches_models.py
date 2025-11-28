from db import get_db_connection

        ### ----- ###     QUERYS     ### ----- ###
QUERY_GET_ALL = "SELECT * FROM smartwatches ORDER BY id_smartwatch"
QUERY_GET_BY_ID = "SELECT * FROM smartwatches WHERE id_smartwatch = %s"
# Corrección: Buscar el smartwatch a través de la tabla children
QUERY_GET_BY_CHILD_ID = """
    SELECT s.* FROM smartwatches s
    JOIN children c ON s.id_smartwatch = c.id_smartwatch
    WHERE c.id_child = %s
"""
QUERY_INSERT = "INSERT INTO smartwatches (device_id, model, status) VALUES (%s, %s, %s)"
QUERY_DEACTIVATE = "UPDATE smartwatches SET status = 'inactive' WHERE id_smartwatch = %s"
QUERY_DELETE = "DELETE FROM smartwatches WHERE id_smartwatch = %s"
QUERY_UPDATE = "UPDATE smartwatches SET status = %s, model = %s WHERE id_smartwatch = %s"

# --- CONSULTAS PARA ASIGNACIÓN ---
QUERY_UNLINK_FROM_CHILDREN = "UPDATE children SET id_smartwatch = NULL WHERE id_smartwatch = %s"
QUERY_LINK_TO_CHILD = "UPDATE children SET id_smartwatch = %s WHERE id_child = %s"
QUERY_UPDATE_STATUS_ONLY = "UPDATE smartwatches SET status = %s WHERE id_smartwatch = %s"


class SmartwatchModel:
    @staticmethod
    def get_all():
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(QUERY_GET_ALL)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_all: {e}")
            return []

    @staticmethod
    def get_by_id(smartwatch_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(QUERY_GET_BY_ID, (smartwatch_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None

    @staticmethod
    def get_by_child_id(child_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(QUERY_GET_BY_CHILD_ID, (child_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_by_child_id: {e}")
            return []

    @staticmethod
    def create(data):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    values = (data['device_id'], data['model'], data.get('status', 'active'))
                    cursor.execute(QUERY_INSERT, values)
                    conn.commit()
                    return cursor.lastrowid
        except Exception as e:
            print(f"Error en create: {e}")
            return None

    @staticmethod
    def deactivate(smartwatch_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(QUERY_DEACTIVATE, (smartwatch_id,))
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en deactivate: {e}")
            return False

    @staticmethod
    def get_details_with_child(smartwatch_id):
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
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(QUERY_UNLINK_FROM_CHILDREN, (smartwatch_id,))
                    cursor.execute(QUERY_DELETE, (smartwatch_id,))
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en safe_delete: {e}")
            return False

    @staticmethod
    def update(smartwatch_id, status=None, model=None):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    if status is None or model is None:
                        cursor.execute(QUERY_GET_BY_ID, (smartwatch_id,))
                        current = cursor.fetchone()
                        if not current: return False
                        if status is None: status = current.get('status')
                        if model is None: model = current.get('model')
                    cursor.execute(QUERY_UPDATE, (status, model, smartwatch_id))
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en update: {e}")
            return False

    # --- AGREGADO: MÉTODOS FALTANTES PARA QUE FUNCIONE READING.PY ---

    @staticmethod
    def activate_and_assign(smartwatch_id, child_id):
        """Activa el reloj y lo asigna al niño (usado en reading.py)."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # 1. Quitar el reloj de cualquier otro niño (limpieza)
                    cursor.execute(QUERY_UNLINK_FROM_CHILDREN, (smartwatch_id,))
                    
                    # 2. Poner estado en 'active'
                    cursor.execute(QUERY_UPDATE_STATUS_ONLY, ('active', smartwatch_id))
                    
                    # 3. Asignar al nuevo niño
                    cursor.execute(QUERY_LINK_TO_CHILD, (smartwatch_id, child_id))
                    
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error en activate_and_assign: {e}")
            return False

    @staticmethod
    def deactivate_and_unassign(smartwatch_id):
        """Desactiva el reloj y lo desvincula (usado en reading.py)."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # 1. Quitar el reloj de cualquier niño
                    cursor.execute(QUERY_UNLINK_FROM_CHILDREN, (smartwatch_id,))
                    
                    # 2. Poner estado en 'inactive'
                    cursor.execute(QUERY_UPDATE_STATUS_ONLY, ('inactive', smartwatch_id))
                    
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error en deactivate_and_unassign: {e}")
            return False