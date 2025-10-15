import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# ------------------- EVENTOS -------------------
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# ------------------- COMANDOS ORIGINALES -------------------
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    if member.joined_at is None:
        await ctx.send(f'{member} has no join date.')
    else:
        await ctx.send(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

# ------------------- COMANDOS DE MÚSICA -------------------
@bot.command()
async def join(ctx, *, channel: discord.VoiceChannel):
    """Joins a voice channel"""
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()
    await ctx.send(f"Me he unido a {channel}")

@bot.command()
async def play(ctx, *, url):
    """Plays audio from a URL (requires FFmpeg)"""
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send('You need to be in a voice channel to play music.')
            return

    source = discord.FFmpegPCMAudio(url)
    ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
    await ctx.send(f'Now playing: {url}')

@bot.command()
async def stop(ctx):
    """Stops and disconnects the bot from voice"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('Me he desconectado del canal de voz.')
    else:
        await ctx.send('No estoy en un canal de voz.')

@bot.command()
async def volume(ctx, volume: int):
    """Changes the player volume"""
    if ctx.voice_client is None:
        return await ctx.send('Not connected to a voice channel.')
    if ctx.voice_client.source is None:
        return await ctx.send('No audio is playing.')
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f'Changed volume to {volume}%')

# ------------------- HELP PERSONALIZADO -------------------
@bot.command(name='helpme')
async def helpme(ctx):
    embed = discord.Embed(
        title="Comandos disponibles",
        description="Lista de todos los comandos:",
        color=discord.Color.blue()
    )
    # Comandos originales
    embed.add_field(name="$hello", value="Saluda al bot", inline=False)
    embed.add_field(name="$heh [n]", value="Escribe 'he' n veces", inline=False)
    embed.add_field(name="$roll NdN", value="Tira dados en formato NdN, ejemplo 2d6", inline=False)
    embed.add_field(name="$repeat [veces] [mensaje]", value="Repite un mensaje varias veces", inline=False)
    embed.add_field(name="$joined [usuario]", value="Muestra la fecha en que un miembro se unió", inline=False)
    embed.add_field(name="$add [num1] [num2]", value="Suma dos números", inline=False)
    # Comandos de música
    embed.add_field(name="$join [canal]", value="Conecta el bot a un canal de voz", inline=False)
    embed.add_field(name="$play [URL]", value="Reproduce audio desde URL", inline=False)
    embed.add_field(name="$stop", value="Detiene la música y desconecta el bot", inline=False)
    embed.add_field(name="$volume [0-100]", value="Cambia el volumen del audio", inline=False)
    await ctx.send(embed=embed)

# ------------------- EJECUCIÓN -------------------
bot.run("Coloca tu token aquí")
