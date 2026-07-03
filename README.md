# Group2 Social Network Project - Part 1

This folder contains only the Part 1 code for the social network software
toolbox.

## Project Structure

- `part1_toolbox/part1_task1_data_modeling.py`: `User` and `SocialGraph`.
- `part1_toolbox/part1_task2_graph_representation.py`: directed graph representation notes and entry point.
- `part1_toolbox/part1_task3_bst_user_index.py`: BST index by follower count.
- `part1_toolbox/part1_task4_dataset.py`: CSV dataset generation and loading.
- `tests/test_part1_toolbox.py`: integrated Part 1 tests.
- `tests/test_task1_user_model.py`: extra tests for `User`.
- `tests/test_task2_graph_representation.py`: extra tests for directed graph operations.
- `tests/test_task3_bst_user_index.py`: extra tests for the BST index.
- `tests/test_task4_dataset.py`: extra tests for CSV generation and loading.
- `dataset/data/social_users.csv`: generated user dataset.
- `dataset/data/social_connections.csv`: generated directed follow relationships.

## Run

```bash
python main.py
```

## Test

```bash
python -m unittest discover -v -s ./tests -p *test*.py
```

The dataset generator creates at least 15 users and at least 25 directed
connections, including hub users, an isolated user, and a strongly connected
cluster.
