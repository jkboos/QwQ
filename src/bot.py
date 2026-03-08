import os
import discord
from discord.ext import commands
import QuaverAPI as QuaverAPI
import json
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='##############')

with open("Client.json", 'r') as f:
    users_id = json.load(f)

@bot.tree.command(name="綁定帳號", description="輸入Quaver用戶名或ID綁定帳號")
async def login(interaction: discord.Interaction, name: str):
    await interaction.response.defer()

    try:
        user = QuaverAPI.GetUser(name)
        if(user):
            with open("Client.json", 'w') as f:
                users_id[str(interaction.user.id)] = user.id
                json.dump(users_id, f, indent=4)
            await interaction.edit_original_response(content="綁定成功 ✅", embed=QuaverAPI.CreateUserEmbed(user))
            return
        await interaction.edit_original_response(content="帳號不存在")
    except ConnectionRefusedError:
        await interaction.edit_original_response(content="請求過於頻繁，請稍後再試")
        return 

@bot.tree.command(name="搜尋帳號", description="輸入Quaver用戶名或ID搜尋帳號資訊")
async def search_user(interaction: discord.Interaction, name: str):
    await interaction.response.defer()

    try:
        user = QuaverAPI.GetUser(name)
        if(user):
            await interaction.edit_original_response(content="<a:osumania:1131244765074178049>", embed=QuaverAPI.CreateUserEmbed(user))
            return
        await interaction.edit_original_response(content="帳號不存在")
    except ConnectionRefusedError:
        await interaction.edit_original_response(content="請求過於頻繁，請稍後再試")
        return 
    
@bot.tree.command(name="查看帳號", description="查看個人帳號資訊")
async def user_profile(interaction: discord.Interaction):
    await interaction.response.defer()

    if(str(interaction.user.id) in users_id):
        await interaction.edit_original_response(content="<a:osumania:1131244765074178049>", embed=QuaverAPI.CreateUserEmbed(QuaverAPI.GetUser(users_id[str(interaction.user.id)])))
        return
    await interaction.edit_original_response(content="請先使用 `/綁定帳號` 綁定Quaver帳號")

@bot.tree.command(name="最近遊玩紀錄", description="查看最近遊玩的紀錄")
async def recent(interaction: discord.Interaction):
    await interaction.response.defer()

    if(str(interaction.user.id) in users_id):
        try:
            record_4k = QuaverAPI.GetRecentPlayed(users_id[str(interaction.user.id)], 1)
            record_7k = QuaverAPI.GetRecentPlayed(users_id[str(interaction.user.id)], 2)

            if(record_4k.date.timestamp() > record_7k.date.timestamp()):
                recent_record = record_4k
            else:
                recent_record = record_7k
            
            await interaction.edit_original_response(content="<a:lao:1099675564085891113> <a:dalao:1079078501270962187>", embed=QuaverAPI.CreateRecordEmbed(record=recent_record, discord_avatar=interaction.user.avatar))
        except ConnectionRefusedError:
            await interaction.edit_original_response(content="請求過於頻繁，請稍後再試")
        return
    await interaction.edit_original_response(content="請先使用 `/綁定帳號` 綁定Quaver帳號")

@bot.event
async def on_ready():
    print(f"已載入 {len(await bot.tree.sync())} 個指令")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Quaver'))
    print("QwQ")

token = os.getenv("TOKEN")
bot.run(token)
