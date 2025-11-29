from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Order:
    placed_in: datetime              # NOT NULL
    customer_id: int                 # NOT NULL, FK to customers (customer_id)
    order_status_id: int             # NOT NULL, FK to order_status (order_status_id)
    order_id: Optional[int] = None  # auto-generated primary key

