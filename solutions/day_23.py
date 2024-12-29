import logging
import sys
from collections import defaultdict
from itertools import combinations

import fire
import networkx as nx
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def solve_a(data: list[str], example: bool = False) -> int:
    adj = defaultdict(set)
    for conn in data:
        a, b = conn.split("-")
        adj[a].add(b)
        adj[b].add(a)
    triplets = set()
    for key, nodes in tqdm(adj.items(), total=len(adj)):
        for a, b in list(combinations(nodes, 2)):
            if a in adj[b] and any(i.startswith("t") for i in (key, a, b)):
                triplets.add(tuple(sorted((key, a, b))))
    return len(triplets)


def solve_b(data: list[str], example: bool = False) -> str:
    adj_list = []
    for conn in data:
        a, b = conn.split("-")
        adj_list.append((a, b))

    graph = nx.Graph()
    graph.add_edges_from(adj_list)
    clique = max(nx.find_cliques(graph), key=len)

    return ",".join(sorted(clique))


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    sys.argv.append("--part=b")
    sys.argv.append("--expected_sample='co,de,ka,ta'")
    fire.Fire(main)
