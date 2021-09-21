## Body
from discord.ext import commands
from asyncio import sleep
from datetime import timedelta, datetime
from pytimeparse import parse
import os
import json

bot = commands.Bot(command_prefix='.')

def get_role(ctx, role):
  """Check guild in ctx for rolename and returns role object, return None if not found."""
  for Role in ctx.guild.roles:
    if role == Role.name:
      return Role
  
  return None

def active_append(filename, content):
  with open(filename, 'r+') as f:
    active = json.load(f)
    active.append(content)
    f.seek(0)
    json.dump(active, f)

@bot.event
async def on_ready():
  with open('main_active.json', 'r') as f:
    active = json.load(f)

  ## Activate active
  for entry in active:
    await event_message(entry)

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

  ## Verification Message
  await ctx.send(f'In {str(timedelta(seconds=seconds))} ping @{role} for {event}.')

  ## TODO: Write to json
  id = datetime.strftime(datetime.utcnow())
  write = {'id': id,
           'guild': ctx.guild.id, 'channel': ctx.channel.id, 'role': role.id,
           'utc': datetime.strftime(datetime.utcnow() + timedelta(seconds=seconds)),
           'event': event}
  
  with open('main_active.json', 'r+') as f:
    active = json.load(f)
    active.append(write)
    f.seek(0)
    json.dump(active, f)

  await event_message(write)

async def event_message(event_dict):
  seconds = event_dict['utc'] - datetime.utcnow()).total_seconds()
  await sleep(seconds)

  guild = next(i for i in bot.guilds if i.id == event_dict['guild'])
  channel = guild.get_channel(event_dict['channel'])
  role = guild.get_role(event_dict['role'])

  await channel.send(f'{event_dict["event"]}! {role.mention}')

  with open('main_active.json', 'r+') as f:
    active = json.load(f)
    active = list(filter(lambda i: i['id'] != event_dict['id'], active))
    f.seek(0)
    json.dump(active, f)


## Run
if __name__ == '__main__':
  ## Keep the bot active on replit using uptimerrobot
  from keep_alive import keep_alive
  keep_alive()
  
  bot.load_extension('mudae')

  print('Extensions: ', bot.extensions.keys())
  print('Cogs: ', bot.cogs.keys())

  bot.run(os.environ['token'])