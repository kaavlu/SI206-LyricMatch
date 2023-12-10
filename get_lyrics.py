import sqlite3
import requests
import json
base_url = "https://api.musixmatch.com/ws/1.1/"
api_key = "&apikey=9843f22c0731122bbc217d7f65785544"
lyrics_matcher = "matcher.lyrics.get"
format_url = "?format=json&callback=callback"
artist_search_parameter = "&q_artist="
track_search_parameter = "&q_track="
count = 0

def generate_lyrics(artist_name, track_name):
    api_call = base_url + lyrics_matcher + format_url + artist_search_parameter + artist_name + track_search_parameter + track_name + api_key
    request = requests.get(api_call)
    data = request.json()
    data = data['message']['body']
    return data['lyrics']['lyrics_body']

def billboard_to_lyrics(input_dict):
    #{rank1: {song: "title", artist: "artist", ...}, rank2:}
    for rank in input_dict:
        artist = input_dict[ranks]["song"]
        track = input_dict[ranks]["artist"]
        input_dict[ranks][lyrics] = generate_lyrics(artist, track)

def db_add_dict(input_dict, database_name='songs_database.db'):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            rank TEXT PRIMARY KEY,
            song TEXT,
            artist TEXT,
            lyrics TEXT
        )
    ''')
    
    for rank, data in input_dict.items():
        cursor.execute('''
            INSERT INTO songs (rank, song, artist, lyrics)
            VALUES (?, ?, ?, ?)
        ''', (rank, data["song"], data["artist"], data.get("lyrics", "")))

    connection.commit()
    connection.close()







