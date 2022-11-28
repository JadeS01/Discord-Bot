import discord

from discord.ext import commands
from discord import Spotify

class Spotify(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Spotify cog')
    
    @commands.command()
    async def track(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        res = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
        if res is None:
            await ctx.send("You're not listening to Spotify.")
        else:
            await ctx.send(f'https://open.spotify.com/track/{res.track_id}')

    @commands.command()
    async def track_details(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        res = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
        if res is None:
            await ctx.send("You're not listening to Spotify.")
        else:
            embed = discord.Embed(title = f"{user.name}", description = "Is currently listening to:\n{}".format(res.title), color = 0x2d9dd6)
            embed.set_thumbnail(url = res.album_cover_url)
            embed.add_field(name = "Artist(s)", value = res.artist or res.artists)
            embed.add_field(name = "Album", value = res.album)
            embed.set_footer(text = f"Duration is {res.duration}")
            await ctx.send(embed = embed)

async def setup(client):
    await client.add_cog(Spotify(client))