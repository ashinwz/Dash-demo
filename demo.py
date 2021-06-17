# @ __auther__:    John Wang
# @ __date__:      2021-06-17
# @ __usage__:     Demo for Dash study

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, ClientsideFunction, State
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_table
import config
from sqlalchemy import create_engine
import pandas as pd

app = dash.Dash(__name__)

host = config.Test_parameters.host
port = config.Test_parameters.port
DB   = config.Test_parameters.DB_URI

engine = create_engine(DB,encoding="utf-8")

fig = px.scatter(x=range(10), y=range(10), height=400)
fig.update_layout(clickmode='event+select')  # Config the click mode

app.layout = html.Div(
    [
        html.H1('SELECT OPTIONES'),
        dbc.Alert(
            "Hello，dash_bootstrap_components", color='success'
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
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Input(placeholder='Enter Username')),
                        dbc.Col(dbc.Input(placeholder='Enter Password'))
                    ]
                )
            ]
        ),
        html.Br(),
        dcc.Checklist(
            options=[
                    {'label': 'Test1', 'value': 'Test1'},
                    {'label': 'Test2', 'value': 'Test2'},
                    {'label': 'Test3', 'value': 'Test3'},
                    {'label': 'Test3', 'value': 'Test3'},
            ],
            value=['Test1']
        ),

        html.Br(),
        dcc.RangeSlider(
            min=0,
            max=20,
            step=0.5,
            value=[5, 15]
        ),
        dbc.Container(
            [
                dbc.Label(id='show_message'),
                dbc.Row(
                    [
                        dbc.Col(dbc.Button('UpdateDB', id='refresh-db', style={'width': '100%'}), width=2),
                        dbc.Col(dcc.Dropdown(id='db-table-names', placeholder='Select Table', style={'width': '100%'}), width=4),
                        dbc.Col(dbc.Button('Query', id='query', style={'width': '100%'}), width=1)
                    ]
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dash_table.DataTable(
                                    id='query-result',
                                    virtualization=True,
                                    editable=True,
                                    page_size=15,
                                    style_filter={
                                        'font-family': 'Times New Romer',
                                        'background-color': '#e3f2fd'
                                    },
                                    style_header={
                                        'font-family': 'Times New Romer',
                                        'font-weight': 'bold',
                                        'text-align': 'center'
                                    },
                                    style_data={
                                        'font-family': 'Times New Romer',
                                        'text-align': 'center'
                                    },
                                    style_data_conditional=[
                                        {
                                            "if": {"state": "selected"},
                                            "background-color": "#b3e5fc",
                                            "border": "none"
                                        },
                                    ],
                                    filter_action="native",
                                    sort_action='native'
                                )
                            ]
                        )
                    ]
                )
            ],
            style={
                'margin-top': '50px'
            }
        )
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


@app.callback(
    Output('db-table-names', 'options'),
    Output('show_message','children'),
    Input('refresh-db', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_table_names(n_clicks):
        table_names = pd.read_sql_query('select table_name from information_schema.tables where table_schema="demo"', con=engine)
        if table_names.empty == False:
            return [{'label': name, 'value': name} for name in table_names['TABLE_NAME']] ,'success'
        else:
            return [{'label': '', 'value': ''}], 'No data'

@app.callback(
    Output('query-result', 'data'),
    Output('query-result', 'columns'),
    Input('query', 'n_clicks'),
    State('db-table-names', 'value'),
    prevent_initial_call=True
)
def query_data_records(n_clicks, value):
    if value:
        # Retrive the data limit to 500 rows
        query_result = pd.read_sql_query(f'select * from {value} limit 500', con=engine)
        #print(query_result)
        #return html.Div(dbc.Table.from_dataframe(query_result, striped=True), style={'height': '600px', 'overflow': 'auto'})
        return query_result.to_dict('records'), [
            {'name': column, 'id': column}
            for column in query_result.columns
        ]
    else:
        return dash.no_update


if __name__ == '__main__':
    app.run_server(host=host,port=port,debug=True)
