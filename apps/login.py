# Dash related dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import hashlib

from app import app
from apps import dbconnect as db

layout = html.Div(
    style={
        'background': '#2E5C43',
        'display': 'flex',
        'flex-direction': 'column',
        'justify-content': 'center',
        'align-items': 'center',
        'height': '100vh',
        'color': 'white',
        'font-family': 'Arial, sans-serif',
        'padding': '1em',
        'border': 'none', 
    },
    children=[
        html.H1("PEARS", className="app-title", style={'margin-bottom': '1.2em', 'font-family': 'Aptos Display'}),
        html.H5("Project Expense, Analysis and Reporting System", className="app-slogan", style={'font-size': '0.8rem', 'margin-bottom': '2.5em', 'color': 'white', 'font-family': 'Aptos Display'}),
        html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardHeader(
                            [
                                html.H3("Log In", className="card-title", style={'font-weight': 'bold', 'color': 'black', 'font-family': 'Source Sans Pro'}),

                            ],
                            className="card-header"
                        ),

                        dbc.CardBody(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(id='username_input', type='text', placeholder='myuseracc', maxLength=30),
                                                dbc.Label("Username"),
                                                dbc.FormFeedback("Invalid input.", type="invalid")
                                            ],
                                            style={'color': 'black'}
                                        ),
                                        width=10,
                                    )
                                ),

                                dbc.Row(
                                    dbc.Col(
                                        dbc.FormFloating(
                                            [
                                                dbc.Input(id='pwd_input', type='password', placeholder='mypassword', maxLength=30),
                                                dbc.Label("Password"),
                                                dbc.FormFeedback("Invalid input.", type="invalid"),
                                            ],
                                            style={'color': 'black'}
                                        ),
                                        width=10,
                                    )

                                ),

                                html.Div(
                                    [
                                        dbc.Button("Log In", id="login_button", color='primary', className='me-1', n_clicks=0),
                                    ],
                                    style={'margin-top': '1rem'}
                                ),

                            ],
                            className='card-body',
                            style={'padding': '2rem'}
                        )
                    ],
                    className='card mb-3',
                    style={'width': '400px', 'max-width': '90%'}
                ),
            ],
            style={'text-align': 'center'}
        ),
        # html.Div("Project Expense, Analysis and Reporting System", style={'font-size': '0.6rem', 'text-align': 'left', 'margin-top': '1em'}),
    ]
)



@app.callback(
#Callback: when log in is clicked,
#   Verify input:
#       If username exists:
#           If password matches:
#               Log in success. Store user ID in "currentuserid" DCC store, and redirect to /home
#           Else: prompt incorrect password
#       Else: prompt user does not exist
    [
        Output('login_modal', 'is_open'),
        Output('login_modal_header', 'children'),
        Output('login_modal_content', 'children'),

        Output('currentuserid', 'data'),
        Output('login-url', 'pathname'),

        #Mark inputs as invalid
        Output('username_input', 'invalid'),
        Output('pwd_input', 'invalid')
    ],
    [
        Input('login_button', 'n_clicks'),
        # Input('signup_button', 'n_clicks'),
        Input('sessionlogout', 'modified_timestamp'),
        Input('login_modal_close', 'n_clicks'),

        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('username_input','value'),
        State('pwd_input','value'),
        State('sessionlogout','data'),
        State('currentuserid', 'data'),
        State('login-url','pathname'),

        State('currentuserid', 'modified_timestamp')
    ]
)
def verify_login_signup(login_btn, sessionlogout_time, modalclose_btn, logintime,
                        username, pwd, sessionlogout, currentuserid, pathname, current_timestamp):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        #print("verify login signup triggered")
        #print("ctx.triggered: ", ctx.triggered)

        # Check if inputs are empty
        if eventid in ["login_button"] and (login_btn):
            if not username and not pwd:
                return [False, None, None, -1, None, True, True]
            if not username:
                return [False, None, None, -1, None, True, False]
            if not pwd:
                return [False, None, None, -1, None, False, True]
        
        # Route login
        if ctx.triggered[0]['prop_id'] == 'currentuserid.modified_timestamp' and current_timestamp != logintime:
            print("Route Log In")
            if currentuserid > 0:
                url_redirect = '/home'
            else:
                url_redirect = '/'
            return [False, None, None, currentuserid, url_redirect, False, False]

        elif eventid == 'login_button' and login_btn: # when the login button is clicked
            sql = '''
                SELECT username FROM users
                WHERE username = %s AND user_delete_ind = False
            '''

            values = [username]
            col = ['username']
            df = db.querydatafromdatabase(sql, values, col)

            if df.empty: # username does not exist
                modal_open = True
                modal_header = "Log In Error"
                modal_content = "User does not exist."
                return [modal_open, modal_header, modal_content, -1, None, False, False]

            # Username exists, check password
            sql = '''
                SELECT user_id, password FROM users
                WHERE username = %s AND user_delete_ind = False
            '''
            values = [username]
            col = ['user_id','password']
            df = db.querydatafromdatabase(sql, values, col)

            if df.empty: # something went wrong with the database query
                modal_open = True
                modal_header = "Log In Error"
                modal_content = "An error occurred while retrieving user data."
                currentuserid = -1
                return [modal_open, modal_header, modal_content, -1, None, False, False]

            stored_password = df['password'][0]
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()

            if encrypt_string(pwd) != stored_password: # incorrect password
                modal_open = True
                modal_header = "Log In Error"
                modal_content = "Incorrect password."
                currentuserid = -1
                return [modal_open, modal_header, modal_content, -1, None, False, False]

            # Password matches. Log In successful!
            currentuserid = df['user_id'][0]  # store user ID in DCC store
            redirect_path = "/home" # redirect to "/home"

            return [False, None, None, currentuserid, redirect_path, False, False]

        # elif eventid == 'signup_button' and signup_btn: # when the signup button is clicked
        #     sql = '''
        #         SELECT username FROM users
        #         WHERE username = %s AND user_delete_ind = False
        #     '''

        #     values = [username]
        #     col = ['username']
        #     df = db.querydatafromdatabase(sql, values, col)

        #     if not df.empty: # username already exists
        #         modal_open = True
        #         modal_header = "Sign Up Error"
        #         modal_content = "Username is already taken. Please enter a new one."
        #     else:
        #         sql = '''
        #                 INSERT INTO users (username, password)
        #                 VALUES (%s, %s)
        #             '''
                
        #         encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
        #         values = [username, encrypt_string(pwd)]

        #         db.modifydatabase(sql, values)

        #         # If this is successful, we want the successmodal to show
        #         modal_open = True
        #         modal_header = "Sign up Success!"
        #         modal_content = "Your account details have been saved. You may now log-in using your username and password."
            
        #     return [modal_open, modal_header, modal_content, -1, None, False, False]
        
        elif eventid == 'login_modal_close' and modalclose_btn: # when the modal "close" btn is clicked
            return [False, None, None, -1, None, False, False]
        
        elif eventid == 'sessionlogout' and pathname == '/logout': # reset the userid if logged out
            currentuserid = -1
            return [False, None, None, currentuserid, None, False, False]
            
        else:
            #print("Prevented Update")
            raise PreventUpdate
    else:
        #print("Prevented Update")
        raise PreventUpdate
