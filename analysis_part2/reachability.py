"""Part 2 Task 2 / 任务2: Reachability / 可达性."""

from __future__ import annotations

from collections import deque


def shortest_path(graph, source_id, target_id):
    """BFS path / BFS路径."""

    graph._require_user(source_id)
    graph._require_user(target_id)
    if source_id == target_id:
        return [source_id]

    queue = deque([source_id])
    parent = {source_id: None}

    while queue:
        current = queue.popleft()
        for nxt in graph.neighbors(current):
            if nxt in parent:
                continue
            parent[nxt] = current
            if nxt == target_id:
                return _build_path(parent, target_id)
            queue.append(nxt)
    return []


def is_reachable(graph, source_id, target_id):
    """Reachable? / 是否可达."""

    return bool(shortest_path(graph, source_id, target_id))


def degrees_of_separation(graph, source_id, target_id):
    """Path length / 路径长度."""

    path = shortest_path(graph, source_id, target_id)
    return None if not path else len(path) - 1


def average_degrees_of_separation(graph):
    """Average degree / 平均分隔."""

    total = 0
    count = 0
    for source_id in graph.user_ids():
        distances = _bfs_distances(graph, source_id)
        for target_id, distance in distances.items():
            if source_id != target_id:
                total += distance
                count += 1
    return total / count if count else 0.0


def _bfs_distances(graph, source_id):
    distances = {source_id: 0}
    queue = deque([source_id])
    while queue:
        current = queue.popleft()
        for nxt in graph.neighbors(current):
            if nxt not in distances:
                distances[nxt] = distances[current] + 1
                queue.append(nxt)
    return distances


def _build_path(parent, target_id):
    path = []
    current = target_id
    while current is not None:
        path.append(current)
        current = parent[current]
    return list(reversed(path))
