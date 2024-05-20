# Usual Dash dependencies
from dash import dcc
from dash import html
from dash import dash_table

import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# Import the necessary libraries 
import base64
import io
import uuid
import pandas as pd

# Let us import the app object in case we need to define
# callbacks here
from app import app

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

        html.H2('Add Project Data'), # Page Header
        html.Hr(),
        dbc.Alert(id='manageproject_alert', is_open=False), # For feedback purposes
        dbc.Form(
            [
                # Form fields here
                dbc.Row(
                [
                    dbc.Label("Project", width=1),
                    dbc.Col(
                        dcc.Dropdown(
                            id='project_dropdown',
                            placeholder='Select Project'
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Switch(
                            id="budget_expense_switch",
                            value=False,
                            style={
                                'transform': 'scale(1.3)',
                                'margin-left': '25px',
                                'padding-top': '8px'  
                            }
                        ),
                        width="auto"  # Auto width to fit the switch
                    ),
                    dbc.Col(
                        html.Div(id="budget_expense_output"),
                        width="auto"  # Auto width to fit the output
                    ),
                ],
                className='mb-2'  # add 1em bottom margin
                ),   
                dbc.Row(
                [   
                    dbc.Label("Reference File", width=1),
                    dbc.Col(
                        dcc.Upload(
                            id='datatable-upload',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Click to Select')
                            ]),
                            style={
                                'width': '80%', 'height': '45px', 'lineHeight': '45px',
                                'borderWidth': '1px', 'borderStyle': 'dashed',
                                'borderRadius': '5px', 'textAlign': 'center', 'margin': '1px'
                            },
                            # multiple=True
                        ),
                    ),
                    dbc.Col(
                    [
                        # Clear Button
                        dbc.Button("  Clear Cells  ", 
                                   id="clear-all-button", 
                                   color="danger", 
                                #    className="mb-3", 
                                   style={
                                'transform': 'scale(1.0)',
                                'margin-left': '0px',
                                'padding-top': '5px'
                            },
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Clear Cells"),
                                dbc.ModalBody("Clear all cells? This action cannot be undone."),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="close-clear_all-modal", className="ml-auto"),
                                        dbc.Button("Clear", id="clear_all-confirm", className="ml-2", color="danger"),
                                    ]
                                ),
                            ],
                            id="confirm-clear_all-modal",
                        ),

                        # Confirm Button
                        dbc.Button(
                            ' Save Changes ',
                            id='save-changes-button',
                            n_clicks=0, # Initialize number of clicks
                            style={
                                'transform': 'scale(1.0)',
                                'margin-left': '5px',
                                'padding-top': '5px'
                            },
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Save Changes"),
                                dbc.ModalBody("Save changes? Make sure all inputs are correct."),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="close-save_changes-modal", className="ml-auto"),
                                        dbc.Button("Save", id="save_changes-confirm", className="ml-2", color="success"),
                                    ]
                                ),
                            ],
                            id="confirm-save_changes-modal",
                        ),
                        dbc.Modal( # Modal = dialog box; feedback for successful saving.
                            [
                                dbc.ModalHeader(
                                    html.H4('Change')
                                ),
                                dbc.ModalBody(
                                    'Changes added successfully!'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        id="proceed_save-modal"
                                        # href='/manage_incharge?mode=add' # Clicking this would lead to a change of pages
                                    )
                                )
                            ],
                            centered=True,
                            id='project_successmodal',
                            backdrop='static' # Dialog box does not go away if you click at\ the background
                        ),
                        dbc.Modal( # Modal = dialog box; feedback for wrong expense input.
                            [
                                dbc.ModalHeader(
                                    html.H4('Expense Error')
                                ),
                                dbc.ModalBody([
                                    html.Div('Expenses should have allotted budget!'),
                                    html.Div('Check the following input(s):'),
                                    html.Div(id='error_item_name', style={'font-weight': 'bold'})
                                ]),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Okay",
                                        id="expense_error-modal-button"
                                    )
                                )
                            ],
                            centered=True,
                            id='expense_error-modal',
                            backdrop='static' # Dialog box does not go away if you click at the background
                        ),

                    ],
                    ),
                ], 
                className='mb-3'
                ),
                dbc.Row(
                    dash_table.DataTable(
                        id='budget_expense_datatable',
                        editable=True,
                        columns=[
                            {'id': 'item_id', 'name': 'Item ID'},
                            {'id': 'item_name', 'name': 'Item'},
                            {'id': 'item_qty', 'name': 'Quantity'},
                            {'id': 'item_unit', 'name': 'Unit'},
                            {'id': 'item_price', 'name': 'Unit Price'},
                            {'id': 'item_desc', 'name': 'Description/Remarks'}
                        ],
                        data=[{'item_id': '', 'item_name': '', 'item_qty': '', 'item_unit': '', 'item_price': '', 'item_desc': ''}] * 5,
                        dropdown={'item_name':{'options':[]}},
                        page_size=25,  # Fixed number of rows to display
                        style_table={'height': '600px', 'overflowY': 'auto',  'overflowX': 'auto'},
                        fixed_rows={'headers': True},
                        style_cell={'textAlign': 'left', 'cursor': 'text'},  
                        style_cell_conditional=[
                            {'if': {'column_id': 'item_id'}, 'minWidth': '50px', 'width': '50px', 'maxWidth': '50px', 'textAlign': 'center'},
                            {'if': {'column_id': 'item_name'}, 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'},
                            {'if': {'column_id': 'item_qty'}, 'minWidth': '50px', 'width': '50px', 'maxWidth': '50px'},
                            {'if': {'column_id': 'item_unit'}, 'minWidth': '50px', 'width': '50px', 'maxWidth': '50px'},
                            {'if': {'column_id': 'item_price'}, 'minWidth': '50px', 'width': '50px', 'maxWidth': '50px'},
                            {'if': {'column_id': 'item_desc'}, 'whiteSpace': 'normal', 'overflowWrap': 'break-word', 'minWidth': 
                             '200px', 'width': '200px', 'maxWidth': '200px'}
                        ],
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'textAlign': 'center'},
                        style_data_conditional=[
                            {
                                'if': {'state': 'active'},  # When a cell is clicked
                                'backgroundColor': 'rgb(220, 255, 220)'  # Set background color 
                            }
                        ],
                        export_format='csv',
                        export_headers='display',
                        
                    ),
                ),
            ]
        ),
    ]
)

