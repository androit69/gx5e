import discord
from discord import app_commands
import json
import os

DATA_FILE = r"C:\Users\andro\PyCharmMiscProject\.venv\data.json"

try:
    if os.path.exists(DATA_FILE):

        os.chmod(DATA_FILE, 0o666)
        print("File permissions modified successfully!")
    else:
        print("File not found:", DATA_FILE)
except PermissionError:
    print("Permission denied: You don't have the necessary permissions to change the permissions of this file.")



def load_data():
    global saves
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                saves = json.load(f)
            except json.JSONDecodeError:
                saves = {}
    else:
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(saves, f, indent=4)


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    load_data()
    await tree.sync(guild=discord.Object(id=1461031535095447667))
    print("Ready!")

@tree.command(
    name="save",
    description="save a message",
    guild=discord.Object(id=1461031535095447667)
)

async def save(interaction, message_link:str, save_as:str):
    save_as = save_as.lower()
    saves[save_as] = message_link
    save_data()
    await interaction.response.send_message(f"{"saved message as"} {save_as}, {saves[save_as]}")

@tree.command(
    name="get",
    description="get saved message",
    guild=discord.Object(id=1461031535095447667)
)

async def get(interaction, save_name:str):
    save_name = save_name.lower()
    try:
        await interaction.response.send_message(f"{"here"} {saves[save_name]}")
    except KeyError:
        await interaction.response.send_message(f"Could not find saved message with name {save_name}")

@tree.command(
    name="show",
    description="show all saved messages",
    guild=discord.Object(id=1461031535095447667)
)

async def show(interaction):
    t = []
    for key, value in saves.items():
        t.append(f"**{key}** : {value}")

    embed = discord.Embed(
        title="List Of Saved Messages",
        color=discord.Colour.blurple()
    )
    x = 0
    for i in t:
        embed.add_field(name=" ", value=f"**{x+1}**. {i}", inline=False)
        x += 1


    await interaction.response.send_message(embed=embed)

@tree.command(
    name="help",
    description="show all commands",
    guild=discord.Object(id=1461031535095447667)
)

async def help(interaction):
    embed = discord.Embed(
        title="List Of All Commands",
        description=f"- /save - input message link and then name of save\n"
                                            f"- /show - show all saved messages\n"
                                            f"- /remove - remove saved message by inputing its saved name\n"
                                            f"- /help - show this help message\n"
                                            f"- /get - get a saved message\n",
        color=discord.Colour.blurple()
    )
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="remove",
    description="remove saved message",
    guild=discord.Object(id=1461031535095447667)
)
async def remove(interaction, msg_name:str):
    msg_name = msg_name.lower()
    try:
        await interaction.response.send_message(f"{"removed"} {saves.pop(msg_name)}")
        save_data()
    except KeyError:
        await interaction.response.send_message(f"No saved message with name {msg_name}")

client.run("token")
