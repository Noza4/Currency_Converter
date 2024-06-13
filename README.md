# Currency_Converter

Overview
This project is a Currency Converter application that uses the freecurrencyapi to fetch up-to-date exchange rate information. It collects user personal information and transaction details, and stores them in a SQL Server Management Studio (SSMS) database. The project demonstrates how to integrate an external API with a local database for a complete data-driven application.

Features
Fetches current exchange rates using the freecurrencyapi.
Saves user personal information in the database.
Records transaction details including currency, quantity, and overall value.
Connects to a local SQL Server database using Python and pyodbc.
Simple command-line interface for user interaction.
Prerequisites
Python 3.x
SQL Server and SQL Server Management Studio (SSMS)
freecurrencyapi API key
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/currency-converter.git
cd currency-converter
Install required Python packages:

bash
Copy code
pip install pyodbc requests
Set up SQL Server:

Download and install SQL Server from Microsoft's official site.
Download and install SQL Server Management Studio (SSMS) from Microsoft's official site.
Configure Database:

Open SSMS and run the following SQL script to create the database and tables:

sql
Copy code
-- Create the database
CREATE DATABASE Converter_db;
GO

-- Switch to the newly created database
USE Converter_db;
GO

-- Create user table
CREATE TABLE dbo.[user] (
    Customer_ID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Personal_ID NVARCHAR(50) NOT NULL UNIQUE
);
GO

-- Create transaction table
CREATE TABLE dbo.[transaction] (
    Transaction_ID INT IDENTITY(1,1) PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Currency NVARCHAR(3) NOT NULL,
    Quantity FLOAT NOT NULL,
    Overall FLOAT NOT NULL,
    Date DATETIME NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES dbo.[user](Customer_ID)
);
GO
Set up API Key:

Obtain your freecurrencyapi API key from here.
Store your API key in a .env file or directly in the script.
Usage
Run the application:

bash
Copy code
python converter.py
Follow the prompts:

Enter user details (name, last name, personal ID).
Enter transaction details (currency, quantity, etc.).
Code Overview
The main functionality is divided into several parts:

converter.py
Handles user interaction, fetching exchange rates, and saving data to the database.

python
Copy code
from datetime import datetime
import pyodbc
import requests
import os

# Load API key from environment or hardcode it here
API_KEY = os.getenv('FREECURRENCYAPI_KEY', 'your_api_key_here')

# Database connection string
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=Nika\SQLEXPRESS;'   # Replace with your server name
    r'DATABASE=Converter_db;'    # Ensure this matches your database name
    r'Trusted_Connection=yes;'
)

def get_exchange_rate(currency):
    url = f"https://freecurrencyapi.net/api/v1/rates?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if currency in data['data']:
        return data['data'][currency]
    else:
        raise ValueError("Invalid currency code")

def create_database_and_tables():
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=Nika\SQLEXPRESS;'   # Replace with your server name
        r'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    cursor.execute("IF DB_ID('Converter_db') IS NULL CREATE DATABASE Converter_db")
    cursor.commit()

    conn.close()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("""
    IF OBJECT_ID('dbo.[user]', 'U') IS NULL
    CREATE TABLE dbo.[user] (
        Customer_ID INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(50) NOT NULL,
        LastName NVARCHAR(50) NOT NULL,
        Personal_ID NVARCHAR(50) NOT NULL UNIQUE
    )
    """)
    cursor.commit()

    cursor.execute("""
    IF OBJECT_ID('dbo.[transaction]', 'U') IS NULL
    CREATE TABLE dbo.[transaction] (
        Transaction_ID INT IDENTITY(1,1) PRIMARY KEY,
        Customer_ID INT NOT NULL,
        Currency NVARCHAR(3) NOT NULL,
        Quantity FLOAT NOT NULL,
        Overall FLOAT NOT NULL,
        Date DATETIME NOT NULL,
        FOREIGN KEY (Customer_ID) REFERENCES dbo.[user](Customer_ID)
    )
    """)
    cursor.commit()

    cursor.close()
    conn.close()
    
def save_user(name, lname, p_num):

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    insert = """
    INSERT INTO dbo.[user] (Name, LastName, Personal_ID)
    VALUES (?, ?, ?)
    """
    cursor.execute(insert, (name, lname, p_num))
    conn.commit()

    print("User Added Successfully")

    cursor.close()
    conn.close()

def search_user(p_num):

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    search = """
    SELECT * FROM dbo.[user] WHERE Personal_ID = ?
    """
    cursor.execute(search, (p_num,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return len(data) > 0

def save_transaction(p_num, curr, quantity, get):

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    search = """
    SELECT Customer_ID FROM dbo.[user] WHERE Personal_ID = ?
    """
    cursor.execute(search, (p_num,))
    user = cursor.fetchone()

    if user is None:
        print("User not found.")
        cursor.close()
        conn.close()
        return

    customer_id = user[0]
    insert = """
    INSERT INTO dbo.[transaction] (Customer_ID, Currency, Quantity, Overall, Date)
    VALUES (?, ?, ?, ?, ?)
    """
    date = datetime.today()
    cursor.execute(insert, (customer_id, curr, quantity, get, date))
    conn.commit()

    print("Transaction Added Successfully")

    cursor.close()
    conn.close()

# Run this first to create database and tables
create_database_and_tables()

# Example usage
p_number = 'your_personal_id'
w_curr = 'USD'
quantity = 100
get = 150.0

save_user('John', 'Doe', p_number)
save_transaction(p_number, w_curr, quantity, get)
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Please read CONTRIBUTING.md for the process for submitting pull requests to us.

Acknowledgments
Thanks to freecurrencyapi for providing the exchange rate API.
Special thanks to everyone who has contributed to this project.






