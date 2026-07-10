"""Part 2 Task 5 / 任务5: Recommend / 推荐."""

from __future__ import annotations

from collections import Counter


def recommend_followees(graph, user_id: int, top_n: int = 3) -> list[int]:
    """Friend-of-friend / 朋友的朋友."""

    graph._require_user(user_id)
    if top_n <= 0:
        return []

    followed = set(graph.get_following(user_id))
    candidates: Counter[int] = Counter()

    for followee_id in followed:
        for candidate_id in graph.get_following(followee_id):
            if candidate_id != user_id and candidate_id not in followed:
                candidates[candidate_id] += 1

    bst_rank = {
        user.user_id: rank
        for rank, user in enumerate(graph.user_index.to_sorted_list(descending=True), start=1)
    }
    ranked = sorted(
        candidates,
        key=lambda candidate_id: (
            -candidates[candidate_id],
            bst_rank.get(candidate_id, len(bst_rank) + 1),
            candidate_id,
        ),
    )
    return ranked[:top_n]


def recommendation_details(graph, user_id: int, top_n: int = 3) -> list[dict[str, int | str]]:
    """Explain recs / 推荐解释."""

    details = []
    for candidate_id in recommend_followees(graph, user_id, top_n):
        mutual_count = sum(
            1 for followee_id in graph.get_following(user_id) if graph.is_following(followee_id, candidate_id)
        )
        user = graph.users[candidate_id]
        details.append(
            {
                "user_id": candidate_id,
                "username": user.username,
                "mutual_followees": mutual_count,
                "follower_count": user.follower_count,
            }
        )
    return details
