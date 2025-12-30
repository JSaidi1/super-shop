-- ================================================================================
-- FILE: data.sql
-- SUBJECT: Inserting initial data to start operations
-- CONTENT: Insert requests to insert data on tables defined on schema.sql script
-- ================================================================================

-- ----------------------------------------------------------
-- DATA: CATEGORIES
-- Corresponds to the "Categories" block of the subject
-- ----------------------------------------------------------
INSERT INTO super_shop_schema.categories (name, description) 
VALUES
    ('Électronique',       'Produits high-tech et accessoires'),
    ('Maison & Cuisine',   'Électroménager et ustensiles'),
    ('Sport & Loisirs',    'Articles de sport et plein air'),
    ('Beauté & Santé',     'Produits de beauté, hygiène, bien-être'),
    ('Jeux & Jouets',      'Jouets pour enfants et adultes');

-- ----------------------------------------------------------
-- DATA: PRODUCTS
-- Corresponds to the "Products" block of the topic
-- ----------------------------------------------------------
INSERT INTO super_shop_schema.products(name, price, available_stock, category_id) 
VALUES
    ('Casque Bluetooth X1000',        79.99,  50,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Électronique')),
    ('Souris Gamer Pro RGB',          49.90, 120,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Électronique')),
    ('Bouilloire Inox 1.7L',          29.99,  80,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Maison & Cuisine')),
    ('Aspirateur Cyclonix 3000',     129.00,  40,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Maison & Cuisine')),
    ('Tapis de Yoga Comfort+',        19.99, 150,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Sport & Loisirs')),
    ('Haltères 5kg (paire)',          24.99,  70,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Sport & Loisirs')),
    ('Crème hydratante BioSkin',      15.90, 200,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Beauté & Santé')),
    ('Gel douche FreshEnergy',         4.99, 300,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Beauté & Santé')),
    ('Puzzle 1000 pièces "Montagne"', 12.99,  95,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Jeux & Jouets')),
    ('Jeu de société "Galaxy Quest"', 29.90,  60,  (SELECT category_id FROM super_shop_schema.categories WHERE name = 'Jeux & Jouets'));

-- ----------------------------------------------------------
-- DATA: CUSTOMERS
-- Corresponds to the "Customers" block in the section
-- ----------------------------------------------------------
INSERT INTO super_shop_schema.customers(first_name, last_name, email, created_at) 
VALUES
    ('Alice',  'Martin',      'alice.martin@mail.com',     '2024-01-10 14:32:00.000001'),
    ('Bob',    'Dupont',      'bob.dupont@mail.com',       '2024-02-05 09:10:00.010000'),
    ('Chloé',  'Bernard',     'chloe.bernard@mail.com',    '2024-03-12 17:22:00.020000'),
    ('David',  'Robert',      'david.robert@mail.com',     '2024-01-29 11:45:00.000000'),
    ('Emma',   'Leroy',       'emma.leroy@mail.com',       '2024-03-02 08:55:00.111000'),
    ('Félix',  'Petit',       'felix.petit@mail.com',      '2024-02-18 16:40:05.000600'),
    ('Hugo',   'Roussel',     'hugo.roussel@mail.com',     '2024-03-20 19:05:00.000002'),
    ('Inès',   'Moreau',      'ines.moreau@mail.com',      '2024-01-17 10:15:00.021000'),
    ('Julien', 'Fontaine',    'julien.fontaine@mail.com',  '2024-01-23 13:55:20.000000'),
    ('Katia',  'Garnier',     'katia.garnier@mail.com',    '2024-03-15 12:00:00.500004');

-- ----------------------------------------------------------
-- DATA: ORDER STATUS
-- Corresponds to the "order_status" block of the subject
-- ----------------------------------------------------------
INSERT INTO super_shop_schema.order_status(order_status_name) 
VALUES
    ('PENDING'),
    ('PAID'),
    ('SHIPPED'),
    ('CANCELLED');

-- ----------------------------------------------------------
-- DATA: ORDERS
-- Corresponds to the "Orders" block of the subject
-- The customer_id is retrieved from the email
-- ----------------------------------------------------------
INSERT INTO super_shop_schema.orders(placed_in, customer_id, order_status_id) 
VALUES
    ('2024-03-01 10:20:10.000009', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'alice.martin@mail.com'),    (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'PAID')),
    ('2024-03-04 09:12:00.000200', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'bob.dupont@mail.com'),      (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'SHIPPED')),
    ('2024-03-08 15:02:20.020000', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'chloe.bernard@mail.com'),   (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'PAID')),
    ('2024-03-09 11:45:00.000003', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'david.robert@mail.com'),    (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'CANCELLED')),
    ('2024-03-10 08:10:00.000000', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'emma.leroy@mail.com'),      (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'PAID')),
    ('2024-03-11 13:50:01.005000', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'felix.petit@mail.com'),     (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'PENDING')),
    ('2024-03-15 19:30:00.000000', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'hugo.roussel@mail.com'),    (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'SHIPPED')),
    ('2024-03-16 10:00:00.060000', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'ines.moreau@mail.com'),     (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'PAID')),
    ('2024-03-18 14:22:00.000000', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'julien.fontaine@mail.com'), (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'PAID')),
    ('2024-03-20 18:00:02.123001', (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'katia.garnier@mail.com'),   (SELECT order_status_id FROM super_shop_schema.order_status WHERE order_status_name = 'PENDING'));

