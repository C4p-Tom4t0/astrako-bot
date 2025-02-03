import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Configuración del bot de Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuración de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv('778a901145ea4bfbb1e139b93c7d727f'), client_secret=os.getenv('d0901efd25a44a64925d232aa38094e1')))

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='buscar')
async def buscar(ctx, *, query):
    results = sp.search(q=query, type='track', limit=5)
    if results['tracks']['items']:
        for idx, track in enumerate(results['tracks']['items']):
            await ctx.send(f"{idx + 1}. {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")
    else:
        await ctx.send('No se encontraron resultados.')

@bot.command(name='reproducir')
async def reproducir(ctx, *, query):
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_url = track['external_urls']['spotify']
        await ctx.send(f"Reproduciendo: {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")
        await ctx.send(track_url)
    else:
        await ctx.send('No se encontraron resultados.')

@bot.command(name='playlist')
async def playlist(ctx, *, playlist_id):
    results = sp.playlist(playlist_id)
    if results['tracks']['items']:
        for track in results['tracks']['items']:
            track_info = track['track']
            track_url = track_info['external_urls']['spotify']
            await ctx.send(f"Reproduciendo: {track_info['name']} - {', '.join([artist['name'] for artist in track_info['artists']])}")
            await ctx.send(track_url)
    else:
        await ctx.send('No se encontraron resultados.')

# Reemplaza 'TU_TOKEN' con el token de tu bot de Discord
bot.run(os.getenv('MTMzNjAwMjY5NzcyNzQ0NzA3MQ.GTK729.lP1o51LuEyNA7E8tHidzX0EiCXlpw8l8hdXON8'))
