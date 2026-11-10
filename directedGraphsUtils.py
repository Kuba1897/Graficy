"""Algorithms and file utilities for directed graphs.

Directed graphs use 1-based vertex numbers.  ``graph[u - 1]`` contains the
out-neighbours of vertex ``u`` and weights are keyed by ordered pairs ``(u,v)``.
"""

import heapq
import random


def load_graph_from_file(filename, file_format="auto"):
    """Load a directed adjacency list or adjacency matrix."""
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
    if not lines:
        raise ValueError("Empty graph file")

    if file_format == "adj_list" or (file_format == "auto" and "." in lines[0].split()[0]):
        graph = []
        for line in lines:
            values = line.split()
            graph.append([int(value) for value in values[1:]])
        return graph

    matrix = [[int(value) for value in line.split()] for line in lines]
    if len(matrix) != len(matrix[0]) or any(len(row) != len(matrix) for row in matrix):
        raise ValueError("Adjacency matrix must be square")
    return [[column + 1 for column, value in enumerate(row) if value != 0]
            for row in matrix]


def save_graph_to_file(graph, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for node, neighbours in enumerate(graph, start=1):
            file.write(f"{node}. {' '.join(map(str, sorted(neighbours)))}\n")


def generate_graph(node_num, probability):
    if node_num < 1 or not 0 <= probability <= 1:
        raise ValueError("node_num must be positive and probability must be in [0, 1]")
    return [[target for target in range(1, node_num + 1)
             if target != source and random.random() < probability]
            for source in range(1, node_num + 1)]


def generate_strongly_connected_graph(node_num, probability):
    """Generate G(n,p) repeatedly until it is strongly connected."""
    if node_num == 1:
        return [[]]
    if probability <= 0:
        raise ValueError("A strongly connected graph with more than one vertex requires probability > 0")

    while True:
        graph = generate_graph(node_num, probability)
        if len(kosaraju(graph)) == 1:
            return graph


def transpose_graph(graph):
    result = [[] for _ in graph]
    for source, neighbours in enumerate(graph, start=1):
        for target in neighbours:
            result[target - 1].append(source)
    return result


def kosaraju(graph):
    visited = set()
    order = []

    def first_dfs(node):
        visited.add(node)
        for neighbour in graph[node - 1]:
            if neighbour not in visited:
                first_dfs(neighbour)
        order.append(node)

    for node in range(1, len(graph) + 1):
        if node not in visited:
            first_dfs(node)

    reversed_graph = transpose_graph(graph)
    visited.clear()
    components = []

    def second_dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbour in reversed_graph[node - 1]:
            if neighbour not in visited:
                second_dfs(neighbour, component)

    for node in reversed(order):
        if node not in visited:
            component = []
            second_dfs(node, component)
            components.append(sorted(component))
    return components


def read_weights(filename):
    weights = {}
    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            values = line.split()
            if len(values) != 3:
                raise ValueError(f"Invalid weight data in line {line_number}")
            source, target, weight = map(int, values)
            weights[(source, target)] = weight
    return weights


def generate_weights(graph, minimum=-5, maximum=10):
    return {(source, target): random.randint(minimum, maximum)
            for source, neighbours in enumerate(graph, start=1)
            for target in neighbours}


def bellman_ford(graph, weights, start):
    distances = {node: float("inf") for node in range(1, len(graph) + 1)}
    predecessors = {node: None for node in distances}
    distances[start] = 0
    edges = [(source, target) for source, neighbours in enumerate(graph, start=1)
             for target in neighbours]

    for _ in range(len(graph) - 1):
        changed = False
        for source, target in edges:
            if distances[source] != float("inf") and distances[target] > distances[source] + weights[(source, target)]:
                distances[target] = distances[source] + weights[(source, target)]
                predecessors[target] = source
                changed = True
        if not changed:
            break

    for source, target in edges:
        if distances[source] != float("inf") and distances[target] > distances[source] + weights[(source, target)]:
            raise ValueError("Graph contains a reachable negative cycle")
    return distances, predecessors


def _dijkstra(graph, weights, start):
    distances = {node: float("inf") for node in range(1, len(graph) + 1)}
    distances[start] = 0
    queue = [(0, start)]
    while queue:
        distance, source = heapq.heappop(queue)
        if distance != distances[source]:
            continue
        for target in graph[source - 1]:
            candidate = distance + weights[(source, target)]
            if candidate < distances[target]:
                distances[target] = candidate
                heapq.heappush(queue, (candidate, target))
    return distances


def johnson(graph, weights):
    """Return all-pairs shortest paths, rejecting graphs with negative cycles."""
    extra_graph = [list(neighbours) for neighbours in graph] + [list(range(1, len(graph) + 1))]
    extra_weights = dict(weights)
    extra_source = len(graph) + 1
    for target in range(1, len(graph) + 1):
        extra_weights[(extra_source, target)] = 0
    potentials, _ = bellman_ford(extra_graph, extra_weights, extra_source)
    reweighted = {(source, target): weight + potentials[source] - potentials[target]
                  for (source, target), weight in weights.items()}
    result = {}
    for source in range(1, len(graph) + 1):
        distances = _dijkstra(graph, reweighted, source)
        result[source] = {target: (distance - potentials[source] + potentials[target]
                                   if distance != float("inf") else distance)
                          for target, distance in distances.items()}
    return result
