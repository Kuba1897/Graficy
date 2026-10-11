###########################################################
#                  Main CLI program                       #
###########################################################
import argparse
import graphUtils as gu
import interactive_graphs as ig

display_types = [
    'adj_list', 
    'adj_matrix', 
    'inc_matrix',
    'graph'
]

################################# CLI parser ##########################################

parser = argparse.ArgumentParser(prog="Graphs",
                                 description="Program for graphs and their usage classes in cli with interactive mode",
                                 epilog="Made by Kuba, Radosław C, Radosław I and Paweł")
parser.add_argument("--dp",
                    "-display",
                    choices=display_types,
                    help="Type of transformation/drawing to show")
parser.add_argument("--f",
                    "-filename",
                    nargs=1,
                    metavar="filename.txt",
                    help="Input file from which graph will be made")
parser.add_argument("--out",
                    "-output",
                    nargs=1,
                    metavar="filename.txt",
                    help="If specified Output will be saved to --out [filename]. Required for drawings!")
parser.add_argument("--gen", 
                    "-generate", 
                    nargs=3,
                    metavar=("{np,nl}", "n", "{l,p}"),
                    help="Can be used when no --f specified to generate desired graph. Usage: '--gen [np,nl] n [l,p]'")
parser.add_argument("--i",
                    "-interactive",
                    action='store_true',
                    help="Enters interactive mode. If used only --f will be taken into account.")

args = parser.parse_args()
# print(args)
############ Parsed values ###############
display_type = args.dp
input_file = args.f
output_file = args.out
generator = args.gen
interactive_mode = args.i

if interactive_mode:
    ig.run_interactive_program(input_file if input_file != None else None)

########################################################### CLI execution ########################################################
if display_type == None:
    raise ValueError("Display format required!")
# Get input and load graph into adjacent list
adjacent_list = None
if input_file != None:
    adjacent_list = gu.load_graph_from_file(filename=input_file[0])
elif generator != None:
    node_num = int(generator[1])
    if generator[0] == 'np':
        random_chance = float(generator[2])
        adjacent_list = gu.generateGraph(node_num=node_num, random_chance_per_edge=random_chance)
    elif generator[0] == 'nl':
        edge_num = int(generator[2])
        adjacent_list = gu.generateGraph(node_num=node_num, edge_num=edge_num)
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

#Tyes from display_types
match display_type:
    case 'adj_list':
        pretty_print(adjacent_list, adjacent_list=True)
        if output_file != None:
            gu.save_graph_to_file(adjecent_list=adjacent_list, filename=output_file[0])

    case 'adj_matrix':
        adjacent_matrix = gu.adjacentListToAdjacentMatrix(adjacent_list)
        pretty_print(adjacent_matrix)
        if output_file != None:
            gu.save_graph_to_file(adjecent_matrix=adjacent_matrix, filename=output_file[0])

    case 'inc_matrix':
        incidents_matrix = gu.adjacentListToIncidentsMatrix(adjacent_list)
        pretty_print(incidents_matrix, transpose=True)
        if output_file != None:
            gu.save_graph_to_file(incidents_matrix=incidents_matrix, filename=output_file[0])

    case 'graph':
        if output_file == None:
            raise ValueError("Output filename required for drawing!")
        gu.graphDisplay(adjacent_list=adjacent_list, filename=output_file[0])
