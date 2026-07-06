import unittest
from datetime import date

from models_part1 import User
from structures_part1 import SocialGraph


class TestStructuresPart1GraphSync(unittest.TestCase):
    def make_graph(self):
        graph = SocialGraph()
        for user_id in range(1, 6):
            graph.add_user(User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN", 999))
        return graph

    def test_add_user_resets_fabricated_count_and_indexes_user(self):
        graph = SocialGraph()
        user = User(1, "Alice", date(2026, 7, 1), "China", 120)
        graph.add_user(user)
        self.assertEqual(user.follower_count, 0)
        self.assertEqual(graph.user_index.search(0), [user])

    def test_add_follow_updates_graph_count_and_bst(self):
        graph = self.make_graph()
        graph.add_follow(1, 2)
        self.assertEqual(graph.get_followers(2), [1])
        self.assertEqual(graph.users[2].follower_count, 1)
        self.assertIn(graph.users[2], graph.user_index.search(1))
        self.assertNotIn(graph.users[2], graph.user_index.search(0))

    def test_duplicate_follow_does_not_double_count(self):
        graph = self.make_graph()
        self.assertTrue(graph.add_follow(1, 2))
        self.assertFalse(graph.add_follow(1, 2))
        self.assertEqual(graph.users[2].follower_count, 1)
        self.assertEqual(graph.get_followers(2), [1])

    def test_remove_follow_updates_graph_count_and_bst(self):
        graph = self.make_graph()
        graph.add_follow(1, 2)
        graph.add_follow(3, 2)
        self.assertEqual(graph.users[2].follower_count, 2)
        self.assertTrue(graph.remove_follow(1, 2))
        self.assertEqual(graph.get_followers(2), [3])
        self.assertEqual(graph.users[2].follower_count, 1)
        self.assertIn(graph.users[2], graph.user_index.search(1))

    def test_remove_user_cleans_edges_and_bst(self):
        graph = self.make_graph()
        graph.add_follow(1, 2)
        graph.add_follow(2, 3)
        graph.add_follow(4, 2)
        graph.remove_user(2)
        self.assertNotIn(2, graph.users)
        self.assertFalse(graph.is_following(1, 2))
        self.assertFalse(graph.is_following(2, 3))
        self.assertEqual(graph.users[3].follower_count, 0)
        self.assertNotIn(2, [user.user_id for user in graph.user_index.to_sorted_list()])

    def test_self_follow_and_missing_users_are_rejected(self):
        graph = self.make_graph()
        with self.assertRaises(ValueError):
            graph.add_follow(1, 1)
        with self.assertRaises(KeyError):
            graph.add_follow(1, 999)

    def test_reachable_from_respects_direction(self):
        graph = self.make_graph()
        graph.add_follow(1, 2)
        graph.add_follow(2, 3)
        graph.add_follow(4, 1)
        self.assertEqual(graph.reachable_from(1), {2, 3})
        self.assertNotIn(4, graph.reachable_from(1))


if __name__ == "__main__":
    unittest.main()
