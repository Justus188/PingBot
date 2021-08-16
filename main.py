## Logging
import logging

logging.basicConfig(level=logging.INFO)

## Body
import discord
from discord.ext import commands
from asyncio import sleep
import datetime
from pytimeparse import parse
import os

bot = commands.Bot(command_prefix='.')

# https://discord.com/api/oauth2/authorize?client_id=876459480768999444&permissions=206912&scope=bot

@bot.event
async def on_ready():
  print('Pingbot has loaded as {0.user}'.format(bot))

@bot.command()
async def event(ctx, timeto, role, *, event):
  ## Check for valid timeto and convert to seconds
  try:
    seconds = parse(timeto)
    # https://github.com/wroberts/pytimeparse
  except:
    await ctx.send('Invalid delay')
    return

  ## Check for valid role and get role object
  for Role in ctx.guild.roles:
    if role == Role.name:
      role = Role
  
  if isinstance(role, str):
    await ctx.send('Role not found')
    return

  ## Verify Request
  await ctx.send(f'In {str(datetime.timedelta(seconds=seconds))} ping @{role} for {event}.')

  ## Wait and Send Reminder
  await sleep(seconds)
  await ctx.send(f'{event}! {role.mention}')

## Keep the bot active on replit using uptimerrobot
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
# https://uptimerobot.com/dashboard#mainDashboard
from keep_alive import keep_alive
keep_alive()

## Run
bot.run(os.environ['token'])