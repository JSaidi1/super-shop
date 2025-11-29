from config.setting import settings
import psycopg
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository



class PostgresCategoryRepository(CategoryRepository):
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
                        CREATE TABLE IF NOT EXISTS super_shop_schema.categories (
                            category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            name VARCHAR(50) NOT NULL UNIQUE,
                            description VARCHAR(200)
                        );
                    """)
        except Exception as e:
            print(f"[KO]: Error when trying to create the category table: {e}")
        finally:
            conn.close()

    def create(self, category: Category) -> Category | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO super_shop_schema.categories (name, description) 
                        VALUES (%s, %s) RETURNING category_id
                        """,
                        (
                            category.name,
                            category.description
                        )
                    )
                    new_id = cur.fetchone()[0]
                    category.category_id = new_id
                    return category
        except Exception as e:
            print(f"[KO]: Error when trying to add the category '{category}': {e}")
            return None
        finally:
            conn.close()

    def get_by_id(self, category_id: int) -> Optional[Category] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM super_shop_schema.categories WHERE category_id = %s",
                        (category_id,)
                    )
                    row = cur.fetchone()
                    if row:
                        return Category(category_id=row[0], name=row[1], description=row[2])
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get the category with id '{category_id}': {e}")
            return None
        finally:
            conn.close()

    def get_all(self) -> list[Category] | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM super_shop_schema.categories")
                    rows = cur.fetchall()
                    if rows:
                        return [Category(category_id=r[0], name=r[1], description=r[2]) for r in rows]
                    return None
        except Exception as e:
            print(f"[KO]: Error when trying to get all categories: {e}")
            return None
        finally:
            conn.close()

    def update(self, category: Category) -> Category | None:
        conn = self._get_connection()
        try:
            if category.category_id is None:
                raise Exception("Category id must not be None when updating")
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE super_shop_schema.categories 
                        SET name = %s, description = %s 
                        WHERE category_id = %s
                        """,
                        (
                            category.name,
                            category.description,
                            category.category_id
                        )
                    )
                    # If no row was updated → return None
                    if cur.rowcount == 0:
                        return None
                return category
        except Exception as e:
            print(f"[KO]: Error when trying to update category '{category}': {e}")
            return None
        finally:
            conn.close()

    def delete(self, category_id: int) -> int | None:
        conn = self._get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM super_shop_schema.categories
                        WHERE category_id = %s
                        """,
                        (category_id,)
                    )
                    # If no row was deleted → return None
                    if cur.rowcount == 0:
                        return None
                    return category_id
        except Exception as e:
            print(f"[KO]: Error when trying to delete category with id '{category_id}': {e}")
            return None
        finally:
            conn.close()



if __name__ == "__main__":

    category1 = Category(name="Joel", description="Smith")
    category2 = Category(name="Joel2", description="Smith2")

    category_with_id = Category(category_id=3, name="Nature et découverte", description="sdfeferfrefrererfefefrfr")
    # replace with your actual connection string / credentials
    DSN = settings.DSN
    repo = PostgresCategoryRepository(DSN)

    # --- Init table :
    # automatically done.

    # --- Create Category:
    print("\n# --- Create Category:")
    print(repo.create(category1))
    print(repo.create(category2))

    # --- Get Category by id:
    print("\n# --- Get Category by id:")
    print(repo.get_by_id(4))

    # --- Get All Categories:
    print("\n# --- Get all Categories:")
    print(repo.get_all())

    # --- Update Category:
    print("\n# --- Update Category:")
    print(repo.update(category_with_id))

    # --- Delete Category:
    print("\n# --- Delete Category:")
    print(repo.delete(3))
    print(repo.delete(47))




