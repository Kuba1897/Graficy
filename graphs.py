###########################################################
#                  Main CLI program                       #
###########################################################
import argparse
import random
import undirectedGraphsUtils as ugu
import interactive_graphs as ig

display_types = [
    'adj_list', 
    'adj_matrix', 
    'inc_matrix',
    'graph',
    'components',
    'euler',
    'hamilton',
    'dijkstra',
    'dijkstra_all',
    'center',
    'minimax_center',
    'mst'
]

# Adjastable
k_regular_randomization_cycles = 10

################################# CLI parser ##########################################

parser = argparse.ArgumentParser(prog="Graphs",
                                 description="Program for graphs and their usage classes in cli with interactive mode",
                                 epilog="Made by Kuba, Radosław C, Radosław I and Paweł")
parser.add_argument("-gh",
                    "--graph",
                    choices=['undirected', 'directed'],
                    help="Type of graph to process")
parser.add_argument("-dp",
                    "--display",
                    choices=display_types,
                    help="Type of transformation/drawing to show")
parser.add_argument("-f",
                    "--filename",
                    nargs=2,
                    metavar=("[auto | adj_matrix | adj_list | inc_matrix| seq]"," filename.txt"),
                    help="Input file from which graph will be made")
parser.add_argument("-out",
                    "--output",
                    nargs=1,
                    metavar="filename.txt",
                    help="If specified Output will be saved to --out [filename]. Required for drawings!")
parser.add_argument("-gen", 
                    "--generate", 
                    nargs=3,
                    metavar=("{np,nl,kregular}", "n", "{l,p,k}"),
                    help="Can be used when no --f specified to generate desired graph. Usage: '--gen [np,nl,kregular] n [l,p, k]'")
parser.add_argument("-c",
                    "--connected",
                    action="store_true",
                    help="Generate a connected graph")

parser.add_argument("-genseq",
                    "--generateSequence",
                    nargs=1,
                    metavar="number_of_nodes",
                    help="Generates graph based on random sequence with number_of_node numbers. Only usable if --f or --gen is not specified!")
parser.add_argument("-geneuler",
                    "--generateEuler",
                    nargs=1,
                    metavar="number_of_nodes",
                    help="Generates euler sequence randomly with number of nodes. Only usable if --f or --gen or --genseq is not specified!")
parser.add_argument("-rand",
                    "--randomize",
                    nargs=1,
                    metavar="number_of_randomizations",
                    help="Specifies how many randomizations will be done")
parser.add_argument("-i",
                    "--interactive",
                    action='store_true',
                    help="Enters interactive mode. If used only --f will be taken into account.")
parser.add_argument("-genweights",
                    "--generateWeights",
                    action='store_true',
                    help="If specified, weights will be generated for edges. Only usable if --output specified!")
parser.add_argument("-weights",
                    "--weights",
                    nargs=1,
                    metavar="weights.txt",
                    help="File containing edge weights to display. Only usable with --display graph.")
parser.add_argument("-dij",
                    "--dijkstra",
                    nargs=1,
                    type=int,
                    metavar="START_NODE",
                    help="Find shortest paths from the specified starting vertex.")

args = parser.parse_args()
# print(args)
############ Parsed values ###############
display_type = args.display
input_file = args.filename
output_file = args.output
generator = args.generate
generator_sequence = args.generateSequence
generator_euler = args.generateEuler
randomize = args.randomize
interactive_mode = args.interactive
graph_type = args.graph
connected = args.connected
generate_weights = args.generateWeights
weights_file = args.weights[0] if args.weights is not None else None
display_weights = weights_file is not None
dijkstra_start = args.dijkstra[0] if args.dijkstra is not None else None

if interactive_mode == True:
    ig.run_interactive_program(input_file if input_file != None else None)

########################################################### CLI execution ########################################################
if display_type == None:
    raise ValueError("Display format required! -h for help")
if graph_type == None:
    raise ValueError("Graph type required! -h for help")

