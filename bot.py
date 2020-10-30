from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from models import *

load_dotenv()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Logged in as {0}'.format(bot.user.name))
    print('With the ID: {0}'.format(bot.user.id))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        await ctx.channel.send("{0} You do not have permission to use that command.".format(ctx.author.mention))


@bot.event
async def on_member_join(member):
    print("User {0.display_name} joined {0.guild}".format(member))
    current_rules = Rules.select(Rules.rule_text).order_by(Rules.created.desc()).get()
    citizen = discord.utils.get(member.guild.roles, name="member")

    # DM user with rules
    await member.send("Hello {0.mention}, welcome to {0.guild}\n Rules:".format(member))
    await member.send(current_rules.rule_text)
    await member.send("Type **!agree** to confirm you have read and agree to the rules")

    def check(m):
        return m.content.upper() == '!agree'.upper()

    response = await bot.wait_for('message', check=check)
    print("{0.display_name} has accepted the rules".format(member))
    await member.add_roles(citizen)


@bot.command(help="Display rules of the LSK Discord server", brief="Display rules of the LSK Discord server")
async def rules(ctx):
    current_rules = Rules.select(Rules.rule_text).order_by(Rules.created.desc()).get()
    await ctx.channel.send(current_rules.rule_text)


@bot.command(
    help="Set the Discord server rules by typing the rules (formatted as desired) after the command",
    brief="Sets the rules"
)
@commands.has_role("@admin")
async def setrules(ctx, *, message):
    new_rule = Rules(rule_text=message, user=ctx.author.id)
    new_rule.save()
    await ctx.channel.send("Rules are now set as: \n" + new_rule.rule_text)


bot.run(os.getenv("BOT_TOKEN"))

