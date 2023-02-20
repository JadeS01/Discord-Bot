import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import numpy
import math
import re
from io import BytesIO

class Plot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Plot cog')

    @commands.command()
    async def plot(self, ctx, *, equation):
        if ',' in equation:
            points = equation.split()[1:]
            try: 
                x = [float(val.split(',')[0]) for val in points]
                y = [float(val.split(',')[1]) for val in points]

                fig, ax = plt.subplots()
                ax.plot(x, y)

                fig.savefig('discord_plot.png')
                with open('discord_plot.png', 'rb') as f:
                    file = discord.File(f)
                    await ctx.send(file=file)
                
            except:
                await ctx.send(f"`{equation}` is not a valid set of points; for help with `$plot`, use `$plot_help`.")
        else:    
            x = numpy.linspace(-10, 10, 1000)
            try:
                # function = eval(equation, {}, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt})
                y = eval(equation)
            except:
                await ctx.send(f"`{equation}` is not valid; for help with `$plot`, use `$plot_help`.")
                return
            
            plt.plot(x, y)
            plt.title(equation)
            plt.xlabel('x')
            plt.ylabel('y')

            plt.savefig('discord_plot.png')
            plt.close()

            with open('discord_plot.png', 'rb') as f:
                file = discord.File(f)
                await ctx.send(file=file)

    @commands.command()
    async def plot_help(self, ctx):
        description = "Here are some tips and examples when using $plot:\n1. It is inferred that `y` equals your function, so leave out `y=`.\n2. Exponents: `x ** 2` instead of `x ^ 2`.\n3. Providing points: `x1,y2 x2,y2...` instead of `(x1,y1),(x2,y2)...`"
        embed = discord.Embed(description=description)
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Plot(client))
