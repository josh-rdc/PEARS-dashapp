# PEARS Dashapp

![Assets/login.png](Assets/login.png)

**Project Expense, Analysis and Reporting System (PEARS)** is a web-based financial management application for small-scale projects and companies. Developed using Python integrated with PostgreSQL, the app enables efficient project cost control by creating a centralized database for multiple projects, allowing users to formulate budgets, track monthly expenses, and ensure financial transparency.

## Installing Locally
To run this project locally, please follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/josh-rdc/PEARS-dashapp
   ```

2. Navigate to the project folder:

   ```
   cd "PEARS-dashapp/App Files"
   ```

3. Install the required libraries:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:

   ```
   streamlit run 🏠_Home.py
   ```

## App Pages
- [Home Page](#home-page)
- [Overview Page](#overview-page)
- [Adding A Project](#adding-a-project)
- [Adding Project Data](#adding-project-data-budget-and-expense)


## Home Page

## Overview Page
### Project Profile

Displays project name, contract amount, total budgeted amount, scope, location, client, start and end date.

---

### Commercial Management Overview

1. **Target Profit**: Shows the difference between the total contract amount and the budgeted amount, providing an estimate of the project’s profit margin.
2. **Remaining Budget**: Indicates the total budgeted amount minus the current total running expenses, helping forecast the final profit.
3. **Main Items**: Lists the top five items with the highest allotted budget and their current running total expenses for effective monitoring.

---

### Monthly Project Expense
Compares planned expenses (total budget divided by the number of months) with actual expenses on a monthly basis.


## Adding A Project
Only TM accounts can add new projects.
1.	Click the “ADD” button to open the project creation interface.
2.	Fill in the basic project details: project name, contract amount, scope, location, client name, and schedule.
3.	Assign a project In-Charge from a drop-down list of users.
4.	Ensure all non-null fields are completed to avoid errors.


## Adding Project Data (Budget and Expense)
### General Interface
1. Access the "MANAGE" tab from the navigation bar.
2. Select the project to manage from the project form.
3. TM accounts can edit data for all projects, while PIC accounts can only edit their assigned projects.

--- 

### Budget Mode
1. Toggle to “Budget” mode.
2. Enter budget data directly into the table or upload a CSV file.
3. Based on needed action, table contents could be cleared or saved to the project budget.

---

### Expense Mode
1. Toggle to “Expense” mode.
2. Enter expenses into the table or upload a CSV file.
3. Based on needed action, table contents could be cleared or saved to the project expenses.
4. Ensure expenses are budgeted and item names match the budget exactly.
