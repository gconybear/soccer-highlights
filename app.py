import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import api_call

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
server = app.server

DROPDOWN_WIDTH = '200px'

global data
data = api_call.getHighlights()

league_drop = dcc.Dropdown(id='league-drop', options=[
    {'label': i, 'value': i} for i in sorted(list(data.keys()))
], placeholder="Choose League / Competition....", style={'width': DROPDOWN_WIDTH})

body = html.Div([
    dbc.Row(
            [
            html.H1(children=["Soccer Highlights"]),
            ], justify="center", align="center", className="h-50"
            ),
    html.Br(),
    html.Center([league_drop, html.Div(id='second-drop-con')]),
    html.Br(), html.Hr(),
    html.Div(id='vid')

])

app.layout = dbc.Container([body])


@app.callback(
    Output('second-drop-con', 'children'),
    [Input('league-drop', 'value')]
)
def second_drop(val):
    games = data[val]
    games_embed = [(x[0], x[2]) for x in games]
    second = dcc.Dropdown(id='game-drop',
                          options=[
                              {'label': game, 'value': source} for (game, source) in games_embed
                          ], placeholder="Choose Match...")

    return second

@app.callback(
    Output('vid', 'children'),
    [Input('league-drop', 'value'),
     Input('game-drop', 'value')]
)
def show_vid(league, source):

    out = html.Center([
        html.Div([
            html.Iframe(src=source, style={'width': '100%', 'height':'100%'})
        ], style={'width': '1000px', 'height':'750px'})
    ])


    return out


if __name__ == "__main__":
    app.run_server(debug=True, port=7050)


