import discord
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))

intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)


async def connect_to_channel():
    """Conecta al canal de voz, limpiando cualquier sesión previa."""
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if channel is None or not isinstance(channel, discord.VoiceChannel):
        print("❌ Canal no encontrado.")
        return False

    guild = channel.guild
    vc = guild.voice_client

    # Desconectar limpiamente si hay sesión colgada
    if vc is not None:
        try:
            await vc.disconnect(force=True)
        except Exception:
            pass
        await asyncio.sleep(3)

    try:
        # reconnect=False para que NO intente reconectar solo (lo manejamos nosotros)
        await channel.connect(reconnect=False, self_deaf=True)
        print(f"✅ Conectado a: {channel.name}")
        return True
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return False


async def watch_loop():
    """Loop principal que vigila la conexión cada 15 segundos."""
    await client.wait_until_ready()
    await asyncio.sleep(3)  # esperar que on_ready termine de conectar

    while True:
        try:
            channel = client.get_channel(CHANNEL_ID)
            if channel is None:
                await asyncio.sleep(15)
                continue

            vc = channel.guild.voice_client

            if vc is None or not vc.is_connected():
                print("🔄 Sin conexión. Reconectando en 5s...")
                await asyncio.sleep(5)
                await connect_to_channel()
            else:
                print(f"🟢 Activo en: {vc.channel.name}")

        except Exception as e:
            print(f"⚠️ Error en watch_loop: {e}")

        await asyncio.sleep(15)


@client.event
async def on_ready():
    print(f"✅ Bot listo: {client.user}")
    ok = await connect_to_channel()
    if not ok:
        print("⚠️ Conexión inicial fallida, el loop intentará reconectar.")
    client.loop.create_task(watch_loop())


client.run(TOKEN, reconnect=True)
