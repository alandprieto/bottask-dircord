import os
import sqlite3
import tempfile
import unittest

from database import manager


class TestManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        manager.DB_PATH = os.path.join(self.tmp_dir.name, "test.db")
        manager.crear_tabla()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_estados_sembrados(self):
        conn = sqlite3.connect(manager.DB_PATH)
        conn.row_factory = sqlite3.Row
        estados = {
            fila["id"]: fila["name"]
            for fila in conn.execute("SELECT id, name FROM states")
        }
        conn.close()
        self.assertEqual(len(estados), 3)
        self.assertEqual(estados[1], "🔴 SIN EMPEZAR")
        self.assertEqual(estados[2], "🟡 EN PROCESO")
        self.assertEqual(estados[3], "🟢 TERMINADO")

    def test_agregar_y_listar(self):
        tarea_id = manager.add_task(
            "Comprar leche", "En el supermercado", manager.EstadoTarea.SIN_EMPEZAR.value, 1
        )
        tareas = manager.list_task(1)
        self.assertEqual(len(tareas), 1)
        tarea = tareas[0]
        self.assertEqual(tarea["id"], tarea_id)
        self.assertEqual(tarea["name"], "Comprar leche")
        self.assertEqual(tarea["description"], "En el supermercado")
        self.assertEqual(tarea["state_name"], "🔴 SIN EMPEZAR")

    def test_aislamiento_por_canal(self):
        manager.add_task("A", "d", 1, 1)
        manager.add_task("B", "d", 1, 2)
        self.assertEqual(len(manager.list_task(1)), 1)
        self.assertEqual(len(manager.list_task(2)), 1)
        self.assertEqual(len(manager.list_task(3)), 0)

    def test_orden_estable(self):
        manager.add_task("Primera", "d", 1, 1)
        manager.add_task("Segunda", "d", 2, 1)
        manager.add_task("Tercera", "d", 3, 1)
        nombres = [t["name"] for t in manager.list_task(1)]
        self.assertEqual(nombres, ["Primera", "Segunda", "Tercera"])

    def test_buscar_por_nombre(self):
        manager.add_task("Programar", "d", 1, 1)
        manager.add_task("Programar más", "d", 1, 1)
        manager.add_task("Otra tarea", "d", 1, 1)
        resultados = manager.search_tasks_name("gram", 1)
        self.assertEqual(len(resultados), 2)
        self.assertEqual(len(manager.search_tasks_name("gram", 2)), 0)

    def test_borrar(self):
        tarea_id = manager.add_task("X", "d", 1, 1)
        self.assertEqual(manager.delete_task(tarea_id, 1), 1)
        self.assertEqual(manager.delete_task(tarea_id, 1), 0)

    def test_borrar_no_afecta_otro_canal(self):
        tarea_id = manager.add_task("Y", "d", 1, 1)
        self.assertEqual(manager.delete_task(tarea_id, 99), 0)
        self.assertEqual(len(manager.list_task(1)), 1)

    def test_cambiar_estado(self):
        tarea_id = manager.add_task("Z", "d", 1, 1)
        filas = manager.change_state(manager.EstadoTarea.TERMINADO.value, tarea_id, 1)
        self.assertEqual(filas, 1)
        self.assertEqual(manager.list_task(1)[0]["state_name"], "🟢 TERMINADO")

    def test_cambiar_estado_no_afecta_otro_canal(self):
        tarea_id = manager.add_task("W", "d", 1, 1)
        filas = manager.change_state(manager.EstadoTarea.TERMINADO.value, tarea_id, 99)
        self.assertEqual(filas, 0)
        self.assertEqual(manager.list_task(1)[0]["state_name"], "🔴 SIN EMPEZAR")

    def test_enum_define_eligibles_para_discord(self):
        choices = [
            (estado.value, estado.etiqueta) for estado in manager.EstadoTarea
        ]
        self.assertEqual(
            choices,
            [(1, "🔴 SIN EMPEZAR"), (2, "🟡 EN PROCESO"), (3, "🟢 TERMINADO")],
        )


if __name__ == "__main__":
    unittest.main()
