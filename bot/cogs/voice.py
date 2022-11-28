import discord
import nacl

from discord.ext import commands

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
        if(ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("I'm not in VC.")

async def setup(client):
    await client.add_cog(Voice(client))