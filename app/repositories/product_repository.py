from abc import ABC, abstractmethod
from typing import Optional, List

from app.models.product import Product

class ProductRepository(ABC):

    # -------- C.R.U.D operations --------    
    @abstractmethod
    def create(self, product: Product) -> Product | None:
        """
        Create a new product record.
        Args:
            product (Product): The product object to be created.
        Returns:
            Product: The created product object, usually with an assigned ID or None (In case of error).
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product] | None:
        """
        Retrieve a product by their unique ID.
        Args:
            product_id (int): The ID of the product to retrieve.
        Returns:
            Optional[Product]: The product object if found, else None if no product found or if no success.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Product] | None:
        """
        Retrieve all product records.
        Returns:
            List[Product]: A list of all categories if found, else None if no product found or if no success.
        """
        pass

    @abstractmethod
    def update(self, product: Product) -> Product | None:
        """
        Update an existing product record.
        Args:
            product (Product): The product object with updated data. Must include the ID.
        Returns:
            Product: The updated product object or None if no product found or if no success.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> int | None:
        """
        Delete a product by their unique ID.
        Args:
            product_id (int): The ID of the product to delete.
        Returns:
            Product id: The id of the deleted product object or None if product not fount or if no success.
        """
        pass

    # ---------- Custom queries ----------
