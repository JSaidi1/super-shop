import datetime
from config.setting import settings
from typing import Literal, List, Optional
import psycopg
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository



class PostgresCustomerRepository(CustomerRepository):
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
                        CREATE TABLE IF NOT EXISTS super_shop_schema.customers (
                            customer_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            first_name VARCHAR(50) NOT NULL,
                            last_name VARCHAR(50) NOT NULL,
                            email VARCHAR(100) NOT NULL UNIQUE,
                            created_at TIMESTAMP NOT NULL DEFAULT NOW()
                        );
                    """)
        except Exception as e:
            print(f"[KO]: Error when trying to create the customer table: {e}")
        finally:
            conn.close()

    # ======================================================================================
    #                         -------- C.R.U.D operations --------
    # ======================================================================================
    def create(self, customer: Customer) -> Customer | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO super_shop_schema.customers (first_name, last_name, email, created_at) "
                        "VALUES (%s, %s, %s, %s) RETURNING customer_id",
                        (customer.first_name, customer.last_name, customer.email, customer.created_at)
                    )
                    new_id = cur.fetchone()[0]
                    customer.customer_id = new_id
                    return customer
        except Exception as e:
            print(f"[KO]: Error when trying to add the customer '{customer}': {e}")
            return None
        finally:
            conn.close()

    def get_by_id(self, customer_id: int) -> Optional[Customer] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM super_shop_schema.customers WHERE customer_id = %s",
                        (customer_id,)
                    )
                    row = cur.fetchone()
                    if row:
                        return Customer(customer_id=row[0], first_name=row[1], last_name=row[2], email=row[3], created_at=row[4])
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get the customer with id '{customer_id}': {e}")
            return None
        finally:
            conn.close()

    def get_all(self) -> list[Customer] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM super_shop_schema.customers")
                    rows = cur.fetchall()
                    if rows:
                        return [Customer(customer_id=r[0], first_name=r[1], last_name=r[2], email=r[3], created_at=r[4]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get all customers: {e}")
            return None
        finally:
            conn.close()

    def update(self, customer: Customer) -> Customer | None:
        conn = self._get_connection()
        try:
            if customer.customer_id is None:
                raise Exception("Customer id must not be None when updating")
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE super_shop_schema.customers 
                        SET first_name = %s, last_name = %s, email = %s, created_at = %s 
                        WHERE customer_id = %s
                        """,
                        (
                            customer.first_name,
                            customer.last_name,
                            customer.email,
                            customer.created_at,
                            customer.customer_id
                        )
                    )
                    # If no row was updated → force jump to except
                    if cur.rowcount == 0:
                        return None
                return customer
        except Exception as e:
            print(f"[KO]: Error when trying to update customer '{customer}': {e}")
            return None
        finally:
            conn.close()

    def delete(self, customer_id: int) -> int | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM super_shop_schema.customers 
                        WHERE customer_id = %s
                        """,
                        (customer_id,)
                    )
                    # If no row was deleted → force jump to except
                    if cur.rowcount == 0:
                        return None
                    return customer_id
        except Exception as e:
            print(f"[KO]: Error when trying to delete customer with id '{customer_id}': {e}")
            return None
        finally:
            conn.close()

    # ======================================================================================
    #                       ---------- Custom queries ----------
    # ======================================================================================
    def list_customers_by_creation_date(self, order: Literal['ascending', 'descending']) -> List[Customer] | None:
        conn = self._get_connection()
        try:
            if order != "ascending" and order != "descending":
                raise Exception("Order must be 'ascending' or 'descending'")
            with conn:
                with conn.cursor() as cur:
                    if order == "ascending":
                        cur.execute(
                            """
                            SELECT * 
                            FROM super_shop_schema.customers 
                            ORDER BY created_at ASC
                            """
                        )
                    else:
                        cur.execute(
                            """
                            SELECT * 
                            FROM super_shop_schema.customers 
                            ORDER BY created_at DESC
                            """
                        )
                    rows = cur.fetchall()
                    if rows:
                        return [Customer(customer_id=r[0], first_name=r[1], last_name=r[2], email=r[3], created_at=r[4])
                                for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying list customers by creation date: {e}")
            return None
        finally:
            conn.close()


if __name__ == "__main__":

    customer1 = Customer(first_name="Joel", last_name="Smith", email="joel1@hotmail.com", created_at=datetime.datetime(2020, 1, 1, 2, 1, 45, 10))
    customer2 = Customer(first_name="Joel2", last_name="Smith2", email="joel2@hotmail.com", created_at=datetime.datetime(2020, 1, 2, 2, 1, 45, 15))

    customer_with_id = Customer(customer_id=30, first_name="Joel", last_name="Smith", email="joel30@hotmail.com", created_at=datetime.datetime(2020, 1, 1))
    # replace with your actual connection string / credentials
    DSN = settings.DSN
    repo = PostgresCustomerRepository(DSN)

    # --- Init table :
    # automatically done.

    # --- Create Customer:
    print("\n# --- Create Customer:")
    print(repo.create(customer1))
    print(repo.create(customer2))

    # --- Get Customer by id:
    print("\n# --- Get Customer by id:")
    print(repo.get_by_id(4))

    # --- Get All Customers:
    print("\n# --- Get all Customers:")
    print(repo.get_all())

    # --- Update Customer:
    print("\n# --- Update Customer:")
    print(repo.update(customer_with_id))

    # --- Delete Customer:
    print("\n# --- Delete Customer:")
    print(repo.delete(47))

    # --- List customers by creation date:
    print("\n# --- List customers by creation date:")
    print("asending = ", repo.list_customers_by_creation_date("ascending"))
    print("desending = ", repo.list_customers_by_creation_date("descending"))



