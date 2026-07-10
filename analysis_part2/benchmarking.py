"""Part 2 Task 4 / 任务4: Benchmark / 性能."""

from __future__ import annotations

import csv
import random
import sys
import time
from datetime import date
from pathlib import Path
from typing import Iterable

from analysis_part2.centrality import degree_centrality
from analysis_part2.community_detection import strongly_connected_components
from analysis_part2.reachability import shortest_path
from models_part1 import User
from structures_part1 import SocialGraph


DEFAULT_BENCHMARK_CSV = Path(__file__).resolve().parent.parent / "dataset" / "benchmark" / "part2_benchmark_results.csv"


def build_synthetic_graph(user_count: int, average_degree: int = 5, seed: int = 7) -> SocialGraph:
    """Synthetic graph / 合成图."""

    if user_count <= 1:
        raise ValueError("user_count must be greater than 1")
    if average_degree < 0:
        raise ValueError("average_degree must be non-negative")

    sys.setrecursionlimit(max(sys.getrecursionlimit(), user_count * 3 + 100))

    rng = random.Random(seed + user_count)
    graph = SocialGraph()
    for user_id in range(1, user_count + 1):
        graph.add_user(User(user_id, f"synthetic_{user_id}", date(2026, 7, 1), "Synthetic"))

    max_edges = user_count * (user_count - 1)
    target_edges = min(user_count * average_degree, max_edges)
    edges: set[tuple[int, int]] = set()
    while len(edges) < target_edges:
        follower_id = rng.randint(1, user_count)
        followee_id = rng.randint(1, user_count)
        if follower_id != followee_id:
            edges.add((follower_id, followee_id))

    for follower_id, followee_id in edges:
        graph.add_follow(follower_id, followee_id)
    return graph


def benchmark_node_insertions(user_count: int) -> float:
    """Insert nodes / 插入节点."""

    sys.setrecursionlimit(max(sys.getrecursionlimit(), user_count * 3 + 100))
    graph = SocialGraph()
    start = time.perf_counter()
    for user_id in range(1, user_count + 1):
        graph.add_user(User(user_id, f"synthetic_{user_id}", date(2026, 7, 1), "Synthetic"))
    return time.perf_counter() - start


def benchmark_size(user_count: int, average_degree: int = 5, seed: int = 7) -> dict[str, float | int]:
    """One size / 单个规模."""

    rng = random.Random(seed * 1000 + user_count)

    insert_seconds = benchmark_node_insertions(user_count)

    start = time.perf_counter()
    graph = build_synthetic_graph(user_count, average_degree, seed)
    construction_seconds = time.perf_counter() - start

    start = time.perf_counter()
    degrees = degree_centrality(graph)
    degree_seconds = time.perf_counter() - start

    start = time.perf_counter()
    components = strongly_connected_components(graph)
    scc_seconds = time.perf_counter() - start

    source_id, target_id = rng.sample(graph.user_ids(), 2)
    start = time.perf_counter()
    path = shortest_path(graph, source_id, target_id)
    path_seconds = time.perf_counter() - start

    return {
        "users": user_count,
        "edges": len(graph.edges()),
        "source_id": source_id,
        "target_id": target_id,
        "degree_items": len(degrees),
        "component_count": len(components),
        "path_length": len(path) - 1 if path else -1,
        "insert_seconds": insert_seconds,
        "construction_seconds": construction_seconds,
        "degree_seconds": degree_seconds,
        "scc_seconds": scc_seconds,
        "path_seconds": path_seconds,
    }


def run_benchmarks(
    sizes: Iterable[int] = (20, 100, 500),
    average_degree: int = 5,
    seed: int = 7,
    output_csv: str | Path | None = None,
) -> list[dict[str, float | int]]:
    """Run timings / 运行计时."""

    results = [benchmark_size(size, average_degree, seed) for size in sizes]
    if output_csv is not None:
        write_benchmark_csv(results, output_csv)
    return results


def write_benchmark_csv(rows: list[dict[str, float | int]], output_csv: str | Path) -> Path:
    """Save CSV / 保存结果."""

    path = Path(output_csv)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return path
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


if __name__ == "__main__":
    # Full run / 完整运行
    output_path = write_benchmark_csv(run_benchmarks(), DEFAULT_BENCHMARK_CSV)
    print(f"Benchmark saved / 结果已保存: {output_path}")
