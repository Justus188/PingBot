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

