from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    product_id: Optional[int] = None     # Auto-generated IDENTITY
    name: str = ""                       # VARCHAR(50) NOT NULL UNIQUE
    price: float = 0.0                   # NUMERIC(10, 2), must be > 0
    available_stock: int = 0             # INT, must be >= 0
    category_id: int = 0                 # FK to categories(category_id)
