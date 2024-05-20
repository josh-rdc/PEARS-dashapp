CREATE TABLE Users (
    userID int PRIMARY KEY,
    password varchar(256) NOT NULL,
    user_type varchar(128) NOT NULL,
    user_del_ind bool DEFAULT false NOT NULL,
    CONSTRAINT unique_userID UNIQUE (userID)
);

CREATE TABLE UserProjectBudget (
    userID int NOT NULL,
    projectID int NOT NULL,
    budgetID varchar(128),
    modifydate timestamp without time zone DEFAULT now() NOT NULL,
    PRIMARY KEY (userID, projectID)
);

CREATE TABLE ProjectExpense (
    userID int NOT NULL,
    projectID int NOT NULL,
    expenseID int NOT NULL,
    PRIMARY KEY (projectID, expenseID)
);

CREATE TABLE Expense (
    expenseID varchar(128),
    itemID int NOT NULL,
    quantity decimal(10, 2) NOT NULL,
    unit varchar(128) ,
    price decimal(15, 2) NOT NULL
);

CREATE TABLE Projects (
    projectID int NOT NULL,
    projectName varchar(256) NOT NULL,
    userID int NOT Null,
    scope varchar(256),
    location varchar(256),
    client varchar(256),
    amount decimal(15, 2) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    delete_pj_ind bool DEFAULT true NOT NULL ,
    modifydate timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT unique_projectID UNIQUE (projectID)
);

CREATE TABLE Budget (
    budgetID varchar(128),
    itemID int NOT NULL,
    quantity decimal(10, 2) ,
    unit varchar(128) ,
    quotation decimal(15, 2) NOT NULL
);

CREATE TABLE Items (
    itemID SERIAL PRIMARY KEY,
    itemname VARCHAR(256),
    itemdescript VARCHAR(256),
    CONSTRAINT unique_itemname UNIQUE (itemname)
);


 TRUNCATE TABLE genres RESTART IDENTITY CASCADE