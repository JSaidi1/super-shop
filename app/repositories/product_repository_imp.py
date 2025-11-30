from typing import Optional, Literal, List, Tuple

from config.setting import settings
import psycopg
from app.models.product import Product
from app.repositories.product_repository import ProductRepository


class PostgresProductRepository(ProductRepository):
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._init_table()

    def _get_connection(self):
        return psycopg.connect(self.dsn)

    def _init_table(self):
        # attempt to create table if not exists
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS super_shop_schema.products (
                            product_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            name VARCHAR(50) NOT NULL UNIQUE,
                            price NUMERIC(10, 2) CHECK (price > 0),
                            available_stock INT CHECK (available_stock >= 0),
                            category_id INT NOT NULL,
                            CONSTRAINT fk_category_id FOREIGN KEY(category_id)
                                REFERENCES super_shop_schema.categories(category_id)
                                ON DELETE CASCADE
                        );
                    """)
        except Exception as e:
            print(f"[KO]: Error when trying to create the product table: {e}")
        finally:
            conn.close()

    # ======================================================================================
    #                         -------- C.R.U.D operations --------
    # ======================================================================================
    def create(self, product: Product) -> Product | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO super_shop_schema.products (name, price, available_stock, category_id) 
                        VALUES (%s, %s, %s, %s) RETURNING product_id
                        """,
                        (
                            product.name,
                            product.price,
                            product.available_stock,
                            product.category_id
                        )
                    )
                    new_id = cur.fetchone()[0]
                    product.product_id = new_id
                    return product
        except Exception as e:
            print(f"[KO]: Error when trying to add the product '{product}': {e}")
            return None
        finally:
            conn.close()

    def get_by_id(self, product_id: int) -> Optional[Product] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM super_shop_schema.products WHERE product_id = %s",
                        (product_id,)
                    )
                    row = cur.fetchone()
                    if row:
                        return Product(product_id=row[0], name=row[1], price=row[2], available_stock=row[3], category_id=row[4])
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get the product with id '{product_id}': {e}")
            return None
        finally:
            conn.close()

    def get_all(self) -> list[Product] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM super_shop_schema.products")
                    rows = cur.fetchall()
                    if rows:
                        return [Product(product_id=r[0], name=r[1], price=r[2], available_stock=r[3], category_id=r[4]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get all products: {e}")
            return None
        finally:
            conn.close()

    def update(self, product: Product) -> Product | None:
        conn = self._get_connection()
        try:
            if product.product_id is None:
                raise Exception("Product id must not be None when updating")
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE super_shop_schema.products 
                        SET name = %s, price = %s, available_stock = %s, category_id = %s
                        WHERE product_id = %s
                        """,
                        (
                            product.name,
                            product.price,
                            product.available_stock,
                            product.category_id,
                            product.product_id
                        )
                    )
                    # If no row was updated → return None
                    if cur.rowcount == 0:
                        return None
                return product
        except Exception as e:
            print(f"[KO]: Error when trying to update product '{product}': {e}")
            return None
        finally:
            conn.close()

    def delete(self, product_id: int) -> int | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM super_shop_schema.products
                        WHERE product_id = %s
                        """,
                        (product_id,)
                    )
                    # If no row was deleted → return None
                    if cur.rowcount == 0:
                        return None
                    return product_id
        except Exception as e:
            print(f"[KO]: Error when trying to delete product with id '{product_id}': {e}")
            return None
        finally:
            conn.close()

    # ======================================================================================
    #                       ---------- Custom queries ----------
    # ======================================================================================
    def list_products_names_and_prices_sorted_by_price(self, order: Literal['ascending', 'descending']) -> list[tuple[str, float]] | None:
        conn = self._get_connection()
        try:
            if order != "ascending" and order != "descending":
                raise Exception("Order must be 'ascending' or 'descending'")
            with conn:
                with conn.cursor() as cur:
                    if order == "ascending":
                        cur.execute(
                            """
                            SELECT name, price 
                            FROM super_shop_schema.products
                            ORDER BY price ASC
                            """
                        )
                    else:
                        cur.execute(
                            """
                            SELECT name, price 
                            FROM super_shop_schema.products
                            ORDER BY price DESC
                            """
                        )
                    rows = cur.fetchall()
                    if rows:
                        return [(r[0], r[1]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying list products names ans prices by price: {e}")
            return None
        finally:
            conn.close()

    def list_products_with_price_above(self, min_price: float) -> List[Product] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT * 
                        FROM super_shop_schema.products
                        WHERE price > %s
                        """,
                        (min_price,)
                    )
                    rows = cur.fetchall()
                    if rows:
                        return [Product(product_id=r[0], name=r[1], price=r[2], available_stock=r[3], category_id=r[4]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to list products which price is above {min_price}: {e}")
            return None
        finally:
            conn.close()

    def list_products_by_category(self, category_name: str, ignore_case: bool=False) -> List[Product] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    if ignore_case:
                        cur.execute(
                            """
                            SELECT p.*
                            FROM super_shop_schema.products p
                            LEFT JOIN super_shop_schema.categories c
                                ON p.category_id = c.category_id
                            WHERE c.name ILIKE %s
                            """,
                            (category_name,)
                        )
                    else:
                        cur.execute(
                            """
                            SELECT p.*
                            FROM super_shop_schema.products p
                            LEFT JOIN super_shop_schema.categories c
                                ON p.category_id = c.category_id
                            WHERE c.name = %s
                            """,
                            (category_name,)
                        )
                    rows = cur.fetchall()
                    if rows:
                        return [Product(product_id=r[0], name=r[1], price=r[2], available_stock=r[3], category_id=r[4])
                                for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to list products which category is '{category_name}': {e}")
            return None
        finally:
            conn.close()

    def list_products_never_sold(self) -> List[Product] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT p.* 
                        FROM super_shop_schema.products p
                        LEFT JOIN super_shop_schema.order_items oi
                            ON p.product_id = oi.product_id
                        WHERE oi.product_id IS NULL;
                        """
                    )
                    rows = cur.fetchall()
                    if rows:
                        return [Product(product_id=r[0], name=r[1], price=r[2], available_stock=r[3], category_id=r[4])
                                for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to list products which never sold: {e}")
            return None
        finally:
            conn.close()

    def list_products_top_best_selling(self, top_nbr: int) -> List[Product] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT p.*
                        FROM super_shop_schema.products p
                        JOIN super_shop_schema.order_items oi
                            ON p.product_id = oi.product_id
                        GROUP BY p.product_id
                        ORDER BY SUM(quantity) DESC
                        LIMIT %s
                        """,
                        (top_nbr,)
                    )
                    rows = cur.fetchall()
                    if rows:
                        return [Product(product_id=r[0], name=r[1], price=r[2], available_stock=r[3], category_id=r[4])
                                for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to list products which are on top best-selling: {e}")
            return None
        finally:
            conn.close()

    def list_products_with_revenue_below(self, max_revenue: float) -> List[Tuple[int, str, float]] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT
                            p.product_id,
                            p.name,
                            COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue
                        FROM super_shop_schema.products p
                        LEFT JOIN super_shop_schema.order_items oi ON oi.product_id = p.product_id
                        LEFT JOIN super_shop_schema.orders o       ON o.order_id = oi.order_id -- AND o.status <> 'CANCELLED'
                        GROUP BY p.product_id, p.name
                        HAVING COALESCE(SUM(oi.quantity * oi.unit_price), 0) < %s
                        ORDER BY total_revenue ASC;
                        """,
                        (max_revenue,)
                    )
                    rows = cur.fetchall()
                    if rows:
                        return [(r[0], r[1], r[2]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to list products which generate less than 'max revenue' in total revenue: {e}")
            return None
        finally:
            conn.close()



if __name__ == "__main__":

    product1 = Product(name="Danonne", price=1.0, available_stock=100, category_id=1)
    product2 = Product(name="Danonne2", price=1.2, available_stock=200, category_id=2)

    product_with_id = Product(product_id=3, name="Danonne3", price=1.3, available_stock=300, category_id=3)
    # replace with your actual connection string / credentials
    DSN = settings.DSN
    repo = PostgresProductRepository(DSN)

    # --- Init table :
    # automatically done.

    # --- Create Product:
    print("\n# --- Create Product:")
    print(repo.create(product1))
    print(repo.create(product2))

    # --- Get Product by id:
    print("\n# --- Get Product by id:")
    print(repo.get_by_id(4))

    # --- Get All Products:
    print("\n# --- Get all Products:")
    print(repo.get_all())

    # --- Update Product:
    print("\n# --- Update Product:")
    print(repo.update(product_with_id))

    # --- Delete Product:
    print("\n# --- Delete Product:")
    print(repo.delete(3))
    print(repo.delete(47))

    # --- List products names and prices sorted by price:
    print("\n# --- List products names and prices sorted by price:")
    print(repo.list_products_names_and_prices_sorted_by_price("ascending"))
    print(repo.list_products_names_and_prices_sorted_by_price("descending"))

    # --- List products with price above a certain price:
    print("\n# --- List products with price above a certain price:")
    print(repo.list_products_with_price_above(50))

    # --- List products by category:
    print("\n# --- List products by category:")
    print(repo.list_products_by_category('Électronique', True))

    # --- List products never sold:
    print("\n# --- List products never sold:")
    print(repo.list_products_never_sold())

    # --- List products top best-selling:
    print("\n# --- List products top best-selling:")
    print(repo.list_products_top_best_selling(3))

    # --- List products with revenue below:
    print("\n# --- List products with revenue below:")
    print(repo.list_products_with_revenue_below(10))


