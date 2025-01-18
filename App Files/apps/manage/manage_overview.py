# Usual Dash dependencies
from dash import dcc
from dash import html
from dash import dash_table

import dash_bootstrap_components as dbc
import dash

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go

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
        html.H2('Project Overview'),  # Page Header
        html.Hr(),
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Project", width=1, style={'font-family': 'Arial Black'}),
                        dbc.Col(
                            dcc.Dropdown(
                                id='constrained_project_dropdown',
                                placeholder='Select Project'
                            ),
                            width=3
                        ),
                        # Confirm Button
                        dbc.Col(
                            dcc.Link(
                                dbc.Button(
                                    'Edit',
                                    id='edit-button',
                                    n_clicks=0,  # Initialize number of clicks
                                    style={
                                        'transform': 'scale(1.0)',
                                        'margin-left': '5px',
                                        'padding-top': '5px',
                                        'width':'25%'
                                    },
                                ),
                                id='edit-link',
                                href='#'
                            ),
                        ),
                    ],
                    className='mb-4'  # add 1em bottom margin
                ),
                dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        children=[
                                            html.Div([
                                                html.Strong('PROJECT PROFILE', 
                                                            style={'font-family': 'Arial Black'}),
                                            ], style={'margin-bottom': '2px'}),
                                        ],
                                        style={
                                            'background': '#262626',
                                            'color': '#FFFFFF',
                                            'padding': '10px',
                                            'border-radius': '25px',
                                            'width': '100%',  # Adjusted width
                                            'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                            'display': 'flex',
                                            'flex-direction': 'column',
                                            'align-items': 'center',
                                            'text-align': 'center'
                                        }
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    children=[
                                                        html.Div([
                                                            html.Strong('Project Name:'),
                                                            html.Span(id='project_name', style={'margin-left': '10px'}),
                                                        ], style={'margin-bottom': '10px'}),
                                                        html.Div([
                                                            html.Strong('Contract Amount:'),
                                                            html.Span(id='contract_amount', style={'margin-left': '10px'}),
                                                        ], style={'margin-bottom': '10px'}),
                                                        html.Div([
                                                            html.Strong('Budget Amount:'),
                                                            html.Span(id='budget_amount', style={'margin-left': '10px'}),
                                                        ], style={'margin-bottom': '10px'}),
                                                        html.Div([
                                                            html.Strong('Scope:'),
                                                            html.Span(id='scope', style={'margin-left': '10px'}),
                                                        ], style={'margin-bottom': '10px'}),
                                                        html.Div([
                                                            html.Strong('Location:'),
                                                            html.Span(id='location', style={'margin-left': '10px'}),
                                                        ], style={'margin-bottom': '10px'}),
                                                        html.Div([
                                                            html.Strong('Client:'),
                                                            html.Span(id='client', style={'margin-left': '10px'}),
                                                        ], style={'margin-bottom': '10px'}),
                                                        html.Div([
                                                            html.Strong('Start Date:'),
                                                            html.Span(id='start_date', style={'margin-left': '10px'}),
                                                        ], style={'margin-bottom': '10px'}),
                                                        html.Div([
                                                            html.Strong('End Date:'),
                                                            html.Span(id='end_date', style={'margin-left': '10px'}),
                                                        ], style={'margin-bottom': '10px'}),
                                                    ],
                                                    style={
                                                        'background': '#CDCDCD',
                                                        'color': 'black',
                                                        'padding': '20px',
                                                        'border-radius': '25px',
                                                        'width': '100%',
                                                        'height': '350px',
                                                        'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                                        'display': 'flex',
                                                        'flex-direction': 'column',
                                                        'justify-content': 'center',
                                                        # 'align-items': 'center',
                                                    }
                                                ),
                                                width=12 
                                            ), 
                                        ],
                                        style={'padding': '10px'} 
                                    ),
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        children=[
                                            html.Div([
                                                html.Strong('COMMERCIAL MANGEMENT OVERVIEW', 
                                                            style={'font-family': 'Arial Black'}),
                                            ], style={'margin-bottom': '2px'}),
                                        ],
                                        style={
                                            'background': '#262626',
                                            'color': '#FFFFFF',
                                            'padding': '10px',
                                            'border-radius': '25px',
                                            'width': '100%',  # Adjusted width
                                            'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                            'display': 'flex',
                                            'flex-direction': 'column',
                                            'align-items': 'center',
                                            'text-align': 'center'
                                        }
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            [
                                                                html.Span('Target Profit',),
                                                            ],
                                                                # style={
                                                                #     # 'align-self': 'flex-end',
                                                                #     # 'text-align': 'center'
                                                                # }
                                                            style={'margin-bottom': '2px', 
                                                                   'vertical-align': 'bottom',
                                                                   'horizontal-align':'center',
                                                                   'margin-top': '24px'}
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.Strong(id='profit_value'),
                                                            ],
                                                            # style={
                                                            #         'margin-bottom': '2px', 
                                                            #         'text-align': 'center',
                                                            #         'flex-grow': '1',
                                                            #         'display': 'flex',
                                                            #         'align-items': 'center',
                                                            #         'justify-content': 'center'
                                                            #     }
                                                            style={'margin-bottom': '2px', 
                                                                   'vertical-align': 'center',
                                                                   'horizontal-align':'center'}
                                                        ),
                                                    ],
                                                    style={
                                                        'background': '#275317',
                                                        'color': '#FFFFFF',
                                                        'padding': '10px',
                                                        'border-radius': '25px',
                                                        'width': '100%',
                                                        'height': '130px',
                                                        'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                                        'display': 'flex',
                                                        'flex-direction': 'column',
                                                        'align-items': 'center',
                                                        'text-align': 'center',
                                                    }
                                                ),
                                                width=6
                                            ),
                                            dbc.Col(
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            [
                                                                html.Span('Remaining Budget',),
                                                            ],
                                                                # style={
                                                                #     # 'align-self': 'flex-end',
                                                                #     # 'text-align': 'center'
                                                                # }
                                                            style={'margin-bottom': '2px', 
                                                                   'vertical-align': 'bottom',
                                                                   'horizontal-align':'center',
                                                                   'margin-top': '24px'}
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.Strong(id='remaining_budget_value'),
                                                            ],
                                                            # style={
                                                            #         'margin-bottom': '2px', 
                                                            #         'text-align': 'center',
                                                            #         'flex-grow': '1',
                                                            #         'display': 'flex',
                                                            #         'align-items': 'center',
                                                            #         'justify-content': 'center'
                                                            #     }
                                                            style={'margin-bottom': '2px', 
                                                                   'vertical-align': 'center',
                                                                   'horizontal-align':'center'}
                                                        ),
                                                    ],
                                                    style={
                                                        'background': '#275317',
                                                        'color': '#FFFFFF',
                                                        'padding': '10px',
                                                        'border-radius': '25px',
                                                        'width': '100%',
                                                        'height': '130px',
                                                        'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                                        'display': 'flex',
                                                        'flex-direction': 'column',
                                                        'align-items': 'center',
                                                        'text-align': 'center',
                                                    }
                                                ),
                                                width=6
                                            ),
                                            # dbc.Col(
                                            #     html.Div(
                                            #         children=[
                                            #             html.Div(
                                            #                 [
                                            #                     html.Span('Profit at Completion',),
                                            #                 ],
                                            #                     # style={
                                            #                     #     # 'align-self': 'flex-end',
                                            #                     #     # 'text-align': 'center'
                                            #                     # }
                                            #                 style={'margin-bottom': '2px', 
                                            #                        'vertical-align': 'bottom',
                                            #                        'horizontal-align':'center'}
                                            #             ),
                                            #             html.Div(
                                            #                 [
                                            #                     html.Strong(id='at_completion_value'),
                                            #                 ],
                                            #                 # style={
                                            #                 #         'margin-bottom': '2px', 
                                            #                 #         'text-align': 'center',
                                            #                 #         'flex-grow': '1',
                                            #                 #         'display': 'flex',
                                            #                 #         'align-items': 'center',
                                            #                 #         'justify-content': 'center'
                                            #                 #     }
                                            #                 style={'margin-bottom': '2px', 
                                            #                        'vertical-align': 'center',
                                            #                        'horizontal-align':'center'}
                                            #             ),
                                            #         ],
                                            #         style={
                                            #             'background': '#275317',
                                            #             'color': '#FFFFFF',
                                            #             'padding': '10px',
                                            #             'border-radius': '25px',
                                            #             'width': '100%',
                                            #             'height': '130px',
                                            #             'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                            #             'display': 'flex',
                                            #             'flex-direction': 'column',
                                            #             'align-items': 'center',
                                            #             'text-align': 'center',
                                            #         }
                                            #     ),
                                            #     width=4
                                            # ),
                                        ],
                                        style={'padding': '10px'} 
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    id='main_items_container',
                                                    children=[
                                                        html.Div(
                                                            id='main_items',
                                                            children=[
                                                                html.Table([
                                                                    html.Thead([
                                                                        html.Tr([
                                                                            html.Th("MAIN ITEMS", 
                                                                                    style={'width': '50%','font-family': 'Arial Black'}),
                                                                            html.Th("BUDGET", 
                                                                                    style={'width': '25%','font-family': 'Arial Black'}),
                                                                            html.Th("TOTAL SPENT", 
                                                                                    style={'width': '25%','font-family': 'Arial Black'})
                                                                        ])
                                                                    ]),
                                                                    html.Tbody(id='main_items_table_body')
                                                                ],
                                                                )
                                                            ],
                                                            style={
                                                                'background': '#FFFFFF',
                                                                'color': 'FFFFFF',
                                                                'padding': '20px',
                                                                'border-radius': '25px',
                                                                'width': '100%',
                                                                'height': '200px',
                                                                'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                                                'display': 'flex',
                                                                'flex-direction': 'column',
                                                                'align-items': 'flex-center'
                                                            }
                                                        )
                                                    ],
                                                ),
                                                width=12
                                            ),
                                        ],
                                        style={'padding': '10px'}
                                    ),
                                ],
                                width=4  
                            ),
                            dbc.Col(
                                [
                                html.Div(
                                    children=[
                                        html.Div([
                                            html.Strong('MONTHLY PROJECT EXPENSE', 
                                                        style={'font-family': 'Arial Black'}),
                                        ], style={'margin-bottom': '2px'}),
                                        
                                    ],
                                    style={
                                        'background': '#262626',
                                        'color': '#FFFFFF',
                                        'padding': '10px',
                                        'border-radius': '25px',
                                        'width': '100%',  # Adjusted width
                                        # 'height': '100%',
                                        'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                        'display': 'flex',
                                        'flex-direction': 'column',
                                        'align-items': 'center',
                                        'text-align': 'center'
                                        }
                                    ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Col(
                                                html.Div(
                                                    children=[
                                                        dcc.Graph(id='project_schedule_graph',
                                                                   style={'width': '2000%',
                                                                          'height': '120%',})
                                                    ],
                                                    style={
                                                        'background': '#FFFFFF',
                                                        'color': '#FFFFFF',
                                                        'padding': '0px',
                                                        'border-radius': '25px',
                                                        'width': '100%',
                                                        'height': '350px',
                                                        'box-shadow': '0px 3px 5px rgba(0, 0, 0, 0.1)',
                                                        'display': 'flex',
                                                        # 'flex-direction': 'column',
                                                        # 'justify-content': 'center',
                                                        'align-items': 'flex-end',
                                                        # 'text-align': 'center',
                                                        'overflow': 'hidden',
                                                        'border': '4px solid #262626',
                                                    }
                                                ),
                                                width=12
                                            ),
                                            width=12 
                                        ), 
                                    ],
                                    style={'padding': '10px'} 
                                ),
                                ],
                                width=4
                            )
                        ],
                    style={'padding': '10px'}
                )
            ]
        ),
    ]
)

