import random
import os
import re
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
INPUT_SQL_FILE = "_localhost-2025_11_26_23_21_06-dump.sql" 
OUTPUT_SQL_FILE = "smartwatch_db_entrenamiento_completo.sql"
NUM_RECORDS = 10000 
NUM_CHILDREN = 50

# Tablas a EXCLUIR
TABLAS_IGNORADAS = ["accelerometer_readings", "audio_recordings"]

# --- ESTRUCTURA FORZADA DE LA TABLA READINGS ---
# Esto garantiza que la tabla exista aunque el dump original falle
ESTRUCTURA_READINGS = """
-- ESTRUCTURA BLINDADA PARA READINGS
DROP TABLE IF EXISTS `readings`;
CREATE TABLE `readings` (
  `id_reading` int(11) NOT NULL AUTO_INCREMENT,
  `bpm` int(11) DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `oxygen_level` int(11) DEFAULT NULL,
  `risk_label` int(11) DEFAULT 0,
  `id_child` int(11) DEFAULT NULL,
  `id_device` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_reading`),
  KEY `idx_child` (`id_child`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

print(f"🚀 Iniciando generador blindado...")

# --- 1. LÓGICA MÉDICA ---
def get_age_profile(child_id):
    if child_id <= 15: return "baby"
    if child_id <= 35: return "toddler"
    return "preschool"

def generate_vitals(age_group, scenario):
    base_bpm = {"baby": (110, 150), "toddler": (95, 140), "preschool": (85, 130)}
    if scenario == "healthy":
        low, high = base_bpm[age_group]
        bpm = random.randint(low, high)
        temp = round(random.uniform(36.5, 37.3), 1)
        oxy = random.randint(96, 100)
    elif scenario == "fever":
        temp = round(random.uniform(37.8, 40.2), 1)
        extra_bpm = int((temp - 37.0) * 10)
        low, high = base_bpm[age_group]
        bpm = random.randint(low + extra_bpm, high + extra_bpm + 20)
        oxy = random.randint(94, 98)
    elif scenario == "respiratory_distress":
        oxy = random.randint(82, 92)
        low, high = base_bpm[age_group]
        bpm = random.randint(high, high + 40)
        temp = round(random.uniform(36.5, 37.6), 1)
    elif scenario == "sleeping":
        low, high = base_bpm[age_group]
        bpm = random.randint(low - 20, low)
        temp = round(random.uniform(36.3, 36.8), 1)
        oxy = random.randint(95, 99)
    else:
        bpm, temp, oxy = 100, 36.7, 98
    return bpm, temp, oxy

def calculate_risk_label(bpm, temp, oxy, age_group):
    risk_score = 0
    if oxy < 90: risk_score += 5
    elif oxy < 94: risk_score += 2
    if temp >= 38.0: risk_score += 3
    elif temp >= 37.6: risk_score += 1
    elif temp < 35.8: risk_score += 3
    if age_group == "baby" and (bpm > 180 or bpm < 80): risk_score += 3
    elif age_group == "toddler" and (bpm > 160 or bpm < 70): risk_score += 3
    elif age_group == "preschool" and (bpm > 150 or bpm < 60): risk_score += 3
    return 1 if risk_score >= 2 else 0

# --- 2. GENERAR NUEVOS DATOS ---
new_inserts = []
header = "INSERT INTO readings (bpm, temperature, oxygen_level, risk_label, id_child, id_device, timestamp) VALUES"
current_date = datetime.now() - timedelta(days=60)
batch_values = []

for i in range(NUM_RECORDS):
    current_date += timedelta(minutes=random.randint(10, 40))
    ts = current_date.strftime('%Y-%m-%d %H:%M:%S')
    child_id = random.randint(1, NUM_CHILDREN)
    age = get_age_profile(child_id)
    scenario = random.choices(['healthy', 'sleeping', 'fever', 'respiratory_distress'], weights=[70, 10, 15, 5])[0]
    bpm, temp, oxy = generate_vitals(age, scenario)
    label = calculate_risk_label(bpm, temp, oxy, age)
    val = f"({bpm}, {temp}, {oxy}, {label}, {child_id}, 1, '{ts}')"
    batch_values.append(val)
    if len(batch_values) >= 1000:
        new_inserts.append(header + "\n" + ",\n".join(batch_values) + ";")
        batch_values = []
if batch_values:
    new_inserts.append(header + "\n" + ",\n".join(batch_values) + ";")

# --- 3. FILTRAR SQL ORIGINAL ---
def filtrar_sql(contenido_original):
    lineas = contenido_original.split('\n')
    sql_limpio = []
    bloque_a_ignorar = False
    
    for linea in lineas:
        # Detectar tablas prohibidas
        for tabla in TABLAS_IGNORADAS:
            if f"`{tabla}`" in linea:
                 if any(cmd in linea for cmd in ["CREATE TABLE", "INSERT INTO", "LOCK TABLES", "ALTER TABLE", "DROP TABLE"]):
                    bloque_a_ignorar = True
                    break
        
        # Detectar la tabla readings ORIGINAL (La vamos a borrar para usar nuestra estructura forzada)
        if "`readings`" in linea and "CREATE TABLE" in linea:
            bloque_a_ignorar = True

        if bloque_a_ignorar:
            if ";" in linea or "UNLOCK TABLES" in linea:
                bloque_a_ignorar = False
            continue
        sql_limpio.append(linea)
    return "\n".join(sql_limpio)

# --- 4. FUSIÓN FINAL ---
try:
    print(f"📂 Leyendo archivo original...")
    with open(INPUT_SQL_FILE, 'r', encoding='utf-8') as f_orig:
        original_content = f_orig.read()
    
    contenido_limpio = filtrar_sql(original_content)
    
    print("🔄 Creando archivo final...")
    with open(OUTPUT_SQL_FILE, 'w', encoding='utf-8') as f_out:
        f_out.write("-- 1. RESPALDO LIMPIO --\n")
        f_out.write(contenido_limpio)
        f_out.write("\n\n-- 2. ESTRUCTURA FORZADA DE READINGS --\n")
        f_out.write(ESTRUCTURA_READINGS) # <--- AQUÍ ESTÁ LA MAGIA
        f_out.write("\n\n-- 3. DATOS IA (TEMPERATURAS CORREGIDAS) --\n")
        for block in new_inserts:
             f_out.write(block + "\n")
            
    print(f"✅ ¡ÉXITO! Archivo blindado creado: {OUTPUT_SQL_FILE}")

except FileNotFoundError:
    print(f"❌ ERROR: No encuentro '{INPUT_SQL_FILE}'.")
except Exception as e:
    print(f"❌ Error: {e}")
