from abc import ABC, abstractmethod
from typing import Optional, List

from app.models.order_item import OrderItem

class OrderItemRepository(ABC):

    # -------- C.R.U.D operations --------    
    @abstractmethod
    def create(self, order_item: OrderItem) -> OrderItem | None:
        """
        Create a new orderItem record.
        Args:
            order_item (OrderItem): The orderItem object to be created.
        Returns:
            OrderItem: The created orderItem object, usually with an assigned ID or None (In case of error).
        """
        pass

    @abstractmethod
    def get_by_id(self, order_id: int, product_id: int) -> Optional[OrderItem] | None:
        """
        Retrieve a orderItem by their unique ID.
        Args:
            order_id (int): The foreign key that refers to the Order entity.
            product_id (int): The foreign key that refers to the Product entity.
        Returns:
            Optional[OrderItem]: The orderItem object if found, else None if no orderItem found or if no success.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[OrderItem] | None:
        """
        Retrieve all order_items records.
        Returns:
            List[OrderItem]: A list of all order_items if found, else None if no orderItem found or if no success.
        """
        pass

    @abstractmethod
    def update(self, order_item: OrderItem) -> OrderItem | None:
        """
        Update an existing order_item record.
        Args:
            order_item (OrderItem): The orderItem object with updated data. Must include the ID (order_id and product_id).
        Returns:
            OrderItem: The updated orderItem object or None if no orderItem found or if no success.
        """
        pass

    @abstractmethod
    def delete(self, order_id: int, product_id: int) -> int | None:
        """
        Delete an order_item by their unique ID (order_id and product_id).
        Args:
            order_id (int): The foreign key that refers to the Order entity.
            product_id (int): The foreign key that refers to the Product entity.
        Returns:
            OrderItem id: The id (order_id, product_id) of the deleted orderItem object or None if orderItem not fount or if no success.
        """
        pass

    # ---------- Custom queries ----------
