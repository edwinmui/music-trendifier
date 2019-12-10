import billboard
import wikipedia
import requests
from bs4 import BeautifulSoup
import sqlite3
import plotly.graph_objects as go


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
finish = 0
for (title, artist, genre) in zip(top_50_song_names, top_50_song_artists, genres):
    if finish == 20:
        break
    try:
        sqliteConnection = sqlite3.connect('track_db.sqlite')
        cursor = sqliteConnection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS billboardTracks(
                        id integer PRIMARY KEY, 
                        Trackid integer ALTERNATE KEY, 
                        name text NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS billboardArtists(
                        id integer PRIMARY KEY,
                        Artistid integer ALTERNATE KEY, 
                        name text NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS billboardGenres(
                        id integer PRIMARY KEY, 
                        Genreid integer ALTERNATE KEY, 
                        name text NOT NULL)''')
        print("Successfully Connected to SQLite")
        title.replace("'", '\'')
        artist.replace("'", '\'')
        genre.replace("'", '\'')
        sqlite_insert_query1 = """INSERT INTO 'billboardTracks'(id, Trackid, name) VALUES ({},{},"{}")""".format(id, id, title)
        sqlite_insert_query2 = """INSERT INTO 'billboardArtists'(id, Artistid, name) VALUES ({},{},"{}")""".format(id, id, artist)
        sqlite_insert_query3 = """INSERT INTO 'billboardGenres'(id, Genreid, name) VALUES ({},{},"{}")""".format(id, id, genre)

        count1 = cursor.execute(sqlite_insert_query1)
        count2 = cursor.execute(sqlite_insert_query2)
        count3 = cursor.execute(sqlite_insert_query3)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        finish += 1
        cursor.close()
        

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
         if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    id += 1


genreDict ={}
for genre in genres:
    if genre in genreDict:
        genreDict[genre] += 1
    else:
        genreDict[genre] = 1


genre_list = []
genre_values = []
for key in genreDict.keys(): 
    genre_list.append(key) 
          
for value in genreDict.values():
    genre_values.append(value)

print(genre_list, genre_values)

fig = go.Figure(data=[go.Pie(labels=genre_list,
                             values=genre_values)])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=10,
                  marker=dict(line=dict(color='#000000', width=2)))

fig.update_layout(title_text="Billboard 2008")
#fig.show()
