import os
import mysql.connector

# Function to connect to MySQL database

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        username="root",   # Replace with your MySQL username
        password="03april2008",   # Replace with your MySQL password
        database="shopping"   # Replace with your database name
    )

# Clear screen function

def clear_screen():
    os.system('cls')

# Center-aligned print function

def center_print(text):
    print(text.center(60))

#Functions defined for Admin Page
#Function to add a new product

def add_product(cursor, connection):
    center_print("=== Add New Product ===")

    name = input("Enter product name: ")
    category = input("Enter product category: ")
    price = float(input("Enter product price: "))
    stock_qty = int(input("Enter product stock quantity: "))

    # SQL query to insert product
    sql = "INSERT INTO products (name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)"
    values = (name, category, price, stock_qty)

    cursor.execute(sql, values)
    connection.commit()

    center_print("Product '" + name + "' added successfully.")
    input("Press enter to continue...")

def update_product(cursor, connection):
    center_print("=== Update Product ===")
    product_id = int(input("Enter product ID to update: "))

    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        clear_screen()
        center_print("Product not found.")
        return

    center_print("Current details: Name = " + product[1] + ", Category = " + product[2] +", Price = " + str(product[3]) + ", Stock = " + str(product[4]))

    # Input new values (skip if empty)
    name = input("Enter new name (press enter to skip): ") or product[1]
    category = input("Enter new category (press enter to skip): ") or product[2]
    price = input("Enter new price (press enter to skip): ") or product[3]
    stock_quantity = input("Enter new stock quantity (press enter to skip): ") or product[4]

    # SQL query to update product
    sql = "UPDATE products SET name = %s, category = %s, price = %s, stock_quantity = %s WHERE product_id = %s"
    values = (name, category, price, stock_quantity, product_id)

    cursor.execute(sql, values)
    connection.commit()


    center_print("Product ID '" + str(product_id) + "' updated successfully.")
    input("Press enter to continue...")


def delete_product(cursor, connection):
    center_print("=== Delete Product ===")
    product_id = int(input("Enter product ID to delete: "))

    # SQL query to delete product
    sql = "DELETE FROM products WHERE product_id = %s"

    cursor.execute(sql, (product_id,))
    connection.commit()


    center_print("Product ID '" + str(product_id) + "' deleted successfully.")
    input("Press enter to continue...")


def view_products(cursor):
    center_print("=== Available Products ===")
    print()
    print("ID".ljust(5) + "Name".ljust(20) + "Category".ljust(15) + "Price".ljust(10) + "Stock".ljust(10))
    print("-" * 60)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if not products:
        center_print("No products available.")
        return

    for product in products:
        product_id = str(product[0]).ljust(5)
        name = product[1].ljust(20)
        category = product[2].ljust(15)
        price = str(product[3]).ljust(10)
        stock = str(product[4]).ljust(10)

        print(product_id + name + category + price + stock)

    input("\nPress Enter to continue...")


def admin_menu(cursor, connection):
    while True:
        clear_screen()
        center_print("--- Admin Menu ---")
        center_print("1. Add Product")
        center_print("2. Update Product")
        center_print("3. Delete Product")
        center_print("4. View Products")
        center_print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_product(cursor, connection)
        elif choice == "2":
            update_product(cursor, connection)
        elif choice == "3":
            delete_product(cursor, connection)
        elif choice == "4":
            view_products(cursor)
        elif choice == "5":
            break
        else:
            center_print("Invalid choice. Please try again.")



# Functions defined for Customer page

cart = [] #Empty List for Cart

def view_products_customer(cursor):
    print()
    center_print("=== Available Products ===")
    print()

    print("ID".ljust(5) + "Name".ljust(20) + "Category".ljust(15) + "Price".ljust(10) )
    print("-" * 60)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    # Display each product
    for product in products:
        product_id = str(product[0]).ljust(5)
        name = product[1].ljust(20)
        category = product[2].ljust(15)
        price = str(product[3]).ljust(10)

        print(product_id + name + category + price )

    input("\nPress Enter to continue...")


