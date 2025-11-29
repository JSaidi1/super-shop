from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    customer_id: Optional[int] = None           # auto-generated primary key
    first_name: str = ""                        # VARCHAR(50) NOT NULL
    last_name: str = ""                         # VARCHAR(50) NOT NULL
    email: str = ""                             # VARCHAR(100) NOT NULL UNIQUE
    created_at: Optional[datetime] = field(default_factory=datetime.now)  # default NOW()
