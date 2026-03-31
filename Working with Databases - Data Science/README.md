# SQL Assessment — City, Customer & Country

## Tables Used
- **country** — List of countries (7 rows)
- **city** — Cities linked to countries (6 rows)
- **customer** — Customers linked to cities (4 rows)

## How to Run

1. Open any SQL tool (MySQL Workbench, DBeaver, pgAdmin, etc.)
2. Open `assessment.sql`
3. Run the full file — it creates tables, inserts data, and runs both queries

## Tasks

### Task 1 — LEFT JOIN (All countries including those without cities/customers)
Lists every country alongside its city and customer.
Countries like Spain and Russia appear with NULL values since they have no cities.

### Task 2 — INNER JOIN + LEFT JOIN (Only countries that have cities)
Excludes Spain and Russia (no cities linked).
Shows all city-country pairs, and for each pair shows customers if any exist.
Pairs without customers still appear (e.g. Belgrade, Los Angeles, Warsaw).
