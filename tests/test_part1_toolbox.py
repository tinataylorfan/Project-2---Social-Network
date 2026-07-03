import tempfile
import unittest
from datetime import date
from pathlib import Path

from part1_toolbox.part1_task1_data_modeling import User
from part1_toolbox.part1_task2_graph_representation import SocialGraph
from part1_toolbox.part1_task3_bst_user_index import UserIndexBST
from part1_toolbox.part1_task4_dataset import generate_dataset, load_dataset


class TestPart1Toolbox(unittest.TestCase):
    def make_user(self, user_id, followers=0):
        return User(user_id, f"user_{user_id}", date(2026, 7, 1), "CN", followers)

    def test_task1_user_validation(self):
        with self.assertRaises(ValueError):
            User(0, "bad", date.today(), "CN", 0)
        with self.assertRaises(ValueError):
            User(1, " ", date.today(), "CN", 0)
        with self.assertRaises(ValueError):
            User(1, "ok", date.today(), "CN", -1)

    def test_task2_graph_crud_and_edge_cases(self):
        graph = SocialGraph()
        for user_id in [1, 2, 3]:
            graph.add_user(self.make_user(user_id))
        self.assertTrue(graph.add_follow(1, 2))
        self.assertFalse(graph.add_follow(1, 2))
        self.assertEqual(graph.get_following(1), [2])
        self.assertEqual(graph.get_followers(2), [1])
        with self.assertRaises(ValueError):
            graph.add_follow(1, 1)
        graph.add_follow(3, 2)
        graph.remove_user(2)
        self.assertFalse(graph.is_following(1, 2))
        self.assertFalse(graph.is_following(3, 2))

    def test_task3_bst_queries_and_dynamic_update(self):
        users = [self.make_user(1, 100), self.make_user(2, 500), self.make_user(3, 100)]
        bst = UserIndexBST()
        for user in users:
            bst.insert(user)
        self.assertEqual([u.user_id for u in bst.search(100)], [1, 3])
        self.assertEqual([u.user_id for u in bst.find_top_k(2)], [2, 1])
        self.assertEqual({u.user_id for u in bst.find_range(90, 550)}, {1, 2, 3})
        bst.update_user_count(users[0], 700)
        self.assertEqual([u.user_id for u in bst.find_top_k(1)], [1])

    def test_task4_dataset_generation_and_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            users_file, connections_file = generate_dataset(tmp, user_count=18, edge_count=30, seed=11)
            self.assertTrue(Path(users_file).exists())
            self.assertTrue(Path(connections_file).exists())
            graph, bst, users = load_dataset(users_file, connections_file)
            self.assertGreaterEqual(len(users), 18)
            self.assertGreaterEqual(len(graph.edges()), 30)
            self.assertEqual(len(bst.find_top_k(3)), 3)


if __name__ == "__main__":
    unittest.main()
