from dataclasses import dataclass
from typing import Optional

@dataclass
class Category:
    category_id: Optional[int] = None           # auto-generated primary key
    name: str = ""                              # VARCHAR(50) NOT NULL UNIQUE
    description: str = ""                       # VARCHAR(200)