# Dropdown for project list
@app.callback(
    [
        # The property of the dropdown we wish to update is the
        # 'options' property
        Output('project_dropdown', 'options'),

    ],
    [
        Input('url', 'pathname')
    ],
)

def projectprofile_dropdown(pathname):
    if pathname == '/manage_incharge':
        sql = """
        SELECT projectid, projectname
        FROM projects 
        WHERE delete_pj_ind = False
        """
        values = []
        cols = ['projectid', 'projectname']

        df = db.querydatafromdatabase(sql, values, cols)        
        project_list = df.to_dict('records')

        # Format the options for the dropdown
        options = [{'label': f"{row['projectid']} - {row['projectname']}", 'value': row['projectid']} for row in project_list]

        return [options]
        
    else:
        # If the pathname is not the desired,
        # this callback does not execute
        raise PreventUpdate
    

# Datatable - values based on switch and uploaded file
# Get budget data from the database
def get_budget_data(budget_id):
    sql = '''
    SELECT b.itemID, i.itemname, i.itemdescript, b.quantity, b.unit, b.quotation
    FROM budget b
    JOIN items i ON b.itemID = i.itemID
    WHERE b.budgetID = %s
    '''
    values = [budget_id]
    cols = ['item_id', 'item_name', 'item_desc', 'item_qty', 'item_unit', 'item_price']
    
    return db.querydatafromdatabase(sql, values, cols)

def get_blank_table():
    return [{'item_id': '', 'item_name': '', 'item_qty': '', 'item_unit': '', 'item_price': '', 'item_desc': ''}] * 5

def get_columns():
    columns = [
                {'id': 'item_id', 'name': 'Item ID'},
                {'id': 'item_name', 'name': 'Item'},
                {'id': 'item_qty', 'name': 'Quantity'},
                {'id': 'item_unit', 'name': 'Unit'},
                {'id': 'item_price', 'name': 'Unit Price'},
                {'id': 'item_desc', 'name': 'Description/Remarks'}
            ]
    return columns

