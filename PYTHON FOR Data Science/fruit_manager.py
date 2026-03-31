# fruit_manager.py
# Module: Fruit Manager
# Handles all fruit stock operations for the Fruit Store application

import logging

# Configure logging to write transactions to a log file
logging.basicConfig(
    filename="transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def add_fruit_stock(fruit_stock):
    """Add a new fruit or update existing fruit stock."""
    print("\nADD FRUIT STOCK")

    while True:
        fruit_name = input("Enter fruit Name : ").strip().title()
        if not fruit_name.isalpha():
            print("  [!] Invalid name. Please enter letters only.")
            continue
        break

    while True:
        qty_input = input("Enter qty (in kg): ").strip()
        if not qty_input.isdigit() or int(qty_input) <= 0:
            print("  [!] Invalid quantity. Please enter a positive number.")
            continue
        qty = int(qty_input)
        break

    while True:
        price_input = input("Enter price (for kg): ").strip()
        try:
            price = float(price_input)
            if price <= 0:
                raise ValueError
        except ValueError:
            print("  [!] Invalid price. Please enter a valid positive number.")
            continue
        break

    # If fruit already exists, add the quantity
    if fruit_name in fruit_stock:
        fruit_stock[fruit_name]["qty"] = str(int(fruit_stock[fruit_name]["qty"]) + qty)
        fruit_stock[fruit_name]["price"] = str(price)
        print(f"  [✔] '{fruit_name}' stock updated successfully.")
        logging.info(f"Updated stock - Fruit: {fruit_name}, Qty: {qty}kg, Price: {price}")
    else:
        fruit_stock[fruit_name] = {"qty": str(qty), "price": str(price)}
        print(f"  [✔] '{fruit_name}' added to stock successfully.")
        logging.info(f"Added new fruit - Fruit: {fruit_name}, Qty: {qty}kg, Price: {price}")


def view_fruit_stock(fruit_stock):
    """Display all available fruit stock."""
    print("\nVIEW FRUIT STOCK")

    if not fruit_stock:
        print("  [!] No stock available. Please add fruits first.")
        return

    print(fruit_stock)
    print("\n  --- Stock Details ---")
    print(f"  {'Fruit':<15} {'Qty (kg)':<12} {'Price (per kg)'}")
    print("  " + "-" * 40)
    for fruit, details in fruit_stock.items():
        print(f"  {fruit:<15} {details['qty']:<12} {details['price']}")
    print("  " + "-" * 40)
    logging.info("Manager viewed all stock.")


def update_fruit_stock(fruit_stock):
    """Update the quantity or price of an existing fruit."""
    print("\nUPDATE FRUIT STOCK")

    if not fruit_stock:
        print("  [!] No stock available to update.")
        return

    while True:
        fruit_name = input("Enter fruit name to update : ").strip().title()
        if fruit_name not in fruit_stock:
            print(f"  [!] '{fruit_name}' not found in stock. Try again.")
            continue
        break

    print(f"  Current details -> Qty: {fruit_stock[fruit_name]['qty']} kg, Price: {fruit_stock[fruit_name]['price']}")

    while True:
        new_qty = input("Enter new qty (in kg): ").strip()
        if not new_qty.isdigit() or int(new_qty) <= 0:
            print("  [!] Invalid quantity. Please enter a positive number.")
            continue
        break

    while True:
        new_price = input("Enter new price (for kg): ").strip()
        try:
            new_price_val = float(new_price)
            if new_price_val <= 0:
                raise ValueError
        except ValueError:
            print("  [!] Invalid price. Please enter a valid positive number.")
            continue
        break

    fruit_stock[fruit_name]["qty"] = new_qty
    fruit_stock[fruit_name]["price"] = new_price
    print(f"  [✔] '{fruit_name}' stock updated successfully.")
    logging.info(f"Updated fruit - Fruit: {fruit_name}, New Qty: {new_qty}kg, New Price: {new_price}")


def manager_menu(fruit_stock):
    """Display and handle Fruit Manager menu."""
    while True:
        print("\n" + " " * 20 + "Fruit Market Manager")
        print("\n" + " " * 20 + "1) Add Fruit Stock")
        print(" " * 20 + "2) View Fruit Stock")
        print(" " * 20 + "3) Update Fruit stock")
        print()

        choice = input("Enter your choice : ").strip()

        try:
            if choice == "1":
                add_fruit_stock(fruit_stock)
            elif choice == "2":
                view_fruit_stock(fruit_stock)
            elif choice == "3":
                update_fruit_stock(fruit_stock)
            else:
                print("  [!] Invalid choice. Please select 1, 2, or 3.")
                continue
        except Exception as e:
            print(f"  [!] An unexpected error occurred: {e}. Returning to menu.")
            logging.error(f"Error in manager menu: {e}")
            continue

        # Ask if manager wants to continue
        while True:
            again = input("\nDo you want to perform more operations : press y for yes and n for no : ").strip().lower()
            if again == "y":
                break
            elif again == "n":
                print("  [✔] Returning to main menu.")
                return
            else:
                print("  [!] Invalid input. Press 'y' for yes or 'n' for no.")
