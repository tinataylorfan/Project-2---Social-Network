from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from data_part1.dataset_generator import DEFAULT_DATA_DIR
from models_part1 import User
from structures_part1 import SocialGraph


def load_dataset(
    users_file: str | Path = DEFAULT_DATA_DIR / "social_users.csv",
    connections_file: str | Path = DEFAULT_DATA_DIR / "social_connections.csv",
) -> tuple[SocialGraph, list[User]]:
    """Task 4 / 任务4: Load / 加载."""

    graph = SocialGraph()
    users: list[User] = []

    with Path(users_file).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            user = User(
                user_id=int(row["user_id"]),
                username=row["username"],
                join_date=date.fromisoformat(row["join_date"]),
                country=row["country"],
            )
            graph.add_user(user)
            users.append(user)

    with Path(connections_file).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            # Sync count / 同步计数
            graph.add_follow(int(row["follower_id"]), int(row["followee_id"]))

    return graph, users
