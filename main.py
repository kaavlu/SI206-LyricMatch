import sqlite3
import os
import matplotlib.pyplot as plt

def set_up_database():
    """Get cur and conn for database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/music.db")
    cur = conn.cursor()
    return cur, conn

def create_table(cur, conn):
    """Create table if it does not yet exist"""
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Billboard_and_Lyrics (id INTEGER PRIMARY KEY AUTOINCREMENT, artist TEXT, song TEXT, count INTEGER)"
    )
    conn.commit()

def insert_dbs(cur, conn):
    cur.execute('SELECT * FROM Billboard')
    for row in cur.fetchall():
        id, artist, song = row
        cur.execute('INSERT INTO Billboard_and_Lyrics (id, artist, song) VALUES (?, ?, ?)', (id, artist, song))

    cur.execute('SELECT * FROM Lyrics')
    for row in cur.fetchall():
        id, count = row
        cur.execute('UPDATE Billboard_and_Lyrics SET count = ? WHERE id = ?', (count, id))

    conn.commit()

def plot_lyrics_count(cur, conn):
    cur.execute('''
        SELECT Billboard.song, Lyrics.count
        FROM Billboard
        JOIN Lyrics ON Billboard.id = Lyrics.id
    ''')

    # Fetch the data
    data = cur.fetchall()

    # Separate the data into two lists for x and y axes
    songs, counts = zip(*data)

    # Plotting the bar plot
    plt.figure(figsize=(12, 8))
    bar_width = 0.6
    plt.bar(songs, counts, color='skyblue', width = bar_width)
    plt.xlabel('Song')
    plt.ylabel('Count')
    plt.title('Lyrics Count for Billboard Songs')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()

def main():
    cur, conn = set_up_database()
    create_table(cur, conn)
    plot_lyrics_count(cur, conn)



if __name__ == "__main__":
    main()
