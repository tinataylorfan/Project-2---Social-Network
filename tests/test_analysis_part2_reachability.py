import unittest
from datetime import date

from analysis_part2.reachability import (
    average_degrees_of_separation,
    degrees_of_separation,
    is_reachable,
    shortest_path,
)
from models_part1 import User
from structures_part1 import SocialGraph


class TestAnalysisPart2Reachability(unittest.TestCase):
    def make_graph(self):
        graph = SocialGraph()
        for user_id in range(1, 6):
            graph.add_user(User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN"))
        graph.add_follow(1, 2)
        graph.add_follow(2, 3)
        graph.add_follow(1, 4)
        graph.add_follow(4, 3)
        return graph

    def test_shortest_path_found(self):
        graph = self.make_graph()
        self.assertEqual(shortest_path(graph, 1, 3), [1, 2, 3])

    def test_same_user_path(self):
        graph = self.make_graph()
        self.assertEqual(shortest_path(graph, 1, 1), [1])
        self.assertEqual(degrees_of_separation(graph, 1, 1), 0)

    def test_unreachable_user(self):
        graph = self.make_graph()
        self.assertFalse(is_reachable(graph, 3, 1))
        self.assertEqual(shortest_path(graph, 3, 1), [])
        self.assertIsNone(degrees_of_separation(graph, 3, 1))

    def test_degrees_and_average(self):
        graph = self.make_graph()
        self.assertTrue(is_reachable(graph, 1, 3))
        self.assertEqual(degrees_of_separation(graph, 1, 3), 2)
        self.assertGreater(average_degrees_of_separation(graph), 0)


if __name__ == "__main__":
    unittest.main()
