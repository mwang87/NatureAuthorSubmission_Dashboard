# -*- coding: utf-8 -*-
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash import dash_table

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
app.title = 'Nature Author Entry Dashboard'

server = app.server

NAVBAR = dbc.Navbar(
    children=[
        dbc.NavbarBrand(
            html.Img(src="https://gnps-cytoscape.ucsd.edu/static/img/GNPS_logo.png", width="120px"),
            href="https://gnps.ucsd.edu"
        ),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Nature Author Entry Dashboard - Version 0.1", href="#")),
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
                    dbc.InputGroupText("Tabular Authors"),
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
        ]
    )
]

INSTRUCTIUONS_DASHBOARD = [
    dbc.CardHeader(html.H5("Instructions")),
    dbc.CardBody(
        [
            dcc.Markdown('''
                1. Enter Authors according to template - [Link](https://docs.google.com/spreadsheets/d/1jjUDQq3EEX2P5OCRK_OtoKjiWKNw6VZo8opTcnjXeVQ/edit?usp=sharing)
                1. Copy from Google Sheets to here
                1. Go to Nature Authors Page
                1. Add number of additional authors you want NOTE: do not copy the corresponding author information which presumably should be last as you'll enter that manually
                1. Hit F12 to bring up debug console
                1. Copy commands and paste into console, hit enter
                1. Enter Corresponding author information
                1. Click save and continue
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
    authors_df = parsing.parse_str_to_df(fielddata)
    authors_df = parsing.clean_author_df(authors_df)
    authors_dedup_df = parsing.deduplicate_affiliations_authors_df(authors_df)

    all_commands_string = parsing.convert_data_commands(authors_dedup_df)

    

    return [[html.Pre(all_commands_string)]]

# API
@server.route("/api")
def api():
    return "Up"    

if __name__ == "__main__":
    app.run_server(debug=True, port=5000, host="0.0.0.0")
