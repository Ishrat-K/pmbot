import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

keep_alive()

handler = logging.FileHandler(filename='discord.log', encoding = 'utf-8', mode= 'w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

def clean(text: str):
    return text.lower().replace(" ", "-")

bot = commands.Bot(command_prefix='s!', intents=intents)

@bot.event
async def on_ready():
    print(f"we are ready to go {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"also join... https://discord.gg/TVb2sJykCU --sent from doll prtl")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "anal" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} shush")

    await bot.process_commands(message)



#START MASS
@bot.command()
async def startmass(ctx):
    massstart = discord.utils.get(ctx.guild.roles, name=". massing")
    startmassembed = discord.Embed(description="⠀⠀⠀⠀<:scythe:1517653026385428631>  mass started \n⠀start posting from <#1517371386346340422> \n⠀⠀⠀⠀post ___bottom to top___", color=discord.Color.from_str("#1a1a1a"))
    if massstart:
        await ctx.author.add_roles(massstart)
        startmessage = await ctx.send(embed=startmassembed)
    else:
        await ctx.send(f"role to be assigned not found, please wait for assistance")



#END MASS

class EndMassView(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=120)

        self.author = author
        self.urgency = None
        self.duration = None

        self.add_item(UrgencySelect())

class UrgencySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="urgent"),
            discord.SelectOption(label="semi-urgent"),
            discord.SelectOption(label="non-urgent"),
        ]

        super().__init__(
            placeholder="select urgency...",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        view: EndMassView = self.view

        # Only the command author can use it
        if interaction.user != view.author:
            await interaction.response.send_message(
                "error: not your command!",
                ephemeral=True
            )
            return

        view.urgency = self.values[0]

        # Remove urgency dropdown
        view.clear_items()

        # Add duration dropdown
        view.add_item(DurationSelect())

        embed = discord.Embed(
            title="<:crossy:1517653034014871642> ・ mass ended",
            description=f"urgency ` {view.urgency} ` \n\nplease⠀ choose⠀ sep⠀ duration",
            color=0x1A1A1A
        )

        await interaction.response.edit_message(
            embed=embed,
            view=view
        )

class DurationSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="1h"),
            discord.SelectOption(label="3h"),
            discord.SelectOption(label="overnight")
        ]

        super().__init__(
            placeholder="select sep duration...",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        view: EndMassView = self.view

        if interaction.user != view.author:
            await interaction.response.send_message(
                "error: not your command!",
                ephemeral=True
            )
            return

        view.duration = self.values[0]

        guild = interaction.guild

        channel = interaction.channel

        urgency = clean(view.urgency)
        duration = clean(view.duration)

        new_name = f"{urgency}・{duration}"

        await channel.edit(name=new_name)

        category = interaction.guild.get_channel(1519427406195196125)
        if isinstance(category, discord.CategoryChannel):
            await channel.edit(category=category, sync_permissions=False)

        queue_channel = discord.utils.get(guild.text_channels, name="・qu")

        if queue_channel:
            embed = discord.Embed(
                description=f"_ _　　　　` {view.urgency} ` <:skully:1517653032366641422> ` {view.duration} `",
                color=0x1A1A1A
            )

            embed.set_image(url="https://cdn.discordapp.com/attachments/1288800799056465923/1517645718062497884/5.png?ex=6a3f9af7&is=6a3e4977&hm=9c754d9f2f4b028a39154ff7aea6ca5c4c6c32ce37b9394aa51528e63f061ac9&")

            await queue_channel.send(
                content=f"{interaction.user.mention} added {interaction.channel.mention} to queue",
                embed=embed
            )

        # Disable the menu
        view.clear_items()

        # ===== YOUR EXISTING ROLE CODE =====

        guild = interaction.guild

        massend = discord.utils.get(guild.roles, name=". massed")
        massstart = discord.utils.get(guild.roles, name=". massing")

        if massend:
            await interaction.user.add_roles(massend)
            await interaction.user.remove_roles(massstart)

        # ================================

        embed = discord.Embed(
            title="<:crossy:1517653034014871642> ・ mass ended",
            description=f"urgency ` {view.urgency} ` \nsep ` {view.duration} `",
            color=0x1A1A1A
        )

        await interaction.response.edit_message(
            embed=embed,
            view=self.view
        )


@bot.command()
async def endmass(ctx):

    embed = discord.Embed(
        title="<:crossy:1517653034014871642> ・ mass ended",
        description="please choose the urgency",
        color=0x1A1A1A
    )

    await ctx.send(
        embed=embed,
        view=EndMassView(ctx.author)
    )


#CHECKPOINT
@bot.command()
async def check(ctx, channel: discord.TextChannel):
    await ctx.message.add_reaction("<:ww1_tick:1520135825197764788>")


#POSTED
TICKET_FILE = "ticket_finder.txt"


def get_ticket_number():
    try:
        with open(TICKET_FILE, "r") as f:
            number = int(f.read())
    except (FileNotFoundError, ValueError):
        number = 0

    number += 1

    with open(TICKET_FILE, "w") as f:
        f.write(str(number))

    return number


async def send_sep_reminder(member, server_link, wait_time):
    await asyncio.sleep(wait_time)

    embed = discord.Embed(
        title="SEP Reminder",
        description=f"Your SEP period has ended.\n\nPlease check:\n{server_link}",
        color=0x1A1A1A
    )

    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        pass


@bot.command()
async def posted(ctx, member: discord.Member, server_link: str):

    guild = ctx.guild
    channel = ctx.channel
    old_name = channel.name

    # -----------------------
    # Determine SEP duration
    # -----------------------

    wait_time = 0
    sep_dur = 0

    if "1h" in old_name:
        wait_time = 3600
        sep_dur = "1h"

    elif "3h" in old_name:
        wait_time = 10800
        sep_dur = "3h"

    elif "overnight" in old_name:
        wait_time = 28800      # change if desired
        sep_dur = "ovn"

    # -----------------------
    # Ticket number
    # -----------------------

    ticket_number = get_ticket_number()

    # -----------------------
    # Send to #fin
    # -----------------------

    fin_channel = discord.utils.get(
        guild.text_channels,
        name="・fin"
    )

    if fin_channel:

        await fin_channel.send(
            content=f"_ _⠀⠀⠀⠀⠀⠀<:teeth:1517653028214149170>⠀` {ticket_number} `⠀ humans⠀ eaten\n⠀⠀\n{member.mention}'s⠀ [server]({server_link}) ⠀has ⠀been ⠀posted ⠀——\n_ _⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀sep ` {sep_dur} `",
        )

    # -----------------------
    # Rename channel
    # -----------------------

    await channel.edit(name="・done")

    # -----------------------
    # Start reminder
    # -----------------------

    if wait_time > 0:
        asyncio.create_task(
            send_sep_reminder(
                member,
                server_link,
                wait_time
            )
        )

    await ctx.message.add_reaction("✅")
#-----------------------------------------

@bot.event
async def on_command_error(ctx, error):
    print(error)


bot.run(token, log_handler = handler, log_level = logging.DEBUG)