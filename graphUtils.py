###############################################
#                Graph Utils                  #
###############################################

import networkx as nx
import matplotlib.pyplot as plt
import random

# Adjacent list conversion

def adjacentListToAdjacentMatrix(adjacent_list=None):
    if adjacent_list == None:
        raise ValueError("Adjacent list required!")
    
    matrix = []
    for i in range(len(adjacent_list)):
        row = [0] * len(adjacent_list)
        for j in adjacent_list[i]:
            row[j - 1] = 1
        matrix.append(row)
    return matrix

def adjacentListToIncidentsMatrix(adjacent_list=None):
    if adjacent_list == None:
        raise ValueError("Adjacent list required!")
    
    matrix = []
    for i in range(len(adjacent_list)):
        for j in adjacent_list[i]:
            if j - 1 >= i:
                col = [0] * len(adjacent_list)
                col[i] = 1
                col[j-1] = 1
                matrix.append(col)
    return matrix

# Adjacent matrix conversion

def adjacentMatrixToIncidentsMatrix(adjacent_matrix=None):
    if adjacent_matrix == None:
        raise ValueError("Adjacent matrix required!")
    
    matrix = []
    for i in range(len(adjacent_matrix)):
        for j in range(i + 1, len(adjacent_matrix)):
            if adjacent_matrix[i][j] == 1:
                col = [0] * len(adjacent_matrix)
                col[i] = 1
                col[j] = 1
                matrix.append(col)
    return matrix

def adjacentMatrixToAdjacentList(adjacent_matrix=None):
    if adjacent_matrix == None:
        raise ValueError("Adjacent matrix required!")
    
    adj_list = []
    for i in range(len(adjacent_matrix)):
        row = []
        for j in range(len(adjacent_matrix)):
            if adjacent_matrix[i][j] == 1:
                row.append(j + 1)
        adj_list.append(row)
    return adj_list

# Incident matrix conversion

def incidentsMatrixToAdjacentList(incidents_matrix=None):
    if incidents_matrix == None:
        raise ValueError("Incidents matrix required!")
    
    matrix = [] * len(incidents_matrix[0])
    for _ in range(len(incidents_matrix[0])):
        matrix.append([] * len(incidents_matrix[0]))
    for i in incidents_matrix:
        first, second = -1,-1
        for j in range(len(incidents_matrix[0])):
            if i[j] == 1:
                if first == -1:
                    first = j
                else:
                    second = j
                    break
        matrix[first].append(second + 1)
        matrix[second].append(first + 1)
            

    return matrix

def incidentsMatrixToAdjacentMatrix(incidents_matrix=None):
    if incidents_matrix == None:
        raise ValueError("Incidents matrix required!")
    
    matrix = [] * len(incidents_matrix[0])
    for _ in range(len(incidents_matrix[0])):
        matrix.append([0] * len(incidents_matrix[0]))
    for i in incidents_matrix:
        first, second = -1,-1
        for j in range(len(incidents_matrix[0])):
            if i[j] == 1:
                if first == -1:
                    first = j
                else:
                    second = j
                    break
        matrix[first][second] = 1
        matrix[second][first] = 1
            

    return matrix

# Graph parameters

def graphNodes(adjacent_list=None):
    if adjacent_list == None:
        raise ValueError("Adjacent list required!")
    return len(adjacent_list)


def graphEdges(adjacent_list=None):
    if adjacent_list == None:
        raise ValueError("Adjacent list required!")
    return len(adjacentListToIncidentsMatrix(adjacent_list))


def deleteNode(adjacent_list=None, node_num=None):
    if adjacent_list == None:
        raise ValueError("Adjacent list required!")
    if node_num == None:
        raise ValueError("Node number index [1...n] required!")
    node_num = node_num - 1
    # Create copy to not modify passed graph
    output_adjacent_list = [list(nodes) for nodes in adjacent_list]
    for connected_nodes in output_adjacent_list[node_num]:
        output_adjacent_list[connected_nodes - 1].remove(node_num + 1)
    return output_adjacent_list

def deleteEdge(adjacent_list=None, edge=None):
    if adjacent_list == None:
        raise ValueError("Adjacent list required!")
    if edge == None or len(edge) != 2:
        raise ValueError("Edge in format [a,b] or (a,b), where a and b are nodes index 1..n required!")
    node1 = edge[0] - 1
    node2 = edge[1] - 1
    # Create copy to not modify passed graph
    output_adjacent_list = [list(nodes) for nodes in adjacent_list]
    output_adjacent_list[node1].remove(node2 + 1)
    output_adjacent_list[node2].remove(node1 + 1)
    return output_adjacent_list


# Displaying