# Dropdown for project list
@app.callback(
    Output('constrained_project_dropdown', 'options'),

    Output('edit-button', 'style'),

    [Input('url', 'pathname')],
    State('currentuserid', 'data'),
    State('currentrole', 'data')
)
def constrained_projectprofile_dropdown(pathname, userid, userrole):
    if pathname == '/project_overview':

        if userrole == 'manager':
            sql = """
            SELECT projectid, projectname
            FROM projects 
            WHERE delete_pj_ind = False
            """

            values = []
            edit_button = {'transform': 'scale(1.0)',
                            'margin-left': '5px',
                            'padding-top': '5px',
                            'width':'25%', 'display': 'block'}

        elif userrole == 'pj_ic':
            sql = """
            SELECT projectid, projectname
            FROM projects 
            WHERE userID = %s AND delete_pj_ind = False
            """
            values = [userid]
            edit_button = {'display': 'none'}

        cols = ['projectid', 'projectname']
        df = db.querydatafromdatabase(sql, values, cols)        
        # project_list = df.sort_values('projectid').to_dict('records')
        # print('df' , df)

        # # Format the options for the dropdown
        # options = [{'label': f"{row['projectid']} - {row['projectname']}", 'value': row['projectid']} for row in project_list]

        df_sorted = df.sort_values('projectid')

        # Format the options for the dropdown
        options = [{'label': f"{row['projectid']} - {row['projectname']}", 'value': row['projectid']} for _, row in df_sorted.iterrows()]

        return options, edit_button

    else:
        raise PreventUpdate

