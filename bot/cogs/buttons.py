import discord
from discord.ext import commands

class Buttons(discord.ui.View):
    def __init__(self, *, timeout = 180.0):
        super().__init__(timeout = timeout)
    
    @discord.ui.button(label = "Button", style = discord.ButtonStyle.gray)
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked a button")

class Click(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Button cog loaded')

    @commands.command()
    async def click(self, ctx):
        await ctx.send('Message', view = Buttons())

async def setup(client):
    await client.add_cog(Click(client))