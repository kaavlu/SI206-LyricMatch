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
        "WHERE id > ? "
        "LIMIT 25",
        (start, )
    )

    # Query 25 billboard songs
    billboard_songs = cur.fetchall()

    # use API to get lyrics
    lyrics_count = get_lyrics(billboard_songs)

    # insert number of words in each song to database
    for count in lyrics_count:
        cur.execute(
            "INSERT INTO Lyrics (count) VALUES (?)",
            (count, )
        )
    print(
        f"Added lyric count for billboard songs {start + 1} - {start + 25} to database")

    conn.commit()


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

    return lyrics_count


def average_lyric_count(lyrics_count):
    return sum(lyrics_count) // len(lyrics_count)


def main():
    cur, conn = set_up_database()
    create_table(cur, conn)
    insert_lyrics(cur, conn)


if __name__ == "__main__":
    main()
