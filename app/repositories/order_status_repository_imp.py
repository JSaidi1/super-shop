from typing import Optional

from config.setting import settings
import psycopg
from app.models.order_status import OrderStatus
from app.repositories.order_status_repository import OrderStatusRepository



class PostgresOrderStatusRepository(OrderStatusRepository):
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
                        CREATE TABLE IF NOT EXISTS super_shop_schema.order_status (
                            order_status_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            order_status_name TEXT UNIQUE CHECK (order_status_name IN ('PENDING', 'PAID', 'SHIPPED', 'CANCELLED'))
                        );
                    """)
        except Exception as e:
            print(f"[KO]: Error when trying to create the order_status table: {e}")
        finally:
            conn.close()

    def create(self, order_status: OrderStatus) -> OrderStatus | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO super_shop_schema.order_status (order_status_name) 
                        VALUES (%s) 
                        RETURNING order_status_id
                        """,
                        (
                            order_status.order_status_name,
                        )
                    )
                    new_id = cur.fetchone()[0]
                    order_status.order_status_id = new_id
                    return order_status
        except Exception as e:
            print(f"[KO]: Error when trying to add the order_status '{order_status}': {e}")
            return None
        finally:
            conn.close()

    def get_by_id(self, order_status_id: int) -> Optional[OrderStatus] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM super_shop_schema.order_status WHERE order_status_id = %s",
                        (order_status_id,)
                    )
                    row = cur.fetchone()
                    if row:
                        return OrderStatus(order_status_id=row[0], order_status_name=row[1])
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get the order_status with id '{order_status_id}': {e}")
            return None
        finally:
            conn.close()

    def get_all(self) -> list[OrderStatus] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM super_shop_schema.order_status")
                    rows = cur.fetchall()
                    if rows:
                        return [OrderStatus(order_status_id=r[0], order_status_name=r[1]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get all order_status: {e}")
            return None
        finally:
            conn.close()

    def update(self, order_status: OrderStatus) -> OrderStatus | None:
        conn = self._get_connection()
        try:
            if order_status.order_status_id is None:
                raise Exception("Order_Status id must not be None when updating")
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE super_shop_schema.order_status 
                        SET order_status_name = %s 
                        WHERE order_status_id = %s
                        """,
                        (
                            order_status.order_status_name,
                            order_status.order_status_id
                        )
                    )
                    # If no row was updated → return None
                    if cur.rowcount == 0:
                        return None
                return order_status
        except Exception as e:
            print(f"[KO]: Error when trying to update order_status '{order_status}': {e}")
            return None
        finally:
            conn.close()

    def delete(self, order_status_id: int) -> int | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM super_shop_schema.order_status
                        WHERE order_status_id = %s
                        """,
                        (order_status_id,)
                    )
                    # If no row was deleted → return None
                    if cur.rowcount == 0:
                        return None
                    return order_status_id
        except Exception as e:
            print(f"[KO]: Error when trying to delete order_status with id '{order_status_id}': {e}")
            return None
        finally:
            conn.close()



if __name__ == "__main__":

    order_status1 = OrderStatus(order_status_name="PENDING")
    order_status2 = OrderStatus(order_status_name="Toto")

    order_status_with_id = OrderStatus(order_status_id=2, order_status_name="SHIPPED")
    # replace with your actual connection string / credentials
    DSN = settings.DSN
    repo = PostgresOrderStatusRepository(DSN)

    # --- Init table :
    # automatically done.

    # --- Create Order_Status:
    print("\n# --- Create Order_Status:")
    print(repo.create(order_status1))
    print(repo.create(order_status2))

    # --- Get Order_Status by id:
    print("\n# --- Get Order_Status by id:")
    print(repo.get_by_id(4))

    # --- Get All Categories:
    print("\n# --- Get all Categories:")
    print(repo.get_all())

    # --- Update Order_Status:
    print("\n# --- Update OrderStatus:")
    print(repo.update(order_status_with_id))

    # --- Delete Order_Status:
    print("\n# --- Delete OrderStatus:")
    print(repo.delete(4))
    print(repo.delete(47))




