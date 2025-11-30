from abc import ABC, abstractmethod
from typing import List, Literal, Optional

from app.models.category import Category

class CategoryRepository(ABC):

    # ======================================================================================
    #                         -------- C.R.U.D operations --------
    # ======================================================================================
    @abstractmethod
    def create(self, category: Category) -> Category | None:
        """
        Create a new category record.
        Args:
            category (Category): The category object to be created.
        Returns:
            Category: The created category object, usually with an assigned ID or None (In case of error).
        """
        pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category] | None:
        """
        Retrieve a category by their unique ID.
        Args:
            category_id (int): The ID of the category to retrieve.
        Returns:
            Optional[Category]: The category object if found, else None if no category found or if no success.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Category] | None:
        """
        Retrieve all category records.
        Returns:
            List[Category]: A list of all categories if found, else None if no category found or if no success.
        """
        pass

    @abstractmethod
    def update(self, category: Category) -> Category | None:
        """
        Update an existing category record.
        Args:
            category (Category): The category object with updated data. Must include the ID.
        Returns:
            Category: The updated category object or None if no category found or if no success.
        """
        pass

    @abstractmethod
    def delete(self, category_id: int) -> int | None:
        """
        Delete a category by their unique ID.
        Args:
            category_id (int): The ID of the category to delete.
        Returns:
            Category id: The id of the deleted category object or None if category not fount or if no success.
        """
        pass

    # ======================================================================================
    #                       ---------- Custom queries ----------
    # ======================================================================================
