import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, dash_table

# Load dataset
df = pd.read_csv('Video_Games.csv')

# Drop the duplicates from the data set for clean data frame
df_cleaned = df.drop_duplicates(subset=['Title'], keep='first')

"""
Question 1: Which of the pokemon games is the highest rated?

Color palette chosen was:
Rich black: #0D1B2A
Oxford Blue: #1B263B
YlnMn Blue: #415A77
Silver Lake Blue: #778DA9
Platinum: #E0E1DD
"""

# Extract data about top 10 highly rated pokemon games
pokemon_games = df_cleaned[df_cleaned['Title'].str.contains(r'pok[eé]mon', case=False, na=False)]
top_10_pokemon_games = pokemon_games.sort_values(by='Rating', ascending=False).head(10)

# Rename game titles to remove "Pokemon" to reduce redundancy.
top_10_pokemon_games['Title'] = top_10_pokemon_games['Title'].str.replace(r'pok[eé]mon ', '', case=False, regex=True)

fig_pokemon = go.Figure()
fig_pokemon.add_trace(go.Bar(
    y=top_10_pokemon_games['Title'],
    x=top_10_pokemon_games['Rating'],
    orientation='h',
    marker=dict(color=['darkslategray', 'goldenrod', 'gray', 'ivory', 'lightgreen', 'lightblue', 'black', 'cyan', 'gold', 'green']),
    text=top_10_pokemon_games['Rating'],
    textposition='outside'
))
fig_pokemon.update_layout(
    xaxis_title=None,
    yaxis_title="Game Title",
    yaxis=dict(autorange='reversed'),
    xaxis=dict(range=[3.5, 5], showticklabels=False, showgrid=False),
    paper_bgcolor='#778DA9',
    plot_bgcolor='#778DA9'
)

"""

Question 2: What is the top most played games?

"""

# Extract data about top played games also replacing 'K' with '000'
df_cleaned['Plays'] = df_cleaned['Plays'].astype(str).str.replace('K', '000', regex=True).astype(float)
top_games = df_cleaned.sort_values(by='Plays', ascending=False).head(10)

fig_top_games = px.bar(top_games, 
                       x='Title', 
                       y='Plays', 
                       color='Plays', 
                       color_continuous_scale='greens')

fig_top_games.update_layout(xaxis_tickangle=-45, 
                            xaxis_title=None,
                            paper_bgcolor='#778DA9',
                            plot_bgcolor='#778DA9')

# Create a sample table with reduced columns of original data set. Summaries and Reviews will be to long to view
df_table = df_cleaned[['Title', 'Release Date', 'Team', 'Rating', 'Genres', 'Plays', 'Playing']]

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout for Dashboard.
app.layout = html.Div(children=[

    # Title at the very top of Dashboard
    html.H1("Video Game Data Dashboard", style={'textAlign': 'center', 'color': 'white'}),
    
    # Sample table of data
    html.Div([
        html.H2("Video Game Data Table", style={'textAlign': 'center', 'color': 'white'}),
            dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in df_table.columns],
            data=df_table.to_dict('records'),
            style_table={'overflowX': 'auto', 'backgroundColor': '#415A77'},
            style_header={'backgroundColor': 'black', 'color': 'white', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'left', 'color': 'white', 'backgroundColor': '#1B263B'},
            page_size=10
        )
    ], style={'backgroundColor': '#415A77', 'padding': '20px', 'borderRadius': '10px', 'margin-top': '50px', 'margin-bottom': '20px'}),
    
    # Creates a bar chart for viewing the highest rated pokemon games
    html.Div([
        html.H2("Highest Rated Pokémon Games", style={'textAlign': 'center', 'color': 'white'}),
        dcc.Graph(figure=fig_pokemon),
    ], style={'backgroundColor': '#415A77', 'padding': '20px', 'borderRadius': '10px', 'margin-bottom': '20px'}),

    # Produces the top most played games
    # ** Redo this to show popularity calculation** 
    html.Div([
        html.H2("Top 10 Most Played Games", style={'textAlign': 'center', 'color': 'white'}),
        dcc.Graph(figure=fig_top_games),
    ], style={'backgroundColor': '#415A77', 'padding': '20px', 'borderRadius': '10px', 'margin-bottom': '20px'}),
], style={'backgroundColor': '#0D1B2A', 'padding': '50px 200px'})


if __name__ == '__main__':
    app.run_server(debug=True)