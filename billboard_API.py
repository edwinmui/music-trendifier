import billboard
import wikipedia
import requests
from bs4 import BeautifulSoup
import sqlite3


chart = billboard.ChartData('hot-100', date='2008-12-31')
song_number1 = chart[0]
song_number2 = chart[1]

top_50 = chart[:50]

top_50_song_artists = []
for entry in top_50:
    top_50_song_artists.append(entry.artist)

top_50_song_names = []
for song in top_50:
    top_50_song_names.append(song.title)

list_of_urls = []
for (x,y) in zip(top_50_song_names, top_50_song_artists):
    search = "{} {}".format(x,y)
    results = wikipedia.search(search,results=2)
    searched = wikipedia.page(results[0])
    list_of_urls.append(searched.url)

genres = []
for url in list_of_urls:
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table', {'class':'infobox'})
    genres1 = table.find('td', {'class': 'category hlist'})
    if genres1 != None: 
        if genres1.find('a') != None:
            genre=genres1.find('a')
            genres.append(genre.text)
            #print(genre.text)
        else: 
            genres.append(genres1.text)
            #print(genre.text)
    else: 
        genre = "unknown"
        genres.append(genre)
        #print(genre) 

id=0
for (title, artist, genre) in zip(top_50_song_names, top_50_song_artists, genres):
    try:
        sqliteConnection = sqlite3.connect('track_db.sqlite')
        cursor = sqliteConnection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS billboardTracks (
                        id integer PRIMARY KEY,
                        name text NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS billboardArtists (
                        id integer PRIMARY KEY,
                        name text NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS billboardGenres (
                        id integer PRIMARY KEY,
                        name text NOT NULL)''')
        print("Successfully Connected to SQLite")
        title.replace("'", '\'')
        artist.replace("'", '\'')
        genre.replace("'", '\'')
        sqlite_insert_query1 = """INSERT INTO `billboardTracks` (id, name) VALUES ({},"{}")""".format(id, title)
        sqlite_insert_query2 = """INSERT INTO `billboardArtists` (id, name) VALUES ({},"{}")""".format(id, artist)
        sqlite_insert_query3 = """INSERT INTO `billboardGenres` (id, name) VALUES ({},"{}")""".format(id, genre)

        count1 = cursor.execute(sqlite_insert_query1)
        count2 = cursor.execute(sqlite_insert_query2)
        count3 = cursor.execute(sqlite_insert_query3)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()
        

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
         if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    id += 1




    











