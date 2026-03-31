-- ============================================================
-- SQL Assessment : City, Customer and Country Tables
-- ============================================================


-- ============================================================
-- STEP 1 : Create Tables
-- ============================================================

CREATE TABLE country (
    id           INT PRIMARY KEY,
    country_name VARCHAR(100),
    country_name_eng VARCHAR(100),
    country_code VARCHAR(10)
);

CREATE TABLE city (
    id         INT PRIMARY KEY,
    city_name  VARCHAR(100),
    lat        DECIMAL(10, 6),
    long       DECIMAL(10, 6),
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE TABLE customer (
    id               INT PRIMARY KEY,
    customer_name    VARCHAR(100),
    city_id          INT,
    customer_address VARCHAR(200),
    next_call_date   DATE,
    ts_inserted      DATETIME,
    FOREIGN KEY (city_id) REFERENCES city(id)
);


-- ============================================================
-- STEP 2 : Insert Data into country table
-- ============================================================

INSERT INTO country VALUES (1, 'Deutschland',              'Germany',                  'DEU');
INSERT INTO country VALUES (2, 'Srbija',                   'Serbia',                   'SRB');
INSERT INTO country VALUES (3, 'Hrvatska',                 'Croatia',                  'HRV');
INSERT INTO country VALUES (4, 'United States of America', 'United States of America', 'USA');
INSERT INTO country VALUES (5, 'Polska',                   'Poland',                   'POL');
INSERT INTO country VALUES (6, 'España',                   'Spain',                    'ESP');
INSERT INTO country VALUES (7, 'Rossiya',                  'Russia',                   'RUS');


-- ============================================================
-- STEP 3 : Insert Data into city table
-- ============================================================

INSERT INTO city VALUES (1, 'Berlin',      52.520008,  13.404954,   1);
INSERT INTO city VALUES (2, 'Belgrade',    44.787197,  20.457273,   2);
INSERT INTO city VALUES (3, 'Zagreb',      45.815399,  15.966568,   3);
INSERT INTO city VALUES (4, 'New York',    40.730610,  -73.935242,  4);
INSERT INTO city VALUES (5, 'Los Angeles', 34.052235,  -118.243683, 4);
INSERT INTO city VALUES (6, 'Warsaw',      52.237049,  21.017532,   5);


-- ============================================================
-- STEP 4 : Insert Data into customer table
-- ============================================================

INSERT INTO customer VALUES (1, 'Jewelry Store', 4, 'Long Street 120',    '2020-01-21', '2020-01-09 14:01:20.000');
INSERT INTO customer VALUES (2, 'Bakery',         1, 'Kurfürstendamm 25',  '2020-02-21', '2020-01-09 17:52:15.000');
INSERT INTO customer VALUES (3, 'Café',           1, 'Tauentzienstraße 44','2020-01-21', '2020-01-10 08:02:49.000');
INSERT INTO customer VALUES (4, 'Restaurant',     3, 'Ulica lipa 15',      '2020-01-21', '2020-01-10 09:20:21.000');


-- ============================================================
-- TASK 1 : List all Countries with related Cities and Customers
--           Using LEFT JOIN to include countries without cities/customers
--           (e.g. Spain & Russia must also appear in results)
-- ============================================================

SELECT
    co.country_name_eng  AS country,
    ci.city_name         AS city,
    cu.customer_name     AS customer
FROM
    country  co
LEFT JOIN city     ci ON ci.country_id = co.id
LEFT JOIN customer cu ON cu.city_id    = ci.id
ORDER BY
    co.id,
    ci.id,
    cu.id;


-- ============================================================
-- TASK 2 : List all Country-City pairs (exclude countries with no city)
--           Then for each pair return all customers (if any)
--           Using INNER JOIN for country-city, LEFT JOIN for customers
-- ============================================================

SELECT
    co.country_name_eng  AS country,
    ci.city_name         AS city,
    cu.customer_name     AS customer
FROM
    country  co
INNER JOIN city     ci ON ci.country_id = co.id
LEFT  JOIN customer cu ON cu.city_id    = ci.id
ORDER BY
    co.id,
    ci.id,
    cu.id;
