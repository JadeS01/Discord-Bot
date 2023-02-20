import discord
import asyncio
import os
import secrets
import helpers

from dotenv import load_dotenv
from discord.ext import commands
from db.mongodb import get_db

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(
    command_prefix='$',
    intents = intents,
    activity = discord.Game(name = 'under development'),
    status = discord.Status.do_not_disturb,
    application_id = os.getenv('APP_ID')
)

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

@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        embed = discord.Embed(title="New Member", description=f"Weclome {member.mention}", color=discord.Color.green())
        embed.set_image(url="https://media.giphy.com/media/icUEIrjnUuFCWDxFpU/giphy.gif")
        await channel.send(embed=embed)

# Apps cmds
@client.tree.context_menu(name = 'Echo', guild = discord.Object(id = os.getenv('GUILD_ID')))
async def echo(interaction: discord.Interaction, message: discord.Message):
    author = message.author.id
    await interaction.response.send_message(f'{message.content} \n\t- <@{author}>')

# Modify this to save user tickets under current guild rather than expose every guild tickets
@client.tree.context_menu(name = 'Save This', guild = discord.Object(id = os.getenv('GUILD_ID')))
async def save_this(interaction: discord.Interaction, message: discord.Message):
    author = message.author.id
    if author == client.user.id:
        await interaction.response.send_message('Why do you need to save my message?')
    else:
        key = {'author': author}
        user = f'<@{author}>'
        attachments = None
        content = None
        if message.attachments:
            attachments = helpers.get_attachments(message.attachments)
        if message.content:
            content = message.content
        data = {'message': content, 'attachments': attachments}
        get_db().server_messages_log.update_one(key, {'$inc': {'tickets': 1}}, True)
        ticket = {f'ticket_id.{secrets.token_hex(6)}': data}
        get_db().server_messages_log.update_one(key, {'$set': ticket}, True)
        await interaction.response.send_message(f"Saved {user} 's message")

# Perhaps modify or create a new command that only returns a certain amount rather than all tickets
@client.tree.context_menu(name = 'Expose Them', guild = discord.Object(id = os.getenv('GUILD_ID')))
async def expose_them(interaction: discord.Interaction, message: discord.Message):
    author = message.author.id
    if author == client.user.id:
        await interaction.response.send_message("You can't expose me.")
    else:
        key = {'author': author}
        messages = ''
        data = get_db().server_messages_log.find_one(key)
        for ticket in data['ticket_id']:
            messages = messages + '\n' + f"'{data['ticket_id'][ticket]['message']}'"
        description = f'Exposing <@{author}>: \n{messages}'
        embed = discord.Embed(description = description)
        await interaction.response.send_message(embed = embed)

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await client.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await client.start(os.getenv('TOKEN'))

asyncio.run(main())