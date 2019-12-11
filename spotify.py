# By: Edwin Mui, Noah Helber, Jen McMullem

import spotipy 
import spotify_info
import spotipy.util as util
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import wikipedia
from bs4 import BeautifulSoup

import sys
import os
import requests
import json
import sqlite3
import webbrowser
import urllib.request, urllib.parse, urllib.error
from json.decoder import JSONDecodeError


# HOW TO RUN: 
# if you want ot check out a different user, just change "username"

# gets spotify's authorization info
clientid = spotify_info.consumer_key
clientid_secret = spotify_info.secret_key
redirecturi = spotify_info.redirect_uri

# user ID: 1294124325
username = '1294124325'
scope = 'user-library-read'

# erase cache and prompt for user permission
try: 
    token = util.prompt_for_user_token(username,scope,client_id= clientid,client_secret=clientid_secret,redirect_uri=redirecturi)

except: 
    os.remove(f'.cache-{username}')
    token = util.prompt_for_user_token(username,scope,client_id=clientid,client_secret=clientid_secret,redirect_uri=redirecturi)

# creates spotify object
spotify_object = spotipy.Spotify(auth=token)

# gets content from the current spotify user
user = spotify_object.current_user()

#gets current users playlists
results = spotify_object.current_user_playlists()

# a list of the playlist IDs --> e.g. [3423sdf, 34230ow, 234234k]
playlist_list_ids = []
# a list of the actual playlist names --> e.g. ['Party!', 'SI 206', 'edwin']
playlist_names = []
# a dictionary where the keys are the ID name and the values are the playlist name --> e.g. ["414345", 'Top 50 Hits of 2013"]
playlist_ids_and_names = {}

for item in results['items']:
    playlist_id = item["id"]
    playlist_name = item['name']

    playlist_list_ids.append(playlist_id)
    playlist_names.append(playlist_names)

    playlist_ids_and_names[playlist_id] = playlist_name

# gets tracks of top 50 hits from 2013
for playlist in playlist_ids_and_names.items():
    if playlist[1] == "Top 50 Hits of 2013":

        # creates a spotify object with id
        playlist_object = spotify_object.user_playlist(username, playlist_id=playlist[0])

        # gets all individuals songs and artists
        songs_and_artists = []
        # list of song
        song_list = []
        # list of artists
        artist_list = []

        # loops through all tracks and adds information to lists
        for track in playlist_object["tracks"]["items"]:
            # helps insert key, value pairs into songs and artists dictionary
            temp_song_list = []
            temp_artist_list = []

            # gets song name
            song_name = track["track"]["name"]
            temp_song_list.append(song_name)
            # appends to actual song list
            song_list.append(song_name)

            # gets all artist information
            artist_name = track["track"]["album"]["artists"]
            # finds the actual artist
            for artist in artist_name:
                actual_artist_name = artist["name"]
                temp_artist_list.append(actual_artist_name)
                # appends to actual artist list
                artist_list.append(actual_artist_name)

            # adds both song and artist in tuple form to the list songs_and_artists
            songs_and_artists.append((temp_song_list[0], temp_artist_list[0]))


# searches up songs and artists to identify genres
list_of_urls = []
# songs_and_artists is a list of track tuples containing the song and artist
for track in songs_and_artists:
    # creates a serach query with the song and artist
    search_query = "{} {} {}".format(track[0],track[1],"song")
    
    # searches wikipedia with the above query and returns url
    search_results = wikipedia.search(search_query, results = 2)
    searched = wikipedia.page(title=search_results[0], pageid=None, redirect=True, preload=False)
    list_of_urls.append(searched.url)

# gets all genres
genre_list = []
# iterates through urls to find genre within page of text
for url in list_of_urls:
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    table = soup.find("table", {"class": "infobox"})
    list_of_genres1 = table.find("td", {"class": "category hlist"})
    if list_of_genres1 != None:
        if list_of_genres1.find("a") != None:
            genre = list_of_genres1.find("a")
            genre_list.append(genre.text)
        else:
            list_of_genres2 = list_of_genres1.find("div", {"class": "hlist hlist-separated"})
            li = list_of_genres1.find("ul")
            genre = li.find("a")
            genre_list.append(genre.text)
    else:
        genre = "unknown"
        genre_list.append(genre)


### INSERTS ARTISTS INTO SQL ###

# the id of each artist
track_id = 0
# counter that determines whether 20 items have been inserted
finish = 0

# connect to database
conn = sqlite3.connect('track_db.sqlite')
cur = conn.cursor()
# creates artists table
cur.execute('CREATE TABLE IF NOT EXISTS spotifyArtists (track_id INTEGER PRIMARY KEY, artists TEXT)') 
conn.close()
#inserts artists into the table
for artist in artist_list:
    if finish == 20:
        break
    try:
        conn = sqlite3.connect('track_db.sqlite')
        cur = conn.cursor()
        cur.execute('INSERT INTO spotifyArtists (track_id, artists) VALUES (?, ?)', (track_id, artist))
        track_id += 1
        finish += 1
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
        track_id += 1

### INSERTS TRACKS INTO SQL ###

# the id of each track
track_id = 0
# counter that determines whether 20 items have been inserted
finish = 0

# connect to database
conn = sqlite3.connect('track_db.sqlite')
cur = conn.cursor()
# creates tracks table
cur.execute('CREATE TABLE IF NOT EXISTS spotifyTracks (track_id INTEGER PRIMARY KEY, tracks TEXT)')
conn.close() 
#inserts songs into the table
for track in song_list:
    if finish == 20:
        break
    try:
        conn = sqlite3.connect('track_db.sqlite')
        cur = conn.cursor()
        cur.execute('INSERT INTO spotifyTracks (track_id, tracks) VALUES (?,?)', (track_id, track))
        track_id += 1
        finish += 1
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
        track_id += 1

### INSERTS GENRES INTO SQL ###

# the id of each genre
track_id = 0
# counter that determines whether 20 items have been inserted
finish = 0

# connect to database
conn = sqlite3.connect('track_db.sqlite')
cur = conn.cursor()
# creates genres table
cur.execute('CREATE TABLE IF NOT EXISTS spotifyGenres (track_id INTEGER PRIMARY KEY, genres TEXT)') 
conn.close()

#inserts genres into the table
for genre in genre_list:
    if finish == 20:
        break
    try:
        conn = sqlite3.connect('track_db.sqlite')
        cur = conn.cursor()
        cur.execute('INSERT INTO spotifyGenres (track_id, genres) VALUES (?,?)', (track_id, genre))
        track_id += 1
        finish += 1
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
        track_id += 1


# calculates genre frequency and inserts it into dictionary
genreDict = {}
for genre in genre_list:
    genreDict[genre] = genreDict.get(genre, 0) + 1

# creates two lists; one with genre names, the other with the frequency at which the genres appear
genre_names = []
genre_frequency = []
for key in genreDict.keys():
    genre_names.append(key) 
for value in genreDict.values():
    genre_frequency.append(value)

# creates bar graph with genres and their frequency
fig = go.Figure(data=[go.Pie(labels=genre_names,
                             values=genre_frequency)])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=10,
                  marker=dict(line=dict(color='#000000', width=2)))

fig.update_layout(title_text="Spotify 2013")
fig.show()










