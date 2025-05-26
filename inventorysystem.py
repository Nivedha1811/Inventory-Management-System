
import mysql.connector as mariadb


# Connect to MySQL database
try:
    db = mariadb.connect(
        host="localhost",
        user=input("please enter the user name of your account: "),
        password=input("please enter the password: "),
        database="invproj"
    )
except:
    print("Please Enter Correct information or Check if a database named Invproj is present or not. Error Code 1" )
    exit()

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Create inventory table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT,
    price FLOAT
)
"""
cursor.execute(create_table_query)
db.commit()

# Function to display menu options
def display_menu():
    print("===== Inventory Management System =====")
    print("1. Add a product")
    print("2. Add product quantity")
    print("3. Delete a product")
    print("4. Modify a product")
    print("5. View inventory")
    
    print("6. Exit")

# Function to add a product
def add_product():
    try:
        name = input("Enter the product name: ")
        quantity = int(input("Enter the quantity: "))
        price = float(input("Enter the price: "))

        add_product_query = """
        INSERT INTO inventory (product_name, quantity, price)
        VALUES (%s, %s, %s)
        """
        cursor.execute(add_product_query, (name, quantity, price))
        db.commit()
        print("Product added successfully!")
    except:
        print("Please Enter the Required Statement")

# Function to add quantity to an existing product
def add_quantity():
    product_id = int(input("Enter the product ID: "))
    quantity = int(input("Enter the quantity to add: "))

    add_quantity_query = """
    UPDATE inventory
    SET quantity = quantity + %s
    WHERE id = %s
    """
    cursor.execute(add_quantity_query, (quantity, product_id))
    db.commit()
    print("Quantity added to the product!")

# Function to delete a product
def delete_product():
    product_id = int(input("Enter the product ID to delete: "))

    delete_product_query = "DELETE FROM inventory WHERE id = %s"
    cursor.execute(delete_product_query, (product_id,))
    db.commit()
    print("Product deleted successfully!")

# Function to modify a product
def modify_product():
    product_id = int(input("Enter the product ID to modify: "))

    # Check if the product exists
    check_product_query = "SELECT * FROM inventory WHERE id = %s"
    cursor.execute(check_product_query, (product_id,))
    product = cursor.fetchone()

    if product is None:
        print("Product not found!")
        return

    print("Current Product Details:")
    print("Product ID:", product[0])
    print("Product Name:", product[1])
    print("Quantity:", product[2])
    print("Price:", product[3])

    name = input("Enter the new product name (leave blank to keep current): ")
    quantity = input("Enter the new quantity (leave blank to keep current): ")
    price = input("Enter the new price (leave blank to keep current): ")

    update_product_query = "UPDATE inventory SET product_name = %s, quantity = %s, price = %s WHERE id = %s"

    if name == "":
        name = product[1]
    if quantity == "":
        quantity = product[2]
    if price == "":
        price = product[3]

    cursor.execute(update_product_query, (name, quantity, price, product_id))
    db.commit()
    print("Product modified successfully!")

# Function to view inventory
def view_inventory():
    print("===== Inventory =====")
    print("1. Sort by ID")
    print("2. Sort by Product Name")
    print("3. Sort by Quantity")
    print("4. Sort by Price")
    print("5. Back to main menu")

    sort_choice = input("Enter your sort choice (1-5): ")

    if sort_choice == "1":
        sort_column = "id"
    elif sort_choice == "2":
        sort_column = "product_name"
    elif sort_choice == "3":
        sort_column = "quantity"
    elif sort_choice == "4":
        sort_column = "price"
    elif sort_choice == "5":
        return
    else:
        print("Invalid choice. Returning to main menu.")
        return

    view_inventory_query = f"SELECT * FROM inventory ORDER BY {sort_column}"
    cursor.execute(view_inventory_query)
    print("======================================")
    inventory = cursor.fetchall()
    print("======================================")

    if len(inventory) == 0:
        print("Inventory is empty!")
    else:
        print("ID\tProduct Name\tQuantity\tPrice")
        for product in inventory:
            print(product[0], "\t", product[1], "\t", product[2], "\t", product[3])
        
# Main program loop
while True:
    display_menu()
    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        add_product()
    elif choice=="2":
        add_quantity()
    elif choice == "3":
        delete_product()
    elif choice == "4":
        modify_product()
    elif choice == "5":
        view_inventory()
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
db.close()
