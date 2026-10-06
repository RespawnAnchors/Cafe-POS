print("WELCOME TO ELYSIUM CAFE POS!!!")
import mysql.connector as mc
conn = mc.connect(host="localhost", user="root", password="pwd")
cursor = conn.cursor()

def create_database():
    q = "CREATE DATABASE IF NOT EXISTS cafe_pos;"
    cursor.execute(q)
    print("Database created successfully!")

def create_table_menu():
    q = """
    CREATE TABLE IF NOT EXISTS cafe_pos.menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255),
    price DECIMAL(10,2)
    );
    """
    cursor.execute(q)
    conn.commit()
    print("Table created successfully!")

def insert_fooditems(item_name, price, quantity):
    q = f"INSERT INTO cafe_pos.menu (item_name, price) VALUES ('{item_name}', {price});"
    conn.commit()
    restock_inventory(item_name, quantity)
    cursor.execute(q)
    print("Item inserted successfully!")

def create_table_inventory():
    q = """
    CREATE TABLE IF NOT EXISTS cafe_pos.inventory (
    item_id INT PRIMARY KEY,
    quantity INT DEFAULT 0,
    minimum_stock INT DEFAULT 10,
    FOREIGN KEY (item_id) REFERENCES menu(id)
    );
    """

    cursor.execute(q)
    conn.commit()

def display_menu():
    q = "SELECT * FROM cafe_pos.menu;"
    cursor.execute(q)
    result = cursor.fetchall()
    print("Menu:")
    for row in result:
        print(f"ID: {row[0]}, Item Name: {row[1]}, Price: {row[2]}")

def take_order(item_id, quantity):
    q = f"SELECT quantity FROM cafe_pos.inventory WHERE item_id = {item_id};"
    cursor.execute(q)
    result = cursor.fetchone()
    if result is None:
        print("Item not in stock.")
        return
    available_quantity = result[0]
    if available_quantity < quantity:
        print(f"Insufficient stock. Available quantity: {available_quantity}")
        return
    new_quantity = available_quantity - quantity
    q = f"UPDATE cafe_pos.inventory SET quantity = {new_quantity} WHERE item_id = {item_id};"
    cursor.execute(q)
    conn.commit()
    print("Order placed successfully!")

def items_under_minimum_stock(): 
    
    
    
    #WHY JOIN???? -> PLEASE CHECK



    q = "SELECT menu.item_name, inventory.quantity, inventory.minimum_stock FROM cafe_pos.menu JOIN cafe_pos.inventory ON menu.id = inventory.item_id WHERE inventory.quantity < inventory.minimum_stock;"
    cursor.execute(q)
    result = cursor.fetchall()
    print("Items under minimum stock:")
    for row in result:
        print(f"Item Name: {row[0]}, Quantity: {row[1]}, Minimum Stock: {row[2]}")



def check_inventory():
    q = "SELECT menu.item_name, inventory.quantity FROM cafe_pos.menu JOIN cafe_pos.inventory ON menu.id = inventory.item_id;"
    cursor.execute(q)
    result = cursor.fetchall()
    print("Inventory:")
    for row in result:
        print(f"Item Name: {row[0]}, Quantity: {row[1]}")


def restock_inventory(item_name, quantity):
    item_id = f"(SELECT id FROM cafe_pos.menu WHERE item_name = '{item_name}');"
    q = f"UPDATE cafe_pos.inventory SET quantity = {quantity} WHERE item_id = {item_id};"
    cursor.execute(q)
    conn.commit()
    print("Inventory restocked successfully!")

#MAIN
create_database()
create_table_menu()
create_table_inventory()


# restock_inventory('Coffee', 50)
# restock_inventory('Tea', 30)
# restock_inventory('Sandwich', 20)
# restock_inventory('Cake', 10)
# restock_inventory('Juice', 25)
# restock_inventory('Salad', 10)
# restock_inventory('Soup', 5)
# restock_inventory('Pasta', 12)

#MAIN PROGRAM -> CAFE POS (MENU AND ORDERING SYSTEM USING Python AND MySQL)

while True:
    print("\n1. Display Menu")
    print("2. Take Order")
    print("3. See Inventory")
    print("4. Restock")
    print("5. Add New Item")
    print("6. Exit")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        display_menu()
    elif choice == '2':
        item_id = int(input("Enter item ID: "))
        quantity = int(input("Enter quantity: "))
        take_order(item_id, quantity)
    elif choice == '3':
        check_inventory()
    elif choice == '4':
        restock_inventory()
    elif choice == '5':
        item_name = input("Enter item name: ")
        quantity = int(input("Enter quantity: "))
        insert_fooditems(item_name, quantity)
    elif choice == '6':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")