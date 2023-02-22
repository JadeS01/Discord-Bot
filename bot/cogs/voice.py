import discord
import nacl
import asyncio

from discord.ext import commands
from discord import FFmpegPCMAudio

import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def join(self, ctx):
        if ctx.voice_client:
            await ctx.send("I'm already in a VC.")
            return
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
    async def box(self, ctx, url):
        if ctx.author.voice and ctx.voice_client:
            source = FFmpegPCMAudio('box.mp3')
            # print(source)
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                ctx.voice_client.play(discord.FFmpegPCMAudio(executable = "C:\\Users\\abhisar.ahuja\\Documents\\ffmpeg\\ffmpeg.exe", source=filename))
            await ctx.send('**Now playing:** {}'.format(filename))
        else:
            await ctx.send('You need to join a VC first.')

async def setup(client):
    await client.add_cog(Voice(client))