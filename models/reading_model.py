from db import get_db_connection

# --- Consultas SQL para Lecturas ---
INSERT_TEMPERATURE = "INSERT INTO temperature_readings (id_smartwatch, temperature) VALUES (%s, %s);"
INSERT_HEART_RATE = "INSERT INTO heart_rate_readings (id_smartwatch, beats_per_minute) VALUES (%s, %s);"
INSERT_OXYGENATION = "INSERT INTO oxygenation_readings (id_smartwatch, spo2_level) VALUES (%s, %s);"
INSERT_ACCELEROMETER = "INSERT INTO accelerometer_readings (id_smartwatch, axis_x, axis_y, axis_z, is_fall) VALUES (%s, %s, %s, %s, %s);"

GET_LAST_TEMPERATURE = "SELECT temperature, timestamp FROM temperature_readings WHERE id_smartwatch = %s ORDER BY timestamp DESC LIMIT 1;"
GET_LAST_HEART_RATE = "SELECT beats_per_minute, timestamp FROM heart_rate_readings WHERE id_smartwatch = %s ORDER BY timestamp DESC LIMIT 1;"
GET_LAST_OXYGENATION = "SELECT spo2_level, timestamp FROM oxygenation_readings WHERE id_smartwatch = %s ORDER BY timestamp DESC LIMIT 1;"

GET_LAST_10_HEART_RATE = "SELECT beats_per_minute, timestamp FROM heart_rate_readings WHERE id_smartwatch = %s ORDER BY timestamp DESC LIMIT 10;"
GET_LAST_10_OXYGENATION = "SELECT spo2_level, timestamp FROM oxygenation_readings WHERE id_smartwatch = %s ORDER BY timestamp DESC LIMIT 10;"


class ReadingModel:
    @staticmethod
    def save_readings(data):
        """
        Guarda un conjunto de lecturas de sensores para un smartwatch.
        'data' es un diccionario que puede contener:
        {
            "id_smartwatch": 1,
            "temperature": 36.9,
            "heart_rate": 112,
            "spo2": 98.7,
            "accelerometer": {"x": 0.05, "y": -0.96, "z": 0.03, "is_fall": False}
        }
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    smartwatch_id = data['id_smartwatch']

                    if 'temperature' in data:
                        cursor.execute(INSERT_TEMPERATURE, (smartwatch_id, data['temperature']))

                    if 'heart_rate' in data:
                        cursor.execute(INSERT_HEART_RATE, (smartwatch_id, data['heart_rate']))

                    if 'spo2' in data:
                        cursor.execute(INSERT_OXYGENATION, (smartwatch_id, data['spo2']))

                    if 'accelerometer' in data:
                        accel = data['accelerometer']
                        cursor.execute(INSERT_ACCELEROMETER,
                                       (smartwatch_id, accel['x'], accel['y'], accel['z'], accel.get('is_fall', False)))

                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error al guardar lecturas: {e}")
            return False

    @staticmethod
    def get_all_last_readings(smartwatch_id):
        """
        Obtiene la última lectura de cada sensor para un smartwatch.
        """
        last_readings = {}
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_LAST_TEMPERATURE, (smartwatch_id,))
                    last_readings['temperature'] = cursor.fetchone()

                    cursor.execute(GET_LAST_HEART_RATE, (smartwatch_id,))
                    last_readings['heart_rate'] = cursor.fetchone()

                    cursor.execute(GET_LAST_OXYGENATION, (smartwatch_id,))
                    last_readings['oxygenation'] = cursor.fetchone()
            return last_readings
        except Exception as e:
            print(f"Error al obtener últimas lecturas: {e}")
            return None

    @staticmethod
    def get_last_10_heart_rate(smartwatch_id):
        """Obtiene las últimas 10 lecturas de ritmo cardíaco."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_LAST_10_HEART_RATE, (smartwatch_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener historial de ritmo cardíaco: {e}")
            return []

    @staticmethod
    def get_last_10_oxygenation(smartwatch_id):
        """Obtiene las últimas 10 lecturas de oxigenación."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(GET_LAST_10_OXYGENATION, (smartwatch_id,))
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener historial de oxigenación: {e}")
            return []