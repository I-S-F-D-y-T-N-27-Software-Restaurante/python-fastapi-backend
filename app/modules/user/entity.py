from typing import Optional

from pydantic.dataclasses import dataclass

from app.shared.timestamp_mixin import TimestampMixin


@dataclass(kw_only=True)
class UserEntity(TimestampMixin):
    name: str
    email: str
    password: str

    id: Optional[int] = None
