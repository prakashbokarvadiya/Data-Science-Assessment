# main.py
# Module Controller: Entry point of the Fruit Store Console Application
# This file controls the flow of the application and ties all modules together.
# Author: Student Submission
# Follows PEP 8 coding standards and conventions

import logging
from fruit_manager import manager_menu
from customer import customer_menu

# -----------------------------------------------------------------------
# Configure logging: All transactions are saved in transactions.log file
# -----------------------------------------------------------------------
logging.basicConfig(
    filename="transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------------------------------------------
# Shared fruit stock dictionary — stores all fruit data in memory
# Format: { "FruitName": { "qty": "5", "price": "100" }, ... }
# -----------------------------------------------------------------------
fruit_stock = {}


def display_main_menu():
    """Display the Welcome main menu to the user."""
    print("\n" + " " * 20 + "WELCOME TO FRUIT MARKET")
    print()
    print(" " * 20 + "1) Manager")
    print(" " * 20 + "2) Customer")
    print(" " * 20 + "3) Exit")
    print()


def main():
    """Main controller function — keeps application running until user exits."""
    logging.info("Application started.")

    while True:
        display_main_menu()

        role = input("Select your Role : ").strip()

        if role == "1":
            # Route to Fruit Manager module
            logging.info("Manager logged in.")
            manager_menu(fruit_stock)

        elif role == "2":
            # Route to Customer module
            logging.info("Customer logged in.")
            customer_menu(fruit_stock)

        elif role == "3":
            # Exit the application
            print("\n  [✔] Thank you for using Fruit Market. Goodbye!\n")
            logging.info("Application exited by user.")
            break

        else:
            # Handle invalid role selection
            print("  [!] Invalid selection. Please enter 1 for Manager, 2 for Customer, or 3 to Exit.")


# -----------------------------------------------------------------------
# Entry point — ensures main() runs only when script is executed directly
# -----------------------------------------------------------------------
if __name__ == "__main__":
    main()
