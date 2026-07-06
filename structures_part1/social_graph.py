from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Set

from models_part1 import User
from structures_part1.user_index_bst import UserIndexBST


class SocialGraph:
    """Part 1 Task 2: directed graph as the main structure.

    The graph owns the BST index and keeps it synchronized. The BST never
    changes the graph, so there are no circular updates.
    """

    def __init__(self) -> None:
        self.users: Dict[int, User] = {}
        self.following: Dict[int, Set[int]] = {}
        self.followers: Dict[int, Set[int]] = {}
        self.user_index = UserIndexBST()

    def add_user(self, user: User) -> None:
        if user.user_id in self.users:
            raise ValueError(f"user_id {user.user_id} already exists")
        user.update_follower_count(0)
        self.users[user.user_id] = user
        self.following[user.user_id] = set()
        self.followers[user.user_id] = set()
        self.user_index.insert(user)

    def remove_user(self, user_id: int) -> None:
        if user_id not in self.users:
            return

        user = self.users[user_id]
        for followee_id in list(self.following[user_id]):
            self.remove_follow(user_id, followee_id)

        for follower_id in list(self.followers[user_id]):
            self.following[follower_id].discard(user_id)

        self.user_index.remove_user(user)
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
        followee = self.users[followee_id]
        self.user_index.update_user_count(followee, followee.follower_count + 1)
        return True

    def remove_follow(self, follower_id: int, followee_id: int) -> bool:
        if follower_id not in self.users or followee_id not in self.users:
            return False
        if followee_id not in self.following[follower_id]:
            return False

        self.following[follower_id].remove(followee_id)
        self.followers[followee_id].remove(follower_id)
        followee = self.users[followee_id]
        self.user_index.update_user_count(followee, followee.follower_count - 1)
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

    def follower_count_is_consistent(self, user_id: int) -> bool:
        self._require_user(user_id)
        return self.users[user_id].follower_count == len(self.followers[user_id])

    def _require_user(self, user_id: int) -> None:
        if user_id not in self.users:
            raise KeyError(f"unknown user_id: {user_id}")
