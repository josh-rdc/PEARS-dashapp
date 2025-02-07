# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

# Let us import the app object in case we need to define
# callbacks here
from app_log import app
#for DB needs
import apps.dbconnect as db

from urllib.parse import urlparse, parse_qs
from datetime import datetime

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='manageproject_toload', storage_type='memory', data=0),
            ],
        ),

        html.H2('Add New Project'), # Page Header
        html.Hr(),
        dbc.Alert(id='manageproject_alert', is_open=False), # For feedback purposes
        dbc.Form(
            [
                # Form fields here
                dbc.Row(
                    [
                        dbc.Label("Project Name", width=1, style={'font-family': 'Arial Black'}),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='project_title',
                                placeholder="Project Name"
                            ),
                            width=4
                        )
                    ],
                    className='mb-2' # add 1em bottom margin
                ),
                dbc.Row(
                [
                        dbc.Label("In-Charge", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                id='project_incharge_dropdown',
                                placeholder='Select Project In-Charge'
                            ),
                            width=4
                        ),
                    ],
                    className='mb-2' # add 1em bottom margin
                ),
               dbc.Row(
                    [
                        dbc.Label("Amount", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='project_amount',
                                placeholder='Amount',
                                # pattern="^[0-9]+(\.[0-9]{1,2})?$", 
                                # debounce=True,
                            ),
                            width=4
                        ),
                        html.Div(id="project_amount_div")
                    ],
                    className='mb-1'  # add 1em bottom margin
                ),
                dbc.Row(
                    [
                        dbc.Label("Scope", width=1),
                        dbc.Col(
                            dbc.Input(
                                id='project_scope',
                                placeholder='Short details for project scope'
                            ),
                            width=4
                        )
                    ],
                    className='mb-2' # add 1em bottom margin
                ),
                dbc.Row(
                    [
                        dbc.Label("Location", width=1),
                        dbc.Col(
                            dbc.Input(
                                id='project_location',
                                placeholder='Location',
                            ),
                            width=4
                        )
                    ],
                    className='mb-2' # add 1em bottom margin
                ),
                dbc.Row(
                    [
                        dbc.Label("Client", width=1),
                        dbc.Col(
                            dbc.Input(
                                id='project_client',
                                placeholder='Client Name',
                            ),
                            width=4
                        )
                    ],
                    className='mb-2' # add 1em bottom margin
                ),
                dbc.Row(
                    [
                        dbc.Label("Project Schedule", width=1),
                        dbc.Col(
                            dcc.DatePickerRange(
                                id='project_schedule',
                                start_date_placeholder_text="Start Date",
                                end_date_placeholder_text="End Date",
                                # calendar_orientation='vertical',
                            ),
                            width=4
                        )
                    ],
                    className='mb-2' # add 1em bottom margin
                ),
            ]
        ),

        # enclosing the checklist in a Div so we can
        # hide it in Add Mode
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Project", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='project_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            style={'fontWeight':'bold'}, 
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            id='project_removerecord_div'
        ),

        dbc.Button(
            ' Add Project ',
            id='project_add_button',
            n_clicks=0 # Initialize number of clicks
        ),
        dbc.Modal( # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Add Project')
                ),
                dbc.ModalBody(
                    'Project added successfully!'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/project_overview',
                        id='add_proceed_successmodal', # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='add_project_successmodal',
            backdrop='static' # Dialog box does not go away if you click at the background
        ),
    ]
)

