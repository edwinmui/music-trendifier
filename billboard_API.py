import billboard
import wikipedia
import requests
from bs4 import BeautifulSoup


chart = billboard.ChartData('hot-100', date='2008-12-31')
song_number1 = chart[0]
song_number2 = chart[1]

top_20 = chart[:20]

top_20_song_artists = []
for entry in top_20:
    top_20_song_artists.append(entry.artist)

top_20_song_names = []
for song in top_20:
    top_20_song_names.append(song.title)

list_of_urls = []
for (x,y) in zip(top_20_song_names, top_20_song_artists):
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

#print(genres)
#print('\n')
#print(top_20_song_names)

genres_names_list = tuple(zip(top_20_song_names, genres))
print(genres_names_list)




    











