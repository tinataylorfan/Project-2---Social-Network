import csv
import tempfile
import unittest
from pathlib import Path

from analysis_part2.benchmarking import build_synthetic_graph, run_benchmarks, write_benchmark_csv


class TestAnalysisPart2Benchmarking(unittest.TestCase):
    def test_build_synthetic_graph_uses_average_degree(self):
        graph = build_synthetic_graph(20, average_degree=2, seed=3)
        self.assertEqual(len(graph.users), 20)
        self.assertEqual(len(graph.edges()), 40)

    def test_invalid_sizes_are_rejected(self):
        with self.assertRaises(ValueError):
            build_synthetic_graph(1)
        with self.assertRaises(ValueError):
            build_synthetic_graph(20, average_degree=-1)

    def test_run_benchmarks_returns_required_metrics(self):
        rows = run_benchmarks(sizes=(20,), average_degree=2, seed=5)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["users"], 20)
        self.assertIn("construction_seconds", rows[0])
        self.assertIn("degree_seconds", rows[0])
        self.assertIn("scc_seconds", rows[0])
        self.assertIn("path_seconds", rows[0])

    def test_write_benchmark_csv(self):
        rows = run_benchmarks(sizes=(20,), average_degree=2, seed=5)
        with tempfile.TemporaryDirectory() as tmp:
            path = write_benchmark_csv(rows, Path(tmp) / "results.csv")
            with path.open(newline="", encoding="utf-8") as handle:
                saved = list(csv.DictReader(handle))
            self.assertEqual(saved[0]["users"], "20")


if __name__ == "__main__":
    unittest.main()
