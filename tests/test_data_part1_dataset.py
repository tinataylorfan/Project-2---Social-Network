import csv
import tempfile
import unittest
from pathlib import Path

from data_part1 import generate_dataset, load_dataset


class TestDataPart1Dataset(unittest.TestCase):
    def test_generator_rejects_too_small_dataset(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                generate_dataset(tmp, user_count=14, edge_count=25)
            with self.assertRaises(ValueError):
                generate_dataset(tmp, user_count=15, edge_count=24)

    def test_generated_csv_headers_and_zero_initial_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            users_file, connections_file = generate_dataset(tmp, user_count=18, edge_count=30, seed=21)
            with Path(users_file).open(newline="", encoding="utf-8") as handle:
                users = list(csv.DictReader(handle))
            with Path(connections_file).open(newline="", encoding="utf-8") as handle:
                connections = list(csv.DictReader(handle))
            self.assertEqual(
                set(users[0].keys()),
                {"user_id", "username", "join_date", "country", "follower_count"},
            )
            self.assertEqual(set(connections[0].keys()), {"follower_id", "followee_id"})
            self.assertGreaterEqual(len(users), 18)
            self.assertGreaterEqual(len(connections), 30)
            self.assertTrue(all(int(row["follower_count"]) == 0 for row in users))

    def test_loader_computes_real_follower_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            users_file, connections_file = generate_dataset(tmp, user_count=18, edge_count=30, seed=7)
            graph, users = load_dataset(users_file, connections_file)
            for user in users:
                self.assertEqual(user.follower_count, len(graph.get_followers(user.user_id)))
                self.assertTrue(graph.follower_count_is_consistent(user.user_id))

    def test_generated_dataset_contains_required_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            users_file, connections_file = generate_dataset(tmp, user_count=18, edge_count=30, seed=7)
            graph, users = load_dataset(users_file, connections_file)
            usernames = {user.username for user in users}
            self.assertIn("news_hub", usernames)
            self.assertIn("tech_star", usernames)
            self.assertIn("isolated_reader", usernames)
            for edge in [(3, 4), (4, 5), (5, 6), (6, 7), (7, 3)]:
                self.assertTrue(graph.is_following(*edge))
            isolated_id = next(user.user_id for user in users if user.username == "isolated_reader")
            self.assertEqual(graph.get_following(isolated_id), [])
            self.assertEqual(graph.get_followers(isolated_id), [])

    def test_bst_ranking_matches_loaded_graph_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            users_file, connections_file = generate_dataset(tmp, user_count=18, edge_count=30, seed=7)
            graph, users = load_dataset(users_file, connections_file)
            ranked_by_graph = sorted(users, key=lambda user: (-len(graph.get_followers(user.user_id)), user.user_id))
            ranked_by_bst = graph.user_index.find_top_k(len(users))
            self.assertEqual([user.user_id for user in ranked_by_bst], [user.user_id for user in ranked_by_graph])


if __name__ == "__main__":
    unittest.main()
