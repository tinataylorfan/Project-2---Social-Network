"""Part 2 Task 1 / 任务1: Centrality / 中心性."""

from __future__ import annotations


def degree_centrality(graph):
    """In/out degree / 入出度."""

    return {
        user_id: {
            "in_degree": graph.in_degree(user_id),
            "out_degree": graph.out_degree(user_id),
        }
        for user_id in graph.user_ids()
    }


def page_rank(graph, damping=0.85, iterations=50, tolerance=1e-8):
    """PageRank / 影响力."""

    user_ids = graph.user_ids()
    if not user_ids:
        return {}

    n = len(user_ids)
    ranks = {user_id: 1.0 / n for user_id in user_ids}

    for _ in range(iterations):
        new_ranks = {user_id: (1.0 - damping) / n for user_id in user_ids}
        dangling_sum = sum(ranks[user_id] for user_id in user_ids if graph.out_degree(user_id) == 0)

        for user_id in user_ids:
            new_ranks[user_id] += damping * dangling_sum / n

        for source_id in user_ids:
            out_degree = graph.out_degree(source_id)
            if out_degree == 0:
                continue
            share = damping * ranks[source_id] / out_degree
            for target_id in graph.neighbors(source_id):
                new_ranks[target_id] += share

        delta = sum(abs(new_ranks[user_id] - ranks[user_id]) for user_id in user_ids)
        ranks = new_ranks
        if delta < tolerance:
            break

    return dict(sorted(ranks.items(), key=lambda item: item[1], reverse=True))


def compute_degree_summary(graph):
    """Old name / 旧接口."""

    return degree_centrality(graph)


def compute_influence_scores(graph):
    """Old name / 旧接口."""

    return page_rank(graph)
