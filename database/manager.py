import logging
import os
import sqlite3 as sql
from contextlib import contextmanager
from enum import IntEnum

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

logger = logging.getLogger(__name__)


class EstadoTarea(IntEnum):
    SIN_EMPEZAR = 1
    EN_PROCESO = 2
    TERMINADO = 3

    @property
    def etiqueta(self) -> str:
        etiquetas = {
            EstadoTarea.SIN_EMPEZAR: "🔴 SIN EMPEZAR",
            EstadoTarea.EN_PROCESO: "🟡 EN PROCESO",
            EstadoTarea.TERMINADO: "🟢 TERMINADO",
        }
        return etiquetas[self]


@contextmanager
def _conexion():
    conn = sql.connect(DB_PATH)
    conn.row_factory = sql.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        logger.exception("Error en operación de base de datos")
        raise
    finally:
        conn.close()


def crear_tabla():
    with _conexion() as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        conn.executemany(
            "INSERT OR IGNORE INTO states (id, name) VALUES (?, ?)",
            [(estado.value, estado.etiqueta) for estado in EstadoTarea],
        )
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                state INTEGER NOT NULL DEFAULT {EstadoTarea.SIN_EMPEZAR.value},
                channel_id INTEGER NOT NULL,
                FOREIGN KEY (state) REFERENCES states (id)
            )
            """)


def add_task(name, description, state, channel_id):
    with _conexion() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (name, description, state, channel_id) "
            "VALUES (?, ?, ?, ?)",
            (name, description, state, channel_id),
        )
        return cursor.lastrowid


def list_task(channel_id):
    with _conexion() as conn:
        cursor = conn.execute(
            """
            SELECT tasks.id, tasks.name, tasks.description, states.name AS state_name
            FROM tasks
            INNER JOIN states ON tasks.state = states.id
            WHERE tasks.channel_id = ?
            ORDER BY tasks.id ASC
            """,
            (channel_id,),
        )
        return cursor.fetchall()


def search_tasks_name(nombre, channel_id):
    with _conexion() as conn:
        cursor = conn.execute(
            "SELECT id, name FROM tasks WHERE name LIKE ? AND channel_id = ?",
            (f"%{nombre}%", channel_id),
        )
        return cursor.fetchall()


def delete_task(tarea_id, channel_id):
    with _conexion() as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id=? AND channel_id = ?", (tarea_id, channel_id)
        )
        return cursor.rowcount


def change_state(new_state_id, task_id, channel_id):
    with _conexion() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET state = ? WHERE id = ? AND channel_id = ?",
            (new_state_id, task_id, channel_id),
        )
        return cursor.rowcount
