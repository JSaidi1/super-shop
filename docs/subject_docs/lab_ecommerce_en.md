## 📘 Complete Lab – PostgreSQL: Sales Analysis for an E-commerce Website

**Level:** Intermediate  
**Target Role:** Data Analyst

---

# 1️⃣ Context

You work for a fictional e-commerce company:

**SuperShop Analytics**

Management wants to analyze:

- sales by product and by category,
- customer behavior,
- revenue by period,
- “top” and “underperforming” products and customers.

Your mission:

1. Design the **relational schema** of the database.
2. Create the tables in PostgreSQL.
3. Insert a provided dataset (values already written in SQL, `INSERT` statements to complete).
4. Write analytical SQL queries: joins, subqueries, aggregates, conditional logic.

---

# 2️⃣ Business Model – Tables to Design (no imposed schema)

You must **deduce on your own**:

- column names,
- SQL data types,
- constraints (NOT NULL, UNIQUE, CHECK, FOREIGN KEY…),
- primary and foreign keys.

> For each table, it is recommended to include **a unique identifier column** (auto-incremented primary key or equivalent).

---

## 2.1 Product Categories (`categories`)

Each product belongs to a **category**.

For each category, store:

- a **category name**
  - relatively short text
  - required
  - two categories must not have the same name

- a **description**
  - longer text
  - optional

You must define:

- the identifier column,
- SQL data types,
- constraints (NOT NULL, UNIQUE…).

---

## 2.2 Products (`products`)

Products are the items sold on the website.

At minimum, store:

- a **product name**
  - short text
  - required

- a **price**
  - numeric
  - strictly positive

- **available stock**
  - integer
  - ≥ 0

- a **category**
  - foreign key referencing the categories table

You must define:

- the identifier column,
- data types,
- constraints (CHECK for price/stock, FK, etc.).

---

## 2.3 Customers (`customers`)

Customers are users who place orders.

For each customer, store:

- a **first name**
- a **last name**
  - both required

- an **email address**
  - required
  - unique

- an **account creation date/time**
  - required

You must define:

- the primary key,
- data types,
- constraints (UNIQUE on email, NOT NULL, etc.).

---

## 2.4 Orders (`orders`)

Orders represent purchases made by customers.

For each order, store:

- the **customer** who placed the order
  - foreign key to `customers`

- the **order date/time**
  - required

- the **order status**
  - short text
  - allowed values strictly limited to:
    - `PENDING`
    - `PAID`
    - `SHIPPED`
    - `CANCELLED`
  - required

You must define:

- the primary key,
- the foreign key to `customers`,
- the constraint validating the status.

---

## 2.5 Order Items (`order_items`)

Each order contains one or more order lines.

For each line:

- the **order**
  - foreign key to `orders`

- the **product**
  - foreign key to `products`

- the **quantity**
  - integer
  - strictly positive

- the **billed unit price**
  - numeric
  - strictly positive
  - may differ from the current product price (promotion, discount, etc.)

You must define:

- the primary key of the line,
- foreign keys,
- constraints (CHECK, NOT NULL…).

---

# 3️⃣ Part 1 – SQL Schema Creation

**Objective:** translate the business model into SQL.

Tasks:

1. Draft your relational schema (tables, columns, PKs, FKs…).
2. Write a SQL script `schema.sql` to:
   - (optional) create the database,
   - create the tables `categories`, `products`, `customers`, `orders`, `order_items` with:
     - PRIMARY KEY,
     - FOREIGN KEY,
     - NOT NULL,
     - UNIQUE,
     - CHECK (price > 0, stock ≥ 0, quantity > 0, etc.).

---

# 4️⃣ Part 2 – Provided Dataset (`.sql` file to complete)

The dataset below is provided **in SQL**, but the `INSERT INTO` statements must be **completed by you**.

- **ID columns are intentionally omitted**: they must be automatically managed by the database (SERIAL, IDENTITY, …).
- You must complete **the table name** and **the list of business columns** in `INSERT INTO … ( ... )`.
- **Do not rewrite the values**: they are already prepared.

