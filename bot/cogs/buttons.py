import discord
from discord.ext import commands
from mongodb import db

class Buttons(discord.ui.View):
    def __init__(self, *, timeout = 180.0):
        super().__init__(timeout = timeout)
    
    @discord.ui.button(label = "Button", style = discord.ButtonStyle.gray)
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # use dir() to view object attrs
        # print(interaction.user.id)
        author = interaction.user.id
        key = {'author': author}
        db.button_clicks.update_one(key, {'$inc': {'clicks': 1}}, True)
        clicks = db.button_clicks.find_one(key)
        await interaction.response.send_message(f"You've clicked {clicks['clicks']} time(s)", ephemeral = True)

class Click(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(db)
        print('Button cog loaded')

    @commands.command()
    async def click(self, ctx):
        await ctx.send('Message', view = Buttons())

async def setup(client):
    await client.add_cog(Click(client))