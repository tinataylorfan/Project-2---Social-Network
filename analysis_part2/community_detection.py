"""Part 2 Task 3 / 任务3: Communities / 社群."""

from __future__ import annotations

import sys


def strongly_connected_components(graph) -> list[list[int]]:
    """Tarjan SCC / 强连通."""

    user_ids = graph.user_ids()
    sys.setrecursionlimit(max(sys.getrecursionlimit(), len(user_ids) * 2 + 100))

    index = 0
    stack: list[int] = []
    on_stack: set[int] = set()
    indices: dict[int, int] = {}
    lowlinks: dict[int, int] = {}
    components: list[list[int]] = []

    def visit(user_id: int) -> None:
        nonlocal index
        indices[user_id] = index
        lowlinks[user_id] = index
        index += 1
        stack.append(user_id)
        on_stack.add(user_id)

        for next_id in graph.neighbors(user_id):
            if next_id not in indices:
                visit(next_id)
                lowlinks[user_id] = min(lowlinks[user_id], lowlinks[next_id])
            elif next_id in on_stack:
                lowlinks[user_id] = min(lowlinks[user_id], indices[next_id])

        if lowlinks[user_id] == indices[user_id]:
            component: list[int] = []
            while True:
                member_id = stack.pop()
                on_stack.remove(member_id)
                component.append(member_id)
                if member_id == user_id:
                    break
            components.append(sorted(component))

    for user_id in user_ids:
        if user_id not in indices:
            visit(user_id)

    return sorted(components, key=lambda group: (-len(group), group[0]))


def largest_communities(graph, limit: int = 3) -> list[list[int]]:
    """Top SCCs / 最大社群."""

    if limit <= 0:
        return []
    return strongly_connected_components(graph)[:limit]
