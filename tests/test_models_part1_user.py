import unittest
from datetime import date

from models_part1 import User


class TestModelsPart1User(unittest.TestCase):
    def test_user_defaults_to_zero_followers(self):
        user = User(1, "Alice", date(2026, 7, 1), "China")
        self.assertEqual(user.follower_count, 0)

    def test_user_strips_text_fields(self):
        user = User(2, "  Bob  ", date(2026, 7, 1), "  USA  ")
        self.assertEqual(user.username, "Bob")
        self.assertEqual(user.country, "USA")

    def test_invalid_user_id_is_rejected(self):
        with self.assertRaises(ValueError):
            User(0, "bad", date(2026, 7, 1), "China")

    def test_blank_username_and_country_are_rejected(self):
        with self.assertRaises(ValueError):
            User(3, " ", date(2026, 7, 1), "China")
        with self.assertRaises(ValueError):
            User(4, "Dora", date(2026, 7, 1), " ")

    def test_join_date_must_be_date_object(self):
        with self.assertRaises(TypeError):
            User(5, "Eve", "2026-07-01", "UK")

    def test_update_follower_count_validates_value(self):
        user = User(6, "Frank", date(2026, 7, 1), "Canada")
        user.update_follower_count(4)
        self.assertEqual(user.follower_count, 4)
        with self.assertRaises(ValueError):
            user.update_follower_count(-1)

    def test_user_equality_and_hash_use_user_id(self):
        user_a = User(7, "Grace", date(2026, 7, 1), "China")
        user_b = User(7, "Grace_New", date(2026, 7, 2), "USA")
        self.assertEqual(user_a, user_b)
        self.assertEqual(hash(user_a), hash(user_b))


if __name__ == "__main__":
    unittest.main()
