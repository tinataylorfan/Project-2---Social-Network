from __future__ import annotations

from datetime import date

from data_part1 import generate_dataset, load_dataset
from models_part1 import User
from structures_part1 import SocialGraph


def main() -> None:
    print("Part 1 Demo - Social Network Software Toolbox")
    print("=" * 60)

    print("\nTask 1 - Data Modelling")
    alice = User(1, "Alice", date(2026, 7, 1), "China")
    bob = User(2, "Bob", date(2026, 7, 2), "USA")
    charlie = User(3, "Charlie", date(2026, 7, 3), "UK")
    print(f"  Created user: {alice}")
    print("  New users start with follower_count = 0.")

    print("\nTask 2 and Task 3 - Graph with Synchronized BST")
    graph = SocialGraph()
    for user in [alice, bob, charlie]:
        graph.add_user(user)
    graph.add_follow(1, 2)
    graph.add_follow(3, 2)
    print("  The graph is the main structure.")
    print("  When a follow is added, follower_count changes and the BST is updated.")
    print(f"  Bob's followers: {graph.get_followers(2)}")
    print(f"  Bob's real follower_count: {bob.follower_count}")
    print(f"  BST top user: {graph.user_index.find_top_k(1)[0].username}")

    print("\nTask 4 - Dataset Generation and Loading")
    users_file, connections_file = generate_dataset()
    loaded_graph, loaded_users = load_dataset(users_file, connections_file)
    print(f"  users CSV: {users_file}")
    print(f"  connections CSV: {connections_file}")
    print(f"  Loaded users: {len(loaded_users)}")
    print(f"  Loaded directed follow relationships: {len(loaded_graph.edges())}")

    print("\nFull graph after loading dataset:")
    print_graph(loaded_graph)

    print("\nBST ranking after loading dataset:")
    print_bst(loaded_graph)

    print("\nPart 1 demo completed successfully.")


def print_graph(graph: SocialGraph) -> None:
    for user_id in graph.user_ids():
        user = graph.users[user_id]
        print(
            f"  {user.user_id:>2} {user.username:<16} "
            f"followers={user.follower_count:<2} "
            f"following={graph.get_following(user_id)} "
            f"followers_list={graph.get_followers(user_id)}"
        )


def print_bst(graph: SocialGraph) -> None:
    for rank, user in enumerate(graph.user_index.to_sorted_list(descending=True), start=1):
        print(f"  #{rank:>2} {user.user_id:>2} {user.username:<16} followers={user.follower_count}")


if __name__ == "__main__":
    main()
