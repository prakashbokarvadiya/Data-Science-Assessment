# customer.py
# Module: Customer
# Handles all customer purchase operations for the Fruit Store application

import logging

# Configure logging
logging.basicConfig(
    filename="transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def view_available_fruits(fruit_stock):
    """Display all fruits available for purchase."""
    print("\n  --- Available Fruits ---")
    if not fruit_stock:
        print("  [!] No fruits available in store right now. Please visit later.")
        return False

    print(f"  {'Fruit':<15} {'Qty (kg)':<12} {'Price (per kg)'}")
    print("  " + "-" * 40)
    for fruit, details in fruit_stock.items():
        print(f"  {fruit:<15} {details['qty']:<12} {details['price']}")
    print("  " + "-" * 40)
    return True


def purchase_fruit(fruit_stock):
    """Allow customer to purchase fruits from available stock."""
    print("\nPURCHASE FRUIT")

    if not view_available_fruits(fruit_stock):
        return

    while True:
        fruit_name = input("\nEnter fruit name to purchase : ").strip().title()
        if not fruit_name.isalpha():
            print("  [!] Invalid name. Please enter letters only.")
            continue
        if fruit_name not in fruit_stock:
            print(f"  [!] '{fruit_name}' is not available. Please choose from the list.")
            continue
        break

    available_qty = int(fruit_stock[fruit_name]["qty"])
    price_per_kg = float(fruit_stock[fruit_name]["price"])

    while True:
        qty_input = input(f"Enter qty to purchase (available: {available_qty} kg): ").strip()
        if not qty_input.isdigit() or int(qty_input) <= 0:
            print("  [!] Invalid quantity. Please enter a positive number.")
            continue
        purchase_qty = int(qty_input)
        if purchase_qty > available_qty:
            print(f"  [!] Insufficient stock. Only {available_qty} kg available.")
            continue
        break

    # Calculate total bill
    total_price = purchase_qty * price_per_kg

    # Deduct from stock
    fruit_stock[fruit_name]["qty"] = str(available_qty - purchase_qty)

    print(f"\n  [✔] Purchase Successful!")
    print(f"  Fruit    : {fruit_name}")
    print(f"  Qty      : {purchase_qty} kg")
    print(f"  Rate     : {price_per_kg} per kg")
    print(f"  Total    : {total_price}")

    logging.info(
        f"Customer purchased - Fruit: {fruit_name}, Qty: {purchase_qty}kg, "
        f"Price/kg: {price_per_kg}, Total: {total_price}"
    )


def customer_menu(fruit_stock):
    """Display and handle Customer menu."""
    while True:
        print("\n" + " " * 20 + "Fruit Market Customer")
        print("\n" + " " * 20 + "1) View Available Fruits")
        print(" " * 20 + "2) Purchase Fruit")
        print()

        choice = input("Enter your choice : ").strip()

        try:
            if choice == "1":
                view_available_fruits(fruit_stock)
            elif choice == "2":
                purchase_fruit(fruit_stock)
            else:
                print("  [!] Invalid choice. Please select 1 or 2.")
                continue
        except Exception as e:
            print(f"  [!] An unexpected error occurred: {e}. Returning to menu.")
            logging.error(f"Error in customer menu: {e}")
            continue

        # Ask if customer wants to continue
        while True:
            again = input("\nDo you want to perform more operations : press y for yes and n for no : ").strip().lower()
            if again == "y":
                break
            elif again == "n":
                print("  [✔] Thank you for shopping! Returning to main menu.")
                return
            else:
                print("  [!] Invalid input. Press 'y' for yes or 'n' for no.")
