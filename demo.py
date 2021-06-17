# @ __auther__:    John Wang
# @ __date__:      2021-06-17
# @ __usage__:     Demo for Dash study

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import config

app = dash.Dash(__name__)

host = config.Test_parameters.host
port = config.Test_parameters.port


fig = px.scatter(x=range(10), y=range(10), height=400)
fig.update_layout(clickmode='event+select')  # Config the click mode

app.layout = html.Div(
    [
        html.H1('SELECT OPTIONES'),
        dbc.Alert(
            "Hello，dash_bootstrap_components！", color='success'
        ),
        html.Br(),
        dcc.Dropdown(
            id='option',
            options=[
                {'label': 'One', 'value': 1},
                {'label': 'Two', 'value': 2},
                {'label': 'Three', 'value': 3}
            ],
            value='Please select options above!!!'
        ),
        html.P(id='select_option'),
        dcc.Graph(figure=fig,id='scatter'),
        html.Div([
            'Selected Content：',
            html.P(id='select')
        ]),
    ]
)


# DEMO 01 :
# Select options
@app.callback(Output('select_option','children'),
              Input('option','value'))
def option_input(option):
    return option

# DEMO 02 :
# Relayout data
@app.callback(Output('select','children'),
              Input('scatter','relayoutData'))
def listen_to_select(relayoutData):
    return str(relayoutData)


if __name__ == '__main__':
    app.run_server(host=host,port=port)
