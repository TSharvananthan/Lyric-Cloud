from dotenv import load_dotenv
import os
import lyricsgenius
import re
import wordcloud

def load_env_variables():
    load_dotenv()
    bot_token = os.getenv("TOKEN")
    genius_api_test_token = os.getenv("GENIUS_API_TEST_TOKEN")

    return (bot_token, genius_api_test_token)

def validate_API_key(key):
    try:
        genius = lyricsgenius.Genius(key, verbose=False)
        genius.search_artist("Andy Shauf", max_songs=3, sort="title")
        return True
    except:
        return False

def search_song(Object, search_query):
    return Object.search_song(search_query)

def sanatize_lyrics(lyrics):
    square_brackets_pattern = "\[.*?\]"
    lyrics = lyrics.replace("\n", " ")
    cleaned_lyrics = re.sub(square_brackets_pattern, '', lyrics)
    return " ".join(cleaned_lyrics.strip().split())

def generate_wordcloud(words):
    wc = wordcloud.WordCloud(width=1000, height=1000, margin=0).generate(words).to_image()
    wc.save("temp/temp.png")

def clear_temp():
    files = [f"temp/{f}" for f in os.listdir("temp")]
    for file in files:
        os.remove(file)

def get_how_to_verify_message():
    return 'How To Get An API Key From Genius\n1. Make your way to https://genius.com/signup_or_login and make an account\n2. Go on https://genius.com/api-clients and click "New API Client"\n3. Enter your App Name (can be anything) and your App Website URL. I would recommend making your App Website URL an invite to your discord server. But it can be any functioning URL\n4. Click "Generate Access Token"\n5. Copy the token that you\'re given\n6. Enter "-lyriccloud verify [Your API Key Here]"'

def get_help_message():
    return "Hello! Welcome to LyricCloud, a discord bot that searches for songs and automatically creates word clouds."
