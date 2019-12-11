import plotly.express as px
import plotly.graph_objects as go
import sqlite3

# reads connection
conn = sqlite3.connect("track_db.sqlite")
cur = conn.cursor()

# gets all track name length and genre
cur.execute("SELECT * FROM trackbyGenre")
genres_and_name_length_list = cur.fetchall()

# disco name lengths
disco_name_lengths = []
# populates with name lengths
for (track, genre) in genres_and_name_length_list:
    if "Disco" in genre:
        disco_name_lengths.append(len(track))

# folk name lengths
folk_name_lengths = []
# populates with name lengths
for (track, genre) in genres_and_name_length_list:
    if "Folk" in genre:
        folk_name_lengths.append(len(track))

# pop name lengths
pop_name_lengths = []
# populates with name lengths
for (track, genre) in genres_and_name_length_list:
    if "Pop" in genre:
        pop_name_lengths.append(len(track))

# hip hop name lengths
hip_hop_name_lengths = []
# populates with name lengths
for (track, genre) in genres_and_name_length_list:
    if "Hip" in genre:
        hip_hop_name_lengths.append(len(track))

# electronic name lengths
electronic_name_lengths = []
# populates with name lengths
for (track, genre) in genres_and_name_length_list:
    if "Elect" in genre:
        electronic_name_lengths.append(len(track))


layout = go.Layout(
    title = "Boxplot of Song Name Length for Disco Songs"
)

layout2 = go.Layout(
    title = "Boxplot of Song Name Length for Folk Songs"
)

layout3 = go.Layout(
    title = "Boxplot of Song Name Length for Pop Songs"
)
layout4 = go.Layout(
    title = "Boxplot of Song Name Length for Hip Hop Songs"
)

layout5 = go.Layout(
    title = "Boxplot of Song Name Length for Electronic Songs"
)

# plots disco name lengths
fig = go.Figure(data=[go.Box(y=disco_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8
    )], layout = layout)

# plots folk name lengths
fig2 = go.Figure(data=[go.Box(y=folk_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8
    )], layout = layout2)

# plots pop name lengths
fig3 = go.Figure(data=[go.Box(y=pop_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8
    )], layout = layout3)

# hip hop name lengths
fig4 = go.Figure(data=[go.Box(y=hip_hop_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8
    )], layout = layout4)

# electronic name lengths
fig5 = go.Figure(data=[go.Box(y=electronic_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8
    )], layout = layout5)

fig.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()


'''
for track in track_data:
    # gets the word length
    word_lenth = 0
    for letter in track[1]:
        word_length +=1
    track_genre_and_word_length.append()
'''


conn.close()

'''
# gets all the track names from database, 
cur.execute("SELECT tracks FROM trackByGenre")

track_data = cur.fetchall()
# counts the number of letters, and insert into a list
track_lengths_data = []
for track in track_data:
    word_length = 0
    for word in track:
        for letter in word:
            word_length +=1
    track_lengths_data.append(int(word_length))

# gets all the corresponding genre names from datase and inserts into a list
cur.execute("SELECT genres FROM trackByGenre")
data = cur.fetchall()
genre_data = [genre[0] for genre in data]

print(genre_data)
print(track_lengths_data)
'''