import unittest
from datetime import date

from analysis_part2.community_detection import largest_communities, strongly_connected_components
from models_part1 import User
from structures_part1 import SocialGraph


class TestAnalysisPart2CommunityDetection(unittest.TestCase):
    def make_graph(self):
        graph = SocialGraph()
        for user_id in range(1, 8):
            graph.add_user(User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN"))
        graph.add_follow(1, 2)
        graph.add_follow(2, 3)
        graph.add_follow(3, 1)
        graph.add_follow(4, 5)
        graph.add_follow(5, 4)
        graph.add_follow(3, 4)
        graph.add_follow(6, 5)
        return graph

    def test_finds_strongly_connected_components(self):
        graph = self.make_graph()
        components = strongly_connected_components(graph)
        self.assertIn([1, 2, 3], components)
        self.assertIn([4, 5], components)
        self.assertIn([6], components)
        self.assertIn([7], components)

    def test_components_are_sorted_by_size(self):
        graph = self.make_graph()
        self.assertEqual(strongly_connected_components(graph)[0], [1, 2, 3])

    def test_largest_communities_limit(self):
        graph = self.make_graph()
        self.assertEqual(largest_communities(graph, 2), [[1, 2, 3], [4, 5]])
        self.assertEqual(largest_communities(graph, 0), [])

    def test_empty_graph(self):
        graph = SocialGraph()
        self.assertEqual(strongly_connected_components(graph), [])


if __name__ == "__main__":
    unittest.main()
