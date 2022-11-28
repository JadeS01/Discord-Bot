import discord
import requests
import os

from discord import app_commands
from discord.ext import commands

class SlashCmds(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Question cog loaded')

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands')
        return
    
    @app_commands.command(name = 'ping', description = 'Test slash command')
    # You can add params like param: str
    async def ping(self, interaction: discord.Interaction):
        ping = round(self.client.latency * 1000)
        await interaction.response.send_message(f'Pong: {ping}ms')
    
    @app_commands.command(name = 'pong', description = 'Test slash command #2')
    async def pong(self, interaction: discord.Interaction):
        await interaction.response.send_message('Ping')

    @app_commands.command(name = 'useless', description = 'Share a useless fact in en/de')
    async def useless(self, interaction: discord.Interaction, language: str):
        if language.lower() == 'en' or language.lower() == 'de':
            language = language.lower()
        else:
            language = 'en'
        res = requests.get(f'http://uselessfacts.jsph.pl/random.json?language={language}').json()
        embed = discord.Embed(description = res['text'])
        await interaction.response.send_message(embed = embed)

async def setup(client):
    await client.add_cog(SlashCmds(client), guilds = [discord.Object(id = os.getenv('GUILD_ID'))])