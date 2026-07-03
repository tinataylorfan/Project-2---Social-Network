import unittest
from datetime import date

from part1_toolbox.part1_task1_data_modeling import User


class TestTask1UserModel(unittest.TestCase):
    def test_user_strips_text_fields(self):
        user = User(1, "  Alice  ", date(2026, 7, 1), "  China  ", 10)
        self.assertEqual(user.username, "Alice")
        self.assertEqual(user.country, "China")

    def test_user_equality_uses_user_id(self):
        user_a = User(1, "Alice", date(2026, 7, 1), "China", 10)
        user_b = User(1, "Alice_New_Name", date(2026, 7, 2), "USA", 99)
        self.assertEqual(user_a, user_b)
        self.assertEqual(hash(user_a), hash(user_b))

    def test_join_date_must_be_date_object(self):
        with self.assertRaises(TypeError):
            User(2, "Bob", "2026-07-01", "USA", 20)

    def test_country_must_not_be_blank(self):
        with self.assertRaises(ValueError):
            User(3, "Charlie", date(2026, 7, 1), "   ", 30)

    def test_update_follower_count(self):
        user = User(4, "Dora", date(2026, 7, 1), "UK", 0)
        user.update_follower_count(88)
        self.assertEqual(user.follower_count, 88)
        with self.assertRaises(ValueError):
            user.update_follower_count(-1)


if __name__ == "__main__":
    unittest.main()
