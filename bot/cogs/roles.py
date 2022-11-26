import discord
from discord.ext import commands

# Can store this information somewhere.
class SurveyModal(discord.ui.Modal, title = ">>>"):
    name = discord.ui.TextInput(label = 'Name')
    answer = discord.ui.TextInput(label = 'Description', style = discord.TextStyle.paragraph)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('wow', ephemeral = False)

# This all appears as a drop down menu
class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label = 'Hi', emoji = '😃', description = 'This is a role!'),
            discord.SelectOption(label = 'Hi2', emoji = '😆', description = 'This is a role2!'),
            discord.SelectOption(label = 'Hi3', emoji = '😋', description = 'This is a role3!')
        ]
        # access discord.ui methods
        super().__init__(placeholder = "Choose a role", max_values = 1, min_values = 0, options = options)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        if self.values[0] == 'Hi':
            role = await guild.create_role(name = 'Hi', colour = discord.Colour.blue())
            await user.edit(roles = [role])
            # ephemeral shows interaction privately
        elif self.values[0] == 'Hi2':
            role = await guild.create_role(name = 'Hi2', colour = discord.Colour.red())
            await user.edit(roles = [role])
        elif self.values[0] == 'Hi3':
            role = await guild.create_role(name = 'Hi3', colour = discord.Colour.green())
        await user.edit(roles = [role])
        # await interaction.response.send_message('Hello!!', ephemeral = True)
        await interaction.response.send_modal(SurveyModal())

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 30):
        super().__init__(timeout = timeout)
        self.add_item(Select())

class Role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def role(self, ctx):
        await ctx.send('Select a role', view = SelectView(), delete_after = 15)

async def setup(client):
    await client.add_cog(Role(client))