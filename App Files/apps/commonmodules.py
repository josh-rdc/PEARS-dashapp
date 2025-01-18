# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# Let us import the app object in case we need to define
# callbacks here
from app_log import app

navlink_style = {
    'color': '#CDCDCD',
    'margin-left': '0.5em',
    'margin-right': '0.5em',
    'font-size': '1.5em',  # Match font size with login form
    'border': '2px solid #003300',  # Add border around links
    'border-radius': '25px',  # Add rounded edges
    'padding': '0.3em 1.0em',  # Add padding inside the links
    'background-color': '#275317',  # Background color for the links
    'text-decoration': 'none'  # Remove underline
}

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src="/assets/PEARSlogo.png", alt="PEARS Logo", style={'height': '85px'}), 
                        style={'margin-right': '2em', 'margin-left': '2em'}
                    ),
                ],
                align="center",
                class_name="g-0",
            ),               
            href="/home",
            style={"text-decoration": "none"},
        ),
        dbc.NavLink("OVERVIEW", href="/project_overview", style=navlink_style),
        dbc.NavLink("MANAGE", id="add_project_link", href="/manage_incharge?mode=add", style=navlink_style),
        dbc.NavLink("ADD", id="manage_project_link", href="/manage_manager?mode=add", style=navlink_style),
        dbc.NavLink("LOGOUT", href="/logout", style={**navlink_style, 'margin-left': 'auto'}),
    ],
    dark=True,
    color='#003300',
    style={'height': '120px'}  # Double the height of the navigation bar
)


@app.callback(
    Output("add_project_link", "style"),
    Output("manage_project_link", "style"),
    Input("currentrole", "data")
)
def toggle_nav_links(currentrole):
    hidden_style = {'display': 'none'}
    active_style = {**navlink_style, 'color': '#CDCDCD'}
    
    if currentrole == 'pj_ic':
        return active_style, hidden_style
    # elif currentrole == 'manager':
    #     return hidden_style, active_style
    else:
        return active_style, active_style
