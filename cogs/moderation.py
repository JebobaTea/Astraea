import discord
import discord.utils
from discord.ext import commands

data = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(title='Moderation Tools', description='A slowmode of '+str(seconds)+' seconds was set for this channel', colour=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self,ctx,*,member: discord.Member=None):
        if member != None:
            await ctx.guild.ban(member)
            embed = discord.Embed(title = 'Moderation Tools', description = 'Member banned.', color = discord.Color.green())
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = 'Moderation Tools', description = 'No member specified!', color = discord.Color.red())
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self,ctx,*,id=None):
        if id != None:
            member = await self.bot.fetch_user(id)
            await ctx.guild.unban(member)
            embed = discord.Embed(title = 'Moderation Tools', description = 'Member unbanned.', color = discord.Color.green())
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = 'Moderation Tools', description = 'No member specified!', color = discord.Color.red())
            await ctx.send(embed = embed)
    
    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self,ctx,*,member: discord.Member=None):
        if member != None:
            await ctx.guild.kick(member)
            embed = discord.Embed(title = 'Moderation Tools', description = 'Member kicked.', color = discord.Color.green())
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = 'Moderation Tools', description = 'No member specified!', color = discord.Color.red())
            await ctx.send(embed = embed)
    
    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def mute(self,ctx,*,member: discord.Member=None):
        if discord.utils.get(member.guild.roles,name = 'Muted'):
            role = discord.utils.get(member.guild.roles,name = 'Muted')
            if role in member.roles:
                embed = discord.Embed(title = 'Moderation Tools', description = 'Already muted!', color = discord.Color.red())
                await ctx.send(embed = embed)
            else:
                await member.add_roles(role)
                embed = discord.Embed(title = 'Moderation Tools', description = 'Member muted.', color = discord.Color.green())
                await ctx.send(embed = embed)
        else:
            perms = discord.Permissions(send_messages=False, read_messages=True)
            await ctx.guild.create_role(name='Muted', permissions=perms)
            role = discord.utils.get(member.guild.roles,name = 'Muted')
            await member.add_roles(role)
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(role, send_messages=False)
            embed = discord.Embed(title = 'Moderation Tools', description = 'Member muted.', color = discord.Color.green())
            await ctx.send(embed = embed)
    
    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def unmute(self,ctx,*,member: discord.Member=None):
        if discord.utils.get(member.guild.roles,name = 'Muted'):
            role = discord.utils.get(member.guild.roles,name = 'Muted')
            if role in member.roles:
                await member.remove_roles(role)
                embed = discord.Embed(title = 'Moderation Tools', description = 'Member unmuted.', color = discord.Color.green())
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = 'Moderation Tools', description = 'Member isn\'t muted!', color = discord.Color.red())
                await ctx.send(embed = embed)
        else:
            perms = discord.Permissions(send_messages=False, read_messages=True)
            await ctx.guild.create_role(name='Muted', permissions=perms)
            role = discord.utils.get(member.guild.roles,name = 'Muted')
            await member.add_roles(role)
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(role, send_messages=False)
            embed = discord.Embed(title = 'Moderation Tools', description = 'Member muted.', color = discord.Color.green())
            await ctx.send(embed = embed)
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx, limit: int = 1):
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)

def setup(bot):
    bot.add_cog(Moderation(bot))
