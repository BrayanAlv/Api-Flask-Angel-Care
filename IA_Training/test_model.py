import joblib
import numpy as np
import os
import mysql.connector
from dotenv import load_dotenv

# Cargar variables de entorno para la conexión
load_dotenv()

MODEL_FILE = 'health_classifier.pkl'

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "240525"),
            database=os.getenv("DB_NAME", "guardianAngel")
        )
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return None

def test_ia_with_db():
    # 1. Verificar modelo
    if not os.path.exists(MODEL_FILE):
        print(f"❌ ERROR: No encuentro '{MODEL_FILE}'.")
        return

    # 2. Cargar modelo
    print(f"🧠 Cargando cerebro: {MODEL_FILE}...")
    try:
        model = joblib.load(MODEL_FILE)
        print("✅ Modelo cargado.\n")
    except Exception as e:
        print(f"❌ Error modelo: {e}")
        return

    # 3. Conectar y extraer 10 datos al azar
    conn = get_db_connection()
    if not conn: return

    cursor = conn.cursor(dictionary=True)
    
    # Traemos datos variados para probar
    print("🔌 Consultando 10 registros aleatorios de la BD...")
    query = """
        SELECT bpm, temperature, oxygen_level, risk_label 
        FROM readings 
        ORDER BY RAND() 
        LIMIT 10
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("⚠️ La tabla 'readings' está vacía.")
        return

    # 4. Encabezados de la tabla
    print(f"{'BPM':<5} | {'TEMP':<6} | {'O2':<5} | {'REAL (BD)':<12} | {'PREDICCIÓN IA':<15} | {'CONFIANZA'}")
    print("-" * 80)

    correctos = 0

    # 5. Evaluar cada fila
    for row in rows:
        bpm = row['bpm']
        temp = row['temperature']
        oxy = row['oxygen_level']
        real_label = row['risk_label'] # 0 o 1

        # Preparar datos para IA
        features = np.array([[bpm, temp, oxy]])
        
        # Predicción
        pred_label = model.predict(features)[0]
        prob = model.predict_proba(features)[0]
        certainty = prob[pred_label] * 100

        # Textos para mostrar
        txt_real = "🔴 RIESGO" if real_label == 1 else "🟢 NORMAL"
        txt_pred = "🔴 RIESGO" if pred_label == 1 else "🟢 NORMAL"
        
        # Verificar acierto
        match = "✅" if real_label == pred_label else "❌"
        if real_label == pred_label: correctos += 1

        print(f"{bpm:<5} | {temp:<6} | {oxy:<5} | {txt_real:<12} | {txt_pred:<15} | {certainty:.1f}% {match}")

    print("-" * 80)
    print(f"🎯 Precisión en esta muestra: {correctos}/10")

if __name__ == "__main__":
    test_ia_with_db()