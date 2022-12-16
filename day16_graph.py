#!/usr/bin/env python
# As well as install the Python package pydot, you
# need to install graphviz for the write_png step to work
import pydot  # type: ignore

from day16 import read_input, build_graph, reduce_graph


def draw_pydot_graph(flow, edges, title, filename):
    graph = pydot.Dot(title, graph_type="graph")
    for c in edges:
        label = f"{c} ({flow[c]})"
        color = "blue" if flow[c] > 0 else "black"
        graph.add_node(pydot.Node(c, label=label, shape="circle", color=color))

    for c, vv in edges.items():
        for v, length in vv.items():
            if c < v:
                graph.add_edge(pydot.Edge(c, v, label=length))
    graph.write_png(filename)


def main():
    lines = read_input()
    flow, full_graph = build_graph(lines)
    graph = reduce_graph(flow, full_graph)

    draw_pydot_graph(flow, full_graph, "Full graph", "day16_full_graph.png")
    draw_pydot_graph(flow, graph, "Reduced graph", "day16_reduced_graph.png")


if __name__ == "__main__":
    main()
