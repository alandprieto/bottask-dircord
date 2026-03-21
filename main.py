import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import manager

# 1. Cargar el token secreto desde el archivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Le demostramos al editor que estamos controlando el caso de que sea None
if TOKEN is None:
    raise ValueError("¡No se encontró el token en el archivo .env!")

# 2. Configurar los "Intents" (los permisos que le dimos en el portal para leer mensajes)
intents = discord.Intents.default()
intents.message_content = True

# 3. Crear la instancia del bot y definir un prefijo para los comandos (ejemplo: !tarea)
bot = commands.Bot(command_prefix="!", intents=intents)


async def setup_hook():
    # Cargar el archivo del cog
    await bot.load_extension("cogs.todo")
    # Sincronizar los comandos con Discord
    await bot.tree.sync()
    print("Comandos sincronizados")


# Le asignamos nuestra función al bot
bot.setup_hook = setup_hook


# 4. Evento de inicio: ¿Qué hace el bot apenas logra conectarse?
@bot.event
async def on_ready():
    manager.crear_tabla()
    print("------------------------------------")
    print(f"¡Éxito! Conectado como {bot.user}")
    print("------------------------------------")


# 5. Encender el motor
if __name__ == "__main__":
    bot.run(TOKEN)
