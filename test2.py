import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
from discord import ui


class MyModal(ui.Modal, title="test"):
    name_button = ui.Button(label="Choose Card", style=discord.ButtonStyle.secondary)
    player_button = ui.Button(label="Choose Player", style=discord.ButtonStyle.secondary)
    guess = ui.TextInput(label="Guess Card")

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
    
    async def on_ready(self):
        synced = await self.tree.sync()
        print("Slash CMDs Synced " + str(len(synced)) + " commands")

TOKEN = 'MTA2MDA2NzE5NDExNDk1MzI0Nw.Goc-9w.JUFIj3fmeFWE1vnUdC1RKrQiG3HtjhBoJr971c' #토큰
intents = discord.Intents.default()
intents.message_content = True
client = Client()

@client.tree.command(name="test2")
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(MyModal())

client.run(TOKEN)
