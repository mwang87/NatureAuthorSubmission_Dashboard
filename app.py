# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go 
from dash.dependencies import Input, Output, State
import os
from zipfile import ZipFile
import urllib.parse
from flask import Flask, send_from_directory

import pandas as pd
import requests
import uuid
import werkzeug

import numpy as np
import urllib
import json

from collections import defaultdict
import uuid

import parsing


server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'GNPS - Template'

server = app.server

NAVBAR = dbc.Navbar(
    children=[
        dbc.NavbarBrand(
            html.Img(src="https://gnps-cytoscape.ucsd.edu/static/img/GNPS_logo.png", width="120px"),
            href="https://gnps.ucsd.edu"
        ),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("GNPS - Template Dashboard - Version 0.1", href="#")),
            ],
        navbar=True)
    ],
    color="light",
    dark=False,
    sticky="top",
)

DATASELECTION_CARD = [
    dbc.CardHeader(html.H5("Data Selection")),
    dbc.CardBody(
        [   
            html.H5(children='Data Selection'),
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Tabular Authors", addon_type="prepend"),
                    dbc.Textarea(id='fielddata', placeholder="Enter Tablular Data", value=""),
                ],
                className="mb-3",
            ),
        ]
    )
]


MIDDLE_DASHBOARD = [
    dbc.CardHeader(html.H5("Output Commands")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="output",
                children=[html.Div([html.Div(id="loading-output-23")])],
                type="default",
            ),
        ]
    )
]

CONTRIBUTORS_DASHBOARD = [
    dbc.CardHeader(html.H5("Contributors")),
    dbc.CardBody(
        [
            "Mingxun Wang PhD - UC San Diego",
            html.Br(),
            html.Br(),
            html.H5("Citation"),
            html.A('Mingxun Wang, Jeremy J. Carver, Vanessa V. Phelan, Laura M. Sanchez, Neha Garg, Yao Peng, Don Duy Nguyen et al. "Sharing and community curation of mass spectrometry data with Global Natural Products Social Molecular Networking." Nature biotechnology 34, no. 8 (2016): 828. PMID: 27504778', 
                    href="https://www.nature.com/articles/nbt.3597")
        ]
    )
]

INSTRUCTIUONS_DASHBOARD = [
    dbc.CardHeader(html.H5("Instructions")),
    dbc.CardBody(
        [
            dcc.Markdown('''
                1. Enter Authors according to template - TODO: link
                1. Copy from Google Sheets to here
                1. Go to Nature Authors Page
                1. Add number of additional authors you want
                1. Hit F12
                1. Copy commands and paste into console, hit enter
                1. Enter Corresponding author information
            ''')  
        ]
    )
]


BODY = dbc.Container(
    [
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([
                    dbc.Card(DATASELECTION_CARD),
                    html.Br(),
                    dbc.Card(INSTRUCTIUONS_DASHBOARD)
                ],
                #dbc.Card(LEFT_DASHBOARD),
                className="w-50"
            ),
            dbc.Col(
                [
                    dbc.Card(MIDDLE_DASHBOARD),
                    html.Br(),
                    dbc.Card(CONTRIBUTORS_DASHBOARD),
                ],
                className="w-50"
            ),
        ], style={"marginTop": 30}),
    ],
    fluid=True,
    className="",
)

app.layout = html.Div(children=[NAVBAR, BODY])

@app.callback([
                Output('output', 'children')
              ],
              [
                  Input('fielddata', 'value')
            ])
def draw_output(fielddata):
    from io import StringIO

    TESTDATA = StringIO(fielddata)
    df = pd.read_csv(TESTDATA, sep=None)

    all_commands_string = parsing.convert_data_commands(df)

    return [[html.Pre(all_commands_string)]]

# API
@server.route("/api")
def api():
    return "Up"    

if __name__ == "__main__":
    app.run_server(debug=True, port=5000, host="0.0.0.0")
