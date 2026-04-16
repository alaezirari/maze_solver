import time
import tracemalloc

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from collections import deque
import heapq

from math import pi

from visualization import (
    plot_step_metrics,
    plot_radar_chart,
    plot_box_plot,
    plot_pie_chart,
    plot_performance_comparison,
    plot_pie_charts,
    plot_performance_comparison,
)
from algorithms import *
from configmaze import width, height, start, goal, maze


def run_experiment(algorithms, runs=100):
    results = []
    for name, algo in algorithms.items():
        for _ in range(runs):
            path, metrics = algo(start, goal)
            results.append(
                {
                    "algorithm": name,
                    "time": metrics["time"][-1],
                    "memory": metrics["memory"][-1],
                    "path_length": len(path),
                    "steps times": metrics["time"],
                    "steps memory": metrics["memory"],
                }
            )
    return pd.DataFrame(results)


if __name__ == "__main__":
    # configurer les algorithmes
    algorithms = {
        "BFS": lambda s, g: bfs(s, g, maze),
        "DFS": lambda s, g: dfs(s, g, maze),
        "A*": lambda s, g: a_star(s, g, maze, heuristic),
        "GBFS": lambda s, g: gbfs(s, g, maze, heuristic),
    }
    # executer les expériences
    df_results = run_experiment(algorithms)
    # analyse statistique
    stats = df.groupby("algorithm").agg(
        {
            "time": ["mean", "std"],
            "memory": ["mean", "std"],
            "path_length": ["mean", "std"],
        }
    )
    print(stats)
    # genérer les visualisations
    plot_step_metrics(df)
    plot_radar_chart(df)
    plot_box_plot(df)
    plot_pie_chart(stats)
    plot_performance_comparison(stats)
