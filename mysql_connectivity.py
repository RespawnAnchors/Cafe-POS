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

def insert_into_menu(item_name, price):
    q = f"INSERT INTO cafe_pos.menu (item_name, price) VALUES ('{item_name}', {price});"
    cursor.execute(q)
    conn.commit()
    print("Item inserted successfully!")

def create_table_inventory():
    q = """
    CREATE TABLE IF NOT EXISTS cafe_pos.inventory (
    item_id INT PRIMARY KEY,
    quantity INT NOT NULL,
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



# def restock_inventory():#to restock the inventory if the quantity is less than the minimum stock
#     q = "SELECT * FROM cafe_pos.inventory;"
#     cursor.execute(q)
#     result = cursor.fetchall()
#     for row in result:
#         item_id, quantity, minimum_stock = row
#         if quantity < minimum_stock:
#             restock_amount = minimum_stock - quantity
#             new_quantity = quantity + restock_amount
#             q = f"UPDATE cafe_pos.inventory SET quantity = {new_quantity} WHERE item_id = {item_id};"
#             cursor.execute(q)
#             conn.commit()
#             print(f"Restocked item ID {item_id} by {restock_amount}. New quantity: {new_quantity}")
    
    
def display_inventory():
    q = "SELECT * FROM cafe_pos.inventory;"
    cursor.execute(q)
    result = cursor.fetchall()
    print("Inventory:")
    for row in result:
        print(f"Item ID: {row[0]}, Quantity: {row[1]}, Minimum Stock: {row[2]}")

# def display_bill():
#     q = "SELECT menu.item_name, menu.price, inventory.quantity FROM cafe_pos.menu JOIN cafe_pos.inventory ON menu.id = inventory.item_id;"
#     cursor.execute(q)
#     result = cursor.fetchall()
#     total_amount = 0
#     print("Bill:")
#     for row in result:
#         item_name, price, quantity = row
#         amount = price * quantity
#         total_amount += amount
#         print(f"Item: {item_name}, Price: {price}, Quantity: {quantity}, Amount: {amount}")
#     print(f"Total Amount: {total_amount}")

#MAIN PROGRAM
print("WELCOME TO ELYSIUM CAFE POS!!!")
create_database()
create_table_menu()
create_table_inventory()
display_menu()
display_inventory()