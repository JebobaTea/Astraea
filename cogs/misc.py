import os
import discord
import time
import DiscordUtils
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        start_time = time.time()
        embed = discord.Embed(title = 'Pinging...', description = f'Please wait', color = discord.Color.green())
        msg = await ctx.send(embed = embed)
        end_time = time.time()
        new_embed = discord.Embed(title = 'Pong!', description = f'Websocket latency: {round(self.bot.latency * 1000)}ms\nAPI latency: {round((end_time - start_time) * 1000)}ms', color = discord.Color.green())
        await msg.edit(embed = new_embed)
    
    @commands.command()
    async def stats(self, ctx):
        embed = discord.Embed(title = 'Server Stats for ' + ctx.guild.name, description = 'Users: ' + str(ctx.guild.member_count) + '\nChannels: ' + str(len(ctx.guild.channels)), color = discord.Color.green())
        await ctx.send(embed = embed)
    
    @commands.command()
    async def help(self, ctx):
        embed1 = discord.Embed(title = 'Help Menu', color = discord.Color.green()).add_field(name = '⚙️ **Misc**', value = '+help\n+ping\n+stats\n+userinfo [<user>]\n+avatar [<user>]', inline = False)
        embed2 = discord.Embed(title = 'Help Menu', color = discord.Color.green()).add_field(name = '🎫 **Tickets**', value = '+closeticket\n+newticket\n+renameticket <string>', inline = False)
        embed3 = discord.Embed(title = 'Help Menu', color = discord.Color.green()).add_field(name = '🔨 **Moderation**', value = '+kick <member>\n+ban <member>\n+mute <member>\n+unmute <member>\n+purge [<int>]', inline = False)
        embed4 = discord.Embed(title = 'Help Menu', color = discord.Color.green()).add_field(name = '🎉 **Fun**', value = '+reddit <string>\n+coinflip\n+8ball <string>\n+hug <member>\n+kill <member>\n+shoot <member>\n+kiss <member>\n+punch <member>\n+trivia', inline = True)
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions = True)
        paginator.add_reaction('⏮️', 'first')
        paginator.add_reaction('⏪', 'back')
        paginator.add_reaction('⏩', 'next')
        paginator.add_reaction('⏭️', 'last')
        embeds = [embed1, embed2, embed3, embed4]
        await paginator.run(embeds)
    
    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author      
        date_format = '%a, %d %b %Y %I:%M %p'
        embed = discord.Embed(color = discord.Color.green(), description = user.mention)
        embed.set_author(name = str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url = user.avatar_url)
        embed.add_field(name = 'Joined', value = user.joined_at.strftime(date_format))
        embed.add_field(name = 'Registered', value = user.created_at.strftime(date_format))
        embed.set_footer(text = 'ID: ' + str(user.id))
        return await ctx.send(embed = embed)
    
    @commands.command()
    async def avatar(self, ctx, *,  member: discord.Member = None):
        if member is None:
            member = ctx.author
        userAvatarUrl = member.avatar_url
        await ctx.send(userAvatarUrl)

def setup(bot):
    bot.add_cog(Misc(bot))