-- ----------------------------------------------------------
-- DATA: ORDER LINES (ORDER_ITEMS)
-- Corresponds to the "Order Lines" block of the subject
-- We retrieve:
-- - order_id via (email + order date)
-- - product_id via product name
-- ----------------------------------------------------------
INSERT INTO super_shop_schema.order_items(order_id, product_id, quantity, unit_price) 
VALUES
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-01 10:20:10.000009' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'alice.martin@mail.com')),    (SELECT product_id FROM super_shop_schema.products WHERE name = 'Casque Bluetooth X1000'),        1,  79.99),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-01 10:20:10.000009' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'alice.martin@mail.com')),    (SELECT product_id FROM super_shop_schema.products WHERE name = 'Puzzle 1000 pièces "Montagne"'), 2,  12.99),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-04 09:12:00.000200' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'bob.dupont@mail.com')),      (SELECT product_id FROM super_shop_schema.products WHERE name = 'Tapis de Yoga Comfort+'),        1,  19.99),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-08 15:02:20.020000' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'chloe.bernard@mail.com')),   (SELECT product_id FROM super_shop_schema.products WHERE name = 'Bouilloire Inox 1.7L'),          1,  29.99),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-08 15:02:20.020000' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'chloe.bernard@mail.com')),   (SELECT product_id FROM super_shop_schema.products WHERE name = 'Gel douche FreshEnergy'),        3,   4.99),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-09 11:45:00.000003' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'david.robert@mail.com')),    (SELECT product_id FROM super_shop_schema.products WHERE name = 'Haltères 5kg (paire)'),          1,  24.99),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-10 08:10:00.000000' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'emma.leroy@mail.com')),      (SELECT product_id FROM super_shop_schema.products WHERE name = 'Crème hydratante BioSkin'),      2,  15.90),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-18 14:22:00.000000' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'julien.fontaine@mail.com')), (SELECT product_id FROM super_shop_schema.products WHERE name = 'Jeu de société "Galaxy Quest"'), 1,  29.90),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-20 18:00:02.123001' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'katia.garnier@mail.com')),   (SELECT product_id FROM super_shop_schema.products WHERE name = 'Souris Gamer Pro RGB'),          1,  49.90),
    ((SELECT order_id FROM super_shop_schema.orders WHERE placed_in = '2024-03-20 18:00:02.123001' and customer_id = (SELECT customer_id FROM super_shop_schema.customers WHERE email = 'katia.garnier@mail.com')),   (SELECT product_id FROM super_shop_schema.products WHERE name = 'Gel douche FreshEnergy'),        2,   4.99);

/*
SELECT order_id 
FROM super_shop_schema.orders 
WHERE placed_in = '2024-03-01 10:20:10.000009' 
AND customer_id = (SELECT customer_id 
                    FROM super_shop_schema.customers 
					WHERE email = 'alice.martin@mail.com');
*/