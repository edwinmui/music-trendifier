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


#connect to database
conn = sqlite3.connect('track_db.sqlite')
cur = conn.cursor()

track_id = 0
#create titles table
cur.execute('DROP TABLE IF EXISTS billboardTracks')
cur.execute('CREATE TABLE billboardTracks (track_id INTEGER, tracks TEXT)')
#insert tracks into the table
for track in top_50_song_names:
    cur.execute('INSERT INTO billboardTracks (track_id, tracks) VALUES (?, ?)', (track_id, track))
    track_id += 1

track_id = 0
# creates artists table
cur.execute('DROP TABLE IF EXISTS billboardArtists')
cur.execute('CREATE TABLE billboardArtists (track_id INTEGER, artists TEXT)') 
#inserts artists into the table
for artist in top_50_song_artists:
    cur.execute('INSERT INTO billboardArtists (track_id, artists) VALUES (?,?)', (track_id, artist))
    track_id += 1

track_id = 0
# creates genres table
cur.execute('DROP TABLE IF EXISTS billboardGenres')
cur.execute('CREATE TABLE billboardGenres (track_id INTEGER, genres TEXT)') 
#inserts genres into the table
for genre in genres:
    cur.execute('INSERT INTO billboardGenres (track_id, genres) VALUES (?,?)', (track_id, genre))
    track_id += 1

conn.commit()
conn.close()











    




    











