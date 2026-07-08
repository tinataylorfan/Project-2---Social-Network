from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from models_part1 import User


@dataclass
class _Node:
    user: User
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None

    @property
    def key(self) -> tuple[int, int]:
        return self.user.follower_count, self.user.user_id


class UserIndexBST:
    """Task 3 / 任务3: BST / 二叉树."""

    def __init__(self) -> None:
        self.root: Optional[_Node] = None

    def insert(self, user: User) -> None:
        self.root = self._insert(self.root, user)

    def search(self, follower_count: int) -> List[User]:
        result: List[User] = []
        self._search_count(self.root, follower_count, result)
        return sorted(result, key=lambda user: user.user_id)

    def find_top_k(self, k: int) -> List[User]:
        if k <= 0:
            return []
        users = self.to_sorted_list(descending=True)
        return users[:k]

    def find_range(self, min_count: int, max_count: int) -> List[User]:
        if min_count > max_count:
            return []
        result: List[User] = []
        self._range_search(self.root, min_count, max_count, result)
        return sorted(result, key=lambda user: (user.follower_count, user.user_id))

    def remove_user(self, user: User, old_follower_count: int | None = None) -> None:
        count = user.follower_count if old_follower_count is None else old_follower_count
        self.root = self._remove(self.root, (count, user.user_id))

    def update_user_count(self, user: User, new_count: int) -> None:
        # Graph only / 仅图调用
        old_count = user.follower_count
        self.remove_user(user, old_count)
        user.update_follower_count(new_count)
        self.insert(user)

    def to_sorted_list(self, descending: bool = False) -> List[User]:
        result: List[User] = []
        self._collect_users(self.root, result)
        result.sort(key=lambda user: (user.follower_count, user.user_id), reverse=descending)
        if descending:
            result.sort(key=lambda user: (-user.follower_count, user.user_id))
        return result

    def _insert(self, node: Optional[_Node], user: User) -> _Node:
        if node is None:
            return _Node(user)
        key = (user.follower_count, user.user_id)
        if key == node.key:
            node.user = user
        elif key < node.key:
            node.left = self._insert(node.left, user)
        else:
            node.right = self._insert(node.right, user)
        return node

    def _search_count(self, node: Optional[_Node], follower_count: int, result: List[User]) -> None:
        if node is None:
            return
        node_count = node.user.follower_count
        if follower_count < node_count:
            self._search_count(node.left, follower_count, result)
        elif follower_count > node_count:
            self._search_count(node.right, follower_count, result)
        else:
            result.append(node.user)
            self._search_count(node.left, follower_count, result)
            self._search_count(node.right, follower_count, result)

    def _range_search(
        self, node: Optional[_Node], min_count: int, max_count: int, result: List[User]
    ) -> None:
        if node is None:
            return
        node_count = node.user.follower_count
        if node_count > min_count:
            self._range_search(node.left, min_count, max_count, result)
        if min_count <= node_count <= max_count:
            result.append(node.user)
        if node_count < max_count:
            self._range_search(node.right, min_count, max_count, result)

    def _collect_users(self, node: Optional[_Node], result: List[User]) -> None:
        if node is None:
            return
        self._collect_users(node.left, result)
        result.append(node.user)
        self._collect_users(node.right, result)

    def _remove(self, node: Optional[_Node], key: tuple[int, int]) -> Optional[_Node]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._remove(node.left, key)
            return node
        if key > node.key:
            node.right = self._remove(node.right, key)
            return node
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        successor = self._min_node(node.right)
        node.user = successor.user
        node.right = self._remove(node.right, successor.key)
        return node

    @staticmethod
    def _min_node(node: _Node) -> _Node:
        while node.left is not None:
            node = node.left
        return node
