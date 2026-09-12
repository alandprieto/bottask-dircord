import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import manager

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("¡No se encontró el token en el archivo .env!")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("taskmaster")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def setup_hook():
    manager.crear_tabla()
    await bot.load_extension("cogs.todo")
    await bot.tree.sync()
    logger.info("Comandos sincronizados")


bot.setup_hook = setup_hook


@bot.event
async def on_ready():
    logger.info("Conectado como %s", bot.user)


if __name__ == "__main__":
    bot.run(TOKEN)