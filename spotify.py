import spotipy 
import spotify_info
import spotipy.util as util
import matplotlib
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

# a list of the playlist IDs --> prints [3423sdf, 34230ow, 234234k]
playlist_list_ids = []
# a list of the actual playlist names --> prints ['Party!', 'SI 206', 'edwin']
playlist_names = []
# a dictionary where the keys are the ID name and the values are the playlist name
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

        # gets all individuals songs
        songs_and_artists = []
        # loops through all tracks and adds information to lists
        for track in playlist_object["tracks"]["items"]:
            # helps insert key, value pairs into songs and artists dictionary
            song_list = []
            artist_list = []

            # gets song name
            song_name = track["track"]["name"]
            song_list.append(song_name)

            # gets all artist information
            artist_name = track["track"]["album"]["artists"]
            # finds the actual artist
            for artist in artist_name:
                actual_artist_name = artist["name"]
                artist_list.append(actual_artist_name)

            # adds both song and artist in tuple form to the list songs_and_artists
            songs_and_artists.append((song_list[0], artist_list[0]))

# print(songs_and_artists)                  DELETE THIS LATER!!

# searches up songs and artists to identify genres
list_of_urls = []
# songs_and_artists is a list of track tuples containing the song and artist
for track in songs_and_artists:
    search = "{} {}".format(track[0],track[1])
    search_results = wikipedia.search(search, results = 2)
    searched = wikipedia.page(search_results[0])
    list_of_urls.append(searched.url)

# gets all genres
genres = []
# iterates through urls to find genre within page of text
for url in list_of_urls:
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    table = soup.find("table", {"class": "infobox"})
    list_of_genres1 = table.find("td", {"class": "category hlist"})
    if list_of_genres1 != None:
        if list_of_genres1.find("a") != None:
            genre = list_of_genres1.find("a")
            genres.append(genre.text)
        else:
            list_of_genres2 = list_of_genres1.find("div", {"class": "hlist hlist-separated"})
            li = list_of_genres1.find("ul")
            genre = li.find("a")
            genres.append(genre.text)
    else:
        genre = "unknown"
        genres.append(genre)

print(genres)
    

# connect to database
conn = sqlite3.connect('SIProject.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Spotify')
cur.execute('CREATE TABLE Spotify (playlist_name TEXT, playlist_id TEXT, song TEXT, artist TEXT)') 
#inserts the dictionary into the table
for (key, val) in songs_in_playlist.items(): 
    for song in val: 
        cur.execute('INSERT INTO Spotify (playlist_name,playlist_id, song, artist) VALUES (?,?,?,?)', (playlist_id_name[key],key, song[0], song[1]))
conn.commit()
conn.close()











