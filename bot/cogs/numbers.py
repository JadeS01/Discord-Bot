import requests
import discord
from discord.ext import commands

class Numbers(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Numbers cog')
     
    @commands.command()
    # checks if person has certain role to run command
    # @commands.has_permissions(administrator = True)
    async def facts(self, ctx, number):
        res = requests.get(f'http://numbersapi.com/{number}')
        embed = discord.Embed(description = res.text)
        await ctx.channel.send(embed = embed)

async def setup(client):
    await client.add_cog(Numbers(client))