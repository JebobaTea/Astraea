import discord
import os
from discord.ext import commands


bot = commands.Bot(command_prefix = '+', activity = discord.Game(name = '+help'))
bot.remove_command('help')


@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title = 'Error', description = 'Unknown Command', color = discord.Color.red())
        await ctx.send(embed = embed)
    elif isinstance(error,discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(title = 'Error', description = 'You\'re missing an argument!', color = discord.Color.red())
        await ctx.send(embed = embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = 'Error', description = 'Insufficient permissions!', color = discord.Color.red())
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title = 'Error', description = str(error), color = discord.Color.red())
        await ctx.send(embed = embed)


bot.load_extension('cogs.tickets')
bot.load_extension('cogs.misc')
bot.load_extension('cogs.moderation')
bot.load_extension('cogs.fun')
bot.run('TOKEN')
