from db import get_db_connection

# --- Consultas SQL para el Modelo Child ---
GET_ALL_CHILDREN_WITH_RELATIONS = """
    SELECT
        c.id_child,
        c.first_name AS child_first_name,
        c.last_name AS child_last_name,
        c.birth_date,
        d.name AS daycare_name,
        t.first_name AS tutor_first_name,
        t.last_name AS tutor_last_name,
        ca.first_name AS caregiver_first_name,
        ca.last_name AS caregiver_last_name,
        s.device_id,
        s.model AS smartwatch_model
    FROM
        children c
    JOIN
        daycares d ON c.id_daycare = d.id_daycare
    JOIN
        users t ON c.id_tutor = t.id_user
    JOIN
        smartwatches s ON c.id_smartwatch = s.id_smartwatch
    LEFT JOIN
        users ca ON c.id_caregiver = ca.id_user;
"""
GET_CHILDREN_BY_TEACHER = """
    SELECT c.id_child, c.first_name, c.last_name, c.birth_date
    FROM children c
    JOIN users u ON c.id_daycare = u.id_daycare
    WHERE u.id_user = %s AND u.role = 'teacher';
"""
GET_CHILD_DETAILS = "SELECT * FROM children WHERE id_child = %s;"

GET_TUTOR_BY_CHILD = """
    SELECT u.id_user, u.first_name, u.last_name, u.email
    FROM users u
    JOIN children c ON u.id_user = c.id_tutor
    WHERE c.id_child = %s;
"""

GET_TEACHERS_BY_CHILD = """
    SELECT u.first_name, u.last_name, u.email, d.phone AS daycare_phone
    FROM users u
    JOIN daycares d ON u.id_daycare = d.id_daycare
    WHERE u.role = 'teacher' AND u.id_daycare = (SELECT id_daycare FROM children WHERE id_child = %s);
"""

GET_SENSOR_AVERAGES_BY_DATE = """
    SELECT
        c.first_name, c.last_name,
        (SELECT AVG(temperature) FROM temperature_readings WHERE id_smartwatch = c.id_smartwatch AND DATE(timestamp) = %s) AS avg_temperature,
        (SELECT AVG(beats_per_minute) FROM heart_rate_readings WHERE id_smartwatch = c.id_smartwatch AND DATE(timestamp) = %s) AS avg_heart_rate,
        (SELECT AVG(spo2_level) FROM oxygenation_readings WHERE id_smartwatch = c.id_smartwatch AND DATE(timestamp) = %s) AS avg_spo2_level
    FROM children c
    WHERE c.id_child = %s;
"""


class ChildModel:
    @staticmethod
    def get_all_with_relations():
        """Obtiene todos los niños con información relacionada (guardería, tutor, cuidador y smartwatch)."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_ALL_CHILDREN_WITH_RELATIONS)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_all_with_relations: {e}")
            return []
    @staticmethod
    def get_by_teacher_id(teacher_id):
        """Obtiene la lista de niños supervisados por un profesor."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_CHILDREN_BY_TEACHER, (teacher_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_by_teacher_id: {e}")
            return []

    @staticmethod
    def get_details_by_id(child_id):
        """Obtiene los datos personales de un niño."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_CHILD_DETAILS, (child_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_details_by_id: {e}")
            return None

    @staticmethod
    def get_tutor_by_child_id(child_id):
        """Obtiene los datos del tutor de un niño."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_TUTOR_BY_CHILD, (child_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_tutor_by_child_id: {e}")
            return None

    @staticmethod
    def get_teachers_by_child_id(child_id):
        """Obtiene la lista de profesores de la guardería de un niño."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_TEACHERS_BY_CHILD, (child_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_teachers_by_child_id: {e}")
            return []

    @staticmethod
    def get_sensor_averages(child_id, date_str):
        """Calcula el promedio de sensores para un niño en una fecha específica."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # La fecha se pasa 3 veces para los 3 sub-selects, y el id al final
                    cursor.execute(GET_SENSOR_AVERAGES_BY_DATE, (date_str, date_str, date_str, child_id))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_sensor_averages: {e}")
            return None