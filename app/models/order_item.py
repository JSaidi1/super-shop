from dataclasses import dataclass
from decimal import Decimal

@dataclass
class OrderItem:
    order_id: int              # FK to orders(order_id)
    product_id: int            # FK to products(product_id)
    quantity: int              # INT, must be > 0
    unit_price: Decimal        # DECIMAL(10, 2), must be > 0
