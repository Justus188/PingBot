## Body
from discord.ext import commands
from asyncio import sleep
from datetime import timedelta, datetime
from pytimeparse import parse
import os
import json

bot = commands.Bot(command_prefix='.')

## Helpers
def get_role(ctx, role):
  """Check guild in ctx for rolename and returns role object, return None if not found."""
  for Role in ctx.guild.roles:
    if role == Role.name:
      return Role
  
  return None

def active_append(filename, content):
  """Opens json list and appends content to the list."""
  with open(filename, 'r+') as f:
    active = json.load(f)
    active.append(content)
    f.seek(0)
    json.dump(active, f)

def active_remove(filename, content_id):
  """Opens json list and removes entry with id = content_id from list."""
  with open(filename, 'r+') as f:
    active = json.load(f)
    active = list(filter(lambda i: i['id'] != content_id, active))
    
    f.seek(0)
    json.dump(active, f)
    f.truncate()


## Body
@bot.event
async def on_ready():
  ## Read log
  with open('main_active.json', 'r') as f:
    active = json.load(f)

  print(f'Pingbot has loaded as {bot.user} in {[guild.name for guild in bot.guilds]}, currently pending {len(active)} messages')

  ## Trigger logged pending messages
  for entry in active:
    await event_message(entry)

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

  ## Log to json
  new_entry = {'id': datetime.utcnow().strftime('%y%m%d%H%M%S%f'),
               'guild': ctx.guild.id, 'channel': ctx.channel.id, 'role': role.id,
               'utc': (datetime.utcnow() + timedelta(seconds=seconds)).strftime('%y%m%d%H%M%S%f'),
               'event': event}
  
  active_append('main_active.json', new_entry)

  ## Verification message and action
  await ctx.send(f'In {str(timedelta(seconds=seconds))} ping @{role} for {event}.')
  await event_message(new_entry)

async def event_message(event_dict):
  seconds = (datetime.strptime(event_dict['utc'],'%y%m%d%H%M%S%f') - datetime.utcnow()).total_seconds()
  await sleep(seconds)

  guild = next(i for i in bot.guilds if i.id == event_dict['guild'])
  channel = guild.get_channel(event_dict['channel'])
  role = guild.get_role(event_dict['role'])

  await channel.send(f'{event_dict["event"]}! {role.mention}')
  active_remove('main_active.json', event_dict['id'])


## Run
if __name__ == '__main__':
  ## Keep the bot active on replit using uptimerrobot
  from keep_alive import keep_alive
  keep_alive()
  
  bot.load_extension('mudae')

  print('Extensions: ', bot.extensions.keys())
  print('Cogs: ', bot.cogs.keys())

  bot.run(os.environ['token'])