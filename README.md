# Group2 Social Network Project - Part 1

This repository currently contains the Part 1 software toolbox for a directed
social network project.

## Structure

The files are organized by content type, with the project part shown in each
folder name:

- `models_part1/`: user data model.
- `structures_part1/`: directed graph and BST index.
- `data_part1/`: CSV dataset generation and loading.
- `tests/`: unit tests.
- `dataset/data/`: generated CSV files.
- `docs/`: short written notes.

## Task 1 - Data Modelling

`models_part1/user.py` defines the `User` class. Each user has:

- `user_id`
- `username`
- `join_date`
- `country`
- `follower_count`

New users start with `follower_count = 0`. The count is not manually invented;
it is updated by the graph when follow relationships change.

## Task 2 - Graph Representation

The project uses a directed graph implemented with adjacency sets.

The most frequent operations are:

- Check whether A follows B.
- Get all users followed by A.
- Get all followers of A.
- Add or remove users.
- Add or remove follow relationships.

The graph stores two maps:

- `following[user_id]`: outgoing edges, or the users that this user follows.
- `followers[user_id]`: incoming edges, or the users who follow this user.

This is a good representation because follow relationships are directed. If A
follows B, B does not automatically follow A. Keeping both outgoing and
incoming adjacency sets makes both main queries efficient.

For N users and E follow relationships, the space complexity is O(N + E).

## Task 3 - BST User Index

`structures_part1/user_index_bst.py` implements a BST sorted by real
`follower_count`.

The graph is the main structure and owns the BST. When the graph changes, it
updates the BST. The BST never changes the graph, so there are no circular
calls.

Supported BST operations:

- Insert user.
- Search by follower count.
- Find top-K users.
- Find all users in a follower-count range.

## Task 4 - Dataset Generation and Loading

`data_part1/dataset_generator.py` creates:

- `dataset/data/social_users.csv`
- `dataset/data/social_connections.csv`

The generated dataset includes:

- at least 15 users,
- at least 25 directed connections,
- hub users,
- an isolated user,
- a strongly connected cluster.

`data_part1/dataset_loader.py` loads both CSV files, builds the graph, and
updates follower counts and the BST while reading the follow relationships.

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
