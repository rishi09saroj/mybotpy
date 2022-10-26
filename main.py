import discord
from discord.ext import commands
import random
import asyncio

import datetime
client = commands.Bot(command_prefix="+")



# Mute command
@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member : discord.Member, *, reason='No reason provided'):
  print("a")
  role = discord.utils.get(ctx.guild.roles, name="Muted")
  if member == ctx.author:
    await ctx.send("You can't mute yourself!")

    
  elif role not in ctx.guild.roles:
    await ctx.send("create muted role please")

  
  
  else:
    print("a")
    await member.add_roles(role)
    embed = discord.Embed(title="Muted.", description=f"**{ctx.author}** has muted **{member}** \nReason: `{reason}`", color = discord.Colour.red())
    await ctx.send(embed=embed)

# Mute error handling
@mute.error
async def mute_error(ctx, error):
  if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=f"Failed.", description=f"Member could not be found.", colour = discord.Colour.red())
        await ctx.send(embed=embed)

# Kick command
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason = None):
  
  # Message sent when reason is not given
  if reason == None:
    reason = "No reason provided."

  # If message is directed to self
  if member == ctx.author:
    await ctx.send("You can't kick yourself!")

  # If user checks pass
  else:
    await member.kick(reason=reason)
    embed = discord.Embed(title="Kicked.", description=f"**{ctx.author}** has kicked **{member}** \nReason: `{reason}`", colour = discord.Colour.red())
    await ctx.send(embed=embed)

# Kick error handling
@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=f"Failed.", description=f"Member could not be found.", colour = discord.Colour.red())
        await ctx.send(embed=embed)

# Ban command
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason = None):
  if reason == None:
    reason = "No reason provided."
  if member == ctx.author:
    await ctx.send("You can't ban yourself!")

  else:
    await member.ban(reason=reason)
    embed = discord.Embed(title="Banned.", description=f"**{ctx.author}** has banned **{member}** \nReason: `{reason}`", colour = discord.Colour.red())
    await ctx.send(embed=embed)

# Ban error handling
@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=f"Failed.", description=f"Member could not be found.", colour = discord.Colour.red())
        await ctx.send(embed=embed)

# Unban command
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, member : int):
  mem = await client.fetch_user(member)
  await ctx.guild.unban(discord.Object(id=member))
  embed = discord.Embed(title="Unbanned.", description=f"Succesfully unbanned **{mem}**.", color = discord.Colour.green())
  await ctx.send(embed=embed)

# Unban error handling
@unban.error
async def unban_error(ctx, error):
  if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=f"Failed.", description=f"Your id contained letters.", colour = discord.Colour.red())
        await ctx.send(embed=embed)


  # Unmute command
@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member : discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Muted")
  if ctx.author == member:
    await ctx.send("You can't unmute yourself.")
  elif role not in member.roles:
    await ctx.send("That member wasn't muted in the first place.")
  else:
    await member.remove_roles(role)
    embed = discord.Embed(title=f"Unmuted.", description=f"**{member}** was succesfully unmuted.", colour = discord.Colour.green())
    await ctx.send(embed=embed)

# Unmute error handling
@unmute.error
async def unmute_error(ctx, error):
  if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=f"Failed.", description=f"Member could not be found.", colour = discord.Colour.red())
        await ctx.send(embed=embed)

def convert(time):
	pos = ["s", "m", "h", "d"]

	time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

	unit = time[-1]

	if unit not in pos:
		return[-1]
	try:
		val = int(time[:-1])
	except:
		return -2

	return val * time_dict[unit]

@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
	# Giveaway command requires the user to have permissions to function properly

	# Stores the questions that the bot will ask the user to answer in the channel that the command was made
	# Stores the answers for those questions in a different list
	giveaway_questions = ['Which channel will I host the giveaway in?', 'What is the prize?',
						  'How long should the giveaway run for (s|m|h|d)?', ]
	giveaway_answers = []

	# Checking to be sure the author is the one who answered and in which channel
	def check(m):
		return m.author == ctx.author and m.channel == ctx.channel

	# Askes the questions from the giveaway_questions list 1 by 1
	# Times out if the host doesn't answer within 30 seconds
	for question in giveaway_questions:
		await ctx.send(question)
		try:
			message = await client.wait_for('message', timeout=30.0, check=check)
		except asyncio.TimeoutError:
			await ctx.send(
				'You didn\'t answer in time.  Please try again and be sure to send your answer within 30 seconds of the question.')
			return
		else:
			giveaway_answers.append(message.content)

	# Grabbing the channel id from the giveaway_questions list and formatting is properly
	# Displays an exception message if the host fails to mention the channel correctly
	try:
		c_id = int(giveaway_answers[0][2:-1])
	except:
		await ctx.send(f'You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}')
		return

	# Storing the variables needed to run the rest of the commands
	channel = client.get_channel(c_id)
	prize = str(giveaway_answers[1])
	time = convert(giveaway_answers[2])
	if time == -1:
		await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d)")
		return
	elif time == -2: 
		await ctx.send(f"The time must be an integer. Please enter an integer")
		return

	# Sends a message to let the host know that the giveaway was started properly
	async def message(ctx, user:discord.Member, *, message=None):
		await ctx.send(
		f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {giveaway_answers[2]}')

	# Giveaway embed message
	give = discord.Embed(color=discord.Color.orange())
	give.set_author(name=f'Giveaway!', icon_url='https://i.imgur.com/VaX0pfM.png')
	give.add_field(name=f'Prize: {prize}!',
				   value=f'React with 🎉 to enter!\n Ends in {round(time / 60, 2)} minutes!', inline=False)
	end = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
	give.set_footer(text=f'Giveaway ends at {end} UTC!')
	my_message = await channel.send(embed=give)

	# Reacts to the message
	await my_message.add_reaction("🎉")
	await asyncio.sleep(time)

	new_message = await channel.fetch_message(my_message.id)

	# Picks a winner
	users = [user for reactions in new_message.reactions
        async for user in reactions.users()
		if user != client.user]
	winner = random.choice(users)
	print(users)
	

	# Announces the winner
	winning_announcement = discord.Embed(color=discord.Color.orange())
	winning_announcement.set_author(name=f'The Giveaway has ended!', icon_url='https://i.imgur.com/DDric14.png')
	winning_announcement.add_field(name=f'🎉 Prize: {prize}',
								   value=f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}',
								   inline=False)
	winning_announcement.set_footer(text='Thanks for entering!')
	await channel.send(embed=winning_announcement)


client.run("MTAzNDc3MDIxOTk0OTg5MTYzNA.GX-iAX.P0VLDYPT0UzHy9u-Qg1ugl-Bb_Khu6uyAPaA1A")