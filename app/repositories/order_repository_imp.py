import datetime
from typing import Optional

from config.setting import settings
import psycopg
from app.models.order import Order
from app.repositories.order_repository import OrderRepository


class PostgresOrderRepository(OrderRepository):
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
                        CREATE TABLE IF NOT EXISTS super_shop_schema.orders (
                            order_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            placed_in TIMESTAMP NOT NULL,
                            customer_id INT NOT NULL,
                            order_status_id INT NOT NULL,
                            CONSTRAINT uq_order UNIQUE (placed_in, customer_id), --Prevents the same customer from placing multiple orders at the exact same timestamp
                            CONSTRAINT fk_customer_id FOREIGN KEY(customer_id)
                                REFERENCES super_shop_schema.customers(customer_id)
                                ON DELETE CASCADE,
                            CONSTRAINT fk_order_status_id FOREIGN KEY(order_status_id)
                                REFERENCES super_shop_schema.order_status(order_status_id)
                                ON DELETE CASCADE
                        );
                    """)
        except Exception as e:
            print(f"[KO]: Error when trying to create the order table: {e}")
        finally:
            conn.close()

    def create(self, order: Order) -> Order | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO super_shop_schema.orders (placed_in, customer_id, order_status_id) 
                        VALUES (%s, %s, %s) RETURNING order_id
                        """,
                        (
                            order.placed_in,
                            order.customer_id,
                            order.order_status_id,
                        )
                    )
                    new_id = cur.fetchone()[0]
                    order.order_id = new_id
                    return order
        except Exception as e:
            print(f"[KO]: Error when trying to add the order '{order}': {e}")
            return None
        finally:
            conn.close()

    def get_by_id(self, order_id: int) -> Optional[Order] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM super_shop_schema.orders WHERE order_id = %s",
                        (order_id,)
                    )
                    row = cur.fetchone()
                    if row:
                        return Order(order_id=row[0], placed_in=row[1], customer_id=row[2], order_status_id=row[3])
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get the order with id '{order_id}': {e}")
            return None
        finally:
            conn.close()

    def get_all(self) -> list[Order] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM super_shop_schema.orders")
                    rows = cur.fetchall()
                    if rows:
                        return [Order(order_id=r[0], placed_in=r[1], customer_id=r[2], order_status_id=r[3]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get all orders: {e}")
            return None
        finally:
            conn.close()

    def update(self, order: Order) -> Order | None:
        conn = self._get_connection()
        try:
            if order.order_id is None:
                raise Exception("Order id must not be None when updating")
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE super_shop_schema.orders 
                        SET placed_in = %s, customer_id = %s, order_status_id = %s
                        WHERE order_id = %s
                        """,
                        (
                            order.placed_in,
                            order.customer_id,
                            order.order_status_id,
                            order.order_id
                        )
                    )
                    # If no row was updated → return None
                    if cur.rowcount == 0:
                        return None
                return order
        except Exception as e:
            print(f"[KO]: Error when trying to update order '{order}': {e}")
            return None
        finally:
            conn.close()

    def delete(self, order_id: int) -> int | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM super_shop_schema.orders
                        WHERE order_id = %s
                        """,
                        (order_id,)
                    )
                    # If no row was deleted → return None
                    if cur.rowcount == 0:
                        return None
                    return order_id
        except Exception as e:
            print(f"[KO]: Error when trying to delete order with id '{order_id}': {e}")
            return None
        finally:
            conn.close()



if __name__ == "__main__":

    order1 = Order(placed_in=datetime.datetime(2020, 1, 1, 2, 1, 45, 10), customer_id=1, order_status_id=1)
    order2 = Order(placed_in=datetime.datetime(2022, 1, 1, 2, 1, 45, 10), customer_id=2, order_status_id=2)

    order_with_id = Order(order_id=3, placed_in=datetime.datetime(2023, 1, 1, 2, 1, 45, 10), customer_id=5, order_status_id=3)
    # replace with your actual connection string / credentials
    DSN = settings.DSN
    repo = PostgresOrderRepository(DSN)

    # --- Init table :
    # automatically done.

    # --- Create Order:
    print("\n# --- Create Order:")
    print(repo.create(order1))
    print(repo.create(order2))

    # --- Get Order by id:
    print("\n# --- Get Order by id:")
    print(repo.get_by_id(4))

    # --- Get All Orders:
    print("\n# --- Get all Orders:")
    print(repo.get_all())

    # --- Update Order:
    print("\n# --- Update Order:")
    print(repo.update(order_with_id))

    # --- Delete Order:
    print("\n# --- Delete Order:")
    print(repo.delete(11))
    print(repo.delete(47))




