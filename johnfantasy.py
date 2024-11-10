# @author Austin Phillips
# @version 1.0.0
# @date 11/9/24

import discord
from discord.ext import commands
from espn_api.football import League
from datetime import datetime

# globals
TOKEN = 'insert token here'
league_id = 115314928
current_year = datetime.now().year

league = League(league_id=league_id, year=current_year)


# housekeeping
intents = discord.Intents.default()
intents.message_content = True  # This is necessary to read message content
bot = commands.Bot(command_prefix='!', intents = intents)

# events and commands
@bot.event
async def on_ready():
    print(f'{bot.user} is dripped out in the chat')

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('the hell is up')

@bot.command(name='score')
async def score(ctx):
    if 'test' in ctx.message.content:
        await ctx.send('success')
    else:
        await ctx.send('failure')

#@bot.command(name="userinfo")
#async def userinfo(ctx):
    # Access attributes of `ctx`
    #user_name = ctx.author.name
    #user_id = ctx.author.id
    #channel_name = ctx.channel.name
    #guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    
    # Send a message with this information
    #await ctx.send(f"User: {user_name}\nID: {user_id}\nChannel: {channel_name}\nServer: {guild_name}")

@bot.command(name='matchups')
async def matchups(ctx):
    matchups = league.scoreboard()
    for matchup in matchups:
        await ctx.send(f"{matchup.home_team} {matchup.home_score} - {matchup.away_score} {matchup.away_team}")
        

# Run the bot
bot.run(TOKEN)  
