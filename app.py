import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import api_call

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

DROPDOWN_WIDTH = '500px'
DROPDOWN_COLOR = '#000000'

global data
data = api_call.getHighlights()

# data = {
#     'a': [(1,2,4)]
# }

# style={'padding-left':'25px'}

league_drop = html.Div(children=[dcc.Dropdown(id='league-drop', options=[
    {'label': i, 'value': i} for i in sorted(list(data.keys()))
], placeholder="Choose League / Competition....", style={'width': DROPDOWN_WIDTH,
                                                         'color': DROPDOWN_COLOR})])

body = html.Div([
    dbc.Row(
            [
            html.H1(children=["Soccer Highlights"]),
            ], justify="center", align="center", className="h-50"
            ),
    html.Br(),
    dbc.Row([
        # dbc.Col(html.Label('Choose League and Match: ')),
        dbc.Col(html.Div(league_drop)),
        dbc.Col(html.Div(id='second-drop-con'))
    ], align='center'),
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
                          ], placeholder="Choose Match...", style={'width': DROPDOWN_WIDTH,
                                                         'color': DROPDOWN_COLOR})


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


