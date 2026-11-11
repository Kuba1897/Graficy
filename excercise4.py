"""Command-line program for exercise 4: directed graphs."""

import argparse

import directedGraphsUtils as dgu


parser = argparse.ArgumentParser(
    prog="excercise4.py",
    description="Algorithms for directed graphs",
)
parser.add_argument(
    "-dp", "--display",
    choices=["adj_list", "scc", "bellman_ford", "johnson"],
    required=True,
    help="Operation to perform",
)
parser.add_argument(
    "-f", "--filename", nargs=2,
    metavar=("[auto|adj_list|adj_matrix]", "FILE"),
    help="Input graph file and its format",
)
parser.add_argument(
    "-out", "--output", nargs=1,
    metavar="PREFIX_OR_FILE",
    help="Output file or prefix for generated weights",
)
parser.add_argument(
    "-gen", "--generate", nargs=3,
    metavar=("np", "N", "P"),
    help="Generate G(N,P)",
)
parser.add_argument(
    "-genweights", "--generateWeights", action="store_true",
    help="Generate directed edge weights in the range [-5, 10]",
)
parser.add_argument(
    "-weights", "--weights", nargs=1,
    metavar="FILE",
    help="File with directed edge weights",
)
parser.add_argument(
    "-dij", "--dijkstra", nargs=1, type=int,
    metavar="START_NODE",
    help="Starting vertex for Bellman-Ford",
)
args = parser.parse_args()

if args.filename is not None:
    graph = dgu.load_graph_from_file(args.filename[1], args.filename[0])
elif args.generate is not None and args.generate[0] == "np":
    graph = dgu.generate_graph(int(args.generate[1]), float(args.generate[2]))
else:
    raise ValueError("Use -f FORMAT FILE or -gen np N P")

weights = None
if args.generateWeights:
    weights = dgu.generate_weights(graph, minimum=-5, maximum=10)
    if args.output is not None:
        dgu.save_weights(weights, args.output[0] + "_weights.txt")
elif args.weights is not None:
    weights = dgu.read_weights(args.weights[0])

if args.display == "adj_list":
    for node, neighbours in enumerate(graph, start=1):
        print(f"{node}: {neighbours}")
    if args.output is not None:
        dgu.save_graph_to_file(graph, args.output[0])
elif args.display == "scc":
    print("Strongly connected components:")
    for number, component in enumerate(dgu.kosaraju(graph), start=1):
        print(f"{number}) {component}")
else:
    if weights is None:
        raise ValueError("Use -weights FILE or -genweights")
    if args.display == "bellman_ford":
        if args.dijkstra is None:
            raise ValueError("Use -dij START_NODE with Bellman-Ford")
        distances, _ = dgu.bellman_ford(graph, weights, args.dijkstra[0])
        print(distances)
    else:
        print("Distance matrix:")
        for source, distances in dgu.johnson(graph, weights).items():
            print(f"{source}: {distances}")
