import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import sqlite3

#Ton token et infos bot
TOKEN = "MTM5MjE4OTcxOTU4ODM3NjYzNw.GR6Pa8.ZdV0L5JBwqQKLPUijUBT_5FJSin5fwBElIgQUM"
CLIENT_ID = 1392189719588376637
GUILD_ID = 1391533981329260718  # ⛔️ Remplace par l'ID de ton serveur Discord (PAS le client ID)

#Rôle à donner et lien vers ton site
ROLE_NAME = "VIP"
SITE_URL = "https://adunlock.onrender.com/unlock"  # 🔁 Ton lien vers le site

#Intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

#Initialisation du bot
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

#Vérifie si la clé est valide
def is_valid_key(key):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT used FROM keys WHERE key = ?", (key,))
    row = cur.fetchone()
    if row and row[0] == 0:
        cur.execute("UPDATE keys SET used = 1 WHERE key = ?", (key,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

#Slash command : /unlock
@tree.command(name="unlock", description="🔓 Obtiens le lien pour générer ta clé.")
async def unlock(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🔑 Clique ici pour générer ta clé : {SITE_URL}",
        ephemeral=True
    )

#Slash command : /valider clé
@tree.command(name="valider", description="✅ Valide ta clé et obtiens un rôle temporaire.")
@app_commands.describe(clé="Ta clé d'accès générée sur le site")
async def valider(interaction: discord.Interaction, clé: str):
    if is_valid_key(clé):
        role = discord.utils.get(interaction.guild.roles, name=ROLE_NAME)
        if not role:
            await interaction.response.send_message("❌ Le rôle 'VIP' est introuvable.")
            return

        await interaction.user.add_roles(role)
        await interaction.response.send_message("✅ Clé validée, rôle VIP attribué pour 30 minutes.")

        await asyncio.sleep(1800)  # 30 minutes
        await interaction.user.remove_roles(role)
        await interaction.followup.send("🕒 Ton accès VIP a expiré.")
    else:
        await interaction.response.send_message("❌ Clé invalide ou déjà utilisée.")

#Synchronisation des commandes au lancement
@bot.event
async def on_ready():
    try:
        guild = discord.Object(id=GUILD_ID)

        # Ajout manuel des commandes dans le GUILD
        tree.copy_global_to(guild=guild)

        # Synchronisation avec le serveur
        synced = await tree.sync(guild=guild)

        print(f"✅ Commandes slash synchronisées ({len(synced)}) pour le serveur.")
    except Exception as e:
        print(f"❌ Erreur de sync : {e}")
    print(f"🤖 Connecté en tant que {bot.user.name}")
    
#Lance le bot
bot.run("MTM5MjE4OTcxOTU4ODM3NjYzNw.GR6Pa8.ZdV0L5JBwqQKLPUijUBT_5FJSin5fwBElIgQUM")
