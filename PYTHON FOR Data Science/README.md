# Fruit Store Console Application

A Python console-based application for managing a fruit market store.

## Modules

- `main.py` — Controller / entry point of the application
- `fruit_manager.py` — Business logic for Fruit Manager role
- `customer.py` — Business logic for Customer role

## Features

### Fruit Manager
- Add Fruit Stock (name, quantity, price)
- View all Fruit Stock
- Update existing Fruit Stock

### Customer
- View available fruits
- Purchase fruits (with stock deduction and bill generation)

## How to Run

```bash
python main.py
```

## Requirements

- Python 3.x (no external libraries required)

## Notes

- All transactions are logged in `transactions.log`
- Input validation is handled for all fields
- Application runs until user chooses to Exit
- Follows PEP 8 coding standards

## Git Workflow

- Features developed on `develop` branch
- Merged into `main` branch after completion