# Graph Generation
def generate_project_schedule_graph(start_date, end_date, total_budget, df_monthly_expenses):
    # Convert start_date and end_date to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Generate the date range with monthly frequency
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    num_months = len(date_range)
    
    # Calculate the monthly budget
    monthly_budget = total_budget / num_months

    # Create a DataFrame for the monthly budget
    df_budget = pd.DataFrame({
        'date': date_range,
        'monthly_budget': [monthly_budget] * num_months
    })

    # Prepare the monthly expenses DataFrame
    df_monthly_expenses['date'] = pd.to_datetime(df_monthly_expenses['expenseyear'].astype(str) + '-' + df_monthly_expenses['expensemonth'].astype(str) + '-01')
    df_monthly_expenses = df_monthly_expenses.set_index('date').reindex(date_range).fillna(0).reset_index()

    # Create the figure
    fig = go.Figure()

    # Add the line plot for the monthly budget
    fig.add_trace(go.Scatter(
        x=df_budget['date'],
        y=df_budget['monthly_budget'],
        mode='lines',
        name='Monthly Budget',
        line=dict(color='blue')
    ))

    # Add the bar plot for the monthly expenses
    fig.add_trace(go.Bar(
        x=df_monthly_expenses['index'],
        y=df_monthly_expenses['monthly_expense'],
        name='Monthly Expenses',
        marker=dict(color='#275317') #FFFFFF 275317
    ))

    # Update the layout
    fig.update_layout(
        title=None,
        xaxis_title='Project Schedule (Monthly)',
        yaxis_title='Amount (PHP)',
        barmode='overlay',
        bargap=0.1,
        legend=dict(
            x=0.56,  # Adjust the x position
            y=0.99,  # Adjust the y position
            bgcolor='rgba(0, 0, 0, 0)', 
            bordercolor='rgba(0, 0, 0, 0)',  
            borderwidth=1,
            font=dict(size=8)  
        ),
        plot_bgcolor='#FFFFFF',  
        paper_bgcolor='rgba(255, 255, 255, 0)' 
    )

    return fig

