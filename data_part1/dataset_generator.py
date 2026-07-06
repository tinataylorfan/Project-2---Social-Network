from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable


DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "dataset" / "data"


def generate_dataset(
    data_dir: str | Path = DEFAULT_DATA_DIR,
    user_count: int = 18,
    edge_count: int = 30,
    seed: int = 7,
) -> tuple[Path, Path]:
    """Part 1 Task 4: generate CSV files.

    follower_count is written as 0 initially. Real counts are computed while
    loading follow relationships into the graph.
    """

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
                "follower_count": 0,
            }
        )

    users[0]["username"] = "news_hub"
    users[1]["username"] = "tech_star"
    users[-1]["username"] = "isolated_reader"

    edges: set[tuple[int, int]] = set()
    cluster = [3, 4, 5, 6, 7]
    for a, b in zip(cluster, cluster[1:] + cluster[:1]):
        edges.add((a, b))
        edges.add((b, a))

    for uid in range(3, user_count):
        for hub_id in [1, 2]:
            if rng.random() < 0.75:
                edges.add((uid, hub_id))

    edges.update({(8, 9), (8, 10), (9, 1), (9, 11), (10, 11), (10, 12)})

    selectable_ids = list(range(1, user_count))
    while len(edges) < edge_count:
        follower_id = rng.choice(selectable_ids)
        followee_id = rng.choice(selectable_ids)
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


def _write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
