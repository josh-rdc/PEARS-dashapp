# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
# Let us import the app object in case we need to define
# callbacks here
from app import app

navlink_style = {
    'color': '#fff',
    'margin-left': '1em',
    'margin-right': '1em',
}

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("PEARS", class_name="ml-2", 
                                    style={'margin-right': '2em',
                                           'margin-left': '2em', 'color': '#fff'}),),
                ],
                align="center",
                class_name="g-0",
            ),               
            href="/home",
            style = {"text-decoration": "none"},
        ),
        dbc.NavLink("Project Overview", href="/project_overview", style=navlink_style),
        dbc.NavLink("Manage", href="/manage_incharge", style=navlink_style),
        dbc.NavLink("Logout", href="/logout", style=navlink_style),
    ],
    dark=True,
    color='#2E5C43',
)