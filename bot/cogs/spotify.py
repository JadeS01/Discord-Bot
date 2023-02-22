import discord
import spotipy
import requests
import base64
import os
from discord.ext import commands, tasks
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify(commands.Cog):
    def __init__(self, client):
        self.client = client
        spotify_client = os.getenv('SPOTIFY_CLIENT')
        spotify_secret = os.getenv('SPOTIFY_SECRET')
        base64_credentials = base64.b64encode(f"{spotify_client}:{spotify_secret}".encode()).decode()
        auth_response = requests.post('https://accounts.spotify.com/api/token', {'grant_type': 'client_credentials'}, headers={'Authorization': f'Basic {base64_credentials}'})
        auth_response_data = auth_response.json()
        playlists_response = requests.get('https://api.spotify.com/v1/me/playlists', headers={'Authorization': f'Bearer {auth_response_data["access_token"]}'})

    @commands.Cog.listener()
    async def on_ready(self):
        print('Spotify cog')

    @commands.command()
    async def play(self, ctx):
        if ctx.voice_client and not ctx.author.voice:
            await ctx.send("You're not in VC.")
            return
        if not ctx.voice_client:
            await ctx.send("Use `$join` so I can hop on VC.")
            return
    
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