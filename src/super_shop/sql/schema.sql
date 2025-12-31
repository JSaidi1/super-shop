-- ================================================================================
-- FILE: schema.sql
-- SUBJECT: Creating the PostgreSQL schema for SuperShop
-- CONTENT: Tables, primary keys, foreign keys, constraints
-- ================================================================================

-- --------------------------------------------------------------------------------
-- Preliminary cleanup (to easily replay the script)
-- --------------------------------------------------------------------------------
DROP SCHEMA IF EXISTS super_shop_schema CASCADE;

-- --------------------------------------------------------------------------------
-- SCHEMA: super_shop_schema
-- --------------------------------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS super_shop_schema;

-- --------------------------------------------------------------------------------
-- TABLE: categories
-- Business model:
-- - category name (required, unique)
-- - description (optional)
-- --------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS super_shop_schema.categories (
	category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(200)
);

-- --------------------------------------------------------------------------------
-- TABLE: products
-- Business model:
-- - name (required, unique)
-- - price (numeric > 0)
-- - stock (integer >= 0)
-- - category (foreign key to categories)
-- --------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS super_shop_schema.products (
	product_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
	available_stock INT NOT NULL CHECK (available_stock >= 0),
	category_id INT NOT NULL,
	CONSTRAINT fk_category_id FOREIGN KEY(category_id)
		REFERENCES super_shop_schema.categories(category_id)
		ON DELETE CASCADE
);

-- --------------------------------------------------------------------------------
-- TABLE: customers
-- Business model:
-- - First name (required)
-- - Last name (required)
-- - Email (required, unique)
-- - Date/time of creation (required, current date time if sign up)
-- --------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS super_shop_schema.customers (
	customer_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	email VARCHAR(100) NOT NULL UNIQUE,
	created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

/*
-- --------------------------------------------------------------------------------
-- TABLE: order_status
-- Business model:
-- - status can only be 'PENDING' or 'PAID' or 'SHIPPED' or 'CANCELLED'
-- --------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS super_shop_schema.order_status (
	order_status_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_status_name TEXT UNIQUE CHECK (order_status_name IN ('PENDING', 'PAID', 'SHIPPED', 'CANCELLED'))
);
*/
-- --------------------------------------------------------------------------------
-- TABLE: orders
-- Business model:
-- - customer (FK to customers)
-- - status (FK to orders_status)
-- - order date/time (required)
-- - order status (short text, required, allowed values strictly limited to: 'PENDING', 'PAID', 'SHIPPED', 'CANCELLED')
-- - the same customer can not place multiple orders at the exact same timestamp
-- --------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS super_shop_schema.orders (
	order_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	placed_in TIMESTAMP NOT NULL,
	customer_id INT NOT NULL,
	order_status TEXT NOT NULL CHECK (order_status IN ('PENDING', 'PAID', 'SHIPPED', 'CANCELLED')),
	CONSTRAINT uq_order UNIQUE (placed_in, customer_id), --Prevents the same customer from placing multiple orders at the exact same timestamp
	CONSTRAINT fk_customer_id FOREIGN KEY(customer_id)
		REFERENCES super_shop_schema.customers(customer_id)
		ON DELETE CASCADE
	--CONSTRAINT fk_order_status_id FOREIGN KEY(order_status_id)
	--	REFERENCES super_shop_schema.order_status(order_status_id)
	--	ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- TABLE: order_items
-- Business model:
-- - order (FK to orders)
-- - product (FK to products)
-- - combination of order and product is the primary key
-- - quantity (integer > 0)
-- - unit price charged (numeric > 0)
-- ----------------------------------------------------------
CREATE TABLE IF NOT EXISTS super_shop_schema.order_items (
	order_id INT NOT NULL,
	product_id INT NOT NULL,
	quantity INT NOT NULL CHECK (quantity > 0),
	unit_price DECIMAL(10, 2) CHECK (unit_price > 0),
	CONSTRAINT pk_order_items_id PRIMARY KEY(order_id, product_id),
    CONSTRAINT fk_order_id FOREIGN KEY(order_id)
		REFERENCES super_shop_schema.orders(order_id)
		ON DELETE CASCADE,
	CONSTRAINT fk_product_id FOREIGN KEY(product_id)
		REFERENCES super_shop_schema.products(product_id)
		ON DELETE CASCADE
);

