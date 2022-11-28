import discord
import nacl
import asyncio

from discord.ext import commands
from discord import FFmpegPCMAudio

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send('You need to join a VC first.')

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("I'm not in VC.")

    @commands.command()
    async def box(self, ctx):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('box.mp3')
            # print(source)
            await voice.play(source)
        else:
            await ctx.send('You need to join a VC first.')

async def setup(client):
    await client.add_cog(Voice(client))