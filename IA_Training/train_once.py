import mysql.connector
import pandas as pd
import joblib
import os
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

load_dotenv()

def train_and_save():
    print("🔌 Conectando a BD...")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "guardianAngel")
        )
    except Exception as e:
        print(f" Error conexión: {e}")
        return
    
    query = "SELECT bpm, temperature, oxygen_level, risk_label FROM readings"
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    
    print(f" Datos cargados: {len(df)}")
    
    if len(df) < 100:
        print(" Error: Pocos datos. Importa el SQL generado primero.")
        return

    X = df[['bpm', 'temperature', 'oxygen_level']]
    y = df['risk_label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(" Entrenando...")
    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)
    
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f" Precisión: {accuracy * 100:.2f}%")
    
    joblib.dump(model, 'health_classifier.pkl')
    print(" Modelo guardado: health_classifier.pkl")

if __name__ == "__main__":
    train_and_save()
