from discord.ext import commands, tasks
from main import get_role
from pytimeparse import parse
from asyncio import sleep

class MudaeCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.role = None
    self.claim_time = None

  ## Roll and claim loop
  @commands.command()
  async def ping_mudae(self, ctx, time_to_claim = None, role = None):
    """
    Call command right before Mudae Claim reset. 
    Pings role every 1h and 3h for rolls and claims respectively. 
    Calling ping_mudae again will stop the pings.
    """
    if self.mudae_pings.is_running():
      await self.end_rolls(ctx)
    else:
      await self.start_rolls(ctx, time_to_claim, role)

  async def start_rolls(self, ctx, time_to_claim, role):
    self.ctx = ctx

    if role is not None:
      self.role = get_role(ctx, role)
    if self.role is None:
      await ctx.send('Invalid role')
      return
    
    try:
      seconds_to_claim = parse(time_to_claim)
    except:
      await ctx.send('Invalid time to claim')
      return

    await ctx.send(f'Mudae Pingbot activated: Ping {self.role.mention} every hour for rolls and every 3 hours for claims.')

    #rolls reset every hour, claims every 3 hours. Possibilities:
    #  Claim is 0h (rounded down) away
    #  Claim is 1h (rounded down) away - 1 roll to claim
    #  Claim is 2h (rounded down) away - 2 rolls to claim
    # 1h is 60*60 seconds

    seconds_to_roll = seconds_to_claim % 3600
    self.counter = seconds_to_claim // 3600 #number of rolls to next claim

    await sleep(seconds_to_roll)
    self.mudae_pings.start()
  
  @tasks.loop(hours = 1)
  async def mudae_pings(self):
    if self.counter == 0:
      self.counter = 2
      await self.ctx.send(f'Claim! {self.role.mention}')
    else:
      self.counter -= 1
      await self.ctx.send(f'Roll! {self.role.mention}')

  async def end_rolls(self, ctx):
    await ctx.send('Mudae Pingbot paused.')
    self.mudae_pings.cancel()

def setup(bot):
  bot.add_cog(MudaeCog(bot))