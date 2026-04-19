"""
GestiCat/crear_bd: Script para crear la base de datos SQLite de GestiCat.

Crea las tres tablas del esquema (responsables, colonias, gatos) en el orden
correcto respetando las claves foráneas, e inserta los datos iniciales de ejemplo.

Si la base de datos ya existe, la elimina y la recrea desde cero. Útil durante
el desarrollo para resetear el estado de la aplicación a un punto de partida limpio.

Se ejecuta desde la carpeta que contiene el paquete gesticat/, antes de arrancar
la aplicación:

    python3 -m gesticat.crear_bd
"""

import sqlite3
from pathlib import Path

# Eliminar la base de datos si ya existe (para recrearla limpia)
ruta_bd = Path("gesticat.db")
if ruta_bd.exists():
    ruta_bd.unlink()

conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Crear tablas (en el orden correcto)
cursor.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS responsables (
    identificacion TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL,
    tipo TEXT NOT NULL,
    fecha_nacimiento TEXT,
    numero_registro TEXT
);

CREATE TABLE IF NOT EXISTS colonias (
    nombre TEXT PRIMARY KEY,
    responsable_identificacion TEXT NOT NULL,
    estado TEXT NOT NULL,
    ultima_actualizacion TEXT NOT NULL,
    FOREIGN KEY (responsable_identificacion) REFERENCES responsables(identificacion)
);

CREATE TABLE IF NOT EXISTS gatos (
    id_gato TEXT PRIMARY KEY,
    colonia_nombre TEXT NOT NULL,
    nombre TEXT NOT NULL,
    color TEXT NOT NULL,
    sexo TEXT NOT NULL,
    estado TEXT NOT NULL,
    clinica_veterinaria TEXT,
    esterilizado INTEGER NOT NULL,
    fecha_registro TEXT NOT NULL,
    FOREIGN KEY (colonia_nombre) REFERENCES colonias(nombre)
);
""")

# Datos iniciales (coinciden con datos_iniciales.py)

# 1. Responsable
cursor.execute("""
    INSERT INTO responsables
    (identificacion, nombre, telefono, email, tipo, fecha_nacimiento, numero_registro)
    VALUES ('12345678A', 'Siboney Apellido', '612345678',
            'siboney_apellido@email.com', 'PERSONA_FISICA', '1986-10-10', NULL)
""")

# 2. Colonia
cursor.execute("""
    INSERT INTO colonias
    (nombre, responsable_identificacion, estado, ultima_actualizacion)
    VALUES ('Colonia Sur', '12345678A', 'SOLICITADA', date('now'))
""")

# 3. Gatos
gatos_iniciales = [
    ("001", "Miguelito",  "Gris",   "M", "COL",  "Clínica Sur",   1, "2024-01-10"),
    ("002", "Kiwi",       "Blanca", "H", "ACOG", "Clínica Sur",   1, "2024-02-15"),
    ("003", "GordiLuis",  "Pardo",  "M", "FALL", "Clínica Norte", 1, "2024-03-20"),
    ("004", "Sombra",     "Negro",  "H", "COL",  None,            0, "2024-04-05"),
    ("005", "Nieve",      "Blanco", "?", "COL",  None,            0, "2024-06-01"),
]

cursor.executemany(
    """INSERT INTO gatos
       (id_gato, colonia_nombre, nombre, color, sexo, estado,
        clinica_veterinaria, esterilizado, fecha_registro)
       VALUES (?, 'Colonia Sur', ?, ?, ?, ?, ?, ?, ?)""",
    gatos_iniciales,
)

conn.commit()
conn.close()

print("Base de datos creada en: gesticat.db")