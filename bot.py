import discord
from discord.ext import commands, tasks
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como: {bot.user}")
    print(f"🔊 Intentando unirse al canal de voz ID: {CHANNEL_ID}")
    await join_and_stay()
    stay_in_channel.start()


async def join_and_stay():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ No se encontró el canal. Verifica el VOICE_CHANNEL_ID.")
        return

    if not isinstance(channel, discord.VoiceChannel):
        print("❌ El canal especificado no es un canal de voz.")
        return

    # Conectar si no está conectado
    guild = channel.guild
    voice_client = guild.voice_client

    if voice_client is None:
        await channel.connect()
        print(f"✅ Conectado al canal: {channel.name}")
    elif voice_client.channel != channel:
        await voice_client.move_to(channel)
        print(f"✅ Movido al canal: {channel.name}")


@tasks.loop(seconds=30)
async def stay_in_channel():
    """Cada 30 segundos verifica que el bot siga en el canal."""
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        return

    guild = channel.guild
    voice_client = guild.voice_client

    if voice_client is None or not voice_client.is_connected():
        print("⚠️  Bot desconectado. Reconectando...")
        await join_and_stay()
    else:
        print(f"🟢 Activo en: {voice_client.channel.name}")


@bot.event
async def on_voice_state_update(member, before, after):
    """Si el bot es expulsado del canal, vuelve a entrar."""
    if member == bot.user and after.channel is None:
        print("⚠️  El bot fue expulsado. Volviendo a entrar...")
        await asyncio.sleep(3)
        await join_and_stay()


bot.run(TOKEN)