if graph_type == 'undirected':
    # Get input and load graph into adjacent list
    adjacent_list = None
    if input_file != None:
        adjacent_list = ugu.load_graph_from_file(filename=input_file[1], fileFormat=input_file[0])
    elif generator != None:
        node_num = int(generator[1])
        if generator[0] == 'np':
                random_chance = float(generator[2])
                adjacent_list = ugu.generateGraph(node_num=node_num, random_chance_per_edge=random_chance) if connected == False else ugu.generateConnectedGraph(node_num=node_num, random_chance_per_edge=random_chance)
        elif generator[0] == 'nl':
                edge_num = int(generator[2])
                adjacent_list = ugu.generateGraph(node_num=node_num, edge_num=edge_num) if connected == False else ugu.generateConnectedGraph(node_num=node_num, edge_num=edge_num)
        elif generator[0] == 'kregular':
                node_degree = int(generator[2])
                adjacent_list = ugu.generateGraphRegularK(node_num=node_num, node_degree=node_degree, randomization_cycles=k_regular_randomization_cycles) if connected == False else ugu.generateConnectedGraphRegularK(node_num=node_num, node_degree=node_degree, randomization_cycles=k_regular_randomization_cycles)
    elif generator_sequence != None:
        node_num = int(generator_sequence[0])
        goodSequence = False
        while goodSequence != True:
            sequence = [random.randint(1, node_num - 1) for _ in range(node_num)]
            if ugu.checkIfGraphicSequence(sequence=sequence) == True:
                adjacent_list = ugu.graphicalSequenceToAdjacentList(sequence=sequence)
                goodSequence = True
    elif generator_euler != None:
        node_num = int(generator_euler[0])
        sequence = ugu.generateEulerSequence(node_num=node_num)
        adjacent_list = ugu.graphicalSequenceToAdjacentList(sequence=sequence)
    else:
        raise ValueError("Input file or generator type required! See help '-h'")

    # print('test', adjacent_list)

    def pretty_print(graph=None, transpose=False, adjacent_list=False):
        if graph == None:
            raise ValueError("[[],[],..] with graph required!")
        if transpose:
            graph = [list(col) for col in zip(*graph)]
        for index, row in enumerate(graph):
            print(f"{index + 1}:" if adjacent_list else "", row)

    def components_print(components: dict=None):
        if components == None:
            raise ValueError("Components as dictionary class required!")

        largest_component = [-1, -1] # [number, nodes_number]
        for index, item in components.items():
            if len(item) > largest_component[1]:
                largest_component[0] = index
                largest_component[1] = len(item)
            print(f"{index}) {item}")
        print(f"Najwieksza skladowa ma numer {largest_component[0]}")

    if randomize != None:
        adjacent_list = ugu.randomize_pair(adjacent_list=adjacent_list, randomize_cycles=int(randomize[0]))

    weights = None

    if generate_weights:
        if output_file is None:
            raise ValueError("Output filename required for weights generation!")
        weights = ugu.generateEdgeWeights(
            adjacent_list=adjacent_list,
            min_weight=1,
            max_weight=10
        )
        ugu.save_weights_to_file(weights, filename=output_file[0]+"_weights.txt")
    elif weights_file is not None:
        weights = ugu.load_weights_from_file(filename=weights_file)

    #Tyes from display_types
    match display_type:
        case 'adj_list':
            pretty_print(adjacent_list, adjacent_list=True)
            if output_file != None:
                ugu.save_graph_to_file(adjecent_list=adjacent_list, filename=output_file[0])

        case 'adj_matrix':
            adjacent_matrix = ugu.adjacentListToAdjacentMatrix(adjacent_list)
            pretty_print(adjacent_matrix)
            if output_file != None:
                ugu.save_graph_to_file(adjecent_matrix=adjacent_matrix, filename=output_file[0])

        case 'inc_matrix':
            incidents_matrix = ugu.adjacentListToIncidentsMatrix(adjacent_list)
            pretty_print(incidents_matrix, transpose=True)
            if output_file != None:
                ugu.save_graph_to_file(incidents_matrix=incidents_matrix, filename=output_file[0])

        case 'graph':
            if output_file is None:
                raise ValueError("Output filename required for drawing!")

            if display_weights and weights is None:
                    raise ValueError("Weights are required for displaying!")

            ugu.graphDisplay(
                adjacent_list=adjacent_list,
                filename=output_file[0],
                weights=weights if display_weights else None
            )

        case 'components':
            components = ugu.graphComponents(adjacent_list=adjacent_list)
            components_print(components=components)
            if output_file != None:
                ugu.graphDisplayComponents(adjacent_list=adjacent_list, components=components, filename=output_file[0])

        case 'euler':
            status, cycle = ugu.findEulerCycle(adjacent_list=adjacent_list)
            if status == True:
                print(cycle)
            else:
                print("Euler cycle not found!")
            if output_file != None and status == True:
                ugu.graphDisplayEulerCycle(euler_cycle=cycle, filename=output_file[0])

        case 'hamilton':
            status, cycle = ugu.findHamiltonCycle(adjacent_list=adjacent_list)
            if status == True:
                print(cycle)
            else:
                print("Hamilton cycle not found!")
            if output_file != None and status == True:
                ugu.graphDisplayHamiltonCycle(adjacent_list=adjacent_list, hamilton_cycle=cycle, filename=output_file[0])

        case 'dijkstra':
            if weights is None:
                raise ValueError(
                    "Edge weights are required. Use --weights or --generateWeights."
                )

            if dijkstra_start is None:
                raise ValueError(
                    "Starting vertex required. Use --dijkstra START_NODE."
                )
            ugu.print_dijkstra_results(
                adjacent_list=adjacent_list,
                weights=weights,
                dijkstra_start=dijkstra_start
                )
        case 'dijkstra_all':
            if weights is None:
                raise ValueError(
                    "Edge weights are required. Use --weights or --generateWeights."
                )

            distance_matrix = ugu.dijkstra_matrix(adjacent_list=adjacent_list, weights=weights)

            print("Distance matrix:")
            pretty_print(distance_matrix)
            if output_file is not None:
                ugu.save_graph_to_file(adjecent_matrix=distance_matrix, filename=output_file[0])

        case 'center':
            if adjacent_list is None:
                raise ValueError("Adjacency list required!")
            if weights is None:
                raise ValueError("Weights dictionary required!")
            central_node, min_sum = ugu.findCentralNode(adjacent_list=adjacent_list, weights=weights)
            print(f"Central node: {central_node}, Distance sum: {min_sum}")

        case 'minimax_center':
            if adjacent_list is None:
                raise ValueError("Adjacency list required!")
            if weights is None:
                raise ValueError("Weights dictionary required!")
            minimax_center_node, min_max_distance = ugu.findMinimaxNode(adjacent_list=adjacent_list, weights=weights)
            print(f"Minimax center node: {minimax_center_node}, Distance from furthest node: {min_max_distance}")

        case 'mst':
            if weights is None:
                raise ValueError(
                    "Edge weights are required. Use --weights or --generateWeights."
                )

            if output_file is None:
                raise ValueError("Output filename required for drawing!")

            mst_edges, mst_weights, total_weight = ugu.kruskalMST(
                adjacent_list=adjacent_list,
                weights=weights
            )

            print("Minimum spanning tree edges:")
            for u, v in mst_edges:
                print(f"{u} -- {v}: weight = {mst_weights[(u, v)]}")

            print(f"Total weight: {total_weight}")

            mst_adjacent_list = [[] for _ in adjacent_list]

            for u, v in mst_edges:
                mst_adjacent_list[u - 1].append(v)
                mst_adjacent_list[v - 1].append(u)

            ugu.graphDisplay(
                adjacent_list=mst_adjacent_list,
                filename=output_file[0],
                weights=mst_weights
            )

        case _:
            print("Unsupported format for undirected")

elif graph_type == 'directed':
    # TODO
    print("Directed utils here")
else:
    print("Unsupported graph type!")
