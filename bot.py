import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='sudo ')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Welcome {member.name}, do ```sudo welcome [First Name] [Last Name (optional)]``` to see the rest of the channels!'
    )


@bot.event
async def on_ready():
    await bot.send("Logged in!")


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
    role2 = discord.utils.get(ctx.guild.roles, name="MUTED")
    if role not in ctx.author.roles and role2 not in ctx.author.roles:
        await ctx.author.edit(nick=arg)
        await ctx.author.add_roles(role)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amt=5.0):
    if amt > 50.0:
        amt = 50.0
        await ctx.send(f"Too many messages")
    await ctx.send(f"Deleting {str(int(amt))} messages")
    await ctx.channel.purge(limit=(int(amt) + 2))


@bot.command()
async def mkdir(ctx):
    if "throwaway" not in str(ctx.guild.channels):
        category = discord.utils.get(ctx.guild.channels, name="chat")
        await ctx.guild.create_text_channel("throwaway", category=category)
    else:
        channel = discord.utils.get(ctx.guild.channels, name="throwaway")
        await channel.delete()


@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Verified")
    await user.remove_roles(role)


@bot.command()
async def ban(ctx, user: discord.Member):
    return user


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, user: discord.Member, reason, level=1):
    warn = level
    admin = discord.utils.get(ctx.guild.roles, name="Admin")
    for role in user.roles:
        if "Warning #1" in role.name:
            warn += 1
        if "Warning #2" in role.name:
            warn += 2
    warn_role = discord.utils.get(ctx.guild.roles,
                                  name="Warning #" + str(warn))

    if warn <= 2:
        await user.add_roles(warn_role)
        embed = discord.Embed(
            title="Warned",
            description=f"Warned {user.mention} for {reason}",
            color=0xff0000)
        embed.set_author(name="ScribeBot")
        embed.add_field(name="Warning Number", value=warn, inline=True)
        await ctx.send(embed=embed)

    elif warn >= 3:
        embed = discord.Embed(
            title="Banned",
            description=
            f"Banned {user.mention} for {reason}. They had 3 strikes.",
            color=0xff0000)
        embed.set_author(name="ScribeBot")
        await ctx.send(embed=embed)
        await user.ban(reason=reason, delete_message_days=0)


@bot.command()
async def sl(ctx):
    await ctx.send(
        "```                          (  ) (@@) ( )  (@)  ()    @@    O     @     O     @ \n                  (@@@) \n              (    ) \n           (@@@@) \n \n         (   ) \n         ====        ________                ___________ \n     _D _|  |_______/        \__I_I_____===__|_________| \n     |(_)---  |   H \________/ |   |        =|___ ___|      _________________\n     /     |  |   H   |  |     |   |         ||_| |_||     _|                \___ \n    |      |  |   H   |__--------------------| [___] |   =| \n    | ________|___H __/__|_____/[][]~\_______|       |   -| \n    |/ |   | -----------I_____I [][] []  D   |=======|____|______________________ \n  __/ =| o |=-~~\  /~~\  /~~\  /~~\ ____Y___________|__|________________________ \n   |/-=|___|=O=====O=====O=====O   |_____/~\___/          |_D__D__D_|  |_D__D__D \n    \_/      \__/  \__/  \__/  \__/      \_/               \_/   \_/    \_/   \ ``` "
    )


@warn.error
@clear.error
async def missing_perms(ctx, error):
    await ctx.send(
        f"{ctx.author.mention} is not in the sudoers file. This incident will be reported."
    )


@bot.command()
async def stream(ctx):
    streamnick = discord.utils.get(ctx.guild.roles
        , name="StreamNick")

    if streamnick == None:
        await ctx.guild.create_role(name="StreamNick",
            color=discord.Color.from_rgb( 255, 85, 85))
    
    if not (streamnick in ctx.author.roles):
        await ctx.author.add_roles(streamnick, reason="Opted into StreamNick")

    await ctx.send("You've opted into the StreamNick!")

@bot.command()
async def nostream(ctx):
    streamnick = discord.utils.get(ctx.guild.roles
        , name="StreamNick")

    if streamnick == None:
        await ctx.guild.create_role(name="StreamNick",
            color=discord.Color.from_rgb( 255, 85, 85))
    
    if (streamnick in ctx.author.roles):
        await ctx.author.remove_roles(streamnick, reason="Opted out of StreamNick")

    await ctx.send("You've opted out of the StreamNick!")


    

@bot.event
async def on_message(message):

    if message.content.startswith("sudo "):
        await bot.process_commands(message)
        return

    if message.author == bot.user:
        return
    if type(message.channel) is discord.DMChannel or type(
            message.channel) is discord.GroupChannel:
        return

    streamnick = discord.utils.get(message.channel.guild.roles
        , name="StreamNick")

    if streamnick == None:
        await message.channel.guild.create_role(name="StreamNick",
            color=discord.Color.from_rgb( 255, 85, 85))
        return

    if streamnick in message.author.roles:
        nick = message.content
        if len(nick) > 32:
            nick = nick[0:30] + "..."
        await message.author.edit(nick=nick, reason="StreamNick opt-in")


bot.run(TOKEN)
