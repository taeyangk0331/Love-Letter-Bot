import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
from discord import ui

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

class TestButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="test")
    async def test(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="second button", view=TestButtons2())

class TestButtons2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="test2")
    async def test2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="hello")

@client.tree.command(name="button")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(content="first button", view=TestButtons(), ephemeral=True)

client.run(TOKEN)
