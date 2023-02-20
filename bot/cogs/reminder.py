from discord.ext import commands
import asyncio
import re

class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reminders = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Reminder cog')

    @commands.command()
    async def remind(self, ctx, timer, *, reason: str):
        if ctx.author.id in self.reminders:
            await ctx.send("Please wait your your existing timer to end.")
            return
        if not re.match(r'\d+min', timer):
            await ctx.send(f"{timer} is not a valid argument. Please format your timer as a number immediately followed by 'min'; e.g. `95min`.")
            return
        duration = timer.replace("min", "")
        duration = int(duration) * 60
        async def timer_task():
            await asyncio.sleep(duration)
            await ctx.send(f"Reminder for {ctx.author.mention}'s `{reason}`.")
            timer_task = self.reminders.pop(ctx.author.id)
            timer_task.cancel()
        timer_task = self.client.loop.create_task(timer_task())
        self.reminders[ctx.author.id] = timer_task
        await ctx.send(f"I'll remind {ctx.author.mention} for `{reason}` in `{timer}`.")

    @commands.command()
    async def cancel_remind(self, ctx):
        if ctx.author.id not in self.reminders:
            await ctx.send("You don't have a reminder set.")
            return
        timer_task = self.reminders.pop(ctx.author.id)
        timer_task.cancel()
        await ctx.send("I've cancelled your reminder.")

async def setup(client):
    await client.add_cog(Reminder(client))