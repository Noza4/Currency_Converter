from datetime import datetime

import pyodbc

ls = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP",
      "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN",
      "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB",
      "TRY", "USD", "ZAR"]

id_ls = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


def save_user(name, lname, p_num):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'  # Ensure this matches your installed driver
        r'SERVER=Nika\SQLEXPRESS;'                   # Use a raw string for the server name
        r'DATABASE=Converter_db;'                            # Replace with your actual database name
        r'Trusted_Connection=yes;'                   # Use Windows Authentication if not using this than
                                                     # you need ssms username and password
    )

    conn = pyodbc.connect(conn_str)

    cursor = conn.cursor()

    insert = """
    INSERT INTO dbo.[user] (Name, LastName, Personal_ID)
    VALUES ( ?, ?, ?)
    """

    cursor.execute(insert, name, lname, p_num)

    conn.commit()
    print("Success")

    cursor.close()
    conn.close()


def search_user(p_num):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'      # Ensure this matches your installed driver
        r'SERVER=Nika\SQLEXPRESS;'                      # Use a raw string for the server name
        r'DATABASE=Converter_db;'                       # Replace with your actual database name
        r'Trusted_Connection=yes;'                      # Use Windows Authentication if not using this than
                                                        # you need ssms username and password
    )

    conn = pyodbc.connect(conn_str)

    cursor = conn.cursor()

    search = """
    SELECT * FROM dbo.[user] WHERE Personal_ID = ?
    """

    cursor.execute(search, (p_num,))

    data = cursor.fetchall()

    if len(data) == 0:
        cursor.close()
        conn.close()
        return False
    else:
        cursor.close()
        conn.close()
        return True


def save_transaction(p_num, curr, quantity, get):
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'  # Ensure this matches your installed driver
        r'SERVER=Nika\SQLEXPRESS;'                  # Use a raw string for the server name
        r'DATABASE=Converter_db;'                   # Replace with your actual database name
        r'Trusted_Connection=yes;'                  # Use Windows Authentication if not using this than
                                                    # you need ssms username and password
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    search = """
    SELECT Customer_ID FROM dbo.[user] WHERE Personal_ID = ?
    """

    # Ensure p_num is passed correctly as a tuple
    cursor.execute(search, (p_num,))
    user = cursor.fetchone()

    customer_id = user[0]

    insert = """
    INSERT INTO dbo.[transaction] (Customer_ID, Currency, Quantity, Overall, Date)
    VALUES (?, ?, ?, ?, ?)
    """

    date = datetime.today()

    cursor.execute(insert, (customer_id, curr.upper(), quantity, get, date))

    conn.commit()
    print("Transaction Added Successfully")

    cursor.close()
    conn.close()
