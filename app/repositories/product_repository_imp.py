from typing import Optional

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




