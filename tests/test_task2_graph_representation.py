import unittest
from datetime import date

from part1_toolbox.part1_task1_data_modeling import User
from part1_toolbox.part1_task2_graph_representation import SocialGraph


class TestTask2GraphRepresentation(unittest.TestCase):
    def make_graph(self):
        graph = SocialGraph()
        for user_id in range(1, 6):
            graph.add_user(User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN", user_id * 10))
        return graph

    def test_duplicate_user_is_rejected(self):
        graph = self.make_graph()
        with self.assertRaises(ValueError):
            graph.add_user(User(1, "duplicate", date(2026, 7, 1), "CN", 1))

    def test_follow_requires_existing_users(self):
        graph = self.make_graph()
        with self.assertRaises(KeyError):
            graph.add_follow(1, 999)
        with self.assertRaises(KeyError):
            graph.get_following(999)

    def test_remove_nonexistent_follow_returns_false(self):
        graph = self.make_graph()
        self.assertFalse(graph.remove_follow(1, 2))
        self.assertFalse(graph.remove_follow(1, 999))

    def test_in_degree_out_degree_and_edges(self):
        graph = self.make_graph()
        graph.add_follow(1, 2)
        graph.add_follow(1, 3)
        graph.add_follow(4, 2)
        self.assertEqual(graph.out_degree(1), 2)
        self.assertEqual(graph.in_degree(2), 2)
        self.assertEqual(graph.edges(), [(1, 2), (1, 3), (4, 2)])

    def test_reachable_from_uses_direction(self):
        graph = self.make_graph()
        graph.add_follow(1, 2)
        graph.add_follow(2, 3)
        graph.add_follow(4, 1)
        self.assertEqual(graph.reachable_from(1), {2, 3})
        self.assertNotIn(4, graph.reachable_from(1))


if __name__ == "__main__":
    unittest.main()
