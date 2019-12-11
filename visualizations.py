import sqlite3
import plotly.graph_objects as go

sqliteConnection = sqlite3.connect('track_db.sqlite')
cursor = sqliteConnection.cursor()
cursor.execute('''SELECT Trackname FROM deezerTracks''') #select all genres from deezer
tracks = cursor.fetchall()
track_list = [x[0] for x in tracks]


cursor.execute('''SELECT duration FROM deezerTracks''')
durations = cursor.fetchall()
duration_list = [x[0] for x in durations]

bar_chart = go.Figure([go.Bar(x=track_list, y=duration_list)])
bar_chart.update_layout(title_text="Deezer 2017 Durations")
bar_chart.show()


cursor.execute('''SELECT GenreName FROM deezerGenres''') #select all genres from deezer
genres = cursor.fetchall()
genreList = [x[0] for x in genres]
genreDict = {}
for genre in genreList:
    if genre in genreDict:
        genreDict[genre] += 1
    else:
        genreDict[genre] = 1


#Get pie chart
genre_list = []
genre_values = []
for key in genreDict.keys(): 
    genre_list.append(key) 
          
for value in genreDict.values():
    genre_values.append(value)

fig = go.Figure(data=[go.Pie(labels=genre_list,
                             values=genre_values)])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=10,
                  marker=dict(line=dict(color='#000000', width=2)))
fig.update_layout(title_text="Deezer 2017")
fig.show()