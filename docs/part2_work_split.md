# Part 2 Work Split

The work is divided by responsibility rather than by task number. This is more
scientific because Part 2 features share the same graph data, algorithms,
testing, benchmark results, and Web interface.

| Role | Owner | Main files | Responsibility |
| --- | --- | --- | --- |
| Algorithm lead / 算法负责人 | Member 1 | `analysis_part2/centrality.py`, `analysis_part2/community_detection.py`, `main.py` | Hardest part: PageRank, Tarjan SCC, algorithm integration, final consistency checks. |
| Traversal and recommendation / 遍历推荐 | Member 2 | `analysis_part2/reachability.py`, `analysis_part2/recommender.py` | BFS path logic, degrees of separation, friend-of-friend recommendation, related tests. |
| Experiments and documentation / 实验文档 | Member 3 | `analysis_part2/benchmarking.py`, `README.md`, `dataset/benchmark/` | Synthetic networks, benchmark CSV, complexity interpretation, documentation. |
| Web visualisation / 网页可视化 | Member 4 | `web_part2/index.html`, `web_part2/style.css`, `web_part2/app.js` | Directed graph UI, community colours, path query, recommendations, benchmark plot. |

Member 1 owns the largest and most difficult part because the central algorithms
must stay consistent with the graph model. Members 2, 3, and 4 split the
remaining work evenly across traversal logic, experiments/documentation, and
Web visualisation.

Each member should replace the owner placeholder with their real name and push
their own commits to GitHub for the files they own.
