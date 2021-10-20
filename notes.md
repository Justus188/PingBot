Link: https://replit.com/@Justus188/PingBot

Learning Points:
* Learning about discord.py and asyncio
* Modularization and extensions
* Reading and writing to NoSQL
* Useing pipreqs to create requirements.txt

Areas for improvement:
* Hosting and downtime
  * Troubleshooting
  * Consider whether data is sensitive
  * Find a better hosting service
* Input parsing for discord commands
  * Input flexibility vs implementation difficulty?
  * Context: Personal / Friend Usage, all friends familiar with programming
    * Lean towards ease of implementation for MVP
  * Explore: NLP packages for more flexibility
    * https://dateparser.readthedocs.io/en/latest/
    * Named Entity Recognition to extract more flexibily: https://spacy.io/usage/linguistic-features#section-named-entities

References:  
https://discordpy.readthedocs.io/en/stable/api.html  
https://discordpy.readthedocs.io/en/stable/ext/commands/api.html

https://www.freecodecamp.org/news/create-a-discord-bot-with-python/  
https://realpython.com/how-to-make-a-discord-bot-python/

mudae_cog Notes:  
Rolls reset every hour, claims every 3 hours. Possibilities:
* Claim is 0h (rounded down) away
* Claim is 1h (rounded down) away - 1 roll to claim
* Claim is 2h (rounded down) away - 2 rolls to claim
* 1h is 60*60 seconds
With the downtime workaround, logic needs to include -ves
* // rounds negatives down
* -3 - less than 3h ago, next one is claim; -3 % 3 = 0
* -2 - less than 2h ago, 1 rolls to claim;  -2 % 3 = 1
* -1 - less than 1h ago, just after claim = 2 rolls to claim; -1 % 3 = 2

``` Alternate get_role
def get_role(ctx, role):
  try: 
    return next(i for i in ctx.guild.roles if i.name == role)
  except StopIteration:
    return None
```

``` Pipreqs
pip install pipreqs
pipreqs
```

``` Logger code block
import logging

logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)
```

``` Command syntax
@bot.command()
async def event(ctx, *args):
  await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
```

``` On member join syntax
@bot.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
      f'Hi {member.name}, welcome to my Discord server!'
  )
```