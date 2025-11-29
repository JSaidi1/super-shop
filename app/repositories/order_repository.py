from abc import ABC, abstractmethod
from typing import Optional, List

from app.models.order import Order

class OrderRepository(ABC):

    # -------- C.R.U.D operations --------    
    @abstractmethod
    def create(self, order: Order) -> Order | None:
        """
        Create a new order record.
        Args:
            order (Order): The order object to be created.
        Returns:
            Order: The created order object, usually with an assigned ID or None (In case of error).
        """
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order] | None:
        """
        Retrieve an order by their unique ID.
        Args:
            order_id (int): The ID of the order to retrieve.
        Returns:
            Optional[Order]: The order object if found, else None if no order found or if no success.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Order] | None:
        """
        Retrieve all order records.
        Returns:
            List[Order]: A list of all categories if found, else None if no order found or if no success.
        """
        pass

    @abstractmethod
    def update(self, order: Order) -> Order | None:
        """
        Update an existing order record.
        Args:
            order (Order): The order object with updated data. Must include the ID.
        Returns:
            Order: The updated order object or None if no order found or if no success.
        """
        pass

    @abstractmethod
    def delete(self, order_id: int) -> int | None:
        """
        Delete an order by their unique ID.
        Args:
            order_id (int): The ID of the order to delete.
        Returns:
            Order id: The id of the deleted order object or None if order not fount or if no success.
        """
        pass

    # ---------- Custom queries ----------
