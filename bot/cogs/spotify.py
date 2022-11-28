import discord
from discord.ext import commands

class Spotify(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def track(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        res = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

        if res is None:
            await ctx.send("You're not listening to Spotify.")
        else:
            await ctx.send(f'https://open.spotify.com/track/{res.track_id}')

async def setup(client):
    await client.add_cog(Spotify(client))