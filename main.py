from __future__ import annotations

from datetime import date

from part1_toolbox.part1_task1_data_modeling import User
from part1_toolbox.part1_task2_graph_representation import SocialGraph
from part1_toolbox.part1_task3_bst_user_index import UserIndexBST
from part1_toolbox.part1_task4_dataset import generate_dataset, load_dataset


def main() -> None:
    print("Part 1 Demo - Social Network Software Toolbox")
    print("=" * 60)

    print("\nTask 1 - Data Modelling")
    alice = User(1, "Alice", date(2026, 7, 1), "China", 120)
    bob = User(2, "Bob", date(2026, 7, 2), "USA", 350)
    charlie = User(3, "Charlie", date(2026, 7, 3), "UK", 120)
    print(f"  Created user: {alice}")
    print(
        "  Fields: "
        f"id={alice.user_id}, username={alice.username}, "
        f"country={alice.country}, followers={alice.follower_count}"
    )

    print("\nTask 2 - Directed Graph Representation")
    graph = SocialGraph()
    for user in [alice, bob, charlie]:
        graph.add_user(user)
    graph.add_follow(1, 2)
    graph.add_follow(3, 2)
    print("  Graph uses two adjacency maps:")
    print("    following[user_id] -> users this person follows")
    print("    followers[user_id] -> users following this person")
    print(f"  Alice follows: {graph.get_following(1)}")
    print(f"  Bob's followers: {graph.get_followers(2)}")
    print(f"  Does Alice follow Bob? {graph.is_following(1, 2)}")

    print("\nTask 3 - BST User Index by Follower Count")
    bst = UserIndexBST()
    for user in [alice, bob, charlie]:
        bst.insert(user)
    print("  Top users by followers:")
    for user in bst.find_top_k(3):
        print(f"    {user.user_id}: {user.username}, followers={user.follower_count}")
    print(f"  Search follower_count=120: {[user.username for user in bst.search(120)]}")
    print(f"  Range 100-400: {[user.username for user in bst.find_range(100, 400)]}")

    print("\nTask 4 - Dataset Generation and Loading")
    users_file, connections_file = generate_dataset()
    loaded_graph, loaded_bst, loaded_users = load_dataset(users_file, connections_file)
    print(f"  users CSV: {users_file}")
    print(f"  connections CSV: {connections_file}")
    print(f"  Loaded users: {len(loaded_users)}")
    print(f"  Loaded directed follow relationships: {len(loaded_graph.edges())}")
    print(f"  Dataset top user by BST: {loaded_bst.find_top_k(1)[0].username}")

    print("\nPart 1 demo completed successfully.")


if __name__ == "__main__":
    main()
