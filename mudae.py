from discord.ext import commands, tasks
from main import get_role
from pytimeparse import parse
from asyncio import sleep
from datetime import timedelta, datetime
import json

class MudaeCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._tasks = {}

    with open('mudae_active.json', 'r') as f:
      active = json.load(f)
    
    print(f'MudaeCog Initialised, loading {len(active)} active guilds.')

    self.bot.loop.create_task(self.load_pending(active))
    print(f'MudaeCog: {len(active)} active guilds loaded')

  async def load_pending(self, active):
    for guild_id, dictionary in active.items():
      await self.start_rolls(guild_id, dictionary)

  ## Roll and claim loop
  @commands.command()
  async def ping_mudae(self, ctx, time_to_claim = None, role = None):
    """
    Pings role every 1h and 3h for rolls and claims respectively. 
    Calling ping_mudae again will stop the pings; only one channel per discord server / guild.
    """
    with open('mudae_active.json', 'r') as f:
      active = json.load(f)

    # stop pings logic
    if ctx.guild.id in active.keys():
      await self.end_rolls(ctx)
      return

    ## Input validation
    role = get_role(ctx, role)
    if role is None:
      await ctx.send('Invalid role')
      return
    
    try:
      seconds_to_claim = parse(time_to_claim)
    except:
      await ctx.send('Invalid time to claim')
      return
    
    ## Log to json
    new_entry = {'channel': ctx.channel.id, 'role': role.id, 
                'claim_utc': (datetime.utcnow() + timedelta(seconds=seconds_to_claim)).strftime('%y%m%d%H%M%S%f')}

    active[ctx.guild.id] = new_entry
    with open('mudae_active.json', 'w') as f:
      json.dump(active,f)
    
    await ctx.send(f'Mudae Pingbot activated: Ping @{role} every hour for rolls and every 3 hours for claims.')
    await self.start_rolls(ctx.guild.id, new_entry)

  async def start_rolls(self, guild_id, event_dict):
    guild = next(i for i in self.bot.guilds if i.id == int(guild_id))
    channel = guild.get_channel(event_dict['channel'])
    role = guild.get_role(event_dict['role'])

    seconds_to_claim = (datetime.strptime(event_dict['claim_utc'],'%y%m%d%H%M%S%f') - datetime.utcnow()).total_seconds()
    seconds_to_roll = seconds_to_claim % 3600
    counter = seconds_to_claim // 3600 #number of rolls to next claim
    if counter <0:
      counter = counter % 3

    print('start_rolls run |', seconds_to_roll)
    
    await sleep(seconds_to_roll)
    self.task_launcher(guild_id, channel, role, counter)
  
  def task_launcher(self, task_id, *args):
    print("Task launcher run")
    new_task = tasks.loop(hours = 1)(self.mudae_pings)
    new_task.start(*args)
    self._tasks[task_id] = new_task

  async def mudae_pings(self, channel, role, counter):
    print('mudae_pings run |', channel, '|', role, '|', counter)
    if counter == 0:
      counter = 2
      await channel.send(f'Claim! {role.mention}')
    else:
      counter -= 1
      await channel.send(f'Roll! {role.mention}')

  async def end_rolls(self, ctx):
    await ctx.send('Mudae Pingbot paused.')
    with open('mudae_active.json', 'r+') as f:
      active = json.load(f)
      active.pop(ctx.guild.id)

      f.seek(0)
      json.dump(active,f)
      f.truncate()
    self._tasks[ctx.guild.id].cancel()

def setup(bot):
  bot.add_cog(MudaeCog(bot))