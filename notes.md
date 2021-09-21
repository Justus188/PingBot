https://discordpy.readthedocs.io/en/stable/api.html
https://discordpy.readthedocs.io/en/stable/ext/commands/api.html

https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
https://realpython.com/how-to-make-a-discord-bot-python/

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

Learning Points:
* Learning about discord py and ascyncio
* Modularization and extensions

Todo:
* Hosting and downtime
  * Troubleshooting to identify problem
  * Possible solutions:
    * Save data / request log to file, read on initialization
      * Consideration: Hosted in github / replit (public)
      * Sensitive data?
    * Find a better hosting service
* Input parsing for discord commands
  * Input flexibility vs implementation difficulty?
  * Context: Personal / Friend Usage, all friends familiar with programming
    * Lean towards ease of implementation for MVP
  * Explore: NLP packages for more flexibility
    * https://dateparser.readthedocs.io/en/latest/
    * Named Entity Recognition to extract more flexibily: https://spacy.io/usage/linguistic-features#section-named-entities