import requests
import sqlite3
import json
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


def get_billboard_info():
    # URL of the Billboard Hot 100 page
    url = "https://www.billboard.com/charts/hot-100/"

    # Get info from url
    response = requests.get(url)

    # Create soup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # [("Rockin' Around the Christmas Tree", "Brenda Lee"), ("All I Want For Christmas Is You", "Mariah Carey")...]
    res = []

    # Get top rated song first
    top = soup.find("li", class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-1@mobile-max")
    res.append((top.find("h3").text.strip(), top.find("span").text.strip()))

    # Get rest of items from billboard
    items = soup.find_all("li", class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-050 lrv-u-padding-l-1@mobile-max")

    # Iterate through items on billboard
    for item in items:
        song_title = item.find("h3").text.strip()
        artist = item.find("span").text.strip()
        res.append((song_title, artist))

    print(res[0])


def main():
    cur, conn = set_up_database()
    get_billboard_info()
    create_table(cur, conn)


if __name__ == "__main__":
    main()
