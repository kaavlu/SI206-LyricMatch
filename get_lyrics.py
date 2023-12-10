import sqlite3
import requests
import json
import os
import math
base_url = "https://api.musixmatch.com/ws/1.1/"
api_key = "&apikey=9843f22c0731122bbc217d7f65785544"
lyrics_matcher = "matcher.lyrics.get"
format_url = "?format=json&callback=callback"
artist_search_parameter = "&q_artist="
track_search_parameter = "&q_track="
count = 0


def set_up_database():
    """Get cur and conn for database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/music.db")
    cur = conn.cursor()
    return cur, conn


def create_table(cur, conn):
    """Create table if it does not yet exist"""
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Lyrics (id INTEGER PRIMARY KEY AUTOINCREMENT, count INTEGER)"
    )
    conn.commit()


def generate_lyrics(artist_name, track_name):
    api_call = base_url + lyrics_matcher + format_url + artist_search_parameter + \
        artist_name + track_search_parameter + track_name + api_key
    request = requests.get(api_call)
    data = request.json()
    data = data['message']['body']
    if not data:
        return ""

    return data['lyrics']['lyrics_body']


def insert_lyrics(cur, conn):
    # Get number of current rows in database
    cur.execute(
        "SELECT COUNT(*) FROM Lyrics"
    )
    start = cur.fetchone()[0]

    # Get 25 corresponding songs from db
    cur.execute(
        "SELECT * FROM Billboard "
        "WHERE id >= ? "
        "LIMIT 25",
        (start, )
    )

    # Query 25 billboard songs
    billboard_songs = cur.fetchall()

    # use API to get lyrics
    get_lyrics(billboard_songs)


def get_lyrics(songs):

    # counts number of words per song
    lyrics_count = []
    for song in songs:
        artist, track = song[1], song[2]
        lyrics = generate_lyrics(artist, track)

        # add number of words in song to list
        # if no data available, add average number of lyrics to not skew data
        lyrics_count.append(
            int(len(lyrics.split()) // 0.3) if lyrics else average_lyric_count(lyrics_count))

    print(lyrics_count)
    print(len(lyrics_count))


def average_lyric_count(lyrics_count):
    return sum(lyrics_count) // len(lyrics_count)

# def billboard_to_lyrics(input_dict):
#     # {rank1: {song: "title", artist: "artist", ...}, rank2:}
#     for rank in input_dict:
#         artist = input_dict[ranks]["song"]
#         track = input_dict[ranks]["artist"]
#         input_dict[ranks][lyrics] = generate_lyrics(artist, track)


# def db_add_dict(input_dict, database_name='songs_database.db'):
#     connection = sqlite3.connect(database_name)
#     cursor = connection.cursor()

#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS songs (
#             rank TEXT PRIMARY KEY,
#             song TEXT,
#             artist TEXT,
#             lyrics TEXT
#         )
#     ''')

#     for rank, data in input_dict.items():
#         cursor.execute('''
#             INSERT INTO songs (rank, song, artist, lyrics)
#             VALUES (?, ?, ?, ?)
#         ''', (rank, data["song"], data["artist"], data.get("lyrics", "")))

#     connection.commit()
#     connection.close()


def main():
    cur, conn = set_up_database()
    create_table(cur, conn)
    insert_lyrics(cur, conn)


if __name__ == "__main__":
    main()
