import sqlite3
import threading

# Function to create databases and tables
def create_databases():
    # Create Users database
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        conn.commit()

    # Create Products database
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        conn.commit()

    # Create Orders database
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        conn.commit()

    print("Databases and tables created successfully.")

# Function to insert data into Users table
def insert_users():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        users_data = [
            ("Alice", "alice@example.com"),
            ("Bob", "bob@example.com"),
            ("Charlie", "charlie@example.com"),
            ("David", "david@example.com"),
            ("Eve", "eve@example.com"),
            ("Frank", "frank@example.com"),
            ("Grace", "grace@example.com"),
            ("Alice", "alice@example.com"),
            ("Henry", "henry@example.com"),
            ("Jane", "jane@example.com"),
        ]
        cursor.executemany("INSERT INTO Users (name, email) VALUES (?, ?)", users_data)
        conn.commit()

# Function to insert data into Products table
def insert_products():
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        products_data = [
            ("Laptop", 1000.00),
            ("Smartphone", 700.00),
            ("Headphones", 150.00),
            ("Monitor", 300.00),
            ("Keyboard", 50.00),
            ("Mouse", 30.00),
            ("Laptop", 1000.00),
            ("Smartwatch", 250.00),
            ("Gaming Chair", 500.00),
            ("Earbuds", -50.00),
        ]
        cursor.executemany("INSERT INTO Products (name, price) VALUES (?, ?)", products_data)
        conn.commit()

# Function to insert data into Orders table
def insert_orders():
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        orders_data = [
            (1, 1, 2),  # user_id, product_id, quantity
            (2, 2, 1),
            (3, 3, 5),
            (4, 4, 1),
            (5, 5, 3),
            (6, 6, 4),
            (7, 7, 2),
            (8, 8, 0),
            (9, 9, -1),
            (10, 10, 2),
        ]
        cursor.executemany("INSERT INTO Orders (user_id, product_id, quantity) VALUES (?, ?, ?)", orders_data)
        conn.commit()

# Function to run all insertions concurrently using threads
def insert_data_concurrently():
    threads = []

    # Create threads for each insertion task
    threads.append(threading.Thread(target=insert_users))
    threads.append(threading.Thread(target=insert_products))
    threads.append(threading.Thread(target=insert_orders))

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All data inserted successfully using concurrent threads.")

# Function to fetch and display data from Users, Products, and Orders tables
def fetch_and_display_data():
    # Fetch and display data from Users table
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        print("Users:")
        for user in users:
            print(user)

    # Fetch and display data from Products table
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        print("\nProducts:")
        for product in products:
            print(product)

    # Fetch and display data from Orders table
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        orders = cursor.fetchall()
        print("\nOrders:")
        for order in orders:
            print(order)

# Call this function to display the data
if __name__ == "__main__":
    create_databases()
    insert_data_concurrently()
    fetch_and_display_data()