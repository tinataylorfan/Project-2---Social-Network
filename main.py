from __future__ import annotations

from datetime import date

from analysis_part2.benchmarking import run_benchmarks
from analysis_part2.centrality import degree_centrality, page_rank
from analysis_part2.community_detection import strongly_connected_components
from analysis_part2.reachability import average_degrees_of_separation, shortest_path
from analysis_part2.recommender import recommendation_details
from data_part1 import generate_dataset, load_dataset
from models_part1 import User
from structures_part1 import SocialGraph


def main() -> None:
    print("Part 1 Demo / 第一部分演示")
    print("=" * 60)

    print("\nTask 1 / 任务1")
    alice = User(1, "Alice", date(2026, 7, 1), "China")
    bob = User(2, "Bob", date(2026, 7, 2), "USA")
    charlie = User(3, "Charlie", date(2026, 7, 3), "UK")
    print(f"  User / 用户: {alice}")
    print("  Count starts at 0 / 粉丝从0开始")

    print("\nTask 2-3 / 任务2-3")
    graph = SocialGraph()
    for user in [alice, bob, charlie]:
        graph.add_user(user)
    graph.add_follow(1, 2)
    graph.add_follow(3, 2)
    print("  Graph main / 图为主")
    print("  BST synced / BST同步")
    print(f"  Bob followers / Bob粉丝: {graph.get_followers(2)}")
    print(f"  Bob count / Bob粉丝数: {bob.follower_count}")
    print(f"  BST top / BST第一: {graph.user_index.find_top_k(1)[0].username}")

    print("\nTask 4 / 任务4")
    users_file, connections_file = generate_dataset()
    loaded_graph, loaded_users = load_dataset(users_file, connections_file)
    print(f"  Users CSV / 用户CSV: {users_file}")
    print(f"  Edges CSV / 关系CSV: {connections_file}")
    print(f"  Users / 用户数: {len(loaded_users)}")
    print(f"  Edges / 关系数: {len(loaded_graph.edges())}")

    print("\nFull Graph / 完整图")
    print_graph(loaded_graph)

    print("\nBST Ranking / BST排名")
    print_bst(loaded_graph)

    print("\nPart 2 Task 1 / 第二部分任务1")
    print_centrality(loaded_graph)

    print("\nPart 2 Task 2 / 第二部分任务2")
    print_reachability(loaded_graph)

    print("\nPart 2 Task 3 / 第二部分任务3")
    print_communities(loaded_graph)

    print("\nPart 2 Task 4 / 第二部分任务4")
    print_benchmark_sample()

    print("\nPart 2 Task 5 / 第二部分任务5")
    print_recommendations(loaded_graph, 3)
    print("  Web / 网页: web_part2/index.html")

    print("\nDone / 完成")


def print_graph(graph: SocialGraph) -> None:
    for user_id in graph.user_ids():
        user = graph.users[user_id]
        print(
            f"  {user.user_id:>2} {user.username:<16} "
            f"count/粉丝={user.follower_count:<2} "
            f"following/关注={graph.get_following(user_id)} "
            f"fans/粉丝表={graph.get_followers(user_id)}"
        )


def print_bst(graph: SocialGraph) -> None:
    for rank, user in enumerate(graph.user_index.to_sorted_list(descending=True), start=1):
        print(f"  #{rank:>2} {user.user_id:>2} {user.username:<16} count/粉丝={user.follower_count}")


def print_centrality(graph: SocialGraph) -> None:
    degrees = degree_centrality(graph)
    scores = page_rank(graph)
    print("  Degree / 度数")
    for user_id in graph.user_ids()[:5]:
        item = degrees[user_id]
        print(f"    {user_id}: in={item['in_degree']} out={item['out_degree']}")
    print("  PageRank / 影响力")
    for user_id, score in list(scores.items())[:3]:
        print(f"    {user_id} {graph.users[user_id].username}: {score:.4f}")


def print_reachability(graph: SocialGraph) -> None:
    path = shortest_path(graph, 3, 1)
    print(f"  Path / 路径 3->1: {path}")
    print(f"  Degrees / 间隔: {len(path) - 1 if path else 'N/A'}")
    print(f"  Average / 平均: {average_degrees_of_separation(graph):.2f}")


def print_communities(graph: SocialGraph) -> None:
    for index, component in enumerate(strongly_connected_components(graph)[:5], start=1):
        print(f"  SCC {index}: {component}")


def print_benchmark_sample() -> None:
    for row in run_benchmarks(sizes=(20, 100, 500), average_degree=5):
        print(
            f"  N={row['users']} E={row['edges']} "
            f"build={row['construction_seconds']:.5f}s "
            f"scc={row['scc_seconds']:.5f}s"
        )


def print_recommendations(graph: SocialGraph, user_id: int) -> None:
    details = recommendation_details(graph, user_id)
    if not details:
        print("  None / 暂无")
        return
    for item in details:
        print(
            f"  {item['user_id']} {item['username']} "
            f"mutual/共同={item['mutual_followees']} "
            f"count/粉丝={item['follower_count']}"
        )


if __name__ == "__main__":
    main()
