from abc import ABC, abstractmethod
from typing import Optional, List, Literal, Tuple

from app.models.product import Product

class ProductRepository(ABC):

    # ======================================================================================
    #                         -------- C.R.U.D operations --------
    # ======================================================================================
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

    # ======================================================================================
    #                       ---------- Custom queries ----------
    # ======================================================================================
    @abstractmethod
    def list_products_names_and_prices_sorted_by_price(self, order: Literal['ascending', 'descending']) -> list[tuple[str, float]] | None:
        """
        List all products names and prices sorted by price (ascending or descending order).
        Args:
                order (str): The order (ascending or descending)
        Returns:
                list[tuple[str, float]]: Sorted list of (name, price) by ascending/descending price or None if no row found or if no success.
        """
        pass

    def list_products_with_price_above(self, min_price: float) -> List[Product] | None:
        """
        List all products which price is above a certain price.
        Args:
                min_price (float): min price
        Returns:
                List[Product]: Products which price is above a certain price or None if no product found or if no success.
        """
        pass

    def list_products_by_category(self, category_name: str, ignore_case: bool=False) -> List[Product] | None:
        """
        List products witch belong to a certain category.
        Args:
            category_name (str): The category name
            ignore_case (bool): To search products with category in case-sensitive or not
        Returns:
            List[Product]: Products which category is on argument or None if no product found or if no success.
        """
        pass

    def list_products_never_sold(self) -> List[Product] | None:
        """
        List products witch never sold.
        Args:
        Returns:
            List[Product]: List products witch never sold or None if no product found or if no success.
        """
        pass

    def list_products_top_best_selling(self, top_nbr: int) -> List[Product] | None:
        """
        List products witch are on top best-selling (limit is top_nbr).
        Args:
            top_nbr (int): The number of products to return
        Returns:
            List[Product]: List products witch are on top best-selling (limit is top_nbr) or None if no product found or if no success.
        """
        pass

    def list_products_with_revenue_below(self, max_revenue: float) -> List[Tuple[int, str, float]]  | None:
        """
        List of Products that generated less than max_revenue in total revenue.
        Args:
            max_revenue (float): Search will be based on it
        Returns:
            List[Product]: List of Products that generated less than max_revenue in total revenue or None if no product found or if no success.
        """
        pass