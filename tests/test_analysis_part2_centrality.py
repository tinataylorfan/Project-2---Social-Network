import unittest
from datetime import date

from analysis_part2.centrality import (
    compute_degree_summary,
    compute_influence_scores,
    degree_centrality,
    page_rank,
)
from models_part1 import User
from structures_part1 import SocialGraph


class TestAnalysisPart2Centrality(unittest.TestCase):
    def make_graph(self):
        graph = SocialGraph()
        for user_id in range(1, 5):
            graph.add_user(User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN"))
        graph.add_follow(1, 2)
        graph.add_follow(3, 2)
        graph.add_follow(2, 4)
        return graph

    def test_degree_centrality(self):
        graph = self.make_graph()
        degrees = degree_centrality(graph)
        self.assertEqual(degrees[2]["in_degree"], 2)
        self.assertEqual(degrees[2]["out_degree"], 1)
        self.assertEqual(degrees[4]["in_degree"], 1)
        self.assertEqual(degrees[4]["out_degree"], 0)

    def test_page_rank_returns_all_users(self):
        graph = self.make_graph()
        scores = page_rank(graph)
        self.assertEqual(set(scores.keys()), {1, 2, 3, 4})
        self.assertAlmostEqual(sum(scores.values()), 1.0, places=6)

    def test_page_rank_reflects_influence(self):
        graph = self.make_graph()
        scores = page_rank(graph)
        self.assertGreater(scores[2], scores[1])
        self.assertGreater(scores[4], scores[1])

    def test_compatibility_function_names(self):
        graph = self.make_graph()
        self.assertEqual(compute_degree_summary(graph), degree_centrality(graph))
        self.assertEqual(compute_influence_scores(graph), page_rank(graph))


if __name__ == "__main__":
    unittest.main()
