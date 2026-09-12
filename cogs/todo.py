import discord
from discord import app_commands
from discord.ext import commands

# Acá vas a tener que importar tu manager.py para usar la BD
from database import manager


class TodoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Así se define un Slash Command
    @app_commands.command(name="añadir", description="Añade una tarea a la lista")
    @app_commands.choices(
        estado=[
            app_commands.Choice(name="🔴 SIN EMPEZAR", value=1),
            app_commands.Choice(name="🟡 EN PROCESO", value=2),
            app_commands.Choice(name="🟢 TERMINADO", value=3),
        ]
    )
    async def añadir_tarea(
        self,
        interaction: discord.Interaction,
        tarea: str,
        descripcion: str,
        estado: app_commands.Choice[int],
    ):
        manager.add_task(tarea, descripcion, estado.value, interaction.channel_id)
        await interaction.response.send_message(
            f"Tarea '{tarea}' añadida correctamente.", ephemeral=True
        )

    @app_commands.command(name="listar", description="Lista todas las tareas")
    async def listar_tareas(self, interaction: discord.Interaction):
        tareas = manager.list_task(interaction.channel_id)
        if not tareas:
            await interaction.response.send_message(
                "No hay tareas pendientes.", ephemeral=True
            )
            return
        mensaje = "Tareas pendientes:\n"
        for tarea in tareas:
            mensaje += (
                f"**{tarea['name']}** (ID: {tarea['id']}) - *{tarea['state_name']}*\n"
                f"> {tarea['description']}\n\n"
            )
        await interaction.response.send_message(mensaje)

    async def tareas_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,  # Lo que el usuario está escribiendo
    ) -> list[app_commands.Choice[int]]:
        # Buscamos en la DB usando nuestra nueva función del manager
        tareas = manager.search_tasks_name(current, interaction.channel_id)

        # Convertimos los resultados en opciones de Discord (Choice)
        # El 'name' es lo que ve el usuario, el 'value' es el ID que recibe el bot
        return [app_commands.Choice(name=nombre, value=idx) for idx, nombre in tareas][
            :25
        ]  # Discord permite un máximo de 25 opciones

    @app_commands.command(name="borrar", description="Borrar una tarea")
    @app_commands.autocomplete(tarea_id=tareas_autocomplete)
    async def borrar_tarea(self, interaction: discord.Interaction, tarea_id: int):
        filas_afectadas = manager.delete_task(tarea_id, interaction.channel_id)
        if filas_afectadas < 1:
            await interaction.response.send_message(
                f"❌ No se encontró ninguna tarea con el ID {tarea_id}.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"🗑️ Tarea con ID {tarea_id} eliminada.", ephemeral=True
            )

    @app_commands.command(name="editar", description="Editar estado de una tarea")
    @app_commands.choices(
        nuevo_estado=[
            app_commands.Choice(name="🔴 SIN EMPEZAR", value=1),
            app_commands.Choice(name="🟡 EN PROCESO", value=2),
            app_commands.Choice(name="🟢 TERMINADO", value=3),
        ]
    )
    @app_commands.autocomplete(tarea_id=tareas_autocomplete)
    async def editar_tarea(
        self,
        interaction: discord.Interaction,
        tarea_id: int,
        nuevo_estado: app_commands.Choice[int],
    ):
        filas = manager.change_state(
            nuevo_estado.value, tarea_id, interaction.channel_id
        )
        if filas > 0:
            await interaction.response.send_message(
                f"✅ Estado de la tarea #{tarea_id} cambiado a **{nuevo_estado.name}**",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"❌ No se encontró la tarea con ID {tarea_id}.", ephemeral=True
            )

    @app_commands.command(
        name="help", description="Muestra la lista de comandos disponibles"
    )
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Guía de Comandos - TaskMaster",
            description="Aquí tenés todo lo que podés hacer con el bot en este canal:",
            color=discord.Color.blue(),
        )

        embed.add_field(
            name="`/añadir`",
            value="Registra una nueva tarea con descripción y estado.",
            inline=False,
        )
        embed.add_field(
            name="`/listar`",
            value="Muestra todas las tareas guardadas en este canal.",
            inline=False,
        )
        embed.add_field(
            name="`/editar`",
            value="Cambia el estado de una tarea existente.",
            inline=False,
        )
        embed.add_field(
            name="`/borrar`", value="Elimina una tarea permanentemente.", inline=False
        )

        embed.set_footer(text="Organización segmentada por canal.")

        await interaction.response.send_message(embed=embed, ephemeral=True)


# Función obligatoria para cargar el Cog
async def setup(bot):
    await bot.add_cog(TodoCog(bot))
