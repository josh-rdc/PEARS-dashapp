import hashlib
import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    style={
        'display': 'flex',
        'flex-direction': 'row',
        'height': '100vh',
        'font-family': 'sans-serif',
        'padding': '1em',
        'border': 'none',
    },
    children=[
        # Left side - App Icon and Name
        html.Div(
            style={
                'background': '#003300',
                'padding': '2em 2em',
                'color': 'white',
                'flex': '0 0 50%',  # Occupy half of the screen
                'display': 'flex',
                'flex-direction': 'column',
                'justify-content': 'center',
                'align-items': 'center',
                'border-radius': '25px 25px 25px 25px',  # Rounded edges
            },
            children=[
                html.Img(src="/assets/PEARSlogo.png", alt="App Icon", 
                         style={'width': '300px', 'height': '300px'}),
                html.H1("PEARS", 
                        style={'margin': '0', 'font-size': '7em', 'color':'#CDCDCD',
                               'font-family': 'Arial Black, sans-serif'}),
                html.H5("Project Expense, Analysis", 
                        style={'margin': '0', 'color':'#CDCDCD', 'font-size': '2.5em',
                               'font-family': 'Arial, sans-serif'}),
                html.H5("and Reporting System", 
                        style={'margin': '0', 'color':'#CDCDCD', 'font-size': '2.5em',
                               'font-family': 'Arial, sans-serif'}),
            ]
        ),
        # Right side - Login Form
        html.Div(
            style={
                'flex': '1',  # Occupy remaining space
                'padding': '6em 8em',  # Padding around the form
                'text-align': 'center',  # Center align children horizontally
                'display': 'flex',  # Use flexbox for vertical centering
                'flex-direction': 'column',  # Stack items vertically
                'justify-content': 'center',  # Center items vertically
                'align-items': 'center',  # Center items horizontally
                'height': '100vh'  # Ensure the form fills the full height
            },
            children=[
                html.Img(src="/assets/LoginLogo.png", alt="Other Logo", 
                         style={'width': '100px', 'height': '100px', 'margin-bottom': '1.5em'}),
                html.Br(),
                dbc.Input(id='login_userid', type='text', placeholder='Enter user ID', maxLength=6, 
                        style={'border': 'none', 'border-bottom': '2px solid #262626', 
                               'background': 'transparent', 'padding': '0.6em',
                               'font-size': '1.8em'}),
                dbc.Input(id='login_password', type='password', placeholder='Enter password', maxLength=30, 
                        style={'border': 'none', 'border-bottom': '2px solid #262626', 
                               'background': 'transparent', 'padding': '0.6em', 'margin-bottom': '1.5em',
                               'font-size': '1.8em'}),
                html.Br(),
                dbc.Button("LOGIN", id="log_inbutton", color='primary', className='me-1', n_clicks=0, 
                        style={'background-color': '#262626', 'color': 'white', 'padding': '0.8em 4.0em', 'border-radius': '15px'}),
            ]
        ),
        # Modal Alerts
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Login Error")),
                dbc.ModalBody("User ID or password is incorrect."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="login_alert_close", n_clicks=0),
                ),
            ],
            backdrop='static',
            id="login_alert",
            centered=True,
            # is_open=False,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Input Error")),
                dbc.ModalBody("User ID or password cannot be blank."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="blank_alert_close", className="ms-auto", n_clicks=0),
                ),
            ],
            backdrop='static',
            id="blank_alert",
            # is_open=False,
            centered=True,
        )
    ]
)


@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('blank_alert', 'is_open'),
        Output('currentuserid', 'data'),
        Output('currentrole', 'data'),
        Output('url', 'pathname')
    ],
    [
        Input('log_inbutton', 'n_clicks'),  # begin login query via button click
        Input('sessionlogout', 'modified_timestamp'),  # reset session userid to -1 if logged out
        Input('login_alert_close', 'n_clicks'),  # Close button for login alert
        Input('blank_alert_close', 'n_clicks'),  # Close button for blank alert
    ],
    [
        State('login_userid', 'value'),
        State('login_password', 'value'),
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('currentrole', 'data'),
        State('url', 'pathname'),
        
    ],
    prevent_initial_call=True
)

def loginprocess(loginbtn, sessionlogout_time, login_alert_close, blank_alert_close,
                 userid, password, sessionlogout, currentuserid, currentrole, pathname):
    
    ctx = callback_context
    
    if ctx.triggered:
        # open_login_alert = False
        # open_blank_alert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # url = pathname  # Default to current pathname

        if eventid == 'log_inbutton' and loginbtn:  # trigger for login process

            if not userid or not password:
                open_blank_alert = True
                open_login_alert = False

                return [open_login_alert, open_blank_alert, -1, -1, '/']
        
            if loginbtn and userid and password:
                sql = """SELECT userID, user_type
                        FROM Users
                        WHERE 
                            userID = %s AND
                            password = %s AND
                            NOT user_del_ind"""
                
                # we match the encrypted input to the encrypted password in the db
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
                # print("encrypt_string", encrypt_string)
                # print("encrypt_string(password)" , encrypt_string(password))
                
                values = [userid, encrypt_string(password)]
                # values = [userid, password]  # using plain text password
                
                cols = ['userID', 'user_type']
                df = db.querydatafromdatabase(sql, values, cols)
                
                if df.shape[0]:  # if query returns rows
                    currentuserid = df['userID'][0]
                    currentrole = df['user_type'][0]
                    url = '/home'  # redirect to home page on successful login
                    open_blank_alert = True
                    open_login_alert = False
                
                    return [open_login_alert, open_blank_alert, currentuserid, currentrole, url]

                else:
                    currentuserid = -1
                    currentrole = -1
                    open_login_alert = True
                    open_blank_alert = False
                    url = '/'

                    return [open_login_alert, open_blank_alert, currentuserid, currentrole, url]
                    
        elif eventid == 'sessionlogout' and pathname == '/logout':  # reset the userid if logged out
            currentuserid = -1
            currentrole = -1
            url = '/'  # redirect to login page on logout
            open_login_alert = False
            open_blank_alert = False

            return [open_login_alert, open_blank_alert, currentuserid, currentrole, url]
        
        elif eventid == 'login_alert_close':
            open_login_alert = False
            currentuserid = -1
            currentrole = -1
            url = '/'  # redirect to login page on logout
            open_login_alert = False

            return [open_login_alert, open_blank_alert, currentuserid, currentrole, url]

        elif eventid == 'blank_alert_close':
            open_login_alert = False
            currentuserid = -1
            currentrole = -1
            url = '/'  # redirect to login page on logout
            open_blank_alert = False

            return [open_login_alert, open_blank_alert, currentuserid, currentrole, url]
        
        else:
            raise PreventUpdate
        
        # return [open_login_alert, open_blank_alert, currentuserid, currentrole, url]
    
    else:
            raise PreventUpdate