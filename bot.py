import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='sudo ')


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
    if role not in ctx.author.roles:
        await ctx.author.edit(nick=arg)
        await ctx.author.add_roles(role)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amt=5.0):
    if amt > 50.0:
        amt = 50.0
        await ctx.send(f"Too many messages")
    await ctx.send(f"Deleting {str(int(amt))} messages")
    await ctx.channel.purge(limit=(int(amt)+2))

@bot.command()
async def mkdir(ctx):
    if "throwaway" not in str(ctx.guild.channels):
        category = discord.utils.get(ctx.guild.channels, name="chat")
        await ctx.guild.create_text_channel("throwaway", category=category)
    else:
        channel = discord.utils.get(ctx.guild.channels, name="throwaway")
        await channel.delete()

@bot.command()
async def ban(ctx, user: discord.Member):
    return user

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, user: discord.Member, reason, level = 1):
    warn = level
    admin = discord.utils.get(ctx.guild.roles, name="Admin") 
    for role in user.roles:
        if "Warning #1" in role.name:
            warn += 1
        if "Warning #2" in role.name:
            warn += 2
    warn_role = discord.utils.get(ctx.guild.roles, name="Warning #"+str(warn))

    if warn <= 2:   
        await user.add_roles(warn_role)
        embed=discord.Embed(title="Warned", description= f"Warned {user.mention} for {reason}", color=0xff0000)
        embed.set_author(name="ScribeBot")
        embed.add_field(name="Warning Number", value=warn, inline=True)
        await ctx.send(embed=embed)
        
    elif warn >= 3:
        embed=discord.Embed(title="Banned", description=f"Banned {user.mention} for {reason}. They had 3 strikes.", color=0xff0000)
        embed.set_author(name="ScribeBot")
        await ctx.send(embed=embed)
        await user.ban(reason=reason, delete_message_days=0)

@warn.error
@clear.error
async def missing_perms(ctx, error):
    await ctx.send(f"{ctx.author.mention} is not in the sudoers file. This incident will be reported.")

bot.run(TOKEN)
