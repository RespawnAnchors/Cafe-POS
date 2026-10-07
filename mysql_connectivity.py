from datetime import date
import mysql.connector as mc
conn = mc.connect(host="localhost", user="root", password="12345")
cursor = conn.cursor()
PASSWORD = "admin123"

def create_database():
    q = "CREATE DATABASE IF NOT EXISTS cafe_pos;"
    cursor.execute(q)

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

def insert_fooditems(item_name, price, quantity):
    q = f"INSERT INTO cafe_pos.menu (item_name, price) VALUES ('{item_name}', {price});"
    restock_inventory(item_name, quantity)
    cursor.execute(q)
    print("Item inserted successfully!")
    conn.commit()

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
    print("\nMenu:")
    if not result:
        print("No items in the menu.")
    else:
        for row in result:
            print(f"ID: {row[0]}, Item Name: {row[1]}, Price: {row[2]}")

def take_order(item_name, quantity):
    item_id = f"(SELECT id FROM cafe_pos.menu WHERE item_name = '{item_name}');"
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
    price_query = f"SELECT price FROM cafe_pos.menu WHERE id = {item_id};"
    return (item_name,price_query,quantity)

def items_under_minimum_stock(): 
    q = "SELECT menu.item_name, inventory.quantity, inventory.minimum_stock FROM cafe_pos.menu JOIN cafe_pos.inventory ON menu.id = inventory.item_id WHERE inventory.quantity < inventory.minimum_stock;"
    cursor.execute(q)
    result = cursor.fetchall()
    if q != "":
        print("WARNING!!⚠️⚠️")
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
    q = f"UPDATE cafe_pos.inventory SET quantity = quantity + {quantity} WHERE item_id = {item_id};"
    cursor.execute(q)
    conn.commit()
    if cursor.rowcount > 0:
        print("Inventory restocked successfully!")

#MAIN
create_database()
create_table_menu()
create_table_inventory()

#MAIN PROGRAM -> CAFE POS (MENU AND ORDERING SYSTEM USING Python AND MySQL)
print("WELCOME TO ELYSIUM CAFE POS!!!")
while True:
    print()
    print("MAIN MENU")
    print("\n1. Customer")
    print("2. Owner")
    print("3. Exit")
    user_choice = input("Enter your choice: ")
    if user_choice == '1':
        customer_name = input("Enter customer name: ")
        bill=[]
        while True:
            print(f"\nWelcome {customer_name} to ELYSIUM CAFE!")
            print("\n1. Display Menu")
            print("2. Take Order")
            print("3. Billing")
            print("4. Go back to main menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                display_menu()
            elif choice == '2': #NEED TO UNDERSTAND HOW THIS WORKS (I FORGOT)
                item_name = input("Enter item name: ")
                quantity = int(input("Enter quantity: "))
                order_details = take_order(item_name, quantity)
                if order_details:
                    bill.append(order_details)
            elif choice == '3':
                total_amount = 0
                print()
                print("----- ELYSIUM CAFE -----")
                print("----------BILL----------")
                print(f"Customer Name: {customer_name}\tDate: {date.today()}")
                print()
                for item in bill:
                    print(f"Item: {item[0]}, Quantity: {item[2]}, Price: {item[1]}")
                    total_amount += item[2] * item[1]
                print("Total Amount: ",int(total_amount))
                print("------------------------")
                print("Thank you for visiting ELYSIUM CAFE!")
                print("------------------------")
                print()
            elif choice == '4':
                print("going back to main menu...")
                break
            else:
                print("Invalid choice. Please try again.")
    elif user_choice == '2':
        password = input("Enter owner password: ")
        if password != PASSWORD:
            print("Incorrect password. Access denied.")
            continue
        #warning for items under minimum stock
        items_under_minimum_stock()

        print("Access granted. Welcome, Owner!")
        while True:
            print("\nOwner Menu:")
            print("\n1. See Inventory")
            print("2. Restock")
            print("3. Add New Item")
            print("4. go back to main menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                check_inventory()   
            elif choice == '2':
                item_name = input("Enter item name: ")
                quantity = int(input("Enter quantity to restock: "))
                restock_inventory(item_name, quantity)
            elif choice == '3':
                item_name = input("Enter item name: ")
                quantity = int(input("Enter quantity: "))
                price = float(input("Enter price: "))
                insert_fooditems(item_name , price, quantity)
            elif choice == '4':
                print("going back to main menu...")
                break
            else:
                print("Invalid choice. Please try again.")
    elif user_choice == '3':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")           

cursor.close()
conn.close()