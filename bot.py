import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print(f"{bot.user.name} connected")

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"{member.name}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong")

@bot.command()
async def invite(ctx):
    link = await ctx.channel.create_invite()
    await ctx.send(f"Here is the invite to {ctx.guild.name}: {link} ")

@bot.command()
async def welcome(ctx, *, arg):
    role = discord.utils.get(ctx.guild.roles, name="Verified")
    await ctx.author.add_roles(role)
    if role not in ctx.author.roles:
       await ctx.author.edit(nick=arg)

@bot.command()
async def prune(ctx, arg):
    role = discord.utils.get(ctx.guild.roles, name="Admin")


bot.run(TOKEN)
