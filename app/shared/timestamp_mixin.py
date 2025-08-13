from datetime import datetime
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class TimestampMixin:
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
