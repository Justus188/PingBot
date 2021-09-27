# Pingbot

A no frills discord bot to automate reminders on a private discord server, because available alternatives were too elaborate and required too much work to set up simple event pings for game sessions.

While it has not been designed for general use, if you wish to add this bot to your server use this link: https://discord.com/api/oauth2/authorize?client_id=876459480768999444&permissions=206912&scope=bot

### Hosting
It is hosted on https://replit.com/ using https://uptimerobot.com/ in a trick documented here: https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
* Not 100% uptime and functionality breaks when it goes down. Fix in progress.

For easy reference, Uptimerobot dashboard can be accessed here: https://uptimerobot.com/dashboard#mainDashboard

### Current commands
.event (time to event) (role name) (event)  
* Will ping role after the time period specified for event.  
  * Time to event is parsed using Will Roberts' pytimeparse (https://github.com/wroberts/pytimeparse), so it's pretty flexible as long as there is no whitespace.  
  * Name of role is without the @.  
  * Event name allows whitespace.
* Example: .event 1h20m dwarves Deep Rock Galactic time  
Pings @dwarves in 1h20min for Deep Rock Galactic time!

### Extensions
#### Mudae  
.ping_mudae (time to next claim) (role name)
* Intended for reminders for the gatcha bot Mudae
* Pings role every 1h for rolls and 3h for claims in the channel it is called.
* Time to claim is parsed using Will Roberts' pytimeparse (https://github.com/wroberts/pytimeparse), so it's pretty flexible as long as there is no whitespace.