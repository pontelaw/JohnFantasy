# @author Austin Phillips
# @version 1.0.3
# @date 09/10/2025

# to do
# implement most factors listed in design doc
# implement cybersecurity elements so that I can host properly
import discord
from discord.ext import commands
from espn_api.football import League, Player
from datetime import datetime

# globals, replace TOKEN, s2, and swid
TOKEN = 'test'
league_id = 115314928
current_year = datetime.now().year
_espn_s2 = "AECLu1g6yJmy3jl1upKaXUwfFOlFJIt1oAWmWsK7V3ZIxqoN3oS0ITfnw%2Fj1%2B9SWAeBbiDcJwxxDpAJiBjjwWkhH4CtUVpF3BbWn6KzM58x%2BZDxt1j5ODy3pFus07bbXh11I9%2FpjHbzZLL6rqFPfOqfZZH0CJ0d6alwuAxzdcYaJihxD9CHHkVy5%2Bf7DYHSE2owAHw2vhDhmZsMKCCk7%2F7fGw4ipddmpHUfLJZ92QLk7p4PK81RGA0Sbp4TNJos06sxXyNNySoWKL1ItJizSbMHaUvBJAISooJEz288AKcWyqaJo75sZhALz%2FAmg5BefitSJEnCqK8ZHGbXrouJZ4X3Y"
_swid = "{E770BC94-0E7D-4E94-98C0-8BF734D83243}"
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

# get and return standings, division, w/l and PF. Ordered by current standings
@bot.command(name='standings', help = "Outputs current standings, along with division, win loss, and PF information.")
async def standings(ctx):
    teams = league.standings()
    index = 1
    mapping = {0 : "West", 1: "East"}
    for team in teams:
        await ctx.send(f"{index}. {team.team_name} - Division: {mapping[team.division_id]} - W/L: {team.wins} - {team.losses} - PF: {team.points_for:.2f}")
        index += 1

# get and return the last n activity messages (trade, FA pickup, waivers, drops, etc.)      
@bot.command(name='recent')
async def recent(ctx):
    size = int(str(ctx.message.content).split(" ")[1])
    if size > 10:
        await ctx.send("Don't overwhelm the bot, max return for this command is 10")
        return
    activity = league.recent_activity(size)
    for a in activity:
        if len(a.actions) == 2:
            if a.actions[0][1] == "TRADED":
                await ctx.send(f"The {a.actions[0][0].team_name} {a.actions[0][1]} {a.actions[0][2].name} to The {a.actions[1][0].team_name} and RECEIVED {a.actions[1][2].name}\n")   
            else:
                await ctx.send(f"The {a.actions[0][0].team_name} {a.actions[0][1]} {a.actions[0][2].name} and {a.actions[1][1]} {a.actions[1][2].name}\n")
        elif len(a.actions) == 1:
            await ctx.send(f"The {a.actions[0][0].team_name} {a.actions[0][1]} {a.actions[0][2].name}\n")
        elif len(a.actions) == 3:
            await ctx.send(f"The {a.actions[0][0].team_name} {a.actions[0][1]} {a.actions[0][2].name} and {a.actions[1][2].name} to The {a.actions[2][0].team_name} and RECEIVED {a.actions[2][2].name}\n")
        elif len(a.actions) == 4:
            await ctx.send(f"The {a.actions[0][0].team_name} {a.actions[0][1]} {a.actions[0][2].name} and {a.actions[1][2].name} to The {a.actions[2][0].team_name} and RECEIVED {a.actions[2][2].name} and {a.actions[3][2].name}\n")
        else:
            await ctx.send("Not implemented for this activity type")

@bot.command(name='boxscores')
async def boxscores(ctx):
    await ctx.send(str(league.power_rankings(int(str(ctx.message.content).split(" ")[1]))))
            
import spacy
#nlp = spacy.load("en_core_web_sm")


async def player_report(ctx, name: str):
    player = league.player_info(name=name)
    if player is None:
        await ctx.send(f"Player: {name} not found, make sure to use full name and correct spelling\n")
    else:  
        strog = (
            f"{player.name}\n"
            f"is rank: {player.posRank} at: {player.position}\n"
            f"is: {player.injuryStatus}\n"
            f"is currently scoring: {player.avg_points} points per game.\n"
            f"is projected: {player.projected_avg_points} points per game going forward.\n"
        )
        await ctx.send(strog)


@bot.command(name='playerReport', help="Outputs basic player info. Usage: !playerReport <First Name> <Last Name>")
async def player(ctx):
    name = f"{ctx.message.content.split()[1]} {ctx.message.content.split()[2]}"
    await player_report(ctx, name)


@bot.command(name='ner')
async def boxscores(ctx):
    doc = nlp(str(ctx.message.content))
    for entity in doc.ents:
        await ctx.send(f"{entity.text}: {entity.label_}")
        if entity.label_ == "PERSON":
            await player_report(ctx, str(entity.text))  # ✅ await the helper
# Run the bot
bot.run(TOKEN)  
