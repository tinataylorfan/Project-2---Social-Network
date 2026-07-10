import unittest
from datetime import date

from analysis_part2.recommender import recommendation_details, recommend_followees
from models_part1 import User
from structures_part1 import SocialGraph


class TestAnalysisPart2Recommender(unittest.TestCase):
    def make_graph(self):
        graph = SocialGraph()
        for user_id in range(1, 7):
            graph.add_user(User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN"))
        graph.add_follow(1, 2)
        graph.add_follow(1, 3)
        graph.add_follow(2, 4)
        graph.add_follow(3, 4)
        graph.add_follow(2, 5)
        graph.add_follow(3, 6)
        graph.add_follow(2, 1)
        return graph

    def test_friend_of_friend_recommendations(self):
        graph = self.make_graph()
        self.assertEqual(recommend_followees(graph, 1), [4, 5, 6])

    def test_recommendations_exclude_self_and_existing_followees(self):
        graph = self.make_graph()
        recommendations = recommend_followees(graph, 1)
        self.assertNotIn(1, recommendations)
        self.assertNotIn(2, recommendations)
        self.assertNotIn(3, recommendations)

    def test_top_n_and_non_positive_limit(self):
        graph = self.make_graph()
        self.assertEqual(recommend_followees(graph, 1, top_n=1), [4])
        self.assertEqual(recommend_followees(graph, 1, top_n=0), [])

    def test_recommendation_details(self):
        graph = self.make_graph()
        details = recommendation_details(graph, 1, top_n=1)
        self.assertEqual(details[0]["user_id"], 4)
        self.assertEqual(details[0]["mutual_followees"], 2)
        self.assertEqual(details[0]["follower_count"], 2)


if __name__ == "__main__":
    unittest.main()