def add_to_cart(cursor):
    clear_screen()
    view_products_customer(cursor)  # Show available products
    while True:

        product_id = int(input("Enter the product ID to add to cart: "))
        quantity = int(input("Enter the quantity: "))

        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            center_print("Product not found.")
            input("Press Enter to continue...")
            continue  # Ask for product ID again

        # Check if product is available in stock
        if quantity > product[4]:
            center_print("Not enough stock available.")
            input("Press Enter to continue...")
            continue  # Ask for product ID again

        # Add product to cart
        cart.append({"product_id": product_id, "name": product[1], "price": product[3], "quantity": quantity})
        center_print("Added '" + str(quantity) + "' of '" + product[1] + "' to cart.")

        ask = input("Do you want to add more items? (yes/no): ").strip().lower()
        if ask != 'yes':
            break  # Exit the loop if the user does not want to add more items

    # Final message before returning to the menu
    input("Press Enter to return to the menu...")


def view_cart():
    print()
    center_print("=== Your Shopping Cart ===")

    if not cart:
        center_print("Your cart is empty.")
        input("Press Enter to continue...")
        return

    # Column headers
    print("ID".ljust(5) + "Name".ljust(20) + "Price".ljust(10) + "Quantity".ljust(10))
    print("-" * 55)

    # Display each item in the cart
    for index, item in enumerate(cart):
        product_id = str(index + 1).ljust(5)  # Assuming ID starts from 1 for display
        name = item["name"].ljust(20)
        price = str(item["price"]).ljust(10)
        quantity = str(item["quantity"]).ljust(10)

        print(product_id + name + price + quantity)

    input("\nPress Enter to continue...")

def checkout():
    print()
    center_print("=== Checkout ===")

    if not cart:
        center_print("Your cart is empty. Cannot checkout.")
        input("Press Enter to continue...")
        return

    # Display the cart items first
    view_cart()  # Display the entire cart before proceeding to checkout

    total_price = sum(item["price"] * item["quantity"] for item in cart)

    center_print("Total Price: " + str(total_price) + " Rs")
    confirm = input("Confirm checkout? (yes/no): ").strip().lower()

    if confirm == "yes":
        cart.clear()  # Clear the cart after successful checkout
        center_print("Checkout successful. Thank you for your purchase!")
    else:
        center_print("Checkout cancelled.")

    input("Press Enter to return to the menu...")

def customer_menu(cursor):
    while True:
        clear_screen()
        center_print("--- Customer Menu ---")
        center_print("1. View Products")
        center_print("2. Add to Cart")
        center_print("3. View Cart")
        center_print("4. Checkout")
        center_print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_products_customer(cursor)
        elif choice == "2":
            add_to_cart(cursor)
        elif choice == "3":
            view_cart()
        elif choice == "4":
            checkout()
        elif choice == "5":
            break
        else:
            center_print("Invalid choice. Please try again.")


#Function for welcome page and login

def admin_login():
    # Admin login credentials
    admin_username = "admin"
    admin_password = "admin123"

    clear_screen()
    center_print("=== Admin Login ===")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == admin_username and password == admin_password:
        center_print("Login successful!")
        input("Press Enter to continue...")
        return True
    else:
        center_print("Invalid username or password.")
        input("Press Enter to return to the main menu...")
        return False

def welcome_page():
    clear_screen()
    center_print("===================================")
    center_print(" Welcome to Shopping Management System ")
    center_print("===================================")
    center_print("\n")
    center_print("1. Admin Login")
    center_print("2. Customer Page")
    center_print("3. Exit")

    choice = input("\nEnter your choice: ")
    return choice

def main():
    # Connect to MySQL
    connection = connect_db()
    cursor = connection.cursor()

    while True:
        choice = welcome_page()  # Show welcome page

        if choice == "1":  # Admin Login
            if admin_login():
                admin_menu(cursor, connection)  # If login is successful, enter Admin Menu
        elif choice == "2":  # Customer Page
            customer_menu(cursor)  # Go to customer menu
        elif choice == "3":  # Exit
            break
        else:
            center_print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

    # Close the database connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
