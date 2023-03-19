import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
from discord import ui

class SelectMenu(discord.ui.Select):
    def __init__(self, options, parent):
        super().__init__(placeholder="What roles do you want", options=options)
        self.parent = parent

    async def callback(self, interaction:discord.Interaction):
        await interaction.response.edit_message(content=f"Successfully given you {self.values} roles")
        await self.parent.additional_clean()

class Select(discord.ui.View):
    def __init__(self, options):
        super().__init__()
        self.add_item(SelectMenu(options, parent=self))
    
    async def additional_clean(self):
        print(f"before = {self.children}")
        for child in self.children:
            self.remove_item(child)

        print(f"after = {self.children}")
            


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
    
    async def on_ready(self):
        synced = await self.tree.sync()
        print("Slash CMDs Synced " + str(len(synced)) + " commands")

TOKEN = 'MTA2MDA2NzE5NDExNDk1MzI0Nw.Gwc8Jn.n_mfQoryHMVa9bzgjd49Ls-v4-Zg1X9gUo0wa8' #토큰
intents = discord.Intents.default()
intents.message_content = True
client = Client()

@client.tree.command(name="test2")
async def select(interaction: discord.Interaction):
    options = [
        discord.SelectOption(label="Youtube"),
        discord.SelectOption(label="Instagram"),
        discord.SelectOption(label="Twitch"),
    ]
    await interaction.response.send_message(content="Select your roles", view=Select(options))

client.run(TOKEN)