# Show project profile based on selected project
@app.callback(
    [
        Output('project_name', 'children'),
        Output('contract_amount', 'children'),
        Output('budget_amount', 'children'),
        Output('scope', 'children'),
        Output('location', 'children'),
        Output('client', 'children'),
        Output('start_date', 'children'),
        Output('end_date', 'children'),

        # COMMERCIAL OVERVIEW
        Output('profit_value', 'children'),
        Output('remaining_budget_value', 'children'),
        Output('main_items', 'children'),

        # OPERATING STATEMENT
        Output('project_schedule_graph', 'figure'),

        # EDIT BUTTON
        Output('edit-link', 'href'),
    ],
    [
        Input('constrained_project_dropdown', 'value'),
        # Input('url', 'pathname')
    ]
)
def load_project_profile(project_id):
    # print('project id: ', project_id)
    outputs = 13

    if project_id:
        # SQL query to fetch project profile data
        sql = """
            SELECT 
                p.projectName,
                p.amount,
                COALESCE(SUM(b.quantity * b.quotation), 0) AS budget_amount,
                p.scope,
                p.location,
                p.client,
                p.start_date,
                p.end_date
            FROM 
                Projects p
            LEFT JOIN 
                UserProjectBudget upb ON p.projectID = upb.projectID
            LEFT JOIN 
                Budget b ON upb.budgetID = b.budgetID
            WHERE 
                p.projectID = %s AND NOT p.delete_pj_ind
            GROUP BY 
                p.projectID, p.projectName, p.amount, p.scope, p.location, p.client, p.start_date, p.end_date
        """

        values = [project_id]
        cols = ["projectName", "amount", "budget_amount", "scope", "location", "client", "start_date", "end_date"]

        df_project_profile  = db.querydatafromdatabase(sql, values, cols)
        print('df_project_profile: ', df_project_profile)

        if not df_project_profile.empty:
            project_info = df_project_profile.iloc[0]

            # SQL query to fetch total expenses
            sql_expenses = """
                SELECT 
                    COALESCE(SUM(e.quantity * e.price), 0) AS total_expenses
                FROM 
                    Expense e
                JOIN 
                    ProjectExpense pe ON e.expenseID = pe.expenseID
                WHERE 
                    pe.projectID = %s
            """

            cols_expenses = ["total_expenses"]

            df_expenses = db.querydatafromdatabase(sql_expenses, values, cols_expenses)

            if not df_expenses.empty:
                total_expenses = df_expenses.iloc[0]['total_expenses']
            else:
                total_expenses = 0

            remaining_budget = project_info['budget_amount'] - total_expenses
            target_profit = project_info['amount'] - project_info['budget_amount']

            # print('remaining budget:',remaining_budget)

            # SQL to fetch monthly expenses
            sql_monthly_expenses = """
                SELECT 
                    expenseyear, 
                    expensemonth, 
                    SUM(quantity * price) AS monthly_expense
                FROM 
                    Expense e
                JOIN 
                    ProjectExpense pe ON e.expenseID = pe.expenseID
                WHERE 
                    pe.projectID = %s
                GROUP BY 
                    expenseyear, expensemonth
                ORDER BY 
                    expenseyear, expensemonth
            """

            cols_monthly_expenses = ["expenseyear", "expensemonth", "monthly_expense"]

            df_monthly_expenses = db.querydatafromdatabase(sql_monthly_expenses, values, cols_monthly_expenses)

            # Generate the graph
            fig = generate_project_schedule_graph(project_info['start_date'], project_info['end_date'], project_info['budget_amount'], df_monthly_expenses)
            # fig = None

            # SQL to fetch top 5 main items of project
            sql_top5_items = """
                SELECT
                    b.itemID,
                    i.itemName,
                    COALESCE(SUM(b.quantity * b.quotation), 0) AS item_budget,
                    COALESCE(SUM(e.quantity * e.price), 0) AS total_spent
                FROM
                    Budget b
                LEFT JOIN
                    Expense e ON b.itemID = e.itemID
                LEFT JOIN
                    Items i ON b.itemID = i.itemID
                WHERE
                    b.budgetID IN (
                        SELECT
                            budgetID
                        FROM
                            UserProjectBudget
                        WHERE
                            projectID = %s
                    )
                GROUP BY
                    b.itemID, i.itemName
                ORDER BY
                    item_budget DESC
                LIMIT 5
            """

            cols_top5_items = ["itemID", "itemName", "item_budget", "total_spent"]

            df_top5_items = db.querydatafromdatabase(sql_top5_items, values, cols_top5_items)
            # print('df_top5_items: ', df_top5_items)

            top5_items = []
            for _, row in df_top5_items.iterrows():
                item_budget = row["item_budget"]
                total_spent = row["total_spent"]

                if item_budget >= 1000000:  # 1 million
                    item_budget_rounded = f"{item_budget / 1000000:.0f}M"
                elif item_budget >= 1000:  # 1 thousand
                    item_budget_rounded = f"{item_budget / 1000:.0f}K"
                else:
                    item_budget_rounded = f"{item_budget:.2f}"

                if total_spent >= 1000000:  # 1 million
                    total_spent_rounded = f"{total_spent / 1000000:.0f}M"
                elif total_spent >= 1000:  # 1 thousand
                    total_spent_rounded = f"{total_spent / 1000:.0f}K"
                else:
                    total_spent_rounded = f"{total_spent:.2f}"

                top5_items.append({
                    "itemName": row["itemName"],
                    "itemBudget": item_budget_rounded,
                    "totalSpent": total_spent_rounded
                })

            # Construct table rows for top5_items
            table_rows = [
                html.Tr([
                    html.Td(item["itemName"]),
                    html.Td(item["itemBudget"]),
                    html.Td(item["totalSpent"])
                ])
                for item in top5_items
            ]

            # Update main_items with the table rows
            main_items = html.Table(
                            [
                                html.Thead(
                                    [
                                        html.Tr(
                                            [
                                                html.Th("MAIN ITEMS", style={"width": "50%", 'font-family': 'Arial Black'}),
                                                html.Th("BUDGET", style={"width": "25%", 'font-family': 'Arial Black'}),
                                                html.Th("TOTAL SPENT", style={"width": "25%", 'font-family': 'Arial Black'}),
                                            ]
                                        )
                                    ]
                                ),
                                html.Tbody(table_rows),
                            ],
                            style={"border-collapse": "collapse"},
                        )

            # Update button
            href=f'/manage_manager?mode=edit&id={project_id}'

            return [
                project_info['projectName'],
                f"PHP {project_info['amount']:,.2f}",
                f"PHP {project_info['budget_amount']:,.2f}",
                project_info['scope'],
                project_info['location'],
                project_info['client'],
                project_info['start_date'],
                project_info['end_date'],
                f"PHP {target_profit:,.2f}",
                f"PHP {remaining_budget:,.2f}",
                main_items,
                fig,
                href
            ]
        
        else:
            return ['' for _ in range(outputs)]
        
    # elif not project_id:
    #     return ['' for _ in range(outputs)]
    
    else:
        # Blank if the dropdown is empty
        # return ['' for _ in range(outputs)]
        PreventUpdate 
