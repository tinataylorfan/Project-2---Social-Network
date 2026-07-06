import unittest
from datetime import date

from models_part1 import User
from structures_part1 import UserIndexBST


class TestStructuresPart1BST(unittest.TestCase):
    def make_user(self, user_id, follower_count):
        return User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN", follower_count)

    def test_empty_tree_queries(self):
        bst = UserIndexBST()
        self.assertEqual(bst.search(10), [])
        self.assertEqual(bst.find_top_k(3), [])
        self.assertEqual(bst.find_range(1, 10), [])

    def test_insert_search_and_duplicate_counts(self):
        bst = UserIndexBST()
        for user in [self.make_user(3, 50), self.make_user(1, 50), self.make_user(2, 50)]:
            bst.insert(user)
        self.assertEqual([user.user_id for user in bst.search(50)], [1, 2, 3])

    def test_top_k_orders_by_followers_then_user_id(self):
        bst = UserIndexBST()
        for user in [self.make_user(1, 10), self.make_user(2, 30), self.make_user(3, 30)]:
            bst.insert(user)
        self.assertEqual([user.user_id for user in bst.find_top_k(3)], [2, 3, 1])
        self.assertEqual(bst.find_top_k(0), [])

    def test_range_query(self):
        bst = UserIndexBST()
        for user in [self.make_user(1, 5), self.make_user(2, 10), self.make_user(3, 20)]:
            bst.insert(user)
        self.assertEqual([user.user_id for user in bst.find_range(6, 20)], [2, 3])
        self.assertEqual(bst.find_range(20, 6), [])

    def test_remove_and_update_user_count(self):
        bst = UserIndexBST()
        user_a = self.make_user(1, 10)
        user_b = self.make_user(2, 20)
        for user in [user_a, user_b]:
            bst.insert(user)
        bst.remove_user(user_b)
        self.assertEqual([user.user_id for user in bst.find_top_k(2)], [1])
        bst.update_user_count(user_a, 30)
        self.assertEqual(bst.search(10), [])
        self.assertEqual([user.user_id for user in bst.search(30)], [1])


if __name__ == "__main__":
    unittest.main()
