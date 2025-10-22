import discord
import random
import requests
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

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
        await ctx.send('Format has to be en formato NdN (por ejemplo 2d6)')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    if member.joined_at is None:
        await ctx.send(f'{member} no tiene fecha de ingreso.')
    else:
        await ctx.send(f'{member} se unió el {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

@bot.command()
async def meme(ctx):
    imagenes = os.listdir('imagenes')
    with open(f'imagenes/{random.choice(imagenes)}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

# ---------- COMANDOS DE IMÁGENES ONLINE ----------

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    await ctx.send(get_duck_image_url())

def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('dog')
async def dog(ctx):
    image_url = get_dog_image_url()
    embed = discord.Embed(title="🐶 ¡Un perrito para ti!")
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

def get_fox_image_url():
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    return data['image']

@bot.command('fox')
async def fox(ctx):
    image_url = get_fox_image_url()
    embed = discord.Embed(title="🦊 ¡Un zorro salvaje aparece!")
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

def get_pokemon():
    pokemon_id = random.randint(1, 151)
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    res = requests.get(url)
    data = res.json()
    nombre = data['name'].capitalize()
    imagen = data['sprites']['front_default']
    return nombre, imagen

@bot.command('pokemon')
async def pokemon(ctx):
    nombre, imagen = get_pokemon()
    embed = discord.Embed(title=f"🎮 ¡Has encontrado a {nombre}!")
    embed.set_image(url=imagen)
    await ctx.send(embed=embed)

def get_anime():
    url = f'https://kitsu.io/api/edge/anime?filter[text]=tokyo'
    res = requests.get(url)
    data = res.json()
    nombre = data['data'][0]['attributes']['canonicalTitle']
    imagen = data['data'][0]['attributes']['posterImage']['original']
    return nombre, imagen

@bot.command('anime')
async def anime(ctx):
    nombre, imagen = get_anime()
    embed = discord.Embed(title=f"🎬 ¡Nuevo anime encontrado! 🎌")
    embed.set_image(url=imagen)
    await ctx.send(embed=embed)

# ---------- NUEVOS COMANDOS AÑADIDOS ----------

@bot.command()
async def gato(ctx):
    url = 'https://api.thecatapi.com/v1/images/search'
    res = requests.get(url)
    data = res.json()
    image_url = data[0]['url']
    embed = discord.Embed(title="🐱 ¡Aquí tienes un gatito!")
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

@bot.command()
async def inspiracion(ctx):
    frases = [
        ("🌅 Nunca es tarde para comenzar de nuevo.", "https://picsum.photos/800/400?random=1"),
        ("💪 Cree en ti, incluso cuando nadie más lo haga.", "https://picsum.photos/800/400?random=2"),
        ("🌻 Hoy es un buen día para ser feliz.", "https://picsum.photos/800/400?random=3"),
        ("🚀 El éxito es la suma de pequeños esfuerzos repetidos día tras día.", "https://picsum.photos/800/400?random=4")
    ]
    frase, imagen = random.choice(frases)
    embed = discord.Embed(description=frase, color=discord.Color.gold())
    embed.set_image(url=imagen)
    await ctx.send(embed=embed)

@bot.command()
async def chiste(ctx):
    chistes = [
        "—¿Qué le dice una impresora a otra? —¿Esa hoja es tuya o es una impresión mía?",
        "¿Por qué el libro de matemáticas estaba triste? Porque tenía demasiados problemas.",
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
        "—Camarero, este filete tiene muchos nervios. —Pues normal, es la primera vez que se lo comen."
    ]
    await ctx.send(random.choice(chistes))

@bot.command()
async def paisaje(ctx):
    paisajes = [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
        "https://images.unsplash.com/photo-1470770903676-69b98201ea1c",
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"
    ]
    embed = discord.Embed(title="🌄 Un paisaje para relajarte")
    embed.set_image(url=random.choice(paisajes))
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, mensaje):
    await ctx.send(mensaje)

# ---------- NUEVOS COMANDOS EXTRA ----------

@bot.command()
async def comida(ctx):
    """Muestra una imagen aleatoria de comida deliciosa 🍕"""
    comidas = [
        "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
        "https://images.unsplash.com/photo-1601050690597-4a3f1b7d1c7f",
        "https://images.unsplash.com/photo-1498579809087-ef1e558fd1da",
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
    ]
    embed = discord.Embed(title="🍔 ¡Hora de comer algo rico!")
    embed.set_image(url=random.choice(comidas))
    await ctx.send(embed=embed)

@bot.command()
async def dato(ctx):
    """Envía un dato curioso aleatorio 💡"""
    datos = [
        "💡 Los pulpos tienen tres corazones.",
        "💡 El sol representa el 99,86% de la masa total del sistema solar.",
        "💡 Los koalas duermen hasta 22 horas al día.",
        "💡 Las abejas pueden reconocer rostros humanos."
    ]
    await ctx.send(random.choice(datos))

@bot.command()
async def reaccion(ctx):
    """Envía una imagen de reacción divertida 😝"""
    reacciones = [
        "https://media.tenor.com/x8v1oNUOmg4AAAAM/rickroll-roll.gif",
        "https://media.tenor.com/OiXsbU2iFZsAAAAM/surprised-pikachu.gif",
        "https://media.tenor.com/8qX0MtD9vRYAAAAM/cat-meme.gif",
        "https://media.tenor.com/2roX3uxz_68AAAAM/cute-cat.gif"
    ]
    embed = discord.Embed(title="😆 ¡Reacciona a esto!")
    embed.set_image(url=random.choice(reacciones))
    await ctx.send(embed=embed)

@bot.command()
async def animales(ctx):
    """Muestra un animal aleatorio 🐾"""
    opciones = ['duck', 'dog', 'fox', 'gato', 'pokemon']
    comando = random.choice(opciones)
    await ctx.invoke(bot.get_command(comando))

# 🌿💚 NUEVA SECCIÓN: ECO-ADOLESCENTES BOT (sin quiz ni puntos)

@bot.command()
async def manualidad(ctx):
    """Da ideas de manualidades recicladas, útiles o decorativas 🎨"""
    ideas = [
        "🎧 **DIY ecológico:** convierte una botella plástica en un porta-lápices o parlante casero.",
        "💡 **Eco-tip:** con cajas de cereal puedes hacer libretas o archivadores súper cool.",
        "🌱 **Idea verde:** usa botellas plásticas cortadas como macetas y píntalas con tus colores favoritos.",
        "🎠 **Crea tu espacio:** con tapas o CD viejos haz un collage artístico para tu pared.",
        "🕯️ **Estilo vintage:** convierte frascos de vidrio en lámparas con luces LED recicladas."
    ]
    await ctx.send(f"♻️✨ {random.choice(ideas)}")

@bot.command()
async def reciclar(ctx, *, objeto):
    """Te dice si un objeto se recicla o no (en lenguaje adolescente 😎)"""
    reciclables = {
        "botella": "✅ Sí, las botellas plásticas se reciclan. Solo recuerda: *¡límpiala antes!* 🧴",
        "papel": "✅ Claro, pero nada de papeles con grasa o comida 🤢.",
        "cartón": "✅ Se recicla, pero aplánalo para que ocupe menos espacio 📦.",
        "vidrio": "🟢 Sí, y además se puede reciclar infinitas veces. ¡Increíble, no?! 🍾",
        "plástico": "⚠️ Depende del tipo. Si tiene el número 1, 2 o 5, ¡va al reciclaje! ♻️",
        "pilas": "❌ Nope. ¡Nunca a la basura! Guárdalas y llévalas a un punto de recolección 🔋.",
        "ropa": "👕 Mejor dónala o haz trapos de limpieza. ¡Reutilizar también cuenta!",
        "lata": "✅ 100% reciclable. ¡El aluminio se puede usar mil veces! 🥫"
    }
    objeto = objeto.lower()
    if objeto in reciclables:
        await ctx.send(reciclables[objeto])
    else:
        await ctx.send("🤔 No estoy seguro de ese objeto. Prueba con: botella, papel, cartón, vidrio, plástico, pilas, ropa o lata.")

@bot.command()
async def descomposicion(ctx, *, objeto):
    """Dice cuánto tarda un material en degradarse ⏳"""
    tiempos = {
        "botella de plástico": "♻️ 500 años (sí... medio milenio).",
        "bolsa plástica": "🛍️ 150 años... mejor lleva tu tote bag 😉",
        "lata": "🥫 200 años. Pero se recicla muy fácil, ¡hazlo!",
        "vidrio": "🍾 4000 años 😱. Así que mejor no lo tires.",
        "papel": "📄 2 a 5 meses, si no tiene tinta ni grasa.",
        "cáscara de plátano": "🍌 2 a 3 semanas. Perfecta para compost.",
        "chicle": "🍬 5 años. No lo pegues bajo la mesa 😅.",
        "colilla de cigarrillo": "🚬 Hasta 10 años. ¡Y contamina el agua!",
        "pilas": "🔋 Las pilas pueden tardar entre 500 y 1,000 años, y contaminan mucho ⚠️",
        "ropa": "👕 La ropa de algodón tarda unos 5 meses, pero la sintética puede durar siglos 👖",
        "plástico": "♻️ El plástico común tarda entre 100 y 1,000 años 🧃",
        "pilas": "🔋 Las pilas pueden tardar entre 500 y 1,000 años, y contaminan mucho ⚠️"
    }
    objeto = objeto.lower()
    if objeto in tiempos:
        await ctx.send(f"🕰️ Una {objeto} tarda {tiempos[objeto]} en desaparecer completamente.")
    else:
        await ctx.send("🤷‍♂️ No tengo ese dato, pero puedo investigarlo si me lo pides 😉")

@bot.command()
async def ecoimagen(ctx):
    """Muestra una imagen inspiradora sobre cuidar el planeta 🌍"""
    imagenes = [
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "https://images.unsplash.com/photo-1470770903676-69b98201ea1c",
        "https://images.unsplash.com/photo-1493810329807-1f92e378d7f9",
        "https://images.unsplash.com/photo-1498579809087-ef1e558fd1da",
        "https://images.unsplash.com/photo-1518837695005-2083093ee35b"
    ]
    frases = [
        "🌎 Cuida el planeta... no hay plan B.",
        "💚 Pequeños cambios, grandes resultados.",
        "🌱 Ser eco no es una moda, es el futuro.",
        "🚴‍♀️ Cada acción cuenta. ¡Haz la tuya hoy!",
        "🌤️ Reciclar es la forma más simple de ayudar."
    ]
    embed = discord.Embed(title=random.choice(frases), color=discord.Color.green())
    embed.set_image(url=random.choice(imagenes))
    await ctx.send(embed=embed)

@bot.command()
async def eco_tip(ctx):
    """Consejos rápidos para cuidar el planeta 🌎"""
    tips = [
        "🚰 Cierra la llave mientras te cepillas los dientes.",
        "💡 Apaga las luces que no uses, ¡no eres una discoteca!",
        "🚶‍♂️ Camina o usa bici para trayectos cortos, cuida el aire.",
        "🛍️ Usa bolsas reutilizables en lugar de plástico.",
        "🧃 Reutiliza tus botellas y lleva tu propio termo.",
        "🌳 Planta un árbol o cuida una planta. Ellos nos dan oxígeno.",
        "🪴 Reutiliza frascos de vidrio para guardar cosas o decorar."
    ]
    await ctx.send(random.choice(tips))

@bot.command()
async def reto_eco(ctx):
    """Reto ecológico del día 🌱"""
    retos = [
        "🌿 Hoy no uses plástico de un solo uso.",
        "🚴‍♀️ Ve al colegio caminando o en bici.",
        "🧃 Lleva tu propia botella reutilizable.",
        "🪴 Planta algo, aunque sea en una botella cortada.",
        "🗑️ Clasifica tu basura correctamente.",
        "📢 Cuéntale a un amigo cómo ayudar al planeta.",
        "💧 Trata de no desperdiciar agua hoy."
    ]
    await ctx.send(f"🔥 Tu reto ecológico del día es: {random.choice(retos)} 💪")

@bot.command()
async def dato_eco(ctx):
    """Muestra datos ecológicos curiosos y sorprendentes 🌎"""
    datos = [
        ("🌱 ¿Sabías qué?", 
         "Un árbol adulto puede absorber hasta **20 kg de CO₂ al año** 🌳."),
        ("🐢 Naturaleza sabia", 
         "Cada año, **millones de tortugas marinas** confunden el plástico con medusas 😢."),
        ("💧 Dato impresionante", 
         "El **agua que bebes hoy** podría haber pasado por un dinosaurio hace millones de años 🦕."),
        ("☀️ Energía limpia", 
         "El sol envía a la Tierra más energía en **una hora** de la que usamos en **todo un año** ⚡."),
        ("♻️ Impacto positivo", 
         "Reciclar una sola lata de aluminio ahorra la energía suficiente para mantener encendido un televisor por 3 horas 📺.")
    ]
    imagenes = [
        "https://images.unsplash.com/photo-1503264116251-35a269479413",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
        "https://images.unsplash.com/photo-1493810329807-1f92e378d7f9",
        "https://images.unsplash.com/photo-1473181488821-2d23949a045a"
    ]
    titulo, texto = random.choice(datos)
    embed = discord.Embed(title=titulo, description=texto, color=discord.Color.teal())
    embed.set_image(url=random.choice(imagenes))
    await ctx.send(embed=embed)

@bot.command()
async def frase_motivadora(ctx):
    """Frases motivadoras para levantar el ánimo 🌈"""
    frases = [
        ("💫 Cree en ti", "No necesitas ser perfecto, solo **valiente** para empezar."),
        ("🔥 Nunca te rindas", "Los grandes cambios comienzan con pequeños pasos 🚀."),
        ("🌻 Brilla", "No compares tu capítulo 1 con el capítulo 20 de alguien más."),
        ("🌈 Tú puedes", "Eres más fuerte de lo que crees. 💪"),
        ("☀️ Energía positiva", "Rodéate de personas que te inspiren a ser mejor.")
    ]
    imagenes = [
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
        "https://images.unsplash.com/photo-1485217988980-11786ced9454",
        "https://images.unsplash.com/photo-1503264116251-35a269479413",
        "https://images.unsplash.com/photo-1511988617509-a57c8a288659",
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f"
    ]
    titulo, frase = random.choice(frases)
    embed = discord.Embed(title=titulo, description=frase, color=discord.Color.orange())
    embed.set_image(url=random.choice(imagenes))
    await ctx.send(embed=embed)

@bot.command()
async def meme_eco(ctx, categoria: str = None):
    """
    Envía memes ecológicos para adolescentes 🌍😂
    Categorías opcionales:
    - animales
    - basura
    - motivacion
    """
    memes_animales = [
        "https://cdn.pixabay.com/photo/2015/03/26/09/41/turtle-690212_1280.jpg",
        "https://cdn.pixabay.com/photo/2014/12/16/22/25/dog-570070_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/03/27/19/55/owl-1284513_1280.jpg"
    ]
    frases_animales = [
        "🐢 Cada vez que reciclas, una tortuga sonríe 💚",
        "🦜 ¡Cuidemos a nuestros amigos alados también! 🌿",
        "🐶 Reciclar y cuidar animales van de la mano 😎"
    ]

    memes_basura = [
        "https://cdn.pixabay.com/photo/2017/01/20/00/30/recycling-1990021_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/11/22/19/33/recycling-1850193_1280.jpg",
        "https://cdn.pixabay.com/photo/2018/02/01/18/27/garbage-3122641_1280.jpg"
    ]
    frases_basura = [
        "♻️ Cuando tiras el plástico en el lugar correcto 😎",
        "🚮 Menos drama, más reciclaje!",
        "🌱 Reciclar es más cool de lo que parece 😏"
    ]

    memes_motivacion = [
        "https://cdn.pixabay.com/photo/2017/06/16/11/40/recycle-2412838_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/11/14/03/16/environmental-protection-1822370_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/11/29/08/50/sky-1867278_1280.jpg"
    ]
    frases_motivacion = [
        "🌱 Cuida el planeta, no hay plan B.",
        "💪 Cada acción cuenta, ¡haz la tuya hoy!",
        "🌎 Pequeños cambios, grandes resultados."
    ]

    # Elegir categoría
    if categoria is None:
        # Si no especifica, elige cualquier categoría
        categoria = random.choice(["animales", "basura", "motivacion"])

    if categoria.lower() == "animales":
        embed = discord.Embed(title=random.choice(frases_animales), color=discord.Color.green())
        embed.set_image(url=random.choice(memes_animales))
    elif categoria.lower() == "basura":
        embed = discord.Embed(title=random.choice(frases_basura), color=discord.Color.orange())
        embed.set_image(url=random.choice(memes_basura))
    elif categoria.lower() == "motivacion":
        embed = discord.Embed(title=random.choice(frases_motivacion), color=discord.Color.blue())
        embed.set_image(url=random.choice(memes_motivacion))
    else:
        await ctx.send("❌ Categoría no válida. Usa: animales, basura, motivacion")
        return

    await ctx.send(embed=embed)


@bot.command()
async def mini_reto(ctx):
    """Desafíos ecológicos rápidos para hacer hoy 💪🌿"""
    retos = [
        ("🚿 Desafío del agua", "Toma duchas de menos de **5 minutos**. ¡Cronométrate!"),
        ("🧃 Cero plástico", "Hoy usa solo recipientes reutilizables 💧."),
        ("🗑️ Clasificador pro", "Separa tus residuos: orgánicos, reciclables y no reciclables ♻️."),
        ("🌳 Modo verde", "Habla con alguien sobre por qué cuidar el planeta importa."),
        ("📵 Detox ecológico", "Desconéctate una hora de pantallas y sal a ver el cielo 🌤️.")
    ]
    imagenes = [
        "https://images.unsplash.com/photo-1501004318641-b39e6451bec6",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
        "https://images.unsplash.com/photo-1470770841072-f978cf4d019e",
        "https://images.unsplash.com/photo-1511988617509-a57c8a288659",
        "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13"
    ]
    titulo, descripcion = random.choice(retos)
    embed = discord.Embed(title=titulo, description=descripcion, color=discord.Color.green())
    embed.set_image(url=random.choice(imagenes))
    await ctx.send(embed=embed)

@bot.command()
async def curiosidad(ctx):
    """Datos curiosos del mundo, ciencia y naturaleza 🌍🧠"""
    curiosidades = [
        ("🦋 Naturaleza mágica", "Las mariposas prueban con sus patas. Así detectan el sabor de las flores."),
        ("🌊 Planeta azul", "El 97% del agua de la Tierra está en los océanos. Solo el 3% es dulce."),
        ("☁️ Cielos vivos", "Cada nube puede pesar más de **500 mil kilos**."),
        ("🌋 Calor extremo", "El centro de la Tierra es más caliente que la superficie del Sol ☀️."),
        ("🦜 Comunicación animal", "Los loros pueden imitar acentos humanos distintos 😅.")
    ]
    imagenes = [
        "https://images.unsplash.com/photo-1470770841072-f978cf4d019e",
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "https://images.unsplash.com/photo-1518837695005-2083093ee35b",
        "https://images.unsplash.com/photo-1503264116251-35a269479413",
        "https://images.unsplash.com/photo-1498579809087-ef1e558fd1da"
    ]
    titulo, texto = random.choice(curiosidades)
    embed = discord.Embed(title=titulo, description=texto, color=discord.Color.purple())
    embed.set_image(url=random.choice(imagenes))
    await ctx.send(embed=embed)

@bot.command()
async def ayuda(ctx):
    """Muestra todos los comandos del bot organizados y con emojis 📜✨"""
    embed = discord.Embed(title="🤖 ¡Lista de comandos del bot!", color=discord.Color.purple())
    
    embed.add_field(
        name="💬 Comandos básicos",
        value=(
            "`$hello` - Saluda al bot\n"
            "`$heh [n]` - Repite 'he' n veces (default 5)\n"
            "`$roll NdN` - Tirar dados, ejemplo: 2d6\n"
            "`$repeat [veces] [mensaje]` - Repite un mensaje\n"
            "`$joined [@miembro]` - Muestra cuándo se unió un miembro\n"
            "`$add [n1] [n2]` - Suma dos números"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📸 Comandos de imágenes",
        value=(
            "`$meme` - Envía un meme al azar (local o internet)\n"
            "`$duck` - Muestra un pato aleatorio\n"
            "`$dog` - Muestra un perrito\n"
            "`$fox` - Muestra un zorro\n"
            "`$pokemon` - Muestra un Pokémon aleatorio\n"
            "`$anime` - Muestra un anime aleatorio"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🌱 Comandos ecológicos",
        value=(
            "`$manualidad` - Ideas de manualidades recicladas\n"
            "`$reciclar [objeto]` - Te dice si se recicla ♻️\n"
            "`$descomposicion [objeto]` - Tiempo de degradación ⏳\n"
            "`$ecoimagen` - Imagen inspiradora ecológica 🌍\n"
            "`$eco_tip` - Consejos rápidos para cuidar el planeta 🌱\n"
            "`$reto_eco` - Reto ecológico del día 💪"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🌟 Comandos grandiosos / divertidos",
        value=(
            "`$dato_eco` - Datos curiosos sobre el planeta 🌎\n"
            "`$frase_motivadora` - Frases motivadoras 🌈\n"
            "`$meme_eco [categoría]` - Memes ecológicos divertidos (categorías: animales, basura, motivacion)\n"
            "`$mini_reto` - Desafíos rápidos ecológicos 💪🌿\n"
            "`$curiosidad` - Curiosidades del mundo y ciencia 🧠🌍"
        ),
        inline=False
    )
    
    embed.set_footer(text="✨ Usa los comandos con el prefijo $ delante. Diviértete y cuida el planeta! 🌱")
    
    await ctx.send(embed=embed)
bot.run("TOKEN")
