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
async def clear(ctx, amt=5):
    await ctx.send(f"Deleting {amt} messages")
    await ctx.channel.purge(limit=(int(amt)+2))

@bot.command()
async def throwaway(ctx, arg):
    if arg == "make" and "throwaway" not in str(ctx.guild.channels):
        category = discord.utils.get(ctx.guild.channels, name="chat")
        await ctx.guild.create_text_channel("throwaway", category=category)
    elif arg == "delete":
        channel = discord.utils.get(ctx.guild.channels, name="throwaway")
        await channel.delete()
bot.run(TOKEN)
