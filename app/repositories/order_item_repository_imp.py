from decimal import Decimal
from typing import Optional

from config.setting import settings
import psycopg
from app.models.order_item import OrderItem
from app.repositories.order_item_repository import OrderItemRepository


class PostgresOrderItemRepository(OrderItemRepository):
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
                        CREATE TABLE IF NOT EXISTS super_shop_schema.order_items (
                            order_id INT NOT NULL,
                            product_id INT NOT NULL,
                            quantity INT CHECK (quantity > 0),
                            unit_price DECIMAL(10, 2) CHECK (unit_price > 0),
                            CONSTRAINT pk_order_items_id PRIMARY KEY(order_id, product_id),
                            CONSTRAINT fk_order_id FOREIGN KEY(order_id)
                                REFERENCES super_shop_schema.orders(order_id)
                                ON DELETE CASCADE,
                            CONSTRAINT fk_product_id FOREIGN KEY(product_id)
                                REFERENCES super_shop_schema.products(product_id)
                                ON DELETE CASCADE
                        );
                    """)
        except Exception as e:
            print(f"[KO]: Error when trying to create the order_items table: {e}")
        finally:
            conn.close()

    # ======================================================================================
    #                         -------- C.R.U.D operations --------
    # ======================================================================================
    def create(self, order_item: OrderItem) -> OrderItem | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO super_shop_schema.order_items (order_id, product_id, quantity, unit_price) 
                        VALUES (%s, %s, %s, %s) 
                        RETURNING order_id, product_id
                        """,
                        (
                            order_item.order_id,
                            order_item.product_id,
                            order_item.quantity,
                            order_item.unit_price
                        )
                    )
                    returned_order_id, returned_product_id = cur.fetchone()

                    # (Optional) validate the DB echoed back the same values
                    if (returned_order_id != order_item.order_id or
                        returned_product_id != order_item.product_id):
                        print("[WARN] Inserted keys differ from input values.")

                    return order_item
        except Exception as e:
            print(f"[KO]: Error when trying to add the order_item '{order_item}': {e}")
            return None
        finally:
            conn.close()

    def get_by_id(self, order_id: int, product_id: int) -> Optional[OrderItem] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT *
                        FROM super_shop_schema.order_items
                        WHERE order_id = %s and product_id = %s
                        """,
                        (order_id, product_id)
                    )
                    row = cur.fetchone()
                    if row:
                        return OrderItem(order_id=row[0], product_id=row[1], quantity=row[2], unit_price=row[3])
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get the orderItem with id '{(order_id, product_id)}': {e}")
            return None
        finally:
            conn.close()

    def get_all(self) -> list[OrderItem] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM super_shop_schema.order_items")
                    rows = cur.fetchall()
                    if rows:
                        return [OrderItem(order_id=r[0], product_id=r[1], quantity=r[2], unit_price=r[3]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get all order_items: {e}")
            return None
        finally:
            conn.close()

    def update(self, order_item: OrderItem) -> OrderItem | None:
        conn = self._get_connection()
        try:
            if order_item.order_id is None or order_item.product_id is None:
                raise Exception(f"order_items id (order_id, product_id) must not be None when updating")
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE super_shop_schema.order_items 
                        SET quantity = %s, unit_price = %s
                        WHERE order_id = %s and product_id = %s
                        """,
                        (
                            order_item.quantity,
                            order_item.unit_price,
                            order_item.order_id,
                            order_item.product_id
                        )
                    )
                    # If no row was updated → return None
                    if cur.rowcount == 0:
                        return None
                return order_item
        except Exception as e:
            print(f"[KO]: Error when trying to update order_items '{order_item}': {e}")
            return None
        finally:
            conn.close()

    def delete(self, order_id: int, product_id: int) -> tuple[int, int] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM super_shop_schema.order_items
                        WHERE order_id = %s and product_id = %s
                        """,
                        (order_id, product_id,)
                    )
                    # If no row was deleted → return None
                    if cur.rowcount == 0:
                        return None
                    return order_id, product_id
        except Exception as e:
            print(f"[KO]: Error when trying to delete orderItem with id '({order_id}, {product_id})': {e}")
            return None
        finally:
            conn.close()

    # ======================================================================================
    #                       ---------- Custom queries ----------
    # ======================================================================================




if __name__ == "__main__":

    order_item1 = OrderItem(order_id=5, product_id=9, quantity=100, unit_price=Decimal(102.50))
    order_item2 = OrderItem(order_id=2, product_id=2, quantity=150, unit_price=Decimal(130.02))

    # orderItem_with_id = OrderItem(orderItem_id=3, name="Danonne3", price=1.3, available_stock=300, category_id=3)
    # replace with your actual connection string / credentials
    DSN = settings.DSN
    repo = PostgresOrderItemRepository(DSN)

    # --- Init table :
    # automatically done.

    # --- Create OrderItem:
    print("\n# --- Create OrderItem:")
    print(repo.create(order_item1))
    print(repo.create(order_item2))

    # --- Get OrderItem by id:
    print("\n# --- Get OrderItem by id:")
    print(repo.get_by_id(1, 9))

    # --- Get All OrderItems:
    print("\n# --- Get all OrderItems:")
    print(repo.get_all())

    # --- Update OrderItem:
    print("\n# --- Update OrderItem:")
    print(repo.update(OrderItem(order_id=5, product_id=9, quantity=100100, unit_price=Decimal(102.50))))

    # --- Delete OrderItem:
    print("\n# --- Delete OrderItem:")
    print(repo.delete(3, 9))
    # print(repo.delete(47))




