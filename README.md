# PEARS Dashapp

![Assets/login.png](Assets/login.png)

**Project Expense, Analysis and Reporting System (PEARS)** is a web-based financial management application for small-scale projects and companies. Developed using Python integrated with PostgreSQL, the app enables efficient project cost control by creating a centralized database for multiple projects, allowing users to formulate budgets, track monthly expenses, and ensure financial transparency.

<details close>
<summary>Installing Locally</summary>

To run this project locally, please follow these steps:

### Clone the repository:
   ```
   git clone https://github.com/josh-rdc/PEARS-dashapp
   ```

### Database Setup 
1. Ensure **PostgreSQL is installed on your machine**. Follow this [PostgreSQL Tutorial Page](https://neon.tech/postgresql/postgresql-getting-started/install-postgresql).

   Check if the app is installed and added to your environment variables properly by checking its version in the terminal:
   ```
   psql --version
   ```

2. **Create the Database**

   To create the database, log in to your PostgreSQL server:
   ```
   psql -U postgres
   ```

   Run the following command to create the database `PEARSdb`:
   ```
   CREATE DATABASE PEARSdb;
   ```

   Exit the psql shell:
   ```
   \q
   ```

3. **Build the Schema tables**

   Navigate to the `App Files` folder from the cloned repository:
   ```
   cd "C:\Users\Josh\000 Files\010 Portfolio\04 PEARS-dashapp\App Files"
   ```

   Run the following terminal command to create the required tables from the `create_tables.sql` file:
   ```
   psql -U postgres -d PEARSdb -f create_tables.sql
   ```

4. Update the `apps/dbconnect.py` file with your PostgreSQL connection details:
   ```
   db = psycopg2.connect(
    host='localhost',          # Update if running on a different host
    database='PEARSdb',        # Database name
    user='your_username',      # PostgreSQL username
    port=5432,                 # Default PostgreSQL port
    password='your_password'   # PostgreSQL password
   )
   ```

### App Setup
1. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```
   

2. Run the application:
   ```
   python app.py
   ```

</details>

## App Pages
- [Log-in and Home Page](#log-in-and-home-page)
- [Overview Page](#overview-page)
- [Adding A Project](#adding-a-project)
- [Adding Project Data](#adding-project-data-budget-and-expense)

---

### Log-in and Home Page
![Assets/Attachment1.gif](Assets/Attachment1.gif)

Defines the pages, their contents and how to use the features.

--- 

### Overview Page

- **Project Profile** displays project name, contract amount, total budgeted amount, scope, location, client, start and end date.

- **Commercial Management Overview**

   1. **Target Profit**: Shows the difference between the total contract amount and the budgeted amount, providing an estimate of the project’s profit margin.
   2. **Remaining Budget**: Indicates the total budgeted amount minus the current total running expenses, helping forecast the final profit.
   3. **Main Items**: Lists the top five items with the highest allotted budget and their current running total expenses for effective monitoring.

- **Monthly Project Expense** compares planned expenses (total budget divided by the number of months) with actual expenses on a monthly basis.

--- 

### Adding A Project

Only `TM accounts` can add new projects.
1.	Click the “ADD” button to open the project creation interface.
2.	Fill in the basic project details: project name, contract amount, scope, location, client name, and schedule.
3.	Assign a project In-Charge from a drop-down list of users.
4.	Ensure all non-null fields are completed to avoid errors.

--- 

### Adding Project Data (Budget and Expense)

- **General Interface**
1. Access the "MANAGE" tab from the navigation bar.
2. Select the project to manage from the project form.
3. TM accounts can edit data for all projects, while PIC accounts can only edit their assigned projects.

- **Budget Mode**
1. Toggle to `“Budget”` mode.
2. Enter budget data directly into the table or upload a CSV file.
3. Based on needed action, table contents could be cleared or saved to the project budget.

- **Expense Mode**
1. Toggle to `“Expense”` mode.
2. Enter expenses into the table or upload a CSV file.
3. Based on needed action, table contents could be cleared or saved to the project expenses.
4. Ensure expenses are budgeted and item names match the budget exactly.