# Dropdown options
@app.callback(
    [
        Output('project_incharge_dropdown', 'options'),
        Output('project_removerecord_div', 'style')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def projectprofile_dropdown(pathname, url_search):
    if pathname == '/manage_manager':
        sql = """
        SELECT userid
        FROM users 
        WHERE user_type = 'pj_ic' and user_del_ind = False
        """
        values = []
        cols = ['userid']

        df = db.querydatafromdatabase(sql, values, cols)        
        project_incharge = df.sort_values('projectid').to_dict('records')

        # Format the options for the dropdown
        options = [{'label': row['userid'], 'value': row['userid']} for row in project_incharge]

        # Parse or decode the 'mode' portion of the search queries
        parsed = urlparse(url_search)
        create_mode = parse_qs(parsed.query).get('mode', ['add'])[0]

        removediv_style = {'display': 'none'} if create_mode == 'add' else None

        return [options, removediv_style]
        
    else:
        # If the pathname is not the desired,
        # this callback does not execute
        raise PreventUpdate
    
# Dropdown 
@app.callback(
    [
        Output('project_title', 'value'),
        Output('project_incharge_dropdown', 'value'),

        # Project information in edit mode
        Output('project_amount', 'value'),
        Output('project_scope', 'value'),
        Output('project_location', 'value'),
        Output('project_client', 'value'),
        Output('project_schedule', 'start_date'),
        Output('project_schedule', 'end_date'),
        Output('project_add_button', 'children')
    ],
    [Input('url', 'search')]
)
def populate_fields(url_search):
    parsed = urlparse(url_search)
    create_mode = parse_qs(parsed.query).get('mode', ['add'])[0]
    project_id = parse_qs(parsed.query).get('id', [None])[0]
    
    if create_mode == 'edit' and project_id:
        sql = """
        SELECT projectName, userid, amount, scope, location, client, start_date, end_date
        FROM projects
        WHERE projectID = %s
        """
        values = [project_id]
        cols = ['projectName', 'userid', 'amount', 'scope', 'location', 'client', 'start_date', 'end_date']
        
        df = db.querydatafromdatabase(sql, values, cols)
        
        if not df.empty:
            project_data = df.iloc[0]
            return (
                project_data['projectName'],
                project_data['userid'],
                project_data['amount'],
                project_data['scope'],
                project_data['location'],
                project_data['client'],
                project_data['start_date'],
                project_data['end_date'],
                'Update Project'
            )
    
    # Default values for 'add' mode
    return (
        '', '', '', '', '', '', None, None,
        'Add Project'
    )

# Error for wrong amount format
@app.callback(
    Output("project_amount_div", "children"),
    Output("project_amount", "className"),
    Input("project_amount", "value")
)
def number_render(input_value):
    try:
        if input_value is None or input_value == "":
            return "", ""

        amount = float(input_value)
        
        if amount < 0:
            raise ValueError("Amount must be non-negative")

        # If value is valid, return no error message and no error class
        return "", ""

    except ValueError:
        error_message = f"\tInvalid value for project amount!"
        error_style = {
            "font-size": "small",
            "color": "red"
        }
        return html.Span(error_message, style=error_style), "invalid"

# Add Projects
def generate_project_id():
    current_year = datetime.now().year % 100  # Get the last two digits of the current year
    # Query the database to find the max project ID
    sql = "SELECT MAX(projectID) FROM projects"
    result = db.querydatafromdatabase(sql, values=None, dfcolumns=['MaxProjectID'])
    
    if result.empty or pd.isnull(result.iloc[0, 0]):
        return f"{current_year:02}" + "001"
    
    max_project_id = int(result.iloc[0, 0])
    new_project_id = max_project_id + 1
    # id = f"{current_year:02}" + str(new_project_id).zfill(3)  
    # print("new_project_id:", new_project_id)
    # print("id: ", id)
    return new_project_id

# Save Project Profile
@app.callback(
    [
        # dbc.Alert Properties
        Output('manageproject_alert', 'color'),
        Output('manageproject_alert', 'children'),
        Output('manageproject_alert', 'is_open'),
    
        # dbc.Modal Properties
        Output('add_project_successmodal', 'is_open')
    ],
    [
        # For buttons, the property n_clicks
        Input('project_add_button', 'n_clicks'),
        Input('add_proceed_successmodal', 'n_clicks'),
    ],
    [
        # The values of the fields are States
        # They are required in this process but they
        # do not trigger this callback
        State('project_title', 'value'),
        State('project_incharge_dropdown', 'value'),
        State('project_amount', 'value'),
        State('project_scope', 'value'),
        State('project_location', 'value'),
        State('project_client', 'value'),

        State('project_schedule', 'start_date'),
        State('project_schedule', 'end_date'),

        State('url', 'search'),  # we need this to identify which mode we are in

        State('project_removerecord', 'value'),  # add this


    ]
)

def projectdetails_saveprofile(submitbtn, proceedbtn, title, userid, amount, scope, location, client,
                               sched_start, sched_end, url_search, remove_ind):
    
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'project_add_button' and submitbtn:
            
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout

            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # We need to check inputs
            if not title: # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check inputs! Project Name cannot be empty!'
            elif not userid:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check inputs! Project In-Charge cannot be empty!'
            elif not amount:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check inputs! Project Amount cannot be empty!'
            elif not sched_start:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check inputs! Start Date cannot be empty!'
            elif not sched_end:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check inputs! End Date cannot be empty!'
            elif sched_start >= sched_end :
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check inputs! Start Date of the project must be before the End Date!'
            else: # all inputs are valid
                
                #parse or decode the 'mode' portion of the search queries
                parsed = urlparse(url_search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    pjid = generate_project_id()
                    
                    # Add the data into the db
                    # Save to db
                    sql = '''
                        INSERT INTO projects (projectID, projectName, userid, amount, 
                        scope, location, client, start_date, end_date, delete_pj_ind, modifydate)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
                    '''

                    scope = " " if not scope else scope
                    location = " " if not location else location
                    client = " " if not client else client

                    values = [pjid , title, userid, amount, scope, location, client, sched_start, sched_end, False]

                    db.modifydatabase(sql, values)

                    # If this is successful, we want the successmodal to show
                    modal_open = True


                elif create_mode == 'edit':
                    print('cr')
                    # 1. We need to get the projectID to update
                    project_id = parse_qs(parsed.query)['id'][0]

                    # 2. We need to update the db

                    sql = '''
                        UPDATE projects
                        SET
                            projectName = %s,
                            userid = %s,
                            amount = %s,
                            scope = %s,
                            location = %s,
                            client = %s,
                            start_date = %s,
                            end_date = %s,
                            delete_pj_ind = %s
                        WHERE
                            projectID = %s
                    '''
                    to_delete = bool(remove_ind)
                    values = [title, userid, amount, scope, location, client, sched_start, sched_end, to_delete, project_id]

                    db.modifydatabase(sql, values)

                    # If this is successful, we want the successmodal to show
                    modal_open = True


            return [alert_color, alert_text, alert_open, modal_open]
        
        if eventid == 'add_proceed_successmodal' and proceedbtn:   

            return ['', '', False, False]

        else: # Callback was not triggered by desired triggers
            raise PreventUpdate

    else:
        raise PreventUpdate
    