# @author Austin Phillips
# @version 1.0.1
# @date 11/16/24

# to do
# implement most factors listed in design doc
# implement cybersecurity elements so that I can host properly
import discord
from discord.ext import commands
from espn_api.football import League
from datetime import datetime

# globals, replace TOKEN, s2, and swid
TOKEN = 'test'
league_id = 115314928
current_year = datetime.now().year
_espn_s2 = "test"
_swid = "test"
league = League(league_id=league_id, year=current_year, espn_s2 = _espn_s2, swid=_swid)


# housekeeping
intents = discord.Intents.default()
intents.message_content = True  # This is necessary to read message content
bot = commands.Bot(command_prefix='!', intents = intents)

# events and commands
@bot.event
async def on_ready():
    print(f'{bot.user} is dripped out in the chat')

@bot.command(name='status')
async def status(ctx):
    await ctx.send('underconstuction.')

@bot.command(name='score')
async def score(ctx):
    if 'test' in ctx.message.content:
        await ctx.send('success')
    else:
        await ctx.send('failure')

# useful, keeping
@bot.command(name="userinfo")
async def userinfo(ctx):
    # Access attributes of `ctx`
    user_name = ctx.author.name
    user_id = ctx.author.id
    channel_name = ctx.channel.name
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    
    # Send a message with this information
    await ctx.send(f"User: {user_name}\nID: {user_id}\nChannel: {channel_name}\nServer: {guild_name}")

# needs formatting, keeping
@bot.command(name='matchups', help = "Outputs a weeks scoreboard. Specify a week number in the command to return a specific week. Default is current week.")
async def matchups(ctx):
    matchups = league.scoreboard(int(str(ctx.message.content).split(' ')[1]))
    for matchup in matchups:
        if matchup.home_score < matchup.away_score :
            temp = matchup.home_team
            temp_score = matchup.home_score
            matchup.home_team = matchup.away_team
            matchup.home_score = matchup.away_score
            matchup.away_team = temp
            matchup.away_score = temp_score
        await ctx.send(f"{matchup.home_team.team_name} defeats the {matchup.away_team.team_name} {matchup.home_score} to {matchup.away_score}")

# this one is a keep
@bot.command(name='standings', help = "Outputs current standings, along with division, win loss, and PF information.")
async def standings(ctx):
    teams = league.standings()
    index = 1
    mapping = {0 : "West", 1: "East"}
    for team in teams:
        await ctx.send(f"{index}. {team.team_name} - Division: {mapping[team.division_id]} - W/L: {team.wins} - {team.losses} - PF: {team.points_for:.2f}")
        index += 1
        
@bot.command(name='test')
async def test(ctx):
    await ctx.send(str(league.recent_activity(size = 5)))

# Run the bot
bot.run(TOKEN)  
