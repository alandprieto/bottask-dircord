# 📋 TaskMaster - Discord To-Do Bot

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.7.1-5865F2?logo=discord&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

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
* **Librería Principal**: [discord.py 2.7](https://discordpy.readthedocs.io/)
* **Base de Datos**: [SQLite3](https://www.sqlite.org/) (Motor relacional ligero)
* **Gestión de Entorno**: [python-dotenv](https://pypi.org/project/python-dotenv/) para la seguridad de credenciales.

## 📖 Comandos

| Comando | Descripción |
|---------|-------------|
| `/añadir` | Añade una tarea con nombre, descripción y estado inicial. |
| `/listar` | Lista todas las tareas del canal actual. |
| `/editar` | Cambia el estado de una tarea existente. |
| `/borrar` | Elimina una tarea permanentemente. |
| `/help` | Muestra la guía de comandos del bot. |

> Los comandos `/borrar` y `/editar` incluyen autocompletado: mientras escribís el nombre de la tarea, el bot te sugiere coincidencias del canal.

## 📂 Arquitectura del Proyecto

```
.
├── main.py                 # Punto de entrada, intents y carga de extensiones
├── cogs/
│   └── todo.py             # Comandos y lógica de interacción (Capa de Presentación)
├── database/
│   ├── manager.py          # Consultas SQL, creación de tablas (Capa de Datos)
│   └── database.db         # Base de datos SQLite (se genera al iniciar)
├── tests/
│   └── test_manager.py     # Pruebas unitarias de la capa de datos
├── requirements.txt        # Dependencias del proyecto
└── .env.example            # Plantilla de variables de entorno
```

El proyecto sigue una estructura modular para facilitar el mantenimiento y el escalado.

## ⚙️ Instalación y Configuración

### 1. Requisitos previos

* [Python 3.11+](https://www.python.org/downloads/)
* Una cuenta en el [Discord Developer Portal](https://discord.com/developers/applications)

### 2. Clonar el repositorio

```bash
git clone https://github.com/alandprieto/bottask-dircord.git
cd bottask-dircord
```

### 3. Crear un entorno virtual e instalar dependencias

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Configurar el token

1. Copiá `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
2. En el Developer Portal, creá una aplicación y agregá un bot.
3. Abrí `.env` y reemplazá `tu_token_aqui` con el token de tu bot:
   ```env
   DISCORD_TOKEN=tu_token_aqui
   ```

> ⚠️ **Nunca compartas ni subas el archivo `.env` a GitHub** (ya está incluido en `.gitignore`).

### 5. Invitar el bot a tu servidor

En la pestaña **OAuth2 → URL Generator** de tu aplicación, seleccioná:

* **Scopes**: `bot` y `applications.commands`
* **Bot Permissions**: `Send Messages`, `Embed Links`, `Read Message History`

Usá la URL generada para invitar el bot. Además, asegurate de tener habilitado el **Message Content Intent** en la pestaña *Bot*.

### 6. Ejecutar el bot

```bash
python main.py
```

## 🧪 Pruebas

```bash
python -m unittest discover -s tests -v
```

## 📝 Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).