from abc import ABC, abstractmethod
from typing import Optional, List
from app.models.order_status import OrderStatus


class OrderStatusRepository(ABC):

    # ======================================================================================
    #                         -------- C.R.U.D operations --------
    # ======================================================================================
    @abstractmethod
    def create(self, order_status: OrderStatus) -> OrderStatus | None:
        """
        Create a new order_status record.
        Args:
            order_status (Order_Status): The order_status object to be created.
        Returns:
            OrderStatus: The created order_status object, usually with an assigned ID or None (In case of error).
        """
        pass

    @abstractmethod
    def get_by_id(self, order_status_id: int) -> Optional[OrderStatus] | None:
        """
        Retrieve an order_status by their unique ID.
        Args:
            order_status_id (int): The ID of the order_status to retrieve.
        Returns:
            Optional[OrderStatus]: The order_status object if found, else None if no order_status found or if no success.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[OrderStatus] | None:
        """
        Retrieve all order_status records.
        Returns:
            List[OrderStatus]: A list of all categories if found, else None if no order_status found or if no success.
        """
        pass

    @abstractmethod
    def update(self, order_status: OrderStatus) -> OrderStatus | None:
        """
        Update an existing order_status record.
        Args:
            order_status (OrderStatus): The order_status object with updated data. Must include the ID.
        Returns:
            OrderStatus: The updated order_status object or None if no order_status found or if no success.
        """
        pass

    @abstractmethod
    def delete(self, order_status_id: int) -> int | None:
        """
        Delete an order_status by their unique ID.
        Args:
            order_status_id (int): The ID of the order_status to delete.
        Returns:
            OrderStatus id: The id of the deleted order_status object or None if order_status not fount or if no success.
        """
        pass

    # ======================================================================================
    #                       ---------- Custom queries ----------
    # ======================================================================================

