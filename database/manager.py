import os
import sqlite3 as sql

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def crear_tabla():
    # 1. Conectar a database/database.db
    conn = sql.connect(DB_PATH)
    # 2. Crear un cursor
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")
    # 3. Ejecutar un CREATE TABLE IF NOT EXISTS...
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute(
        "INSERT OR IGNORE INTO states (id, name) VALUES (1, '🔴 SIN EMPEZAR')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO states (id, name) VALUES (2, '🟡 EN PROCESO')"
    )
    cursor.execute("INSERT OR IGNORE INTO states (id, name) VALUES (3, '🟢 TERMINADO')")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            state INTEGER NOT NULL DEFAULT 1,
            channel_id INTEGER NOT NULL,
            FOREIGN KEY (state) REFERENCES states (id)
        )
        """)
    cursor.execute("INSERT OR IGNORE INTO states (id, name) VALUES (1, 'SIN COMENZAR')")
    # 4. Hacer commit y cerrar conexión
    conn.commit()
    conn.close()
    pass


def add_task(name, description, state, channel_id):
    # Lógica de INSERT INTO...
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tasks (name, description, state, channel_id) VALUES (?, ?, ?, ?)",
            (name, description, state, channel_id),
        )
        conn.commit()
        return cursor.lastrowid
    except Exception:
        # Manejar/loggear el error según prefieras; aquí lo re-lanzamos
        raise
    finally:
        conn.close()


def list_task(channel_id):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT tasks.id, tasks.name, tasks.description, states.name
            FROM tasks
            INNER JOIN states ON tasks.state = states.id
            WHERE tasks.channel_id = ?
            """,
            (channel_id,),
        )
        tareas = cursor.fetchall()
        return tareas
    except Exception:
        raise
    finally:
        conn.close()


def search_tasks_name(nombre, channel_id):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Buscamos tareas que contengan el texto ingresado
        query = "SELECT id, name FROM tasks WHERE name LIKE ? AND channel_id = ?"
        cursor.execute(query, (f"%{nombre}%", channel_id))
        return cursor.fetchall()  # Devuelve una lista de tuplas [(id, nombre), ...]
    finally:
        conn.close()


def delete_task(tarea_id, channel_id):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM tasks WHERE id=? AND channel_id = ?", (tarea_id, channel_id)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def change_state(new_state_id, task_id, channel_id):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE tasks SET state = ? WHERE id = ? AND channel_id = ?",
            (new_state_id, task_id, channel_id),
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
