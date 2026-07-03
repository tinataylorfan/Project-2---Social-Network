from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Set

from part1_toolbox.part1_task1_data_modeling import User


class SocialGraph:
    """Task 2: directed graph / 有向社交图."""

    def __init__(self) -> None:
        # following 是出边，followers 是入边 / outgoing and incoming edges
        self.users: Dict[int, User] = {}
        self.following: Dict[int, Set[int]] = {}
        self.followers: Dict[int, Set[int]] = {}

    def add_user(self, user: User) -> None:
        if user.user_id in self.users:
            raise ValueError(f"user_id {user.user_id} already exists")
        self.users[user.user_id] = user
        self.following[user.user_id] = set()
        self.followers[user.user_id] = set()

    def remove_user(self, user_id: int) -> None:
        if user_id not in self.users:
            return
        for followee_id in list(self.following[user_id]):
            self.followers[followee_id].discard(user_id)
        for follower_id in list(self.followers[user_id]):
            self.following[follower_id].discard(user_id)
        del self.following[user_id]
        del self.followers[user_id]
        del self.users[user_id]

    def add_follow(self, follower_id: int, followee_id: int) -> bool:
        self._require_user(follower_id)
        self._require_user(followee_id)
        if follower_id == followee_id:
            raise ValueError("self-follow is not allowed")
        if followee_id in self.following[follower_id]:
            return False
        self.following[follower_id].add(followee_id)
        self.followers[followee_id].add(follower_id)
        return True

    def remove_follow(self, follower_id: int, followee_id: int) -> bool:
        if follower_id not in self.users or followee_id not in self.users:
            return False
        if followee_id not in self.following[follower_id]:
            return False
        self.following[follower_id].remove(followee_id)
        self.followers[followee_id].remove(follower_id)
        return True

    def get_following(self, user_id: int) -> List[int]:
        self._require_user(user_id)
        return sorted(self.following[user_id])

    def get_followers(self, user_id: int) -> List[int]:
        self._require_user(user_id)
        return sorted(self.followers[user_id])

    def is_following(self, follower_id: int, followee_id: int) -> bool:
        return followee_id in self.following.get(follower_id, set())

    def out_degree(self, user_id: int) -> int:
        self._require_user(user_id)
        return len(self.following[user_id])

    def in_degree(self, user_id: int) -> int:
        self._require_user(user_id)
        return len(self.followers[user_id])

    def edges(self) -> List[tuple[int, int]]:
        return sorted((a, b) for a, targets in self.following.items() for b in targets)

    def user_ids(self) -> List[int]:
        return sorted(self.users)

    def neighbors(self, user_id: int) -> Iterable[int]:
        self._require_user(user_id)
        return self.following[user_id]

    def reachable_from(self, source_id: int) -> Set[int]:
        self._require_user(source_id)
        visited = {source_id}
        queue = deque([source_id])
        while queue:
            current = queue.popleft()
            for nxt in self.following[current]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        visited.remove(source_id)
        return visited

    def _require_user(self, user_id: int) -> None:
        if user_id not in self.users:
            raise KeyError(f"unknown user_id: {user_id}")


__all__ = ["SocialGraph"]