@app.callback(
    Output("budget_expense_output", "children"),
    Output("budget_expense_switch", "label"),
    Output('budget_expense_datatable', 'data', allow_duplicate=True),
    Output('budget_expense_datatable', 'dropdown'),

    Input("budget_expense_switch", "value"),
    Input('datatable-upload', 'contents'),

    State('project_dropdown', 'value'),
    State('datatable-upload', 'filename'),
    prevent_initial_call=True
)
def update_datatable(switch_value, contents, project_value, filename):
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    # Toggle switch 
    if triggered_input == "budget_expense_switch":
        if switch_value and project_value: # Budget Mode

            budget_id = get_budgetID(project_value)
            budget_data = get_budget_data(budget_id).to_dict('records')

            if not budget_data:
                budget_data = get_blank_table()

            return " ", "    Budget", budget_data, {}
        
        else: # Expense Mode
            budget_id = get_budgetID(project_value)
            budget_data = get_budget_data(budget_id).to_dict('records')
            # print("budget_data: ", budget_data)

            unique_item_names = set(row['item_name'] for row in budget_data)
            item_name_options = [{'label': name, 'value': name} for name in unique_item_names]

            dropdown = {'item_name': {'options': item_name_options}}
            # print('dropdown: ', dropdown)
            return " ", "    Expense", get_blank_table(), dropdown
    
    # Upload 
    elif triggered_input == "datatable-upload" and contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            else:
                return dash.no_update
        except Exception as e:
            print(e)
            return dash.no_update
        
        return dash.no_update, dash.no_update, df.to_dict('records'), {}

    return dash.no_update, dash.no_update, get_blank_table(), {}


# Clear Modal
@app.callback(
    Output("confirm-clear_all-modal", "is_open"),

    Input("clear-all-button", "n_clicks"),
    Input("clear_all-confirm", "n_clicks"),
    Input("close-clear_all-modal", "n_clicks"),

    State("confirm-clear_all-modal", "is_open"),
)

def toggle_modal(clear_button, clear_confirm, close_button, is_open):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "clear-all-button":
            return True
        elif button_id == "clear_all-confirm" or button_id == "close-clear_all-modal":
            return False
    return is_open

# Callback to clear all cells when the confirmation button is clicked
@app.callback(
    Output('budget_expense_datatable', 'data'),

    Input('clear_all-confirm', 'n_clicks'),

    State('budget_expense_datatable', 'data')
)

def clear_all_cells(n_clicks, data):
    ctx = dash.callback_context
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'clear_all-confirm.n_clicks':
        # Clear all cells
        data = [{key: '' for key in row} for row in data]

    return data

# Save Changes Modal
@app.callback(
    Output("confirm-save_changes-modal", "is_open"),

    Input("save-changes-button", "n_clicks"),
    Input("save_changes-confirm", "n_clicks"),
    Input("close-save_changes-modal", "n_clicks"),

    State("confirm-save_changes-modal", "is_open"),
)

def toggle_modal(save_button, save_confirm, close_button, is_open):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "save-changes-button":
            return True
        elif button_id == "save_changes-confirm" or button_id == "close-save_changes-modal":
            return False
    return is_open

# To check if an item exists in the database
def get_or_create_itemID(item_name, item_desc):
    str(item_name)
    str(item_desc)

    sql_check = "SELECT itemID FROM items WHERE itemName = %s"
    values_check = [item_name]
    result = db.querydatafromdatabase(sql_check, values_check, ['itemID'])
    # print("result: ", result)
    
    if result.empty:
        # print("item_name: ", item_name)
        # print("item_desc: ", item_desc)
        # Item does not exist, insert a new item and retrieve the new itemID
        sql_insert = "INSERT INTO items (itemname, itemdescript) VALUES (%s, %s)"
        values_insert = [item_name, item_desc]
        db.modifydatabase(sql_insert, values_insert)
        
        # Retrieve the new itemID
        new_item_id_result = db.querydatafromdatabase(sql_check, values_check, ['itemID'])
        itemID = new_item_id_result['itemID'].iloc[0]
    else:
        # Item exists, retrieve the itemID
        itemID = result['itemID'].iloc[0]

    return itemID

# To extract project ID and create budget ID
def get_budgetID(project_value):
    budgetID = f'b-{project_value}'  # Create budget ID by prefixing 'b-'

    return budgetID

# To create expense ID based on budget ID
def get_next_expense_id(budget_id):
    base_expense_id = f"{budget_id}-"
    sql = '''
    SELECT expenseID
    FROM Expense
    WHERE expenseID LIKE %s
    ORDER BY expenseID DESC
    LIMIT 1
    '''
    values = [f"{base_expense_id}%"]
    result = db.querydatafromdatabase(sql, values, ['expenseID'])

    if result.empty:
        next_id = f"{base_expense_id}001"
    else:
        last_id = result['expenseID'].iloc[0]
        next_num = int(last_id.split('-')[-1]) + 1
        next_id = f"{base_expense_id}{next_num:03d}"

    return next_id

