import discord
from discord.ext import commands
import utils
import lyricsgenius

bot_token, genius_api_test_token = utils.load_env_variables()
verified = False

bot = commands.Bot(command_prefix="-lyriccloud ")
genius = lyricsgenius.Genius("", verbose=False)

@bot.event
async def on_ready():
    print(f"I am running on {bot.user.name} (ID {bot.user.id})")

@bot.command()
async def help_me(ctx):
    await ctx.send(utils.get_help_message())

@bot.command()
async def how_to_verify(ctx):
    await ctx.author.send(utils.get_how_to_verify_message())


@bot.command()
async def verify(ctx, key):
    global verified
    key_works = utils.validate_API_key(key)
    if key_works:
        verified = True
        genius._ACCESS_TOKEN = key
        await ctx.send("API Key Validated")
    else:
        await ctx.send("WARNING: API Key Invalid")

@bot.command()
async def generate(ctx, *, search_query):
    if verified:
        song = utils.search_song(genius, search_query)
        if song == None:
            await ctx.send("No Results Have Been Found.")
        else:
            header = f"Wordcloud for {song.title} by {song.artist}"
            lyrics_results = song.lyrics
            lyrics = utils.sanatize_lyrics(lyrics_results)
            utils.generate_wordcloud(lyrics)

            await ctx.send(header)
            await ctx.send(file=discord.File('temp/temp.png'))

    else:
        await ctx.send("You need to verify LyricCloud with a Genius API key. For more information, enter \"-lyriccloud how_to_verify\"")

bot.run(bot_token)
