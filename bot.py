import os
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ⚠️ REMPLACE ces IDs par les tiens
GUILD_ID = 123456789012345678
ROLE_1_ID = 111111111111111111
ROLE_2_ID = 222222222222222222

async def toggle_role(interaction: discord.Interaction, role_id: int):
    member = interaction.user
    role = interaction.guild.get_role(role_id)

    if role in member.roles:
        await member.remove_roles(role)
        await interaction.response.send_message(
            f"❌ Rôle retiré : {role.name}", ephemeral=True
        )
    else:
        await member.add_roles(role)
        await interaction.response.send_message(
            f"✅ Rôle ajouté : {role.name}", ephemeral=True
        )

class RoleButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Rôle 1", style=discord.ButtonStyle.primary)
    async def role1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await toggle_role(interaction, ROLE_1_ID)

    @discord.ui.button(label="Rôle 2", style=discord.ButtonStyle.secondary)
    async def role2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await toggle_role(interaction, ROLE_2_ID)

@tree.command(name="roles", description="Choisir ses rôles")
async def roles(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Choisis tes rôles :", view=RoleButtons()
    )

@client.event
async def on_ready():
    await tree.sync()
    client.add_view(RoleButtons())
    print(f"✅ Connecté en tant que {client.user}")

client.run(TOKEN)