# Save table data
@app.callback(
        # dbc.Modal Properties
        Output('project_successmodal', 'is_open'),
        Output('expense_error-modal', 'is_open'),
        Output('error_item_name', 'children'),

        # For buttons, the property n_clicks
        Input('save_changes-confirm', 'n_clicks'),
        Input('expense_error-modal-button', "n_clicks"),

        # proceed_save-modal
        # Table Data
        State('project_dropdown', 'value'),
        State("budget_expense_switch", "value"),
        State('budget_expense_datatable', 'data')
)

def savechanges_to_db(submitbtn, expensebtn, project_value, mode, data):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'save_changes-confirm' and submitbtn:

            if mode:  # Budget Mode

                # print("project_value:", project_value)
                budgetID = get_budgetID(project_value)

                for row in data:

                    # Skip row if item_qty is blank
                    if not row.get('item_qty'):
                        continue

                    item_name = row.get('item_name')
                    item_desc = row.get('item_desc')

                    # print("item name: ", item_name)
                    # print("item description: ", item_desc)
                    itemID = get_or_create_itemID(item_name, item_desc)
                    # print("Item ID: ", itemID)

                    sql = '''
                        INSERT INTO budget (budgetID, itemID, 
                        quantity, unit, quotation)
                        VALUES (%s, %s, %s, %s, %s)
                    '''

                    values = values = [
                        str(budgetID),
                        int(itemID),
                        float(row.get('item_qty')),
                        str(row.get('item_unit')),
                        float(row.get('item_price')),
                    ]

                    db.modifydatabase(sql, values)

                # If this is successful, show model
                return True, False, None
            
            else:  # Expense mode
                budgetID = get_budgetID(project_value)
                expenseID = get_next_expense_id(budgetID)
            
                # Check if expense items exist in the budget

                wrong_expenses = []
                for row in data:
                    
                    # Skip row if item_qty is blank
                    if not row.get('item_qty'):
                        continue

                    item_name = row.get('item_name')
                    item_desc = row.get('item_desc')

                    itemID = get_or_create_itemID(item_name, item_desc)

                    # Check if itemID exists in the budget
                    sql_check_item_in_budget = '''
                    SELECT EXISTS (
                        SELECT 1
                        FROM budget b
                        JOIN items i ON b.itemID = i.itemID
                        WHERE b.budgetID = %s AND i.itemname = %s
                    )
                    '''
                    values_check_item_in_budget = [budgetID, item_name]
                    result_check_item_in_budget = db.querydatafromdatabase(sql_check_item_in_budget, values_check_item_in_budget, ['exists'])
                    if result_check_item_in_budget.iloc[0]['exists'] != 1:    
                        if wrong_expenses:    
                            wrong_expenses.append(", " + item_name)
                        else:
                            wrong_expenses.append(item_name)

                # print("wrong_expenses: ", wrong_expenses)
                # Break the process, show an error indicating wrong expense name
                if wrong_expenses: 
                    return False, True, wrong_expenses
                    
                for row in data:
                    
                    # Skip row if item_qty is blank
                    if not row.get('item_qty'):
                        continue

                    item_name = row.get('item_name')
                    item_desc = row.get('item_desc')

                    itemID = get_or_create_itemID(item_name, item_desc)

                    sql = '''
                        INSERT INTO Expense (expenseID, itemID, 
                        quantity, unit, price)
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                    values = [
                        str(expenseID),
                        int(itemID),
                        float(row.get('item_qty')),
                        str(row.get('item_unit')),
                        float(row.get('item_price')),
                    ]

                    db.modifydatabase(sql, values)

                return True, False, None
            
        elif eventid == "expense_error-modal-button" and expensebtn:
            
            return False, False, None

    raise PreventUpdate

# # Clear Modal
# @app.callback(
#     Output("confirm-clear_all-modal", "is_open"),
#     Output("expense_error-modal", "is_open", allow_duplicate=True),

#     Input("clear-all-button", "n_clicks"),
#     Input("clear_all-confirm", "n_clicks"),
#     Input("close-clear_all-modal", "n_clicks"),
#     Input('expense_error-modal-button', "n_clicks"),

#     State("confirm-clear_all-modal", "is_open"),
#     State("expense_error-modal", "is_open")
# )

# def toggle_modal(clear_button, clear_confirm, close_button, expense_close_button, is_clear_open, is_expense_open):
#     ctx = dash.callback_context
#     if ctx.triggered:
#         button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#         print("button id:", button_id)
#         if button_id == "clear-all-button":
#             return True, False
#         elif button_id == "clear_all-confirm" or button_id == "close-clear_all-modal":
#             return False, False
#         elif button_id == "expense_error-modal-button":
#             return False, True
        
#     return is_clear_open, is_expense_open