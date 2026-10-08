from datetime import date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
console = Console()
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
    console.print("✅ [green]Item inserted successfully![/green]")
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
    table = Table(
    title="☕ ELYSIUM MENU ☕",
    border_style="cyan"
)
    table.add_column("ID", justify="center")

    table.add_column("Item Name")

    table.add_column("Price", justify="right")
    console.print("\nMenu:")
    if not result:
        console.print("No items in the menu.")
    else:
        for row in result:
            table.add_row(str(row[0]), row[1], f"${row[2]:.2f}")
    console.print(table)

def take_order(item_name, quantity):
    item_id = f"(SELECT id FROM cafe_pos.menu WHERE item_name = '{item_name}');"
    q = f"SELECT quantity FROM cafe_pos.inventory WHERE item_id = {item_id};"
    cursor.execute(q)
    result = cursor.fetchone()
    if result is None:
        console.print("❌ [red]Item not in stock.[/red]")
        return
    available_quantity = result[0]
    if available_quantity < quantity:
        console.print(f"❌ [red]Insufficient stock. Available quantity: {available_quantity}[/red]")
        return
    new_quantity = available_quantity - quantity
    q = f"UPDATE cafe_pos.inventory SET quantity = {new_quantity} WHERE item_id = {item_id};"
    cursor.execute(q)
    conn.commit()
    console.print("✅ [green]Order placed successfully![/green]")
    price_query = f"SELECT price FROM cafe_pos.menu WHERE id = {item_id};"
    return (item_name,price_query,quantity)

def items_under_minimum_stock(): 
    q = "SELECT menu.item_name, inventory.quantity, inventory.minimum_stock FROM cafe_pos.menu JOIN cafe_pos.inventory ON menu.id = inventory.item_id WHERE inventory.quantity < inventory.minimum_stock;"
    cursor.execute(q)
    result = cursor.fetchall()
    if q != "":
        console.print("⚠️ [yellow] WARNING!![/yellow] ⚠️")
        console.print("Items under minimum stock:")
    for row in result:
        console.print(f"Item Name: {row[0]}, Quantity: {row[1]}, Minimum Stock: {row[2]}")
    
def check_inventory():
    q = "SELECT menu.item_name, inventory.quantity,inventory.minimum_stock FROM cafe_pos.menu JOIN cafe_pos.inventory ON menu.id = inventory.item_id;"
    cursor.execute(q)
    result = cursor.fetchall()
    table = Table(
    title="📦 Inventory",
    border_style="green"
)
    table.add_column("Item")

    table.add_column("Quantity", justify="center")

    table.add_column("Minimum", justify="center")
    console.print("Inventory:")
    for row in result:
        quantity = row[1]
        minimum = row[2]
        if quantity < minimum:
            quantity_color = " red"
        else:
            quantity_color = " green"
        table.add_row(
            row[0],
            f"[{quantity_color}]{quantity}[/{quantity_color}]",
            str(minimum)
        )
    console.print(table)


def restock_inventory(item_name, quantity):
    item_id = f"(SELECT id FROM cafe_pos.menu WHERE item_name = '{item_name}');"
    q = f"UPDATE cafe_pos.inventory SET quantity = quantity + {quantity} WHERE item_id = {item_id};"
    cursor.execute(q)
    conn.commit()
    if cursor.rowcount > 0:
        console.print("✅ [green]Inventory restocked successfully![/green]")
def welcome_screen():
    console.print()

    console.print(
        Align.center(
            Panel.fit(
                "[cyan]☕ ELYSIUM CAFE ☕[/cyan]\n"
                "[white]Point Of Sale Management System[/white]",
                border_style="bright_blue"
            )
        )
    )

    console.print(
        Align.center("[italic green]Developed by Devrag Vyshnav & Vinayak[/italic green]")
    )

    console.print()
#MAIN
create_database()
create_table_menu()
create_table_inventory()

#MAIN PROGRAM -> CAFE POS (MENU AND ORDERING SYSTEM USING Python AND MySQL)
welcome_screen()
while True:
    console.print()
    console.print("[magenta]========= MAIN MENU =========[/magenta]", justify="center")
    console.print("[green][1][/green] Customer")
    console.print("[yellow][2][/yellow] Owner")
    console.print("[red][3][/red] Exit")

    console.print()
    user_choice = console.input("[cyan]Enter your choice➜ [/cyan] ")
    if user_choice == '1':
        customer_name = console.input("[cyan]Enter customer name: [/cyan] ")
        bill=[]
        while True:
            console.rule("[green]Customer Menu[/green]")
            print(f"\nWelcome {customer_name} to ELYSIUM CAFE!")
            print("\n1. Display Menu")
            print("2. Take Order")
            print("3. Billing")
            print("4. Go back to main menu")
            choice = console.input("[cyan]Enter your choice ➜ [/cyan]")
            if choice == '1':
                display_menu()
            elif choice == '2':
                item_name = console.input("[cyan]Enter item name: [/cyan] ")
                quantity = int(input("Enter quantity: "))
                order_details = take_order(item_name, quantity)
                if order_details:
                    bill.append(order_details)
            elif choice == '3':
                total_amount = 0
                bill_table = Table(
                title="🧾 CUSTOMER BILL",
                border_style="bright_green"
                )   
                bill_table.add_column("Item")

                bill_table.add_column("Qty", justify="center")

                bill_table.add_column("Price", justify="right")

                bill_table.add_column("Amount", justify="right")
                print()
                console.rule("[cyan]ELYSIUM CAFE[/cyan]")
                console.rule("[cyan]BILL[/cyan]")
                console.print(
                f"[]Customer:[/] {customer_name}"
            )

                console.print(
                    f"[]Date:[/] {date.today()}"
            )
                print()
                for item in bill:
                    
                    total_amount += item[2] * item[1]
                    bill_table.add_row(
                    item[0],
                    str(item[2]),
                    f"₹{item[1]}",
                    f"₹{total_amount}"
                )
                console.print(bill_table)
                console.print(
                f"[ green]TOTAL : ₹{total_amount:.2f}[/ green]",
                justify="right"
            )
                console.print(
                Panel.fit(
                    "[ green]Thank You For Visiting! ☕[/ green]\n"
                    "Visit Again!",
                    border_style="green"
                )
)
                print()
            elif choice == '4':
                print("going back to main menu...")
                break
            else:
                print("Invalid choice. Please try again.")
    elif user_choice == '2':
        password = input("Enter owner password: ")
        if password != PASSWORD:
            console.print("🔒 [red]Incorrect password![/red]")
            continue
        #warning for items under minimum stock
        items_under_minimum_stock()

        print("Access granted. Welcome, Owner!")
        while True:
            console.rule("[green]Owner Menu[/green]")
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
        console.print()

        console.print(
            Panel.fit(
                "[green]Thank You For Visiting ☕[/green]\n"
                "Have A Great Day!",
                border_style="green"
            ),
            justify="center"
        )
        break
    else:
        console.print("❌ [red]Invalid choice. Please try again.[/red]")

cursor.close()
conn.close()