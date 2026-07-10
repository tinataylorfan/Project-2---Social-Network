# Group2 Social Network Project

This project implements a directed social network analysis toolbox. Users can
follow each other, and the system can analyse influence, reachability,
communities, benchmark performance, recommend new followees, and visualise the
network in a Web interface.

## Structure

- `models_part1/`: user data model.
- `structures_part1/`: directed graph and BST user index.
- `data_part1/`: CSV dataset generation and loading.
- `analysis_part2/`: centrality, reachability, community detection, benchmarking, and recommendation.
- `web_part2/`: Web graph visualisation and benchmark plot.
- `tests/`: unit tests.
- `dataset/data/`: generated social network CSV files.
- `dataset/benchmark/`: benchmark CSV output.
- `docs/`: design notes and work split.

## Part 1 Task 1 - Data Modelling

`models_part1/user.py` defines the `User` class with:

- `user_id`
- `username`
- `join_date`
- `country`
- `follower_count`

New users start with `follower_count = 0`. The value is not fabricated; it is
updated from real follow relationships in the graph.

## Part 1 Task 2 - Graph Representation

The project uses a directed graph with adjacency sets.

The most frequent operations are:

- check whether A follows B,
- get all users followed by A,
- get all followers of A,
- add or remove users,
- add or remove follow relationships.

The graph stores:

- `following[user_id]`: outgoing edges, users this user follows.
- `followers[user_id]`: incoming edges, users who follow this user.

This representation fits the problem because follow relationships are directed:
if A follows B, B does not automatically follow A. Keeping both incoming and
outgoing sets makes the main queries direct and efficient.

For N users and E follow relationships, the space complexity is O(N + E).

## Part 1 Task 3 - BST User Index

`structures_part1/user_index_bst.py` implements a BST sorted by real
`follower_count`.

The graph is the main structure and owns the BST. When users or follow
relationships change in the graph, the BST is updated. The BST never changes
the graph, so there are no circular calls.

The BST supports:

- insert user,
- search by follower count,
- find top-K most followed users,
- find users in a follower-count range.

The BST is useful because the graph alone would need a full scan for ranked
queries.

## Part 1 Task 4 - Dataset

`data_part1/dataset_generator.py` creates:

- `dataset/data/social_users.csv`
- `dataset/data/social_connections.csv`

The generated dataset includes at least 15 users, at least 25 directed
connections, hub users, an isolated user, and one strongly connected cluster.

`data_part1/dataset_loader.py` loads both CSV files, builds the graph, and
updates follower counts and the BST while reading follow relationships.

## Part 2 Task 1 - Influence and Centrality

`analysis_part2/centrality.py` computes:

- in-degree: number of followers,
- out-degree: number of followed users,
- PageRank: a deeper influence score.

PageRank was chosen because it considers not only how many followers a user has,
but also how influential those followers are.

The result matches intuition because hub users usually rank highly. A user with
fewer direct followers can still rank well if those followers are themselves
important.

## Part 2 Task 2 - Reachability

`analysis_part2/reachability.py` uses BFS to find:

- whether B is reachable from A,
- the shortest follow path,
- degrees of separation,
- average degrees of separation across reachable pairs.

BFS was chosen because follow relationships are unweighted, so BFS finds the
shortest path first. The worst-case complexity is O(N + E).

The average degrees of separation can be compared with the "six degrees of
separation" idea.

## Part 2 Task 3 - Community Detection

`analysis_part2/community_detection.py` uses Tarjan's algorithm to find strongly
connected components.

Tarjan's algorithm was chosen because it finds all SCCs in one DFS pass. The
SCCs reveal groups where users can reach each other through directed follow
paths. The time complexity is O(N + E).

## Part 2 Task 4 - Empirical Benchmarking

`analysis_part2/benchmarking.py` generates synthetic networks with:

- N = 20, 100, 500 users,
- average degree about 5.

It benchmarks:

- node insertion,
- graph construction,
- in/out degree computation,
- SCC detection,
- shortest path between two random users.

Run the full benchmark with:

```bash
python -m analysis_part2.benchmarking
```

The output is saved to:

```text
dataset/benchmark/part2_benchmark_results.csv
```

The Web interface plots the benchmark results. The report should compare actual
timing trends with theoretical complexity. If a timing trend conflicts with the
theory, the extra code logic causing the difference should be discussed.

## Part 2 Task 5 - Recommender and Web Interface

`analysis_part2/recommender.py` recommends top-3 users with friend-of-a-friend
logic:

1. look at users followed by U,
2. collect users followed by those followees,
3. remove U and users already followed by U,
4. rank candidates by mutual followees and BST follower ranking.

The Web interface is implemented with HTML, CSS, and JavaScript in `web_part2/`.
It visualises:

- directed graph arrows,
- node size proportional to follower count,
- colour-coded communities,
- path queries,
- follow recommendations,
- benchmark timing plot.

Start a local static server from the project root:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/web_part2/index.html
```

## Run

```bash
python main.py
```

## Test

```bash
python -m unittest discover -v -s ./tests -p *test*.py
```

## Git Notes

Generated Python cache files such as `__pycache__/` and `*.pyc` should not be
committed to GitHub.

## Part 2 Work Split

The detailed four-person split is in `docs/part2_work_split.md`. The split is
organised by responsibility, not by task number, so the project is easier to
integrate and review.
