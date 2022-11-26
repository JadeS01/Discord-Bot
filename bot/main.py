import discord
import asyncio
import os

from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents = intents, application_id = os.getenv('APP_ID'))


@client.event
async def on_ready():
    print('Online')
    await client.tree.sync(guild = discord.Object(id = os.getenv('GUILD_ID')))

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message[0] == '$':
        return
    if message.author == client.user:
        return
    await message.channel.send('elloo')

# Apps cmds
@client.tree.context_menu(name = 'Echo', guild = discord.Object(id = os.getenv('GUILD_ID')))
async def hello(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(f'{message.content}')

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await client.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await client.start(os.getenv('TOKEN'))

asyncio.run(main())