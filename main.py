import sqlite3
import os
import matplotlib.pyplot as plt

def set_up_database():
    """Get cur and conn for database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/music.db")
    cur = conn.cursor()
    return cur, conn


def plot_lyrics_count(cur, conn):
    cur.execute('''
        SELECT Billboard.id, Lyrics.count
        FROM Billboard
        JOIN Lyrics ON Billboard.id = Lyrics.id
    ''')

    # Fetch the data
    data = cur.fetchall()

    # Separate the data into two lists for x and y axes
    songs, counts = zip(*data)

    # Plotting the bar plot
    plt.figure(figsize=(20, 8)) 
    bar_width = 0.4
    x_ticks = range(1, 101)
    plt.bar(songs, counts, color='skyblue', align="center", width=bar_width)
    plt.xlabel('Song ID')
    plt.ylabel('Count')
    plt.title('Lyrics Count for Billboard Songs')
    plt.xticks(x_ticks, rotation=45, ha='right')  # Set explicit x-ticks
    plt.tight_layout()
    plt.show()


def plot_pie_chart(cur, conn):
    cur.execute('''
        SELECT Billboard.id, Lyrics.count
        FROM Billboard
        JOIN Lyrics ON Billboard.id = Lyrics.id
    ''')

    # Fetch the data
    data = cur.fetchall()

    # Separate the data into two lists for x and y axes
    songs, counts = zip(*data)

    labels = ["0-250", "251-500", '501-750', "751+"]
    sizes = [0, 0, 0, 0]

    for count in counts:
        if count <= 250:
            sizes[0] += 1
        elif count <= 500:
            sizes[1] += 1
        elif count <= 750:
            sizes[2] += 1
        else:
            sizes[3] += 1
    # Plotting the bar plot
    legend = ["0-250 words per Song", "251-500 words per Song", "501-750 words per Song", "751+ words per Song"]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140, colors=plt.cm.Paired.colors)
    plt.axis('equal')
    plt.legend(legend, loc="best")
    plt.title('Distribution of Items by Category')
    plt.show()

def data_to_text(cur, conn):
    cur.execute('''
        SELECT Billboard.id, Billboard.artist, Billboard.song, Lyrics.count
        FROM Billboard
        JOIN Lyrics ON Billboard.id = Lyrics.id
    ''')
    data = cur.fetchall()
    ids, artists, songs, counts = zip(*data)
    lists = [ids, artists, songs, counts]
    list_names = ["Ids", "Artists", "Songs", "Lyric Word Counts"]

    # Writing data to a text file
    with open('output.txt', 'w') as file:
        for name, data in zip(list_names, lists):
            file.write(f"{name} : {', '.join(map(str, data))}\n")
    

def main():
    cur, conn = set_up_database()
    plot_lyrics_count(cur, conn)
    plot_pie_chart(cur, conn)
    data_to_text(cur, conn)



if __name__ == "__main__":
    main()
