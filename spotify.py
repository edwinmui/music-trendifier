import spotify_info
import requests
import json
import sqlite3
import webbrowser

import urllib.request, urllib.parse, urllib.error
import sys
import os
import spotipy 
import spotipy.util as util
import matplotlib
import matplotlib.pyplot as plt 

#HOW TO RUN: 
#run the code, and you will get redirected to google. enter the google URL into terminal and click enter
#after you do that, run the code again and you will be all set!

clientid = spotify_info.consumer_key
clientid_secret = spotify_info.secret_key
redirecturi = spotify_info.redirect_uri

#get the username from terminal!
username = 'miriam_akkary@yahoo.com'
scope = 'user-library-read'
try: 
    token = util.prompt_for_user_token(username, scope,client_id=clientid, client_secret= clientid_secret, redirect_uri= redirecturi)

except: 
    os.remove(f'.cache-{username}')
    token = util.prompt_for_user_token(username, scope,client_id=clientid, client_secret= clientid_secret, redirect_uri= redirecturi)



#token = util.prompt_for_user_token(username, scope,client_id=clientid, client_secret= clientid_secret, redirect_uri= redirecturi)
#creating spotify object
spotify_object = spotipy.Spotify(auth=token)

#gets content from the current spotify user
user = spotify_object.current_user()
#print(json.dumps(user, sort_keys=True, indent=4))

#gets current users playlists
results = spotify_object.current_user_playlists()
#creates a list of playlist ID numbers
playlist_list = []
playlist_name_list = []
playlist_id_name = {}
# playlist_list is a list of the playlist IDs --> prints [3423sdf, 34230ow, 234234k]
# playlist_name_list is a list of the actual playlist names --> prints ['Party!', 'SI 206', 'miriam']
# playlist_id_name is a dictionary where the keys are the ID name and the values are the playlist name
for x in results['items']:
    playlist_name = x["id"]
    my_playlist_names = x['name']

    playlist_list.append(playlist_name)
    playlist_name_list.append(my_playlist_names)

    playlist_id_name[playlist_name] = my_playlist_names

# makes a dictionary where the key is the ID number and the value are all the songs in the playlist
playlist_result_dict = {}
playlist_count = 0
for x in playlist_list:
    playlist_result_dict[x] = spotify_object.user_playlist(username, playlist_id = x)
    #new_results = spotify_object.user_playlist(username, x)

#gets all the individual songs in the playlist and adds them to a dictionary 
songs_in_playlist = {}
for playlist_id in playlist_result_dict.keys():
    song_list = []
    artist_list = []
    song_plus_artist = []
    for y in playlist_result_dict[playlist_id]["tracks"]['items']:
        song_name = y['track']['name']
        song_list.append(song_name)
        artist_name = y['track']['album']['artists']
        for artist in artist_name:
            actual_artist = artist['name']
            artist_list.append(actual_artist)
    for x in range(len(song_list)):
        song_plus_artist.append((song_list[x], artist_list[x]))
    songs_in_playlist[playlist_id] = song_plus_artist
    print(songs_in_playlist)

try:
    filename = open('spotify.json', 'r')
    file_results = json.loads(filename)
    filename.close()
    filename = open('spotify.json', 'w')
    for x in playlist_result_dict.keys():
        if x not in file_result.keys():
            filename.write(json.dumps(playlist_result_dict[x]))

except:
    filename = open('spotify.json', 'w')
    filename.write(json.dumps(playlist_result_dict))

# CREATING A DATABASE!
conn = sqlite3.connect('SIProject.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Spotify')
cur.execute('CREATE TABLE Spotify (playlist_name TEXT, playlist_id TEXT, song TEXT, artist TEXT)') 
#inserts the dictionary into the table! 
for (key, val) in songs_in_playlist.items(): 
    for song in val: 
        cur.execute('INSERT INTO Spotify (playlist_name,playlist_id, song, artist) VALUES (?,?,?,?)', (playlist_id_name[key],key, song[0], song[1]))
conn.commit()
conn.close()