def graphDisplay(adjacent_list, filename="graphs_output"):
    graph = nx.Graph()
    for i in range(len(adjacent_list)):
        graph.add_node(i + 1)
    for index, row in enumerate(adjacent_list):
        for i in row:
            graph.add_edge(i, index + 1)

    _, ax = plt.subplots(figsize=(7,7))
    pos = nx.circular_layout(graph)

    bg_circle = plt.Circle(
        (0, 0),
        radius=1.0,
        color="lightgray",
        fill=False,
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        zorder=1
    )
    ax.add_patch(bg_circle)

    #For yupiter implementation to see output
    nx.draw_networkx_nodes(
        graph, pos, node_color="skyblue", node_size=700, ax=ax
    )
    nx.draw_networkx_labels(
        graph, pos, font_weight="bold", ax=ax
    )
    nx.draw_networkx_edges(
        graph, pos, edge_color="gray", ax=ax
    )

    ax.set_aspect("equal")
    plt.axis("off")

    plt.savefig(f"{filename}.jpg", bbox_inches="tight", dpi=300)
    plt.show()
    plt.close()


# Graph generation

def generateGraph(node_num = None, edge_num=None, random_chance_per_edge=None):
    if node_num == None:
        raise ValueError("Graph without node can't be created")
    if (edge_num == None and random_chance_per_edge == None) or (edge_num != None and random_chance_per_edge != None):
        raise ValueError("Chose one option edge_num (default) or random_chance_per_edge")

    outputAdjacentList = []
    if random_chance_per_edge != None:
        if (random_chance_per_edge < 0 or random_chance_per_edge > 1):
            raise("Bad random chance number")
        for _ in range(node_num):
            outputAdjacentList.append([])
        for i in range(node_num):
            for j in range(i + 1, node_num):
                if random_chance_per_edge >= random.random():
                    outputAdjacentList[i].append(j + 1)
                    outputAdjacentList[j].append(i + 1)
    elif edge_num != None:
        if edge_num < 0 or edge_num > (node_num* (node_num - 1)) // 2:
            raise ValueError("Bad edge number")
        matrix = [] * node_num
        for _ in range(node_num):
            matrix.append([0] * node_num)
        edges_generated = 0
        while edges_generated < edge_num:
            x, y = random.randint(0, node_num - 1), random.randint(0, node_num - 1)
            if x == y:
                continue
            if matrix[x][y] == 0:
                matrix[x][y] = 1
                matrix[y][x] = 1
                edges_generated = edges_generated + 1

        outputAdjacentList = adjacentMatrixToAdjacentList(matrix)

    return outputAdjacentList

# File operations
def load_graph_from_file(filename=None):
    if filename == None:
        raise ValueError("Filename is needed!")
    
    adjacent_list = []
    with open(filename, "r") as fp:
        lines = fp.readlines()
        rows_num = len(lines)
        if rows_num == 0:
            raise ValueError("Empty file!")
        cols_num = len(lines[0].split())

        # lines[0][0] have '.', e.g '1.' its adjacent list format
        if (lines[0].split())[0].find('.') != -1:
            for index, line in enumerate(lines):
                adjacent_list.append([])
                for i in line.split()[1:]: #node index is not used
                    adjacent_list[index].append(int(i))
        elif cols_num == rows_num:
            # First check if its incidents list (all cols would have two 1's only)
            adjacent_matrix_type = [[int(val) for val in line.split()] for line in lines]
            incicent_matrix_type = [list(col) for col in zip(*adjacent_matrix_type)]

            incicent_matrix_form = True
            for col in incicent_matrix_type:
                if col.count(1) != 2:
                    incicent_matrix_form = False

            if incicent_matrix_form:
                adjacent_list = incidentsMatrixToAdjacentList(incicent_matrix_type)
            else:
                adjacent_list = adjacentMatrixToAdjacentList(adjacent_matrix_type)

        else: # Incidents list
            rows = [[int(val) for val in line.split()] for line in lines]
            incidents_matrix = [list(col) for col in zip(*rows)]
            adjacent_list = incidentsMatrixToAdjacentList(incidents_matrix)
        
    for row in adjacent_list:
        row.sort()
    return adjacent_list

def  save_graph_to_file(adjecent_matrix=None, adjecent_list=None, incidents_matrix=None, filename=None):
    if adjecent_matrix == None and adjecent_list == None and incidents_matrix == None:
        raise ValueError("Graph matrix is required!")
    if filename == None:
        raise ValueError("Filename required!")

    # Check if only one format selected
    options_count = 0
    if adjecent_matrix != None:
        options_count = options_count + 1
    if adjecent_list != None:
        options_count = options_count + 1
    if incidents_matrix != None:
        options_count = options_count + 1

    if options_count != 1:
        raise ValueError("Only graph representation should be passed to function!")

    with open(filename, 'w') as fp:
        if adjecent_matrix:
            for row in adjecent_matrix[:-1]:
                fp.write(" ".join(map(str, row)) + "\n")
            fp.write(" ".join(map(str, adjecent_matrix[-1]))) # Don't end file with \n

        if adjecent_list:
            for index, row in enumerate(adjecent_list[:-1]):
                fp.write(f"{index + 1}. " + " ".join(map(str, row)) + "\n")
            fp.write(f"{len(adjecent_list)}. " + " ".join(map(str, adjecent_list[-1]))) # Don't end file with \n

        if incidents_matrix:
            transposed = [list(col) for col in zip(*incidents_matrix)]
            for row in transposed[:-1]:
                fp.write(" ".join(map(str, row)) + "\n")
            fp.write(" ".join(map(str, transposed[-1]))) # Don't end file with \n
