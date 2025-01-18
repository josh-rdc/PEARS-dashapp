from dash import html


layout = html.Div(
    [
        html.H2('Welcome to the PEARS!'),
        html.Hr(),
        
        # Overview Page
        html.Div(
            [
                html.H3('Overview Page'),
                html.Div(
                    [
                        html.H4('Project Profile'),
                        html.P('Displays project name, contract amount, total budgeted amount, scope, location, client, start and end date.'),
                        html.Br(),
                        html.H4('Commercial Management Overview'),
                        html.Ul(
                            [
                                html.Li('Target Profit: Shows the difference between the total contract amount and the budgeted amount, providing an estimate of the project’s profit margin.'),
                                html.Li('Remaining Budget: Indicates the total budgeted amount minus the current total running expenses, helping forecast the final profit.'),
                                html.Li('Main Items: Lists the top five items with the highest allotted budget and their current running total expenses for effective monitoring.'),
                            ]
                        ),
                        html.Br(),
                        html.H4('Monthly Project Expense'),
                        html.P('Compares planned expenses (total budget divided by the number of months) with actual monthly expenses on.'),
                    ]
                )
            ]
        ),
        
        html.Hr(),

        # Adding a Project
        html.Div(
            [
                html.H3('Adding a Project'),
                html.P('Note: Only TM accounts can add new projects.'),
                html.Ol(
                    [
                        html.Li('Click the “ADD” button to open the project creation interface.'),
                        html.Li('Fill in the basic project details: project name, contract amount, scope, location, client name, and schedule.'),
                        html.Li('Assign a project In-Charge from a drop-down list of users.'),
                        html.Li('Ensure all non-null fields are completed to avoid errors.'),
                    ]
                ),
            ]
        ),
        
        html.Hr(),

        # Adding Project Data (Budget and Expense)
        html.Div(
            [
                html.H3('Adding Project Data (Budget and Expense)'),
                html.Div(
                    [
                        html.H4('General Interface'),
                        html.Ol(
                            [
                                html.Li('Access the "MANAGE" tab from the navigation bar.'),
                                html.Li('Select the project to manage from the project form.'),
                                html.Li('Note: TM accounts can edit data for all projects. PIC accounts can only edit their assigned projects.'),
                            ]
                        ),
                        html.Br(),
                        html.H4('Budget Mode'),
                        html.Ol(
                            [
                                html.Li('Toggle to “Budget” mode.'),
                                html.Li('Enter budget data directly into the table or upload a CSV file.'),
                                html.Li('Based on needed action, table contents could be cleared or saved to the project budget.'),
                            ]
                        ),
                        html.Br(),
                        html.H4('Expense Mode'),
                        html.Ol(
                            [
                                html.Li('Toggle to “Expense” mode.'),
                                html.Li('Enter expenses into the table or upload a CSV file.'),
                                html.Li('Based on needed action, table contents could be cleared or saved to the project expenses.'),
                                html.Li('Ensure expenses are budgeted and item names match the budget exactly!'),
                            ]
                        ),
                    ]
                )
            ]
        ),
    ]
)