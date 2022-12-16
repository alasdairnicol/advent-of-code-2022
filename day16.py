#!/usr/bin/env python


def build_graph(lines):
    """
    Builds two dictionaries where the keys are the nodes

       flow: maps nodes to flow rate
       edges: maps nodes n1 to a dict where the keys n2 represent
              the end node of the edge n1->n2 and the values
              represent the edge weight (edge weight is always 1
              according to problem)
    """
    flow = {}
    edges = {}

    for line in lines:
        words = line.split()
        cave = words[1]
        flow[cave] = int(words[4][5:-1])
        edges[cave] = {tunnel.rstrip(","): 1 for tunnel in words[9:]}

    return flow, edges


def dijkstra(edges, starting_node):
    """
    Use dijksta's algorithm to calculate the shortest distance
    from starting_node to edges
    """
    distances = {}
    queue = [(starting_node, 0)]
    visited = set()
    while queue:
        queue.sort(key=lambda x: x[1], reverse=True)
        node, distance = queue.pop()
        if node not in distances or distance < distances[node]:
            distances[node] = distance
        visited.add(node)
        for neighbour, new_distance in edges[node].items():
            if neighbour not in visited:
                queue.append((neighbour, distance + new_distance))
    return distances


def reduce_graph(flow, edges):
    """
    Return a new edges graph which contains the interesting nodes.

    Nodes with flow==0 are excluded, except for the starting node
    AA which is included.

    The edge weights now represent the number of minutes to move from
    the start node to the end node *and* turn on flow (i.e. we add 1
    to all the weights calculated using dijkstra.
    """
    # Include AA because it's the initial node
    non_zero_nodes = [k for k, v in flow.items() if v > 0 or k == "AA"]
    interesting_nodes = non_zero_nodes + ["AA"]

    graph = {}

    for node in interesting_nodes:
        distances = dijkstra(edges, node)
        # Add 1 to every value to open valve.
        # Turning on AA would be pointless, but it doesn't really matter because
        # we'll never return there
        important_distances = {
            k: v + 1 for k, v in distances.items() if k in interesting_nodes
        }
        graph[node] = important_distances
    return graph


def score_routes(flow, graph, visited, time_remaining, current_score, routes):
    """
    Recursively visit nodes while there are still unvisited nodes and time to
    visit them.

    Builds a dictionary routes where the keys are the nodes visited in order
    and the values are the score
    """
    if visited not in routes or current_score > routes[visited]:
        routes[visited] = current_score

    remaining = tuple(node for node in graph if node not in visited)
    for node in remaining:
        new_time = graph[visited[-1]][node]
        new_time_remaining = time_remaining - new_time
        if new_time_remaining > 0:
            new_score = current_score + new_time_remaining * flow[node]
            score_routes(
                flow, graph, visited + (node,), new_time_remaining, new_score, routes
            )


def do_part_1(flow, graph, time_remaining):
    routes = {}
    score_routes(
        flow,
        graph,
        visited=("AA",),
        time_remaining=time_remaining,
        current_score=0,
        routes=routes,
    )
    return max(routes.values())


def do_part_2(flow, graph, time_remaining):
    routes = {}
    score_routes(
        flow,
        graph,
        visited=("AA",),
        time_remaining=time_remaining,
        current_score=0,
        routes=routes,
    )

    # Now look for pairs of routes where the only common node is the starting node AA
    # We want to find the maximum combined score of these pairs
    visited_and_scores = [(set(visited), score) for visited, score in routes.items()]
    visited_and_scores.sort(key=lambda x: x[1], reverse=True)
    max_score = 0
    for visited_1, score_1 in visited_and_scores:
        if score_1 > max_score:
            max_score = score_1
        for visited_2, score_2 in visited_and_scores:
            total = score_1 + score_2
            if total <= max_score:
                # No point checking the remaining scores for this pair
                # since it won't result in a new max score
                break
            if visited_1 & visited_2 == {"AA"}:
                max_score = score_1 + score_2
                break
    return max_score


def main():

    lines = read_input()
    flow, full_graph = build_graph(lines)

    graph = reduce_graph(flow, full_graph)

    part_1 = do_part_1(flow, graph, time_remaining=30)
    print(f"{part_1=}")

    part_2 = do_part_2(flow, graph, time_remaining=26)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day16.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
