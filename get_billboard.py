import requests
import sqlite3
import os
from bs4 import BeautifulSoup


def set_up_database():
    """Get cur and conn for database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/music.db")
    cur = conn.cursor()
    return cur, conn


def create_table(cur, conn):
    """Create table if it does not yet exist"""
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Billboard (id INTEGER PRIMARY KEY AUTOINCREMENT, artist TEXT, song TEXT)"
    )
    conn.commit()


def insert_songs(cur, conn):
    # Get number of current rows in database
    cur.execute(
        "SELECT COUNT(*) FROM Billboard"
    )
    num_rows = cur.fetchone()[0]

    # Get 25 songs that do not yet exist in db
    songs = get_billboard_info(num_rows)

    for song in songs:
        cur.execute(
            "INSERT INTO Billboard (artist, song) VALUES (?, ?)",
            (song[1], song[0])
        )

    print(
        f"Added billboard songs {num_rows + 1} - {num_rows + 25} to database")

    conn.commit()


def get_billboard_info(num_rows):
    # URL of the Billboard Hot 100 page
    url = "https://www.billboard.com/charts/hot-100/"

    # Get info from url
    response = requests.get(url)

    # Create soup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # [("Rockin' Around the Christmas Tree", "Brenda Lee"), ("All I Want For Christmas Is You", "Mariah Carey")...]
    songs = []

    # Get first song if not in table already
    if num_rows == 0:
        top = soup.find("li", class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-1@mobile-max")
        songs.append((top.find("h3").text.strip(),
                     top.find("span").text.strip()))

    # Get rest of items from billboard
    items = soup.find_all("li", class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-050 lrv-u-padding-l-1@mobile-max")

    # Iterate through items on billboard
    for i in range(num_rows - (num_rows != 0), num_rows - (num_rows != 0) + 25 - (num_rows == 0), 1):
        song_title = items[i].find("h3").text.strip()
        artist = items[i].find("span").text.strip()
        songs.append((song_title, artist))

    return songs


def main():
    cur, conn = set_up_database()
    create_table(cur, conn)
    insert_songs(cur, conn)


if __name__ == "__main__":
    main()
