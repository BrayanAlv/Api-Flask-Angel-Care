from db import get_db_connection

# --- Consultas SQL para el Modelo Child ---
GET_ALL_CHILDREN_WITH_RELATIONS = """
    SELECT
        c.id_child,
        c.first_name AS child_first_name,
        c.last_name AS child_last_name,
        c.birth_date,
        c.profile_image,  -- NUEVO CAMPO
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

GET_CHILDREN_WITH_TUTOR_CAREGIVER_DAYCARE = """
    SELECT
        c.id_child,
        c.first_name AS child_first_name,
        c.last_name AS child_last_name,
        c.birth_date,
        c.profile_image, -- NUEVO CAMPO
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
"""

GET_CHILDREN_BY_CAREGIVER = """
    SELECT c.id_child, c.first_name, c.last_name, c.birth_date, c.profile_image, c.id_smartwatch
    FROM children c
    JOIN users u ON c.id_caregiver = u.id_user
    WHERE u.id_user = %s AND u.role = 'caregiver';
"""

GET_CHILDREN_BY_TUTOR = """
    SELECT 
        c.id_child, 
        c.first_name, 
        c.last_name, 
        c.birth_date, 
        c.profile_image, -- NUEVO CAMPO
        d.name AS daycare_name,
        s.device_id
    FROM children c
    JOIN daycares d ON c.id_daycare = d.id_daycare
    LEFT JOIN smartwatches s ON c.id_smartwatch = s.id_smartwatch
    WHERE c.id_tutor = %s;
"""

GET_CHILD_DETAILS = "SELECT * FROM children WHERE id_child = %s;"

GET_TUTOR_BY_CHILD = """
    SELECT u.id_user, u.first_name, u.last_name, u.email, u.phone
    FROM users u
    JOIN children c ON u.id_user = c.id_tutor
    WHERE c.id_child = %s;
"""

GET_CAREGIVERS_BY_CHILD = """
    SELECT u.first_name, u.last_name, u.email, u.phone, d.phone AS daycare_phone
    FROM users u
    JOIN daycares d ON u.id_daycare = d.id_daycare
    WHERE u.role = 'caregiver' AND u.id_daycare = (SELECT id_daycare FROM children WHERE id_child = %s);
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

# ACTUALIZADO: Incluye profile_image
CREATE_CHILD = """
    INSERT INTO children (first_name, last_name, birth_date, id_daycare, id_tutor, id_smartwatch, id_caregiver, profile_image)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

UPDATE_CHILD_BASE = "UPDATE children SET {set_clause} WHERE id_child = %s;"

# --- Consultas SQL para Notas ---
GET_NOTES_BY_CHILD = """
    SELECT 
        n.id_note, 
        n.title, 
        n.content, 
        n.priority, 
        n.created_at,
        u.first_name AS author_first_name, 
        u.last_name AS author_last_name,
        u.role AS author_role
    FROM child_notes n
    JOIN users u ON n.id_author = u.id_user
    WHERE n.id_child = %s
    ORDER BY n.created_at DESC;
"""
GET_NOTE_BY_ID = "SELECT * FROM child_notes WHERE id_note = %s;"
CREATE_NOTE = """
    INSERT INTO child_notes (id_child, id_author, title, content, priority, created_at)
    VALUES (%s, %s, %s, %s, %s, NOW());
"""
UPDATE_NOTE_BASE = "UPDATE child_notes SET {set_clause} WHERE id_note = %s;"
DELETE_NOTE = "DELETE FROM child_notes WHERE id_note = %s;"

# --- Consultas SQL para Horarios (Schedules) ---
GET_SCHEDULES_BY_CHILD = """
    SELECT 
        id_schedule, 
        day_of_week, 
        TIME_FORMAT(start_time, '%H:%i') as start_time, 
        TIME_FORMAT(end_time, '%H:%i') as end_time, 
        activity_name, 
        description
    FROM weekly_schedules
    WHERE id_child = %s
    ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), start_time;
"""
CREATE_SCHEDULE = """
    INSERT INTO weekly_schedules (id_child, day_of_week, start_time, end_time, activity_name, description, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, NOW());
