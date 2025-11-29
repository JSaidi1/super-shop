from abc import ABC, abstractmethod
from typing import List, Literal, Optional

from app.models.customer import Customer

class CustomerRepository(ABC):

    # -------- C.R.U.D operations --------    
    @abstractmethod
    def create(self, customer: Customer) -> Customer | None:
        """
        Create a new customer record.
        Args:
            customer (Customer): The customer object to be created.
        Returns:
            Customer: The created customer object, usually with an assigned ID or None (In case of error).
        """
        pass

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer] | None:
        """
        Retrieve a customer by their unique ID.
        Args:
            customer_id (int): The ID of the customer to retrieve.
        Returns:
            Optional[Customer]: The customer object if found, else None if no customer found or if no success.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Customer] | None:
        """
        Retrieve all customer records.
        Returns:
            List[Customer]: A list of all customers if found, else None if no customer found or if no success.
        """
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Customer | None:
        """
        Update an existing customer record.
        Args:
            customer (Customer): The customer object with updated data. Must include the ID.
        Returns:
            Customer: The updated customer object or None if no customer found or if success.
        """
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> int | None:
        """
        Delete a customer by their unique ID.
        Args:
            customer_id (int): The ID of the customer to delete.
        Returns:
            Customer id: The id of the deleted customer object or None if customer not fount or if no success.
        """
        pass

    # ---------- Custom queries ----------
    @abstractmethod
    def list_customers_by_creation_date(self, order: Literal['ascending', 'descending']) -> List[Customer] | None:
        """
        List all customers sorted by account creation date (ascending or descending order).
        Args:
            order (str): The order (ascending or descending)
        Returns:
            List[Customer]: A list of customers or None if no customer found or if no success.
        """
        pass
