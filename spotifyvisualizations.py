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
    pointpos = -1.8,
    marker_color='rgb(7,40,89)',
    line_color='rgb(7,40,89)',
    name="Disco"
    )], layout = layout)

# plots folk name lengths
fig2 = go.Figure(data=[go.Box(y=folk_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8,
    marker_color='rgb(7,40,89)',
    line_color='rgb(7,40,89)',
    name="Folk"
    )], layout = layout2)

# plots pop name lengths
fig3 = go.Figure(data=[go.Box(y=pop_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8,
    marker_color='rgb(7,40,89)',
    line_color='rgb(7,40,89)',
    name="Pop"
    )], layout = layout3)

# hip hop name lengths
fig4 = go.Figure(data=[go.Box(y=hip_hop_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8,
    marker_color='rgb(7,40,89)',
    line_color='rgb(7,40,89)',
    name="Hip Hop"
    )], layout = layout4)

# electronic name lengths
fig5 = go.Figure(data=[go.Box(y=electronic_name_lengths,
    boxpoints = 'all',
    jitter = 0.3,
    pointpos = -1.8,
    marker_color='rgb(7,40,89)',
    line_color='rgb(7,40,89)',
    name="Electronic"
    )], layout = layout5)

fig.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()


conn.close()
