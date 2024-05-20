# Dash related dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import webbrowser
import logging
import hashlib

# Importing your app definition from app.py so we can use it
from app import app
from apps import commonmodules as cm
from apps import login
from apps.home import home_layout
# from apps.movies import movies_home, movies_profile
from apps.manage import manage_incharge
# from apps.manage import manage_manager
import apps.dbconnect as db

CONTENT_STYLE = {
    "margin-top": "1em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),

        cm.navbar,

        # Page Content -- Div that contains page layout
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

@app.callback(
    
        Output('page-content', 'children')
    ,
    
        Input('url', 'pathname')
    
)

def displaypage (pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if pathname == '/' or pathname == '/home':
                returnlayout = 'home'
            elif pathname == '/project_overview':
                returnlayout = 'Overview'
            elif pathname == '/manage_incharge':
                returnlayout = manage_incharge.layout
            elif pathname == '/logout':
                returnlayout = 'logout'
            else:
                returnlayout = 'error404'
            return returnlayout
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050', new=0, autoraise=True)
    app.run_server(debug=True)
