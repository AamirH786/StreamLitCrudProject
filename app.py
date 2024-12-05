import streamlit as st
import sqlite3
import pandas as pd

# Function to fetch data from Users table
def fetch_users(name=None):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        if name:
            cursor.execute("SELECT * FROM Users WHERE name LIKE ?", ('%' + name + '%',))
        else:
            cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        return pd.DataFrame(users, columns=["ID", "Name", "Email"])

# Function to fetch data from Products table
def fetch_products(name=None):
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        if name:
            cursor.execute("SELECT * FROM Products WHERE name LIKE ?", ('%' + name + '%',))
        else:
            cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        return pd.DataFrame(products, columns=["ID", "Name", "Price"])

# Function to fetch data from Orders table
def fetch_orders(user_id=None, product_id=None):
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM Orders WHERE user_id = ?", (user_id,))
        elif product_id:
            cursor.execute("SELECT * FROM Orders WHERE product_id = ?", (product_id,))
        else:
            cursor.execute("SELECT * FROM Orders")
        orders = cursor.fetchall()
        return pd.DataFrame(orders, columns=["ID", "User ID", "Product ID", "Quantity"])

# Function to insert data into Users table
def insert_user(name, email):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()

# Function to insert data into Products table
def insert_product(name, price):
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()

# Function to insert data into Orders table
def insert_order(user_id, product_id, quantity):
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Orders (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, quantity))
        conn.commit()

# Function to update data in Users table
def update_user(id, name, email):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Users SET name = ?, email = ? WHERE id = ?", (name, email, id))
        conn.commit()

# Function to update data in Products table
def update_product(id, name, price):
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Products SET name = ?, price = ? WHERE id = ?", (name, price, id))
        conn.commit()

# Function to update data in Orders table
def update_order(id, user_id, product_id, quantity):
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Orders SET user_id = ?, product_id = ?, quantity = ? WHERE id = ?", (user_id, product_id, quantity, id))
        conn.commit()

# Function to delete data from Users table
def delete_user(id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
        conn.commit()

# Function to delete data from Products table
def delete_product(id):
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Products WHERE id = ?", (id,))
        conn.commit()

# Function to delete data from Orders table
def delete_order(id):
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Orders WHERE id = ?", (id,))
        conn.commit()

# Streamlit UI setup
def app():
    st.title("Database Viewer")

    # Sidebar for navigation and actions
    st.sidebar.title("Actions")
    page = st.sidebar.selectbox("Choose a table", ["Users", "Products", "Orders"])

    # Search section
    search_term = st.sidebar.text_input("Search", "")

    # Choose action (Add, Update, Delete)
    action = st.sidebar.radio("Choose an action", ["Add", "Update", "Delete"])

    # Insert data section
    if page == "Users":
        st.header("Users Table")
        if action == "Add":
            st.subheader("Add New User")
            name = st.text_input("Name")
            email = st.text_input("Email")
            if st.button("Add User"):
                if name and email:
                    insert_user(name, email)
                    st.success(f"User {name} added successfully!")
                else:
                    st.error("Please provide both name and email.")
        elif action == "Update":
            st.subheader("Update User")
            user_id = st.number_input("User ID to Update", min_value=1)
            new_name = st.text_input("New Name")
            new_email = st.text_input("New Email")
            if st.button("Update User"):
                if new_name and new_email:
                    update_user(user_id, new_name, new_email)
                    st.success(f"User ID {user_id} updated successfully!")
                else:
                    st.error("Please provide both new name and email.")
        elif action == "Delete":
            st.subheader("Delete User")
            delete_user_id = st.number_input("User ID to Delete", min_value=1)
            if st.button("Delete User"):
                delete_user(delete_user_id)
                st.success(f"User ID {delete_user_id} deleted successfully!")

        # Display users
        users = fetch_users(search_term)
        st.dataframe(users)

    elif page == "Products":
        st.header("Products Table")
        if action == "Add":
            st.subheader("Add New Product")
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0.01, step=0.01)
            if st.button("Add Product"):
                if name and price:
                    insert_product(name, price)
                    st.success(f"Product {name} added successfully!")
                else:
                    st.error("Please provide both product name and price.")
        elif action == "Update":
            st.subheader("Update Product")
            product_id = st.number_input("Product ID to Update", min_value=1)
            new_name = st.text_input("New Product Name")
            new_price = st.number_input("New Price", min_value=0.01, step=0.01)
            if st.button("Update Product"):
                if new_name and new_price:
                    update_product(product_id, new_name, new_price)
                    st.success(f"Product ID {product_id} updated successfully!")
                else:
                    st.error("Please provide both new product name and price.")
        elif action == "Delete":
            st.subheader("Delete Product")
            delete_product_id = st.number_input("Product ID to Delete", min_value=1)
            if st.button("Delete Product"):
                delete_product(delete_product_id)
                st.success(f"Product ID {delete_product_id} deleted successfully!")

        # Display products
        products = fetch_products(search_term)
        st.dataframe(products)

    elif page == "Orders":
        st.header("Orders Table")
        if action == "Add":
            st.subheader("Add New Order")
            user_id = st.number_input("User ID", min_value=1)
            product_id = st.number_input("Product ID", min_value=1)
            quantity = st.number_input("Quantity", min_value=1)
            if st.button("Add Order"):
                if user_id and product_id and quantity:
                    insert_order(user_id, product_id, quantity)
                    st.success(f"Order for user {user_id} and product {product_id} added successfully!")
                else:
                    st.error("Please provide valid user ID, product ID, and quantity.")
        elif action == "Update":
            st.subheader("Update Order")
            order_id = st.number_input("Order ID to Update", min_value=1)
            updated_user_id = st.number_input("Updated User ID", min_value=1)
            updated_product_id = st.number_input("Updated Product ID", min_value=1)
            updated_quantity = st.number_input("Updated Quantity", min_value=1)
            if st.button("Update Order"):
                update_order(order_id, updated_user_id, updated_product_id, updated_quantity)
                st.success(f"Order ID {order_id} updated successfully!")
        elif action == "Delete":
            st.subheader("Delete Order")
            delete_order_id = st.number_input("Order ID to Delete", min_value=1)
            if st.button("Delete Order"):
                delete_order(delete_order_id)
                st.success(f"Order ID {delete_order_id} deleted successfully!")

        # Display orders
        orders = fetch_orders(search_term)
        st.dataframe(orders)

if __name__ == "__main__":
    app()
