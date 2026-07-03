import unittest
from datetime import date

from part1_toolbox.part1_task1_data_modeling import User
from part1_toolbox.part1_task3_bst_user_index import UserIndexBST


class TestTask3BSTUserIndex(unittest.TestCase):
    def make_user(self, user_id, follower_count):
        return User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN", follower_count)

    def test_empty_tree_queries(self):
        bst = UserIndexBST()
        self.assertEqual(bst.search(10), [])
        self.assertEqual(bst.find_top_k(3), [])
        self.assertEqual(bst.find_range(1, 100), [])

    def test_top_k_handles_zero_and_negative_k(self):
        bst = UserIndexBST()
        bst.insert(self.make_user(1, 100))
        self.assertEqual(bst.find_top_k(0), [])
        self.assertEqual(bst.find_top_k(-2), [])

    def test_duplicate_follower_counts_are_all_searchable(self):
        bst = UserIndexBST()
        for user in [self.make_user(3, 50), self.make_user(1, 50), self.make_user(2, 50)]:
            bst.insert(user)
        self.assertEqual([user.user_id for user in bst.search(50)], [1, 2, 3])

    def test_range_with_invalid_bounds_returns_empty(self):
        bst = UserIndexBST()
        bst.insert(self.make_user(1, 100))
        self.assertEqual(bst.find_range(200, 100), [])

    def test_remove_user_and_update_count(self):
        bst = UserIndexBST()
        user_a = self.make_user(1, 100)
        user_b = self.make_user(2, 200)
        user_c = self.make_user(3, 300)
        for user in [user_a, user_b, user_c]:
            bst.insert(user)

        bst.remove_user(user_b)
        self.assertEqual([user.user_id for user in bst.find_top_k(3)], [3, 1])

        bst.update_user_count(user_a, 500)
        self.assertEqual([user.user_id for user in bst.find_top_k(1)], [1])
        self.assertEqual(bst.search(100), [])


if __name__ == "__main__":
    unittest.main()
