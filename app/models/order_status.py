from dataclasses import dataclass
from typing import Optional
from app.enums.order_status import OrderStatusName


@dataclass
class OrderStatus:
    order_status_id: Optional[int] = None                          # auto-generated primary key
    order_status_name: OrderStatusName = OrderStatusName.PENDING   # Status name restricted to the allowed enum values
