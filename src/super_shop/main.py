def menu():
    return """
    ===================================================== SUPER SHOP ======================================================
    --------------------------------
    ------ Basic SQL Queries -------
    --------------------------------
    1. List all customers ordered by account creation date (from oldest to newest).
    2. List all products (product name and price) ordered by descending price.
    3. List all orders placed between two dates (for example, between March 1st and March 15th, 2024).
    4. List all products whose price is strictly greater than €50.
    5. List all products belonging to a given category (for example, “Electronic”).
    --------------------------------
    --------- Simple Joins ---------
    --------------------------------
    6. List all products with their category name.
    7. List all orders with the customer's full name (first name + last name).
    8. List all order items with: customer name, product name, quantity, billed unit price.
    9. List all orders whose status is PAID or SHIPPED.
    --------------------------------
    -------- Advanced Joins --------
    --------------------------------
    10. Display the complete details of each order, including: order date, customer name, list of products,
        quantity, billed unit price, total line amount (quantity x unit price).
    11. Calculate the total amount of each order and display only: the order ID, the customer name, the total order amount.
    12. Display orders whose total amount exceeds €100.
    13. List all categories with their total revenue (sum of line amounts for all products in that category).
    --------------------------------
    ---------- Subqueries ----------
    --------------------------------
    14. List products that have been sold at least once.
    15. List products that have never been sold.
    16. Find the customer who has spent the most (TOP 1 by total revenue).
    17. Display the top 3 best-selling products in terms of total quantity sold.
    18. List orders whose total amount is strictly greater than the average of all orders.
    --------------------------------
    --- Statistics & Aggregates ----
    --------------------------------
    19. Calculate the total revenue (all orders combined, optionally excluding cancelled orders).
    20. Calculate the average basket value (average amount per order).
    21. Calculate the total quantity sold per category.
    22. Calculate the monthly revenue (based on the provided data).
    23. Format monetary amounts to display only two decimal places.
    --------------------------------
    --- Conditional Logic (CASE) ---
    --------------------------------
    24. For each order, display: order ID, customer, order date, status, a human-readable version of the status using CASE:
        PAID → “Paid”, SHIPPED → “Shipped”, PENDING → “Pending”, CANCELLED → “Cancelled”
    25. For each customer, calculate the total amount spent and classify them into segments: < €100 → “Bronze”,
        €100-300 → “Silver”, > €300 → “Gold”
        Display: first name, last name, total amount spent, segment.
    --------------------------------
    ------- Final Challenge --------
    --------------------------------
    26. Propose and write 5 additional advanced analytical queries, for example:
    27. Top 5 most active customers (number of orders).
    28. Top 5 customers by total spending.
    29. Top 3 most profitable categories.
    30. Products that generated less than €10 in total revenue.
    31. Customers who placed only one order.
    32. Products included in cancelled orders, with the corresponding “lost” revenue.
    33. Generate a Text Report with: 'Total revenue', 'Average basket value', 'Most ordered product (by total quantity)',
        'Top 3 customers by total spending', 'Revenue by category'.
    =======================================================================================================================
    """

def main():
    print(menu())

if __name__ == "__main__":
    main()