## Logging
#import logging

#logging.basicConfig(level=logging.INFO)

## Body
from discord.ext import commands
from asyncio import sleep
from datetime import timedelta
from pytimeparse import parse
import os

bot = commands.Bot(command_prefix='.')

def get_role(ctx, role):
  """Check guild in ctx for rolename and returns role object, return None if not found."""
  for Role in ctx.guild.roles:
    if role == Role.name:
      return Role
  
  return None

@bot.event
async def on_ready():
  print(f'Pingbot has loaded as {bot.user} in {[guild.name for guild in bot.guilds]}')

@bot.command()
async def event(ctx, timeto, role, *, event):
  """"Pings role after set amount of time."""
  
  ## Check for valid timeto and convert to seconds
  try:
    seconds = parse(timeto)
  except:
    await ctx.send('Invalid delay')
    return

  ## Check for valid role and get role object
  role = get_role(ctx, role)
  if role is None:
    await ctx.send('Role not found')
    return

  ## Verify Request
  await ctx.send(f'In {str(timedelta(seconds=seconds))} ping @{role} for {event}.')

  ## Wait and Send Reminder
  await sleep(seconds)
  await ctx.send(f'{event}! {role.mention}')

## Run
if __name__ == '__main__':
  ## Keep the bot active on replit using uptimerrobot
  from keep_alive import keep_alive
  keep_alive()
  
  bot.load_extension('mudae')

  print('Extensions: ', bot.extensions.keys())
  print('Cogs: ', bot.cogs.keys())

  bot.run(os.environ['token'])