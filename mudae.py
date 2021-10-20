from discord.ext import commands, tasks
from main import get_role
from pytimeparse import parse
from asyncio import sleep, gather
from datetime import timedelta, datetime
import json

class MudaeCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._tasks = {}
    self.counter = {}

    with open('mudae_active.json', 'r') as f:
      active = json.load(f)
    
    print(f'MudaeCog Initialised, loading {len(active)} active guilds.')

    self.bot.loop.create_task(self.load_pending(active))
    print(f'MudaeCog: {[i.name for i in self.bot.guilds if str(i.id) in active.keys()]} running pings.')

  async def load_pending(self, active):
    await gather(*[self.start_rolls(k, v) for k, v in active.items()])

  ## Roll and claim loop
  @commands.command()
  async def ping_mudae(self, ctx, time_to_claim = None, role = None, early_by = 3):
    """
    Pings role every 1h and 3h for rolls and claims respectively, early_by min before reset.
    Calling ping_mudae again will stop the pings; only one channel per discord server / guild is supported.
    """
    with open('mudae_active.json', 'r') as f:
      active = json.load(f)

    guild_id = str(ctx.guild.id)

    ## Stop pings if already running
    if guild_id in active.keys():
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
                'claim_utc': (datetime.utcnow() + timedelta(seconds=seconds_to_claim)).strftime('%y%m%d%H%M%S%f'),
                'early': early_by}
    
    active[guild_id] = new_entry
    with open('mudae_active.json', 'w') as f:
      json.dump(active,f)
    
    await ctx.send(f'Mudae Pingbot activated: Ping @{role} every hour {early_by} min before roll reset and every 3 hours {early_by} min before claim resets.')
    await self.start_rolls(guild_id, new_entry)

  async def start_rolls(self, guild_id, event_dict):
    """Processes JSON-compatible dictionary entry into discord.py task parameters to run self.task_launcher"""
    interval_seconds = 3600
    max_rolls_b4_claim = 2 # includes 0
    
    early_by = event_dict['early']

    seconds_to_claim = (datetime.strptime(event_dict['claim_utc'],'%y%m%d%H%M%S%f') - datetime.utcnow()).total_seconds() - int(early_by)*60
    seconds_to_roll = seconds_to_claim % interval_seconds

    self.counter[guild_id] = seconds_to_claim // interval_seconds # counter = rolls to claim
    if self.counter[guild_id] <0:
      self.counter[guild_id] = self.counter[guild_id] % (max_rolls_b4_claim +1)
    self.counter[guild_id] = int(self.counter[guild_id])
    
    await sleep(seconds_to_roll)

    guild = next(i for i in self.bot.guilds if str(i.id) == guild_id)
    channel = guild.get_channel(event_dict['channel'])
    role = guild.get_role(event_dict['role'])

    self.task_launcher(self.mudae_pings, guild_id, interval_seconds, channel, role, early_by)
  
  def task_launcher(self, f, task_id, interval_seconds, *args):
    """
    Constructs loop task from parameters and saves it to self._tasks.
    Abstraction necessary to run multiple loop instances from one template method (f).
    """
    new_task = tasks.loop(seconds = interval_seconds)(f)
    new_task.start(task_id, *args)
    self._tasks[task_id] = new_task

  async def mudae_pings(self, guild_id, channel, role, early_by):
    """Message logic"""
    if self.counter[guild_id] == 0:
      self.counter[guild_id] = 2
      await channel.send(f'{early_by} min before Claim reset! {role.mention}')
    else:
      await channel.send(f'{early_by} min before Roll reset! {self.counter[guild_id]} roll reset(s) before claim! {role.mention}')
      self.counter[guild_id] -= 1

  async def end_rolls(self, ctx):
    """Terminates mudae_ping loop instance and removes JSON log for guild"""
    await ctx.send('Mudae Pingbot paused.')
    with open('mudae_active.json', 'r+') as f:
      active = json.load(f)
      active.pop(str(ctx.guild.id))

      f.seek(0)
      json.dump(active,f)
      f.truncate()
    self._tasks[str(ctx.guild.id)].cancel()
    self.counter.pop(str(ctx.guild.id))

def setup(bot):
  bot.add_cog(MudaeCog(bot))