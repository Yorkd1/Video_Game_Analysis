"""
Question 1: Which of the pokemon games is the highest rated?

Question 2: What is the top most played games in 2023?

This file is only for running code a little at a time. The Dashboard file is in
VG_Dashboard. 
"""

#%%
##########################START############################
# Import needed libraries and make a data frame of the csv file.
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('Video_Games.csv')

###########################END#############################



#%%
##########################START############################
# Cleaning the data
# Displays max number of columns and rows.
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Dropping duplicate rows by title
df_cleaned = df.drop_duplicates(subset=['Title'], keep='first')

###########################END#############################


#%%
##########################START############################
# For test, create data with Pokemon in the title.
pokemon_games = df_cleaned[(df_cleaned['Title'].str.contains(r'pok[eé]mon', case=False))]

print(pokemon_games.head(10))

###########################END#############################



#%%
##########################START############################
# Create a graph for top 10 pokemon games
top_10_pokemon_games = pokemon_games.sort_values(by='Rating', ascending=False).head(10)

fig = go.Figure()

fig.add_trace(go.Bar(
    y=top_10_pokemon_games['Title'],
    x=top_10_pokemon_games['Rating'],
    orientation='h',
    marker=dict(
        color=['darkslategray', 'goldenrod', 'gray', 'ivory', 'lightgreen', 'lightblue', 'black', 'cyan', 'gold', 'green']
    ),
    text=top_10_pokemon_games['Rating'],
    textposition='outside'
))

# Update layout
fig.update_layout(
    title="Highest Rated Pokemon Games",
    xaxis_title="Rating",
    yaxis_title="Game Title",
    yaxis=dict(autorange='reversed'),
    xaxis=dict(range=[3,5], showticklabels=False)
)
fig.show()
###########################END#############################


# %%
##########################START############################
# Taking a gander at the top games played.
df_cleaned['Plays'] = df_cleaned['Plays'].str.replace('K', '000', regex=True).astype(float)
top_games = df_cleaned.sort_values(by='Plays', ascending=False).head(10)

fig = px.bar(top_games, x='Title', y='Plays', title='Top 10 Most Popular Games 2023',
             color='Plays', color_continuous_scale='greens')
fig.update_layout(xaxis_tickangle=-45,
                  xaxis_title=None)
fig.show()
###########################END#############################