**Recommended file:** `data.sql`

```sql
-- ===========================================
--  DATA: CATEGORIES
--  Objective: insert product categories
--  TODO: complete table name and column list (excluding identifier column)
-- Expected example:
--   INSERT INTO categories (name, description) VALUES ...
-- ===========================================

INSERT INTO /* TODO */ VALUES
  ('Electronics',        'High-tech products and accessories'),
  ('Home & Kitchen',     'Appliances and kitchen utensils'),
  ('Sports & Leisure',   'Sports and outdoor items'),
  ('Beauty & Health',    'Beauty, hygiene, and wellness products'),
  ('Games & Toys',       'Toys for children and adults');
```
# 5️⃣ Part 3 – Basic SQL Queries

1. List all customers ordered by account creation date (from oldest to newest).

2. List all products (product name and price) ordered by descending price.

3. List all orders placed between two dates  
   *(for example, between March 1st and March 15th, 2024).*

4. List all products whose price is **strictly greater than €50**.

5. List all products belonging to a given category  
   *(for example, “Electronics”).*


# 6️⃣ Part 4 – Simple Joins

1. List all products with their category name.
2. List all orders with the customer’s full name (first name + last name).
3. List all order items with:
   - customer name,
   - product name,
   - quantity,
   - billed unit price.
4. List all orders whose status is `PAID` or `SHIPPED`.

---

# 7️⃣ Part 5 – Advanced Joins

1. Display the complete details of each order, including:
   - order date,
   - customer name,
   - list of products,
   - quantity,
   - billed unit price,
   - total line amount (quantity × unit price).

2. Calculate the **total amount of each order** and display only:
   - the order ID,
   - the customer name,
   - the total order amount.

3. Display orders whose total amount **exceeds €100**.

4. List all categories with their **total revenue** (sum of line amounts for all products in that category).

---

# 8️⃣ Part 6 – Subqueries

1. List products that have been sold **at least once**.
2. List products that have **never been sold**.
3. Find the customer who has **spent the most** (TOP 1 by total revenue).
4. Display the **top 3 best-selling products** in terms of total quantity sold.
5. List orders whose total amount is **strictly greater than the average** of all orders.

---

# 9️⃣ Part 7 – Statistics & Aggregates

1. Calculate the **total revenue** (all orders combined, optionally excluding cancelled orders).
2. Calculate the **average basket value** (average amount per order).
3. Calculate the **total quantity sold per category**.
4. Calculate the **monthly revenue** (based on the provided data).
5. Format monetary amounts to display **only two decimal places**.

---

# 🔟 Part 8 – Conditional Logic (CASE)

1. For each order, display:
   - order ID,
   - customer,
   - order date,
   - status,
   - a human-readable version of the status using `CASE`:
     - `PAID` → “Paid”
     - `SHIPPED` → “Shipped”
     - `PENDING` → “Pending”
     - `CANCELLED` → “Cancelled”

2. For each customer, calculate the **total amount spent** and classify them into segments:
   - `< €100` → “Bronze”
   - `€100–300` → “Silver”
   - `> €300` → “Gold”

   Display:
   - first name,
   - last name,
   - total amount spent,
   - segment.

---

# 1️⃣1️⃣ Part 9 – Final Challenge

Propose and write **5 additional advanced analytical queries**, for example:

1. Top 5 most active customers (number of orders).
2. Top 5 customers by total spending.
3. Top 3 most profitable categories.
4. Products that generated **less than €10** in total revenue.
5. Customers who placed **only one order**.
6. Products included in **cancelled orders**, with the corresponding “lost” revenue.

---

## Extension – Generate a Text Report with psycopg

### Objective

Write a Python script that:

- connects to the `supershop` database,
- executes several SQL queries from the lab,
- generates a file named `rapport_supershop.txt` containing:
  - descriptive sentences in English (e.g. *“Most ordered product: …”*),
  - query results (numbers, names, etc.).

### Suggested Report Sections

1. Total revenue.
2. Average basket value.
3. Most ordered product (by total quantity).
4. Top 3 customers by total spending.
5. Revenue by category.
