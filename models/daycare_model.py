from db import get_db_connection

class DaycareModel:

    @staticmethod
    def get_all():
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM daycares ORDER BY name")
            return cursor.fetchall()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_id(id_daycare):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM daycares WHERE id_daycare = %s", (id_daycare,))
            return cursor.fetchone()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def create(data):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO daycares (name, address, phone) VALUES (%s, %s, %s)"
            cursor.execute(query, (data['name'], data.get('address'), data.get('phone')))
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
    def update(id_daycare, data):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "UPDATE daycares SET name = %s, address = %s, phone = %s WHERE id_daycare = %s"
            cursor.execute(query, (data['name'], data.get('address'), data.get('phone'), id_daycare))
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
    def delete(id_daycare):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM daycares WHERE id_daycare = %s", (id_daycare,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()