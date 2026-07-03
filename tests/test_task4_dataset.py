import csv
import tempfile
import unittest
from pathlib import Path

from part1_toolbox.part1_task4_dataset import generate_dataset, load_dataset


class TestTask4Dataset(unittest.TestCase):
    def test_generator_rejects_too_small_dataset(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                generate_dataset(tmp, user_count=14, edge_count=25)
            with self.assertRaises(ValueError):
                generate_dataset(tmp, user_count=15, edge_count=24)

    def test_generated_csv_headers_and_sizes(self):
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

    def test_generated_dataset_contains_required_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            users_file, connections_file = generate_dataset(tmp, user_count=18, edge_count=30, seed=7)
            graph, bst, users = load_dataset(users_file, connections_file)

            usernames = {user.username for user in users}
            self.assertIn("news_hub", usernames)
            self.assertIn("tech_star", usernames)
            self.assertIn("isolated_reader", usernames)

            # Users 3-7 form a strongly connected cluster through mutual cycle edges.
            for edge in [(3, 4), (4, 5), (5, 6), (6, 7), (7, 3)]:
                self.assertTrue(graph.is_following(*edge))

            isolated_id = next(user.user_id for user in users if user.username == "isolated_reader")
            self.assertEqual(graph.get_following(isolated_id), [])
            self.assertEqual(graph.get_followers(isolated_id), [])
            self.assertEqual(bst.find_top_k(1)[0].username, "news_hub")


if __name__ == "__main__":
    unittest.main()
