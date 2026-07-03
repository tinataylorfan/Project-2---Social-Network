from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

from part1_toolbox.part1_task1_data_modeling import User
from part1_toolbox.part1_task2_graph_representation import SocialGraph
from part1_toolbox.part1_task3_bst_user_index import UserIndexBST


DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "dataset" / "data"


def generate_dataset(
    data_dir: str | Path = DEFAULT_DATA_DIR,
    user_count: int = 18,
    edge_count: int = 30,
    seed: int = 7,
) -> tuple[Path, Path]:
    """Task 4: generate CSV files for users and directed follow relationships."""

    if user_count < 15:
        raise ValueError("user_count must be at least 15")
    if edge_count < 25:
        raise ValueError("edge_count must be at least 25")

    rng = random.Random(seed)
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)
    countries = ["China", "USA", "UK", "Canada", "Japan", "Germany", "Brazil"]
    base_day = date(2026, 7, 1)

    users: list[dict[str, object]] = []
    for uid in range(1, user_count + 1):
        users.append(
            {
                "user_id": uid,
                "username": f"user_{uid}",
                "join_date": (base_day - timedelta(days=rng.randint(10, 1200))).isoformat(),
                "country": rng.choice(countries),
                "follower_count": rng.randint(5, 450),
            }
        )

    hub_ids = [1, 2]
    users[0]["username"] = "news_hub"
    users[0]["follower_count"] = 5000
    users[1]["username"] = "tech_star"
    users[1]["follower_count"] = 3200
    users[-1]["username"] = "isolated_reader"
    users[-1]["follower_count"] = 0

    edges: set[tuple[int, int]] = set()

    # Strongly connected cluster among users 3-7.
    cluster = [3, 4, 5, 6, 7]
    for a, b in zip(cluster, cluster[1:] + cluster[:1]):
        edges.add((a, b))
        edges.add((b, a))

    # Hub users receive many follows.
    for uid in range(3, user_count):
        for hub_id in hub_ids:
            if rng.random() < 0.75:
                edges.add((uid, hub_id))

    # Extra ordinary directed edges make the network less trivial.
    edges.update({(8, 9), (8, 10), (9, 1), (9, 11), (10, 11), (10, 12)})

    all_ids = [int(row["user_id"]) for row in users]
    while len(edges) < edge_count:
        follower_id = rng.choice(all_ids[:-1])
        followee_id = rng.choice(all_ids[:-1])
        if follower_id != followee_id:
            edges.add((follower_id, followee_id))

    users_file = data_path / "social_users.csv"
    connections_file = data_path / "social_connections.csv"
    _write_csv(users_file, users, ["user_id", "username", "join_date", "country", "follower_count"])
    _write_csv(
        connections_file,
        [{"follower_id": a, "followee_id": b} for a, b in sorted(edges)],
        ["follower_id", "followee_id"],
    )
    return users_file, connections_file


def load_dataset(
    users_file: str | Path = DEFAULT_DATA_DIR / "social_users.csv",
    connections_file: str | Path = DEFAULT_DATA_DIR / "social_connections.csv",
) -> tuple[SocialGraph, UserIndexBST, list[User]]:
    """Task 4: load CSVs and initialize graph + BST."""

    graph = SocialGraph()
    bst = UserIndexBST()
    users: list[User] = []

    with Path(users_file).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            user = User(
                user_id=int(row["user_id"]),
                username=row["username"],
                join_date=date.fromisoformat(row["join_date"]),
                country=row["country"],
                follower_count=int(row["follower_count"]),
            )
            graph.add_user(user)
            bst.insert(user)
            users.append(user)

    with Path(connections_file).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                graph.add_follow(int(row["follower_id"]), int(row["followee_id"]))
            except ValueError:
                continue
    return graph, bst, users


def _write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


__all__ = ["DEFAULT_DATA_DIR", "generate_dataset", "load_dataset"]
