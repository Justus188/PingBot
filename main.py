## Body
from discord.ext import commands
from asyncio import sleep, gather
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


## Body
@bot.event
async def on_ready():
  ## Read log
  with open('main_active.json', 'r') as f:
    active = json.load(f)

  print(f'Pingbot has loaded as {bot.user} in {[guild.name for guild in bot.guilds]}, loading {len(active)} pending messages')

  ## Trigger logged pending messages
  await gather(*[event_message(k, v) for k, v in active.items()])
  
  print(f'Pingbot: {len(active)} pending messages loaded.')

  bot.load_extension('mudae')

  print('Extensions: ', list(bot.extensions.keys()))
  print('Cogs: ', list(bot.cogs.keys()))

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
  new_entry = {'guild': ctx.guild.id, 'channel': ctx.channel.id, 'role': role.id,
               'utc': (datetime.utcnow() + timedelta(seconds=seconds)).strftime('%y%m%d%H%M%S%f'),
               'event': event}
  event_id = datetime.utcnow().strftime('%y%m%d%H%M%S%f') + str(ctx.guild.id)


  with open('main_active.json', 'r+') as f:
    active = json.load(f)
    active[event_id] = new_entry
    f.seek(0)
    json.dump(active, f)

  ## Verification message and action
  await ctx.send(f'In {str(timedelta(seconds=seconds))} ping @{role} for {event}.')
  await event_message(event_id, new_entry)

async def event_message(event_id, event_dict):
  seconds = (datetime.strptime(event_dict['utc'],'%y%m%d%H%M%S%f') - datetime.utcnow()).total_seconds()
  await sleep(seconds)

  guild = next(i for i in bot.guilds if i.id == event_dict['guild'])
  channel = guild.get_channel(event_dict['channel'])
  role = guild.get_role(event_dict['role'])

  await channel.send(f'{event_dict["event"]}! {role.mention}')

  with open('main_active.json', 'r+') as f:
    active = json.load(f)
    active.pop(event_id)
    
    f.seek(0)
    json.dump(active, f)
    f.truncate()

## Run
if __name__ == '__main__':
  ## Keep the bot active on replit using uptimerrobot
  from keep_alive import keep_alive
  keep_alive()
  
  bot.run(os.environ['token'])