import os
import discord
import random
import asyncio
import requests
import asyncpraw
from discord.ext import commands
from aiohttp import ClientSession
from typing import Union
from trivia import trivia


session = ClientSession(trust_env=True)
reddit = asyncpraw.Reddit(client_id='ID',client_secret='SECRET', password='PW',user_agent='AGENT', username='USERNAME')


def kawaii(sub): 
    r = requests.get(f'https://kawaii.red/api/gif/{sub}/token=TOKEN')
    return str(r.json()['response'])


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

  
    @commands.command()
    async def reddit(self,ctx,*,arg):
        em = discord.Embed(title = 'Loading', description = 'Fetching your post from the API...', color = discord.Color.green())
        msg = await ctx.send(embed = em)
        subreddit = await reddit.subreddit(arg)
        all_subs = []
        hot = subreddit.hot(limit = 100)
        async for submission in hot:
          all_subs.append(submission)
        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url
        content = random_sub.selftext
        em = discord.Embed(title = name, description = content, color = discord.Color.green())
        em.set_image(url = url)
        await msg.edit(embed = em)

  
    @commands.command()
    async def hug(self, ctx,*,arg: discord.Member):
        em = discord.Embed(title = 'Hugged '+str(arg),color = discord.Color.green())
        em.set_image(url=kawaii('hug'))
        await ctx.send(embed=em)


    @commands.command()
    async def kill(self, ctx,*,arg: discord.Member):
        em = discord.Embed(title = 'Killed '+str(arg),color = discord.Color.green())
        em.set_image(url=kawaii('kill'))
        await ctx.send(embed=em)


    @commands.command()
    async def shoot(self, ctx,*,arg: discord.Member):
        em = discord.Embed(title = 'Shot '+str(arg),color = discord.Color.green())
        em.set_image(url=kawaii('shoot'))
        await ctx.send(embed=em)

  
    @commands.command()
    async def kiss(self, ctx,*,arg: discord.Member):
        em = discord.Embed(title = 'Kissed '+str(arg),color = discord.Color.green())
        em.set_image(url=kawaii('kiss'))
        await ctx.send(embed=em)

  
    @commands.command()
    async def boop(self, ctx,*,arg: discord.Member):
        em = discord.Embed(title = 'Booped '+str(arg),color = discord.Color.green())
        em.set_image(url=kawaii('boop'))
        await ctx.send(embed=em)

  
    @commands.command()
    async def punch(self, ctx,*,arg: discord.Member):
        em = discord.Embed(title = 'Punched '+str(arg),color = discord.Color.green())
        em.set_image(url=kawaii('punch'))
        await ctx.send(embed=em)

  
    @commands.command()
    async def coinflip(self,ctx):
        em = discord.Embed(title = '🪙 Coinflip', description = 'Coin landed...', color = discord.Color.green())
        msg = await ctx.send(embed=em)
        await asyncio.sleep(1)
        results = ['heads', 'tails']
        em = discord.Embed(title = '🪙 Coinflip', description = 'Coin landed... '+random.choice(results)+' up', color = discord.Color.green())
        await msg.edit(embed=em)

  
    @commands.command(aliases=['8ball','ball','eightball','magic8ball','magiceightball'])
    async def magicball(self,ctx,*,arg):
        em = discord.Embed(title = 'Magic 8-Ball', description = 'Thinking...', color = discord.Color.green())
        msg = await ctx.send(embed=em)
        await asyncio.sleep(1)
        results = ['It is certain.','It is decidedly so.','Without a doubt.','Yes, definitely.','You may rely on it.','As I see it, yes.','Yes.','Most likely.','Outlook good.','Signs point to yes.','Reply hazy, try again.','Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.','Don\'t count on it.','My reply is no.','My sources say no.','Outlook not so good.','Very doubtful.']
        em = discord.Embed(title = 'Magic 8-Ball', description = random.choice(results), color = discord.Color.green())
        await msg.edit(embed=em)

  
    @commands.command()
    async def trivia(self,ctx):
      question = await trivia.question(amount=1, quizType='multiple')
      answers = question[0].get('incorrect_answers')
      answers.append(question[0].get('correct_answer'))
      random.shuffle(answers)
      em = discord.Embed(title = question[0].get('question'), description = 'Category: '+question[0].get('category'), color = discord.Color.green())
      for i in answers:
        em.add_field(name=answers.index(i)+1, value=i, inline=False)
      embed = await ctx.send(embed=em)
      await embed.add_reaction('1️⃣')
      await embed.add_reaction('2️⃣')
      await embed.add_reaction('3️⃣')
      await embed.add_reaction('4️⃣')
      def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):
          return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and \
                str(r.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
      try:
          reaction, user = await self.bot.wait_for(event = 'reaction_add', check = check, timeout = 20.0)
      except asyncio.TimeoutError:
          a = answers.index(question[0].get('correct_answer')) + 1
          new_embed = discord.Embed(title = 'Time\'s up! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
          await embed.edit(embed=new_embed)
          return
      else:
          a = answers.index(question[0].get('correct_answer')) + 1
          if str(reaction.emoji) == '1️⃣':
              if a == 1:
                  new_embed = discord.Embed(title = 'That\'s right! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
                  await embed.edit(embed=new_embed)
              else:
                  new_embed = discord.Embed(title = 'Not quite! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
                  await embed.edit(embed=new_embed)
          if str(reaction.emoji) == '2️⃣':
              if a == 2:
                  new_embed = discord.Embed(title = 'That\'s right! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
                  await embed.edit(embed=new_embed)
              else:
                  new_embed = discord.Embed(title = 'Not quite! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
                  await embed.edit(embed=new_embed)
          if str(reaction.emoji) == '3️⃣':
              if a == 3:
                  new_embed = discord.Embed(title = 'That\'s right! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
                  await embed.edit(embed=new_embed)
              else:
                  new_embed = discord.Embed(title = 'Not quite! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
                  await embed.edit(embed=new_embed)
          if str(reaction.emoji) == '4️⃣':
              if a == 4:
                  new_embed = discord.Embed(title = 'That\'s right! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
                  await embed.edit(embed=new_embed)
              else:
                  new_embed = discord.Embed(title = 'Not quite! The correct answer was...', description = '['+str(a)+'] '+question[0].get('correct_answer'), color = discord.Color.green())
                  await embed.edit(embed=new_embed)
        

def setup(bot):
    bot.add_cog(Fun(bot))
