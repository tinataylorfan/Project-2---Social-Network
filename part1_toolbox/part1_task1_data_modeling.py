from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(eq=False)
class User:
    """Task 1: user node / 用户节点."""

    user_id: int
    username: str
    join_date: date
    country: str
    follower_count: int

    def __post_init__(self) -> None:
        # 基本合法性检查 / basic validation
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            raise ValueError("user_id must be a positive integer")
        if not isinstance(self.username, str) or not self.username.strip():
            raise ValueError("username must be a non-empty string")
        if not isinstance(self.join_date, date):
            raise TypeError("join_date must be a datetime.date object")
        if not isinstance(self.country, str) or not self.country.strip():
            raise ValueError("country must be a non-empty string")
        if not isinstance(self.follower_count, int) or self.follower_count < 0:
            raise ValueError("follower_count must be a non-negative integer")
        self.username = self.username.strip()
        self.country = self.country.strip()

    def __hash__(self) -> int:
        return hash(self.user_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, User) and self.user_id == other.user_id

    def update_follower_count(self, new_count: int) -> None:
        if not isinstance(new_count, int) or new_count < 0:
            raise ValueError("follower_count must be a non-negative integer")
        self.follower_count = new_count


__all__ = ["User"]