"""
DELETE_SCHEDULE = "DELETE FROM weekly_schedules WHERE id_schedule = %s;"
GET_SCHEDULE_BY_ID = "SELECT * FROM weekly_schedules WHERE id_schedule = %s;"


class ChildModel:
    @staticmethod
    def get_all_with_relations():
        """Obtiene todos los niños con información relacionada."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_ALL_CHILDREN_WITH_RELATIONS)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_all_with_relations: {e}")
            return []

    @staticmethod
    def get_children_with_tutor_caregiver_daycare():
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_CHILDREN_WITH_TUTOR_CAREGIVER_DAYCARE)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_children_with_tutor_caregiver_daycare: {e}")
            return []

    @staticmethod
    def get_by_caregiver_id(caregiver_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_CHILDREN_BY_CAREGIVER, (caregiver_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_by_caregiver_id: {e}")
            return []

    @staticmethod
    def get_by_tutor_id(tutor_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_CHILDREN_BY_TUTOR, (tutor_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_by_tutor_id: {e}")
            return []

    @staticmethod
    def get_details_by_id(child_id):
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
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_TUTOR_BY_CHILD, (child_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_tutor_by_child_id: {e}")
            return None

    @staticmethod
    def get_caregivers_by_child_id(child_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_CAREGIVERS_BY_CHILD, (child_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_caregivers_by_child_id: {e}")
            return []

    @staticmethod
    def get_sensor_averages(child_id, date_str):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_SENSOR_AVERAGES_BY_DATE, (date_str, date_str, date_str, child_id))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_sensor_averages: {e}")
            return None

    @staticmethod
    def create_child(first_name, last_name, birth_date, id_daycare, id_tutor, id_smartwatch=None, id_caregiver=None, profile_image=None):
        """Crea un nuevo niño y devuelve su registro completo."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        CREATE_CHILD,
                        (
                            first_name,
                            last_name,
                            birth_date,
                            id_daycare,
                            id_tutor,
                            id_smartwatch,
                            id_caregiver,
                            profile_image  # NUEVO CAMPO
                        ),
                    )
                    child_id = cursor.lastrowid
                conn.commit()
            return ChildModel.get_details_by_id(child_id)
        except Exception as e:
            print(f"Error en create_child: {e}")
            return None

    @staticmethod
    def update_child(child_id, fields):
        """Actualiza campos del niño indicado dinámicamente."""
        if not fields:
            return None
        # AGREGADO: profile_image
        allowed = {"first_name", "last_name", "birth_date", "id_daycare", "id_tutor", "id_smartwatch", "id_caregiver", "profile_image"}
        set_parts = []
        values = []
        for key, val in fields.items():
            if key in allowed:
                set_parts.append(f"{key} = %s")
                values.append(val)
        if not set_parts:
            return None
        query = UPDATE_CHILD_BASE.format(set_clause=", ".join(set_parts))
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (*values, child_id))
                conn.commit()
            return ChildModel.get_details_by_id(child_id)
        except Exception as e:
            print(f"Error en update_child: {e}")
            return None

    # --- MÉTODOS PARA NOTAS Y HORARIOS (Sin cambios) ---
    @staticmethod
    def get_notes(child_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_NOTES_BY_CHILD, (child_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_notes: {e}")
            return []

    @staticmethod
    def get_note_by_id(note_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_NOTE_BY_ID, (note_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_note_by_id: {e}")
            return None

    @staticmethod
    def create_note(child_id, id_author, title, content, priority):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(CREATE_NOTE, (child_id, id_author, title, content, priority))
                    note_id = cursor.lastrowid
                conn.commit()
            return note_id
        except Exception as e:
            print(f"Error en create_note: {e}")
            return None

    @staticmethod
    def update_note(note_id, fields):
        if not fields:
            return None
        allowed = {"title", "content", "priority"}
        set_parts = []
        values = []
        for key, val in fields.items():
            if key in allowed:
                set_parts.append(f"{key} = %s")
                values.append(val)
        if not set_parts:
            return None
        query = UPDATE_NOTE_BASE.format(set_clause=", ".join(set_parts))
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (*values, note_id))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error en update_note: {e}")
            return False

    @staticmethod
    def delete_note(note_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DELETE_NOTE, (note_id,))
                    if cursor.rowcount == 0:
                        return False
                conn.commit()
            return True
        except Exception as e:
            print(f"Error en delete_note: {e}")
            return False

    @staticmethod
    def get_schedules(child_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_SCHEDULES_BY_CHILD, (child_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_schedules: {e}")
            return []

    @staticmethod
    def get_schedule_by_id(schedule_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_SCHEDULE_BY_ID, (schedule_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error en get_schedule_by_id: {e}")
            return None

    @staticmethod
    def create_schedule(child_id, day_of_week, start_time, end_time, activity_name, description):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        CREATE_SCHEDULE, 
                        (child_id, day_of_week, start_time, end_time, activity_name, description)
                    )
                    schedule_id = cursor.lastrowid
                conn.commit()
            return schedule_id
        except Exception as e:
            print(f"Error en create_schedule: {e}")
            return None

    @staticmethod
    def delete_schedule(schedule_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DELETE_SCHEDULE, (schedule_id,))
                    if cursor.rowcount == 0:
                        return False
                conn.commit()
            return True
        except Exception as e:
            print(f"Error en delete_schedule: {e}")
            return False