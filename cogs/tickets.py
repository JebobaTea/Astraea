import discord
import json
from discord.ext import commands


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newticket(self, ctx):
        with open('data.json') as f:
            data = json.load(f)
        id = str(ctx.message.guild.id)
        if id not in data:
            data[id] = {'ticket-counter': 0, 'ticket-channel-ids': []}
        ticket_number = int(data[id]['ticket-counter'])
        ticket_number += 1
        ticket_channel = await ctx.guild.create_text_channel('ticket-{}'.format(ticket_number))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages = False, read_messages = False)
        for role in ctx.guild.roles:
            if role.permissions.manage_guild:
                await ticket_channel.set_permissions(role, send_messages = True, read_messages = True, add_reactions = True, embed_links = True, attach_files = True, read_message_history = True, external_emojis = True)
        await ticket_channel.set_permissions(ctx.author, send_messages = True, read_messages = True, add_reactions = True, embed_links = True, attach_files = True, read_message_history = True, external_emojis = True)
        data[id]['ticket-channel-ids'].append(ticket_channel.id)
        data[id]['ticket-counter'] = int(ticket_number)
        with open('data.json', 'w') as f:
            json.dump(data, f)
        embed = discord.Embed(title = 'Ticket Creator', description = 'Your ticket has been created.', color = discord.Color.green())
        await ctx.send(embed = embed)
    
    @commands.command()
    async def closeticket(self, ctx):
        with open('data.json') as f:
            data = json.load(f)
        id = str(ctx.message.guild.id)
        if id not in data:
            data[id] = {'ticket-counter': 0, 'ticket-channel-ids': []}
        if ctx.channel.id in data[id]['ticket-channel-ids']:
            channel_id = ctx.channel.id
            await ctx.channel.delete()
            index = data[id]['ticket-channel-ids'].index(channel_id)
            del data[id]['ticket-channel-ids'][index]
            with open('data.json', 'w') as f:
                json.dump(data, f)
        else:
            embed = discord.Embed(title = 'Ticket Creator', description = 'Please run this in the channel you want to close!', color = discord.Color.red())
            await ctx.send(embed = embed)
    
    @commands.command()
    async def renameticket(self, ctx, *, arg):
        with open('data.json') as f:
            data = json.load(f)
        id = str(ctx.message.guild.id)
        if id not in data:
            data[id] = {'ticket-counter': 0, 'ticket-channel-ids': []}
        if ctx.channel.id in data[id]['ticket-channel-ids']:
            channel = ctx.channel
            await channel.edit(name = arg)
            embed = discord.Embed(title = 'Ticket Creator', description = 'Your ticket has been renamed.', color = discord.Color.green())
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = 'Ticket Creator', description = 'Please run this in the channel you want to rename!', color = discord.Color.red())
            await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Tickets(bot))
