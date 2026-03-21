# 📋 TaskMaster - Discord To-Do Bot

**TaskMaster** es un bot de Discord diseñado para la gestión de tareas grupales de manera organizada y eficiente. A diferencia de otros bots de listas, TaskMaster permite que cada canal de un servidor tenga su propia lista de tareas independiente, lo que lo hace ideal para servidores con múltiples grupos de estudio o proyectos (como los de la **UNLP**).

## 🚀 Características Principales

* **Segmentación por Canal**: Las tareas creadas en un canal son invisibles para otros canales, manteniendo la privacidad y el orden.
* **Comandos de Barra (Slash Commands)**: Interacción moderna y fluida integrada directamente en la interfaz de Discord.
* **Autocompletado Inteligente**: Al intentar borrar o editar una tarea, el bot sugiere opciones en tiempo real basadas en los nombres guardados.
* **Gestión de Estados**: Clasificación visual de tareas mediante estados fijos:
    * 🔴 **SIN EMPEZAR**
    * 🟡 **EN PROCESO**
    * 🟢 **TERMINADO**
* **Persistencia de Datos**: Utiliza una base de datos relacional para asegurar que la información no se pierda al reiniciar el bot.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje**: [Python 3.11+](https://www.python.org/)
* **Librería Principal**: [discord.py](https://discordpy.readthedocs.io/)
* **Base de Datos**: [SQLite3](https://www.sqlite.org/) (Motor relacional ligero)
* **Gestión de Entorno**: `python-dotenv` para la seguridad de credenciales.

## 📂 Arquitectura del Proyecto

El proyecto sigue una estructura modular para facilitar el mantenimiento y escalado:

* `main.py`: Punto de entrada, configuración de intents y carga de extensiones.
* `cogs/todo.py`: Definición de comandos y lógica de interacción con el usuario (Capa de Presentación).
* `database/manager.py`: Gestión de consultas SQL, creación de tablas y lógica de datos (Capa de Datos).

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/alandprieto/bottask-dircord.git](https://github.com/alandprieto/bottask-dircord.git)
   cd bottask-dircord
